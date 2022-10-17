from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import ViewList
from sphinx.util.nodes import nested_parse_with_titles

from sphinx.util import logging

logger = logging.getLogger(__name__)


class IfBuilderDirective(Directive):
    """
    Directive to add content based on builder.
    """
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    @property
    def docname(self):
        return self.state.document.settings.env.docname

    @property
    def env(self):
        return self.state.document.settings.env

    def run(self):
        """Renders the content only, if specified builder is used"""

        builder = self.arguments[0]

        content_node = nodes.container()
        if self.env.app.builder.name.upper() == builder.upper():
            rst = ViewList()
            for line in self.content:
                rst.append(line, self.docname, self.lineno)
            node_collection_content = nodes.Element()
            node_collection_content.document = self.state.document
            nested_parse_with_titles(self.state, rst, node_collection_content)
            content_node += node_collection_content.children

        return [content_node]
