from sphinx_simplepdf.directives.ifbuilder import IfBuilderDirective, IfBuilder
from sphinx_simplepdf.directives.ifinclude import IfIncludeDirective, IfInclude


def setup(app):
    app.add_node(IfBuilder)
    app.add_directive('if-builder', IfBuilderDirective)
    app.add_directive('if-include', IfIncludeDirective)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
