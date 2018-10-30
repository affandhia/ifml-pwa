from main.utils.ast.base import Node
from main.utils.jinja.angular import base_file_writer

class LoginTypescriptClass(Node):

    def __init__(self):
        super().__init__()
        self.selector_name = 'login'
        self.class_name = 'Login'

    def render(self):
        return base_file_writer('src/app/login/login.component.ts.template')

    def get_class_name(self):
        return self.class_name

class LoginHTML(Node):

    def __init__(self):
        super().__init__()

    def render(self):
        return base_file_writer('src/app/login/login.component.html.template')