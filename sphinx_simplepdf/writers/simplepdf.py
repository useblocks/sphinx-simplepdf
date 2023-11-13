import logging

from docutils import nodes
from docutils.nodes import Element
from sphinx.locale import __
from sphinx.writers.html5 import HTML5Translator

logger = logging.getLogger(__name__)


class SimplepdfTranslator(HTML5Translator):

    def get_secnumber(self, node: Element) -> tuple[int, ...] | None:
        if node.get('secnumber'):
            return node['secnumber']

        if isinstance(node.parent, nodes.section):
            docname = self.docnames[-1]
            anchorname = "{}/#{}".format(docname, node.parent['ids'][0])
            if anchorname not in self.builder.secnumbers:
                anchorname = "%s/" % docname  # try first heading which has no anchor

            if self.builder.secnumbers.get(anchorname):
                return self.builder.secnumbers[anchorname]

        return None

    def add_secnumber(self, node: Element) -> None:
        secnumber = self.get_secnumber(node)
        if secnumber:
            self.body.append('<span class="section-number">')
            self.body.append('.'.join(map(str, secnumber)) + self.secnumber_suffix)
            self.body.append('</span>')

    def get_fignumber(self, node: Element) -> str | None:
        figtype = self.builder.env.domains['std'].get_enumerable_node_type(node)
        if not figtype:
            return None

        if len(node['ids']) == 0:
            msg = __('Any IDs not assigned for %s node') % node.tagname
            logger.warning(msg, location=node)
            return None

        key = f"{self.docnames[-1]}/{figtype}"
        figure_id = node['ids'][0]
        if figure_id not in self.builder.fignumbers.get(key, {}):
            return None

        prefix = self.config.numfig_format.get(figtype)
        if prefix is None:
            msg = __('numfig_format is not defined for %s') % figtype
            logger.warning(msg)
            return None

        numbers = self.builder.fignumbers[key][figure_id]
        return prefix % '.'.join(map(str, numbers))

    def add_fignumber(self, node: Element) -> None:
        fignumber = self.get_fignumber(node)
        if fignumber:
            self.body.append('<span class="caption-number">')
            self.body.append(fignumber + ' ')
            self.body.append('</span>')
