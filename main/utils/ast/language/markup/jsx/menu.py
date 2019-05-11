from main.utils.ast.base import Node
from main.utils.jinja.language.markup.jsx import base_jsx_writer
from yattag import Doc


class JSXMenuTemplate(Node):
    def __init__(self, name, auth_enabled=False):
        self.auth_enabled = auth_enabled
        self.menu_name = name
        self.button_list = []

    def append_html_into_body(self, button):
        doc, tag, text = Doc().tagtext()
        with tag('li'):
            doc.asis(button)
        self.button_list.append(doc.getvalue())

    def render(self):
        return base_jsx_writer('menu.jsx.template',
                               list_button='\n'.join(self.button_list),
                               menu_name=self.menu_name,
                               auth_enabled=self.auth_enabled)
