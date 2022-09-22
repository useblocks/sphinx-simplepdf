from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives import images
from docutils.statemachine import ViewList
from sphinx.util.nodes import nested_parse_with_titles

from sphinx.util import logging

logger = logging.getLogger(__name__)


class PdfImage(nodes.General, nodes.Element):
    pass


class PdfImageDirective(Base):
    """
    Directive to add content based on builder.
    """
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "page": directives.unchanged_required
    }

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def run(self):
        """Creates an image from a PDF file and presents this image"""
        pdf_path = self.arguments[0]

        content_node = nodes.container()
        nodes.I

        return [content_node]
