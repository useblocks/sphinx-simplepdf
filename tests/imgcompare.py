#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import cv2
import fitz  # PyMuPDF
import numpy as np
from skimage.metrics import structural_similarity as ssim


# -----------------------------
# PDF -> PNG pages with PyMuPDF
# -----------------------------
def pdf_to_pngs(
    pdf_path: str | Path,
    out_dir: str | Path,
    dpi: int = 300,
) -> list[Path]:
    """
    Render all pages of a PDF as PNG files using PyMuPDF.

    Returns a sorted list of the generated PNG file paths.
    """
    pdf_path = Path(pdf_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    images: list[Path] = []

    # Choose zoom factor so that the target DPI is approximated.
    # Default PDF resolution is ~72 dpi → zoom = dpi / 72
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)

    for page_index in range(doc.page_count):
        page = doc.load_page(page_index)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        out_path = out_dir / f"{pdf_path.stem}_{page_index + 1:03d}.png"
        # Save directly as PNG
        pix.pil_save(str(out_path), format="PNG", optimize=False)
        images.append(out_path)

    doc.close()
    return images


# -----------------------------
# Image comparison (SSIM on gray)
# -----------------------------
def load_gray(path: str | Path) -> np.ndarray:
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(path)
    return img


def normalize_size(a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    if a.shape == b.shape:
        return a, b
    h = min(a.shape[0], b.shape[0])
    w = min(a.shape[1], b.shape[1])
    return a[:h, :w], b[:h, :w]


def compare_images_ssim(
    ref_path: str | Path,
    test_path: str | Path,
    blur_sigma: int = 1,
    diff_threshold: int = 25,
):
    ref = load_gray(ref_path)
    test = load_gray(test_path)

    ref, test = normalize_size(ref, test)

    if blur_sigma > 0:
        k = 2 * blur_sigma + 1
        ref_blur = cv2.GaussianBlur(ref, (k, k), 0)
        test_blur = cv2.GaussianBlur(test, (k, k), 0)
    else:
        ref_blur, test_blur = ref, test

    score, ssim_map = ssim(
        ref_blur,
        test_blur,
        data_range=255,
        full=True,
    )

    abs_diff = cv2.absdiff(ref_blur, test_blur)
    _, diff_mask = cv2.threshold(abs_diff, diff_threshold, 255, cv2.THRESH_BINARY)

    kernel = np.ones((3, 3), np.uint8)
    diff_mask_clean = cv2.morphologyEx(diff_mask, cv2.MORPH_OPEN, kernel, iterations=1)

    changed_pixels = int(np.count_nonzero(diff_mask_clean))
    total_pixels = int(diff_mask_clean.size)
    changed_ratio = changed_pixels / total_pixels

    return {
        "ssim": float(score),
        "changed_ratio": float(changed_ratio),
        "changed_pixels": changed_pixels,
        "total_pixels": total_pixels,
        "diff_mask": diff_mask_clean,
        "abs_diff": abs_diff,
        "ssim_map": ssim_map,
    }


def save_debug_images(
    out_dir: str | Path,
    diff_mask: np.ndarray,
    abs_diff: np.ndarray,
    ssim_map: np.ndarray,
):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    ssim_norm = (ssim_map * 255).astype(np.uint8)
    cv2.imwrite(str(out_dir / "diff_mask.png"), diff_mask)
    cv2.imwrite(str(out_dir / "abs_diff.png"), abs_diff)
    cv2.imwrite(str(out_dir / "ssim_map.png"), ssim_norm)


# -----------------------------
# Full workflow: PDFs -> PNG -> comparison
# -----------------------------
def compare_pdfs(
    ref_pdf: str | Path,
    test_pdf: str | Path,
    work_dir: str | Path = "artifacts",
    dpi: int = 300,
    ssim_threshold: float = 0.99,
    changed_ratio_threshold: float = 0.001,
    pages: slice | None = None,
) -> bool:
    """
    Compare two PDFs page by page.

    If `pages` is given, only the selected page indices (0-based) are compared.
    Example: pages=slice(1, 3) compares pages 1 and 2.
    """
    work_dir = Path(work_dir)
    ref_dir = work_dir / "ref"
    test_dir = work_dir / "test"

    print(f"[INFO] Render reference PDF: {ref_pdf}")
    ref_pages = pdf_to_pngs(ref_pdf, ref_dir, dpi=dpi)
    print(f"[INFO] Render test PDF: {test_pdf}")
    test_pages = pdf_to_pngs(test_pdf, test_dir, dpi=dpi)

    if len(ref_pages) != len(test_pages):
        print(f"[ERROR] Page count mismatch: ref={len(ref_pages)}, test={len(test_pages)}")
        return False

    # Apply slice if given (0-based indices)
    if pages is not None:
        ref_pages = ref_pages[pages]
        test_pages = test_pages[pages]
        print(f"[INFO] Restricting comparison to pages slice {pages}")

    all_ok = True

    if len(ref_pages) == 0:
        print("[ERROR] No page selected for reference")
        return False

    for ref_img, test_img in zip(ref_pages, test_pages, strict=True):
        page_name = ref_img.name
        print(f"[INFO] Compare page: {page_name}")

        result = compare_images_ssim(ref_img, test_img)

        s = result["ssim"]
        r = result["changed_ratio"]
        print(f" SSIM          : {s:.6f}")
        print(f" Changed ratio : {r * 100:.6f}%")

        is_ok = s > ssim_threshold and r < changed_ratio_threshold
        print(f" RESULT        : {'OK' if is_ok else 'MISMATCH'}")

        if not is_ok:
            all_ok = False
            debug_dir = work_dir / f"debug_{ref_img.stem}"
            save_debug_images(debug_dir, result["diff_mask"], result["abs_diff"], result["ssim_map"])
            print(f" Debug images  : {debug_dir}")

    return all_ok


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} REF.pdf TEST.pdf")
        sys.exit(1)

    ref_pdf = sys.argv[1]
    test_pdf = sys.argv[2]

    ok = compare_pdfs(ref_pdf, test_pdf)
    sys.exit(0 if ok else 2)
