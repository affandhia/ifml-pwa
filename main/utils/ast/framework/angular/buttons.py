import logging

from yattag import Doc

from main.utils.ast.base import Node
from main.utils.ast.language.typescript import FunctionDeclType, ImportStatementType, VarDeclType
from main.utils.naming_management import dasherize, camel_function_style, creating_title_sentence_from_dasherize_word
from .base import NGX_SMART_MODAL_LOCATION, AngularMainModule

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

    def add_statements_into_function_body(self, list_of_statement):
        for statement in list_of_statement:
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
        function_node = self.function_node.render()

        # Rendering Button HTML
        html = self.button_template()

        return html, function_node

class AngularMenuButton(AngularButtonWithFunctionHandler):

    def __init__(self, name, type=''):
        super().__init__(name, type)

    def button_template(self):
        doc, tag, text = Doc().tagtext()
        with tag('button', ('id', 'view-event-{name}'.format(name=self.button_id_name)),
                 ('class', 'event view-element-event'), ('(click)', "{handler}({obj_param})".format(
                    handler=self.function_node.function_name, obj_param=self.object_param))):
            with tag('a', id='v-menu-{name}'.format(name=self.button_id_name), klass='menu-a'):
                text(self.button_text)

        return doc.getvalue()


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


class AngularModalButtonAndFunction(AngularButtonWithFunctionHandler):

    def __init__(self, name, type=''):
        super().__init__(name, type)
        self.import_ngx_modal_service_node = None
        self.ngx_service_constructor = None
        self.service_var_name = 'ngxSmartModalService'
        self.declare_ngx_service_param_constructor()
        self.importing_ngx_modal_service_node()

    def declare_ngx_service_param_constructor(self):
        self.ngx_service_constructor = VarDeclType(self.service_var_name)
        self.ngx_service_constructor.acc_modifiers = 'public'
        self.ngx_service_constructor.variable_datatype = AngularMainModule.IMPORTED_SMART_MODAL_SERVICE

    def importing_ngx_modal_service_node(self):
        self.import_ngx_modal_service_node = ImportStatementType()
        self.import_ngx_modal_service_node.set_main_module(NGX_SMART_MODAL_LOCATION)
        self.import_ngx_modal_service_node.add_imported_element(AngularMainModule.IMPORTED_SMART_MODAL_SERVICE)

    def set_target_modal(self, modal_identifier):
        self.add_statement_into_function_body(
            'this.{servicevar}.getModal(\'{modal_name}\').open();'.format(servicevar=self.service_var_name,
                                                                         modal_name=modal_identifier))
