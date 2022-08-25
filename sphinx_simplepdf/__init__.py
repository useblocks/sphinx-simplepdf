from sphinx_simplepdf.directives.ifbuilder import IfBuilderDirective, IfBuilder


def setup(app):
    app.add_node(IfBuilder)
    app.add_directive('if-builder', IfBuilderDirective)
