from main.utils.ast.base import Node
from main.utils.jinja.html_template import base_html_writer
from yattag import Doc


class HTMLMenuTemplate(Node):
    def __init__(self):
        self.button_list = []

    def add_button_to_menu(self, button):
        doc, tag, text = Doc.tagtext()
        with tag('li'):
            text(button)
        self.button_list.append(doc.getvalue())

    def render(self):
        return base_html_writer('menu.html.template', list_button='\n'.join(self.button_list))
