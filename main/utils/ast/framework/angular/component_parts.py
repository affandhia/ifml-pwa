from main.utils.ast.base import Node
from main.utils.jinja.angular import angular_html_writer
from main.utils.naming_management import dasherize, camel_function_style, \
    creating_title_sentence_from_dasherize_word


class InputField(Node):

    def __init__(self, name, type='text'):
        self.dasherize_name = dasherize(name)
        self.title_name = creating_title_sentence_from_dasherize_word(name)
        self.var_camel_name = camel_function_style(name)
        self.placeholder = True
        self.value = ''
        self.type = type

    def disable_placeholder(self):
        self.placeholder = False

    def set_default_value(self, value):
        self.value = value

    def render(self):
        return angular_html_writer('form_input.html.template', dasherize_name=self.dasherize_name,
                                   title_name=self.title_name, var_camel_name=self.var_camel_name,
                                   placeholder=self.placeholder, value=self.value, type=self.type)
