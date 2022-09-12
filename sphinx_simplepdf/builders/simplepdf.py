import os
from typing import Any, Dict
import subprocess

import sass

from bs4 import BeautifulSoup

from sphinx.application import Sphinx

from sphinx.builders.singlehtml import SingleFileHTMLBuilder


class SimplePdfBuilder(SingleFileHTMLBuilder):
    name = "simplepdf"
    format = "html"  # Must be html instead of "pdf", otherwise plantuml has problems
    file_suffix = ".pdf"
    links_suffix = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.app.config.html_theme != "simplepdf_theme":
            print("Setting theme to sphinx_simplepdf")
            # We need to overwrite some config values, as they are set for the normal html build, but
            # simplepdf can normally not handle them.
            self.app.config.html_theme = "simplepdf_theme"
            self.app.config.html_sidebars = {'**': ["localtoc.html"]}
            self.app.config.html_theme_options = {}  # Sphinx would write warnings, if given options are unsupported.

        # Generate main.css
        print('Generating css files from scss-templates')
        css_folder = os.path.join(self.app.outdir, f'_static/styles')
        scss_folder = os.path.join(os.path.dirname(__file__), '../themes/simplepdf_theme/static/styles/sources')
        #print(f'css_folder: {css_folder}')
        #print(f'scss_folder: {scss_folder}')
        sass.compile(dirname=(scss_folder, css_folder), output_style='nested',
                     custom_functions={sass.SassFunction('config', ('$a', '$b'), self.get_config_var)}
                     )

    def get_config_var(self, name, default):
        """
        Gets a config variables for scss out of the Sphinx configuration.
        If name is not found in config, the specified defualt var is returned.

        Args:
            name: Name of the config vr to use
            default: Default value, if name can not be found in config

        Returns: Value
        """
        simplepdf_vars = self.app.config.simplepdf_vars
        if name not in simplepdf_vars:
            return default
        return simplepdf_vars[name]

    def finish(self) -> None:
        super().finish()

        index_path = os.path.join(self.app.outdir, f'{self.app.config.root_doc}.html')

        # Manipulate index.html
        with open(index_path, 'rt', encoding='utf-8') as index_file:
            index_html = "".join(index_file.readlines())

        new_index_html = self._toctree_fix(index_html)

        with open(index_path, 'wt', encoding='utf-8') as index_file:
            index_file.writelines(new_index_html)


        args = [
            'weasyprint',
            index_path,
            os.path.join(self.app.outdir, f'{self.app.config.project}.pdf'),

        ]
        subprocess.run(args)

    def _toctree_fix(self, html):
        soup = BeautifulSoup(html, "html.parser")
        sidebar = soup.find("div", class_="sphinxsidebarwrapper")

        links = sidebar.find_all('a', class_='reference internal')
        for link in links:
            link['href'] = link['href'].replace(f'{self.app.config.root_doc}.html', '')

        return soup.prettify(formatter='html')


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_config_value("simplepdf_vars", {}, "html", types=[dict])
    app.add_builder(SimplePdfBuilder)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
