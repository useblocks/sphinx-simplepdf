from bs4 import BeautifulSoup
from pdfminer.high_level import extract_pages, extract_text


def extract_pdf_text(pdf_path):
    """Extrahiere gesamten Text aus PDF."""
    return extract_text(str(pdf_path))


def page_count(pdf_path):
    """get page count of pdf"""
    page_count = 0
    for _page_layout in extract_pages(pdf_path):
        page_count += 1
    return page_count


def prettify_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return str(soup.prettify(formatter="html"))


def build_and_capture_stdout(sphinx_build, capsys, srcdir, build_kwargs=None, **sphinx_kwargs):
    """Baue das PDF und liefere das captured stdout zurück."""
    build_kwargs = build_kwargs or {}
    result = sphinx_build(srcdir=srcdir, **sphinx_kwargs).build(**build_kwargs)
    captured = capsys.readouterr()
    result.warnings += captured.out.splitlines()
    return result
