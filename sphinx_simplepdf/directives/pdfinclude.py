from docutils import nodes
from docutils.parsers.rst import Directive, directives

from sphinx.util import logging

logger = logging.getLogger(__name__)


class PdfIncludeDirective(Directive):
    """
    Directive to add content based on builder.
    """
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "width": directives.length_or_percentage_or_unitless,
        "height": directives.length_or_percentage_or_unitless,
        "page": directives.positive_int,
        "toolbar": directives.nonnegative_int,
    }

    def __init__(self, *args, **kw):
        self.pdf_specs = ''

        super().__init__(*args, **kw)

    @property
    def env(self):
        return self.state.document.settings.env

    def _add_spec(self, name, option, default=None):
        spec = self.options.get(option, default)

        if spec is not None:
            if self.pdf_specs == '':
                self.pdf_specs = '#'

            self.pdf_specs += f"{name}={spec}&"

    def run(self):
        """Embeds a PDF into HTML code"""

        pdf_file = self.arguments[0]
        height = self.options.get("height", "400px")
        width = self.options.get("width", "100%")

        self._add_spec('page', 'page')
        self._add_spec('toolbar', 'toolbar')

        html_code = f'<iframe src="{pdf_file}{self.pdf_specs}" style="height: {height}; width: {width}"></iframe>'
        node = nodes.raw('', html_code, format='html')

        return [node]
