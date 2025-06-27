from collections import Counter
import os
import re
from typing import Any, Dict
import subprocess
import weasyprint

import sass

from bs4 import BeautifulSoup

from sphinx import __version__
from sphinx.application import Sphinx

from sphinx.builders.singlehtml import SingleFileHTMLBuilder

from sphinx_simplepdf.builders.debug import DebugPython

from sphinx.util import logging

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
            "simple_config": {
                x.name: x.value
                for x in self.app.config
                if x.name.startswith("simplepdf")
            },
        }
        self.app.config.html_context["spd"] = debug_sphinx

        # Generate main.css
        logger.info("Generating css files from scss-templates")
        css_folder = os.path.join(self.app.outdir, f"_static")
        scss_folder = os.path.join(
            os.path.dirname(__file__),
            "..",
            "themes",
            "simplepdf_theme",
            "static",
            "styles",
            "sources",
        )
        sass.compile(
            dirname=(scss_folder, css_folder),
            output_style="nested",
            custom_functions={
                sass.SassFunction("config", ("$a", "$b"), self.get_config_var),
                sass.SassFunction(
                    "theme_option", ("$a", "$b"), self.get_theme_option_var
                ),
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

    def finish(self) -> None:
        super().finish()

        index_path = os.path.join(self.app.outdir, f"{self.app.config.root_doc}.html")

        # Manipulate index.html
        with open(index_path, "rt", encoding="utf-8") as index_file:
            index_html = "".join(index_file.readlines())

        new_index_html = self._toctree_fix(index_html)

        with open(index_path, "wt", encoding="utf-8") as index_file:
            index_file.writelines(new_index_html)

        args = ["weasyprint"]

        if isinstance(self.config["simplepdf_weasyprint_flags"], list) and (
            0 < len(self.config["simplepdf_weasyprint_flags"])
        ):
            args.extend(self.config["simplepdf_weasyprint_flags"])

        file_name = (
            self.app.config.simplepdf_file_name or f"{self.app.config.project}.pdf"
        )

        args.extend(
            [
                index_path,
                os.path.join(self.app.outdir, f"{file_name}"),
            ]
        )

        timeout = self.config["simplepdf_weasyprint_timeout"]

        filter_list = self.config["simplepdf_weasyprint_filter"]
        filter_pattern = (
            "(?:% s)" % "|".join(filter_list) if 0 < len(filter_list) else None
        )

        if self.config["simplepdf_use_weasyprint_api"]:
            doc = weasyprint.HTML(index_path)

            doc.write_pdf(
                target=os.path.join(self.app.outdir, f"{file_name}"),
            )

        else:
            retries = self.config["simplepdf_weasyprint_retries"]
            success = False
            for n in range(1 + retries):
                try:
                    wp_out = subprocess.check_output(
                        args, timeout=timeout, text=True, stderr=subprocess.STDOUT
                    )

                    for line in wp_out.splitlines():
                        if filter_pattern is not None and re.match(
                            filter_pattern, line
                        ):
                            pass
                        else:
                            print(line)
                    success = True
                    break
                except subprocess.TimeoutExpired:
                    logger.warning(f"TimeoutExpired in weasyprint, retrying")
                except subprocess.CalledProcessError as e:
                    logger.warning(
                        f"CalledProcessError in weasyprint, retrying\n{str(e)}"
                    )
                finally:
                    if (n == retries - 1) and not success:
                        raise RuntimeError(
                            f"maximum number of retries {retries} failed in weasyprint"
                        )

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
        print("checking for potential toctree page numbering errors")
        soup = BeautifulSoup(html, "html.parser")
        sidebar = soup.find("div", class_="sphinxsidebarwrapper")

        # sidebar contains the toctree
        if sidebar is not None:
            toc_links = sidebar.find_all("a", class_="reference internal")

            # find max toctree lvl
            toctree_lvls = set(
                sidebar.find_all("li", class_=re.compile("toctree-l[1-9]"))
            )

            max_toctree_lvl = 0

            for i in toctree_lvls:
                lvl = int(
                    i["class"][0].split("-l")[-1]
                )  # toctree entries have a single class, example "toctree-l1" for lvl 1, get lvl
                if lvl > max_toctree_lvl:
                    max_toctree_lvl = lvl

            # remove document file reference
            for toc_link in toc_links:
                toc_link["href"] = toc_link["href"].replace(
                    f"{self.app.config.root_doc}.html", ""
                )

            # search for duplicates
            counts = dict(Counter([str(x).split(">")[0] for x in toc_links]))
            references = {key: value for key, value in counts.items()}

            if references:

                print(f"found duplicate chapters:\n{references}")

            for text in references.keys():

                ref = re.findall('href="#.*"', str(text))

                # clean href data for searching
                cleaned_ref_toc = (
                    ref[0].replace('href="', "").replace('"', "")
                )  # "#target"
                cleaned_ref_target = (
                    ref[0].replace('href="#', "").replace('"', "")
                )  # "target"

                occurences = soup.find_all("section", attrs={"id": cleaned_ref_target})

                # name occurences section-id which is the target for internal refs with increasing id
                # occurence-0, occurence-1, occurence-2 ...
                if len(occurences) > 1:
                    occ_counter = 0
                    for occ in occurences:
                        occ["id"] = occ["id"] + "-" + str(occ_counter)
                        occ_counter += 1

                else:
                    continue

                # index of toctree entry
                replace_counter = 0

                # scan all occurences, if occurenca has too high of a HTML headline level compared to the max_toctree_level (depth)
                # the occurence is a "deeper" level which does not correspond to the toctree refernce. This is only needed when there
                # are chaptters with the same name AND one of them is at a level which should not be referenced in the toc but becomes an

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
                                            e_class = element.contents[0].attrs[
                                                "class"
                                            ][0]
                                        except KeyError:
                                            continue

                                        if e_class == "section-number":
                                            target_lvl = int(name[-1])

                                            # if headlinelevel either is max_toctree lvl or + 1 the chapter should be included in the toc
                                            # break both loops and edit occurrence via repalce_counter
                                            if (
                                                target_lvl == max_toctree_lvl + 1
                                                or target_lvl == max_toctree_lvl
                                            ):
                                                match_found = True
                                                break  # headline match found

                                            else:
                                                # skip this occurrence if headline level too big
                                                replace_counter += 1
                                                continue

                            # edit target of toc reference with correct occurence
                            toc_link["href"] = (
                                toc_link["href"] + "-" + str(replace_counter)
                            )
                            replace_counter += 1

                        except IndexError:
                            continue

        for heading_tag in ["h1", "h2"]:
            headings = soup.find_all(heading_tag, class_="")
            for number, heading in enumerate(headings):
                class_attr = heading.attrs["class"] if heading.has_attr("class") else []
                logger.debug(f"found heading {heading}")
                if 0 == number:
                    class_attr.append("first")
                if 0 == number % 2:
                    class_attr.append("even")
                else:
                    class_attr.append("odd")
                if len(headings) - 1 == number:
                    class_attr.append("last")

                heading.attrs["class"] = class_attr

        logger.debug(soup.prettify(formatter="html"))
        return str(soup)


def setup(app: Sphinx) -> Dict[str, Any]:
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
    app.add_config_value(
        "simplepdf_sidebars", {"**": ["localtoc.html"]}, "html", types=[dict]
    )
    app.add_builder(SimplePdfBuilder)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
