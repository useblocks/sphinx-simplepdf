from sphinx_simplepdf.directives.ifbuilder import IfBuilderDirective
from sphinx_simplepdf.directives.ifinclude import IfIncludeDirective
from sphinx_simplepdf.directives.pdfinclude import PdfIncludeDirective
from sphinx_simplepdf.parallel_build import register as register_parallel_build


def setup(app):
    # Register simplepdf config and builder on every build: Sphinx loads this extension
    # for all builders, but only loads builders/simplepdf.py automatically for -b simplepdf.
    from sphinx_simplepdf.builders.simplepdf import setup as _builder_setup

    _builder_setup(app)

    app.add_directive("if-builder", IfBuilderDirective)
    app.add_directive("if-include", IfIncludeDirective)
    app.add_directive("pdf-include", PdfIncludeDirective)

    register_parallel_build(app)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
