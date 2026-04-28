from collections import Counter
import importlib
import os
import re
import subprocess
from typing import Any

from bs4 import BeautifulSoup
import sass
from sphinx import __version__
from sphinx.application import Sphinx
from sphinx.builders.singlehtml import SingleFileHTMLBuilder
from sphinx.errors import ExtensionError
from sphinx.util import logging

from sphinx_simplepdf.builders.debug import DebugPython
from sphinx_simplepdf.writers.simplepdf import SimplepdfTranslator

logger = logging.getLogger(__name__)


class SimplePdfBuilder(SingleFileHTMLBuilder):
    name = "simplepdf"
    format = "html"  # Must be html instead of "pdf", otherwise plantuml has problems
    file_suffix = ".pdf"
    links_suffix = None

    default_translator_class = SimplepdfTranslator

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.app.config.simplepdf_theme is not None:
            logger.info(f"Setting theme to {self.app.config.simplepdf_theme}")
            self.app.config.html_theme = self.app.config.simplepdf_theme

        # We need to overwrite some config values, as they are set for the normal html build, but
        # simplepdf can normally not handle them.
        self.app.config.html_sidebars = self.app.config.simplepdf_sidebars
        self.app.config.html_theme_options = self.app.config.simplepdf_theme_options
        # Sphinx would write warnings, if given options are unsupported.

        # Add SimplePDf specific functions to the html_context. Mostly needed for printing debug information.
        self.app.config.html_context["simplepdf_debug"] = self.config["simplepdf_debug"]
        self.app.config.html_context["pyd"] = DebugPython()

        debug_sphinx = {
            "version": __version__,
            "confidr": self.app.confdir,
            "srcdir": self.app.srcdir,
            "outdir": self.app.outdir,
            "extensions": self.app.config.extensions,
            "simple_config": {x.name: x.value for x in self.app.config if x.name.startswith("simplepdf")},
        }
        self.app.config.html_context["spd"] = debug_sphinx

        # Generate main.css
        logger.info("Generating css files from scss-templates")
        css_folder = os.path.join(self.app.outdir, "_static")
        scss_folder = self._resolve_scss_folder()
        sass.compile(
            dirname=(scss_folder, css_folder),
            output_style="nested",
            custom_functions={
                sass.SassFunction("config", ("$a", "$b"), self.get_config_var),
                sass.SassFunction("theme_option", ("$a", "$b"), self.get_theme_option_var),
            },
        )

    def get_config_var(self, name, default):
        """
        Gets a config variables for scss out of the Sphinx configuration.
        If name is not found in config, the specified default var is returned.

        Args:
            name: Name of the config var to use
            default: Default value, if name can not be found in config

        Returns: Value
        """
        simplepdf_vars = self.app.config.simplepdf_vars
        if name not in simplepdf_vars:
            return default
        return simplepdf_vars[name]

    def get_theme_option_var(self, name, default):
        """
        Gets a option  variables for scss out of the Sphinx theme options.
        If name is not found in theme options, the specified default var is returned.

        Args:
            name: Name of the option var to use
            default: Default value, if name can not be found in config

        Returns: Value
        """
        simplepdf_theme_options = self.app.config.simplepdf_theme_options
        if name not in simplepdf_theme_options:
            return default
        return simplepdf_theme_options[name]

    def _resolve_scss_folder(self):
        """Resolve the SCSS sources folder from the configured theme package.

        Imports the theme module and calls its get_scss_sources_path(). Falls
        back to the bundled simplepdf_theme if the theme cannot be imported or
        does not define get_scss_sources_path(), or if calling the hook raises.
        If the hook returns a path that is not an existing directory after
        abspath normalization, raises ExtensionError.
        """
        theme_name = self.app.config.simplepdf_theme or "simplepdf_theme"
        fallback_module = importlib.import_module("sphinx_simplepdf.themes.simplepdf_theme")

        def bundled_scss_folder():
            return fallback_module.get_scss_sources_path()

        try:
            # theme_name comes from conf.py; dynamic import is no extra trust boundary vs. Sphinx config.
            theme_module = importlib.import_module(theme_name)
        except Exception as exc:
            logger.warning(
                f"Could not import theme '{theme_name}' ({type(exc).__name__}: {exc!s}), "
                "falling back to bundled simplepdf_theme",
                type="simplepdf",
                subtype="theme",
            )
            return bundled_scss_folder()

        if not hasattr(theme_module, "get_scss_sources_path"):
            logger.warning(
                f"Theme '{theme_name}' does not define get_scss_sources_path(), "
                "falling back to bundled simplepdf_theme",
                type="simplepdf",
                subtype="theme",
            )
            return bundled_scss_folder()

        try:
            scss_folder = theme_module.get_scss_sources_path()
        except Exception as exc:
            logger.warning(
                f"Theme '{theme_name}' get_scss_sources_path() failed ({type(exc).__name__}: {exc!s}), "
                "falling back to bundled simplepdf_theme",
                type="simplepdf",
                subtype="theme",
            )
            return bundled_scss_folder()

        scss_folder = os.path.abspath(scss_folder)
        if not os.path.isdir(scss_folder):
            raise ExtensionError(
                f"Theme '{theme_name}' get_scss_sources_path() returned non-existent directory: {scss_folder}"
            )
        return scss_folder

    def finish(self) -> None:
        super().finish()

        index_path = os.path.join(self.app.outdir, f"{self.app.config.root_doc}.html")

        # Manipulate index.html
        with open(index_path, encoding="utf-8") as index_file:
            index_html = "".join(index_file.readlines())

        new_index_html = self._toctree_fix(index_html)

        with open(index_path, "w", encoding="utf-8") as index_file:
            index_file.writelines(new_index_html)

        args = ["weasyprint"]

        if isinstance(self.config["simplepdf_weasyprint_flags"], list) and (
            len(self.config["simplepdf_weasyprint_flags"]) > 0
        ):
            args.extend(self.config["simplepdf_weasyprint_flags"])

        file_name = self.app.config.simplepdf_file_name or f"{self.app.config.project}.pdf"

        args.extend(
            [
                index_path,
                os.path.join(self.app.outdir, f"{file_name}"),
            ]
        )

        timeout = self.config["simplepdf_weasyprint_timeout"]

        filter_list = self.config["simplepdf_weasyprint_filter"]
        filter_pattern = "(?:{})".format("|".join(filter_list)) if len(filter_list) > 0 else None

        if self.config["simplepdf_use_weasyprint_api"]:
            # Import only when this code path runs so ``extensions = ["sphinx_simplepdf"]`` on
            # ``-b html`` does not load WeasyPrint's native dependencies (e.g. macOS CI).
            import weasyprint

            doc = weasyprint.HTML(index_path)

            doc.write_pdf(
                target=os.path.join(self.app.outdir, f"{file_name}"),
            )

        else:
            retries = self.config["simplepdf_weasyprint_retries"]
            success = False
            for n in range(1 + retries):
                try:
                    wp_out = subprocess.check_output(args, timeout=timeout, text=True, stderr=subprocess.STDOUT)

                    for line in wp_out.splitlines():
                        if filter_pattern is not None and re.match(filter_pattern, line):
                            pass
                        else:
                            print(line)
                    success = True
                    break
                except subprocess.TimeoutExpired:
                    logger.info("TimeoutExpired in weasyprint, retrying")
                except subprocess.CalledProcessError as e:
                    logger.info(f"CalledProcessError in weasyprint, retrying\n{e!s}")
                finally:
                    if (n == retries - 1) and not success:
                        logger.warning(f"weasyprint failed after {retries} retries")
                        raise RuntimeError(f"maximum number of retries {retries} failed in weasyprint")

    """
    attempts to fix cases where a document has multiple chapters that have the same name.

    the following structure would be a problem for showing the toc correctly:

    Documentation:
    1. Hardware
        1.1 Introduction
        1.2 Description
        1.3 Content
    2. Software
        2.1 Structure
            2.1.1 Introduction
            2.1.2 Description
            2.1.3 Content
    3. Backend
        3.1 Introduction
        3.2 Description

    we want a toctree showing only lvl 1 and lvl 2 chapters
    since there lvl 3 chapters with the same name as a lvl 2 chapter and we merge all the documentation into a single HTML for the PDF build
    the counting for chapters in the PDF toctree gets messed up

    """

    def _toctree_fix(self, html):
        logger.info("checking for potential toctree page numbering errors")
        soup = BeautifulSoup(html, "html.parser")
        sidebar = soup.find("div", class_="sphinxsidebarwrapper")

        # sidebar contains the toctree
        if sidebar is not None:
            toc_links = sidebar.find_all("a", class_="reference internal")

            # find max toctree lvl
            toctree_lvls = set(sidebar.find_all("li", class_=re.compile("toctree-l[1-9]")))

            max_toctree_lvl = 0

            for i in toctree_lvls:
                lvl = int(
                    i["class"][0].split("-l")[-1]
                )  # toctree entries have a single class, example "toctree-l1" for lvl 1, get lvl
                if lvl > max_toctree_lvl:
                    max_toctree_lvl = lvl

            # remove document file reference
            for toc_link in toc_links:
                toc_link["href"] = toc_link["href"].replace(f"{self.app.config.root_doc}.html", "")

            # search for duplicates
            counts = dict(Counter([str(x).split(">")[0] for x in toc_links]))
            references = dict(counts.items())

            if references:
                logger.info(f"found duplicate chapters:\n{references}")

            for text in references:
                ref = re.findall('href="#.*"', str(text))

                # clean href data for searching
                cleaned_ref_toc = ref[0].replace('href="', "").replace('"', "")  # "#target"
                cleaned_ref_target = ref[0].replace('href="#', "").replace('"', "")  # "target"

                occurences = soup.find_all("section", attrs={"id": cleaned_ref_target})

                # name occurrences section-id which is the target for internal refs with increasing id
                # occurrence-0, occurrence-1, occurrence-2 ...
                if len(occurences) > 1:
                    occ_counter = 0
                    for occ_counter, occ in enumerate(occurences):
                        occ["id"] = occ["id"] + "-" + str(occ_counter)

                else:
                    continue

                # index of toctree entry
                replace_counter = 0

                # scan all occurrences, if occurrence has too high of a HTML headline level compared to the max_toctree_level (depth)
                # the occurrence is a "deeper" level which does not correspond to the toctree reference. This is only needed when there
                # are chapters with the same name AND one of them is at a level which should not be referenced in the toc but becomes an

                for toc_link in toc_links:
                    if toc_link["href"] == cleaned_ref_toc:
                        # edit toctree reference
                        try:
                            match_found = False

                            for j in range(replace_counter, len(occurences)):
                                if match_found:
                                    break

                                children = set(occurences[j].contents)

                                target_lvl = 99

                                for element in children:
                                    name = element.name

                                    # find headline of chapter
                                    if name and re.search("h[1-9]", name):
                                        try:
                                            e_class = element.contents[0].attrs["class"][0]
                                        except KeyError:
                                            continue
                                        except AttributeError:
                                            continue

                                        if e_class == "section-number":
                                            target_lvl = int(name[-1])

                                            # if headlinelevel either is max_toctree lvl or + 1 the chapter should be included in the toc
                                            # break both loops and edit occurrence via replace_counter
                                            if target_lvl == max_toctree_lvl + 1 or target_lvl == max_toctree_lvl:
                                                match_found = True
                                                break  # headline match found

                                            else:
                                                # skip this occurrence if headline level too big
                                                replace_counter += 1
                                                continue

                            # edit target of toc reference with correct occurrence
                            toc_link["href"] = toc_link["href"] + "-" + str(replace_counter)
                            replace_counter += 1

                        except IndexError:
                            continue

        for heading_tag in ["h1", "h2"]:
            headings = soup.find_all(heading_tag)
            for number, heading in enumerate(headings):
                class_attr = heading.get("class", [])
                if number == 0:
                    class_attr += ["first"]
                class_attr += [f"heading-{number}"]
                heading["class"] = class_attr

                parent = heading.find_parent("section")
                # is the parent a section
                if parent and parent.name == "section":
                    prev_span = parent.find_previous_sibling("span", id=True)
                    # check if previous sibling is span with an id
                    if prev_span:
                        # add classes for css handling
                        prev_span["class"] = [*prev_span.get("class", []), "anchor-before-heading"]
                        if number == 0:
                            prev_span["class"] = [*prev_span.get("class", []), "first"]
                        if number % 2 == 0:
                            prev_span["class"] = [*prev_span.get("class", []), "even"]
                        else:
                            prev_span["class"] = [*prev_span.get("class", []), "odd"]
                        if len(headings) - 1 == number:
                            prev_span["class"] = [*prev_span.get("class", []), "last"]

        logger.debug("DEBUG HTML START")
        logger.debug(soup.prettify(formatter="html"))
        logger.debug("DEBUG HTML END")
        return str(soup)


def setup(app: Sphinx) -> dict[str, Any]:
    app.add_config_value("simplepdf_vars", {}, "html", types=[dict])
    app.add_config_value("simplepdf_file_name", None, "html", types=[str])
    app.add_config_value("simplepdf_debug", False, "html", types=bool)
    app.add_config_value("simplepdf_weasyprint_timeout", None, "html", types=[int])
    app.add_config_value("simplepdf_weasyprint_retries", 0, "html", types=[int])
    app.add_config_value("simplepdf_weasyprint_flags", None, "html", types=[list])
    app.add_config_value("simplepdf_weasyprint_filter", [], "html", types=[list])
    app.add_config_value("simplepdf_use_weasyprint_api", None, "html", types=[bool])
    app.add_config_value("simplepdf_theme", "simplepdf_theme", "html", types=[str])
    app.add_config_value("simplepdf_theme_options", {}, "html", types=[dict])
    app.add_config_value("simplepdf_sidebars", {"**": ["localtoc.html"]}, "html", types=[dict])
    app.add_builder(SimplePdfBuilder)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
