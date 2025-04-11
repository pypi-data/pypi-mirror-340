from functools import partial
from docutils import nodes
from docutils.parsers.rst import directives
from pygments.lexers import get_all_lexers
from sphinx.highlighting import lexer_classes
from sphinx.util.docutils import SphinxDirective
from sphinx.directives.code import CodeBlock

LEXER_MAP = {}
for lexer in get_all_lexers():
    for short_name in lexer[1]:
        LEXER_MAP[short_name] = lexer[0]


class SphinxTabsContainer(nodes.container):
    pass


class SphinxTabsPanel(nodes.container):
    pass


class SphinxTabsTab(nodes.paragraph):
    pass


class SphinxTabsTablist(nodes.container):
    pass


class TabsDirective(SphinxDirective):
    """Top-level tabs directive"""

    has_content = True

    def run(self):
        """Parse a tabs directive"""
        self.assert_has_content()

        node = nodes.container(type="tab-element")
        self.state.nested_parse(self.content, self.content_offset, node)

        return [node]


class TabDirective(SphinxDirective):
    """Tab directive, for adding a tab to a collection of tabs"""

    has_content = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        """Parse a tab directive"""
        self.assert_has_content()

        tab_name = SphinxTabsTab()
        self.state.nested_parse(self.content[0:1], 0, tab_name)
        # Remove the paragraph node that is created by nested_parse
        tab_name.children[0].replace_self(tab_name.children[0].children)

        tab_title = tab_name.children[0].astext()
        if tab_title not in self.env.config.tabs_select:
            return []

        # Use base docutils classes
        node = nodes.container()
        self.state.nested_parse(self.content[1:], self.content_offset, node)

        return [node]


class GroupTabDirective(TabDirective):
    """Tab directive that toggles with same tab names across page"""

    has_content = True

    def run(self):
        self.assert_has_content()

        node = super().run()
        return node


class CodeTabDirective(GroupTabDirective):
    """Tab directive with a codeblock as its content"""
    has_content = True
    required_arguments = 1  # Lexer name
    optional_arguments = 1  # Custom label
    final_argument_whitespace = True
    option_spec = {  # From sphinx CodeBlock
        "force": directives.flag,
        "linenos": directives.flag,
        "dedent": int,
        "lineno-start": int,
        "emphasize-lines": directives.unchanged_required,
        "caption": directives.unchanged_required,
        "class": directives.class_option,
        "name": directives.unchanged,
    }

    def run(self):
        """Parse a code-tab directive"""
        self.assert_has_content()

        if len(self.arguments) > 1:
            tab_name = self.arguments[1]
        elif self.arguments[0] in lexer_classes and not isinstance(
                lexer_classes[self.arguments[0]], partial
        ):
            tab_name = lexer_classes[self.arguments[0]].name
        else:
            try:
                tab_name = LEXER_MAP[self.arguments[0]]
            except KeyError as invalid_lexer_error:
                raise ValueError(
                    f"Lexer not implemented: {self.arguments[0]}"
                ) from invalid_lexer_error


        # All content parsed as code
        code_block = CodeBlock.run(self)

        # Reset to generate tab node
        self.content.data = [tab_name, ""]
        self.content.items = [(None, 0), (None, 1)]

        node = super().run()
        if len(node):
            node[0].extend(code_block)
        return node


def setup(app):
    """Set up the plugin"""
    app.add_config_value("tabs_select", [], "")
    # if not set tabs_select, will not use this plugin override sphinx-tabs.tabs
    if not app.config.tabs_select:
        return
    # override the tabs directive from sphinx-tabs.tabs
    app.add_directive("tabs", TabsDirective, override=True)
    app.add_directive("tab", TabDirective, override=True)
    app.add_directive("group-tab", GroupTabDirective, override=True)
    app.add_directive("code-tab", CodeTabDirective, override=True)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
