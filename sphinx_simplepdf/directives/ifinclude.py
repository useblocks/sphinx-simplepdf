from docutils import nodes
from docutils.parsers.rst import Directive


from docutils import nodes
from pathlib import Path


from sphinx.util import logging

logger = logging.getLogger(__name__)


class IfIncludeDirective(Directive):
    """
    Directive to add a file based on builder.
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
        """Includes the file only, if specified builder is used"""

        builder = self.arguments[0]

        if self.env.app.builder.name.upper() == builder.upper():

            include_list = self.content

            # files get added in reversed order, probable cause is static target in doc, inserting element 1 at line
            # xy and then inserting element 2 at line xy leads to element 2 being in front of element 1
            # solution -> reverse list
            for file in reversed(include_list):

                file = Path(file)
                self.state_machine.insert_input([".. include:: " + str(file)],
                                                self.state_machine.document.attributes["source"])

        return []


