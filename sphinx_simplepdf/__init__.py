from sphinx_simplepdf.directives.ifbuilder import IfBuilderDirective, IfBuilder


def setup(app):
    app.add_node(IfBuilder)
    app.add_directive('if-builder', IfBuilderDirective)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
