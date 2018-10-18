import logging

from yattag import Doc

from main.utils.ast.base import Node
from main.utils.ast.language.typescript import FunctionDeclType
from main.utils.naming_management import dasherize, camel_function_style, creating_title_sentence_from_dasherize_word

logger_ifml_angular_interpreter = logging.getLogger("main.utils.ast.framework.angular.buttons")


class AngularButtonWithFunctionHandler(Node):

    def __init__(self, name, type=''):
        self.function_handler_name = camel_function_style(name)
        self.button_id_name = dasherize(name)
        self.button_text = creating_title_sentence_from_dasherize_word(name)
        self.function_node = FunctionDeclType(self.function_handler_name)
        self.function_node.function_type = type
        self.object_param = ''

    def add_function_param(self, param):
        self.function_node.add_param(param)

    def add_html_object_param(self, object_param):
        self.object_param = object_param

    def add_statement_into_function_body(self, statement):
        self.function_node.add_statement_to_body(statement)

    def button_template(self):
        doc, tag, text = Doc().tagtext()
        with tag('button', ('id', 'view-event-{name}'.format(name=self.button_id_name)),
                 ('class', 'event view-element-event'), ('(click)', "{handler}({obj_param})".format(
                    handler=self.function_node.function_name, obj_param=self.object_param))):
            text(self.button_text)

        return doc.getvalue()

    def render(self):
        # Rendering function first
        function = self.function_node.render()

        # Rendering Button HTML
        html = self.button_template()

        return html, function

class AngularOnclickType(AngularButtonWithFunctionHandler):

    def __init__(self, name, type=''):
        super().__init__(name, type=type)

    def onclick_html_call(self):
        ngsubmit_string = '(click)=\'{handler}({obj_param})\''.format(handler=self.function_node.function_name,
                                                                         obj_param=self.object_param)
        return ngsubmit_string

    def render(self):
        # Rendering function first
        function = self.function_node.render()

        # Rendering OnClick HTML
        html = self.onclick_html_call()

        return html, function

class AngularSubmitButtonType(AngularButtonWithFunctionHandler):

    def __init__(self, name, type=''):
        super().__init__(name, type=type)

    def button_template(self):
        doc, tag, text = Doc().tagtext()
        with tag('button', ('type', 'submit'), ('id', 'onsubmit-event-{name}'.format(name=self.button_id_name)),
                 ('class', 'event onsubmit-event')):
            text(self.button_text)

        return doc.getvalue()

    def ngsubmit_html_call(self):
        ngsubmit_string = '(ngSubmit)=\'{handler}({obj_param})\''.format(handler=self.function_node.function_name,
                                                                         obj_param=self.object_param)
        return ngsubmit_string

    def render(self):
        # Rendering function first
        function = self.function_node.render()

        # Rendering Button HTML
        html = self.button_template()

        # Rendering ngSubmit Call HTML
        ngsubmit = self.ngsubmit_html_call()

        return html, function, ngsubmit
