from main.utils.ast.base import Node
from main.utils.jinja.html_template import base_html_writer
from yattag import Doc


class HTMLMenuTemplate(Node):
    def __init__(self, name):
        self.menu_name = name
        self.button_list = []

    def append_html_into_body(self, button):

        doc, tag, text = Doc().tagtext()
        with tag('li'):
            doc.asis(button)
        self.button_list.append(doc.getvalue())

    def render(self):
        return base_html_writer('menu.html.template', list_button='\n'.join(self.button_list), menu_name=self.menu_name)
