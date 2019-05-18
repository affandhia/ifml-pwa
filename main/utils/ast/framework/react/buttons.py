import logging

from yattag import Doc

from main.utils.ast.base import Node
from main.utils.ast.language.eseight import ImportStatementType, \
    VarDeclType, MethodAsInstanceVarDeclType
from main.utils.naming_management import dasherize, camel_function_style, \
    creating_title_sentence_from_dasherize_word
from .base import NGX_SMART_MODAL_LOCATION, ReactMainModule

logger_ifml_angular_interpreter = logging.getLogger(
    "main.utils.ast.framework.angular.buttons")


class ButtonWithFunctionHandler(Node):

    def __init__(self, name, type=''):
        self.function_handler_name = camel_function_style(name)
        self.button_id_name = dasherize(name)
        self.button_text = creating_title_sentence_from_dasherize_word(name)
        self.function_holder = MethodAsInstanceVarDeclType(
            self.function_handler_name)
        self.function_node = self.function_holder.function_as_value
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
        with tag('button',
                 ('id', 'view-event-{name}'.format(name=self.button_id_name)),
                 ('class', 'event view-element-event'),
                 ('(click)', "{handler}({obj_param})".format(
                     handler=self.function_node.function_name,
                     obj_param=self.object_param))):
            text(self.button_text)

        return doc.getvalue()

    def render(self):
        # Rendering function first
        function_node = self.function_node.render()

        # Rendering Button HTML
        html = self.button_template()

        return html, function_node


class MenuButton(ButtonWithFunctionHandler):

    def __init__(self, name, type=''):
        super().__init__(name, type)

    def button_template(self):
        doc, tag, text = Doc().tagtext()
        with tag('button',
                 ('id', 'view-event-{name}'.format(name=self.button_id_name)),
                 ('class', 'event view-element-event'),
                 ('(click)', "{handler}({obj_param})".format(
                     handler=self.function_node.function_name,
                     obj_param=self.object_param))):
            with tag('a', id='v-menu-{name}'.format(name=self.button_id_name),
                     klass='menu-a'):
                text(self.button_text)

        return doc.getvalue()


class OnclickType(ButtonWithFunctionHandler):

    def __init__(self, name, type=''):
        super().__init__(name, type=type)

    def onclick_html_call(self):
        ngsubmit_string = '(click)=\'{handler}({obj_param})\''.format(
            handler=self.function_node.function_name,
            obj_param=self.object_param)
        return ngsubmit_string

    def render(self):
        # Rendering function first
        function = self.function_node.render()

        # Rendering OnClick HTML
        html = self.onclick_html_call()

        return html, function


class SubmitButtonType(ButtonWithFunctionHandler):
    """
    Represent submit button in IFML where create a clicked button event
    listener function. This function is in a form of property of component
    class. Later, this function will call the API produced by action event
    IFML. This API calling will be supplied by the required parameter by the
    API itself.

    handlerMethod = (e) => {...}

    <button onClick={this.handlerMethod} id="button-name" name="name" >
        Name
    </button>

    """

    def __init__(self, name, type=''):
        super().__init__(name, type=type)

    def button_template(self):
        """
        As simple as to create a button JSX.

        :return: Button JSX
        """

        return f'''\
        <button
          onClick={{this.{self.function_holder.variable_name}}}
          id="button-{self.button_id_name}"
          name="{self.button_id_name}"
        >
          {self.button_text}
        </button>
        '''

    def ngsubmit_html_call(self):
        ngsubmit_string = '(ngSubmit)=\'{handler}({obj_param})\''.format(
            handler=self.function_node.function_name,
            obj_param=self.object_param)
        return ngsubmit_string

    def render(self):
        # Rendering function first
        function = self.function_holder.render()

        # Rendering Button HTML
        html = self.button_template()

        # Rendering ngSubmit Call HTML
        ngsubmit = self.ngsubmit_html_call()

        return html, function, ngsubmit


class ModalButtonAndFunction(ButtonWithFunctionHandler):

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
        self.ngx_service_constructor.variable_datatype = ReactMainModule.IMPORTED_SMART_MODAL_SERVICE

    def importing_ngx_modal_service_node(self):
        self.import_ngx_modal_service_node = ImportStatementType()
        self.import_ngx_modal_service_node.set_main_module(
            NGX_SMART_MODAL_LOCATION)
        self.import_ngx_modal_service_node.add_imported_element(
            ReactMainModule.IMPORTED_SMART_MODAL_SERVICE)

    def set_target_modal(self, modal_identifier):
        self.add_statement_into_function_body(
            'this.{servicevar}.getModal(\'{modal_name}\').open();'.format(
                servicevar=self.service_var_name,
                modal_name=modal_identifier))

    def button_template(self):
        doc_landmark, tag_landmark, text_landmark = Doc().tagtext()
        with tag_landmark('button', ('class', 'landmark-event'),
                          ('id', 'view-event-{name}'.format(
                              name=self.button_id_name)),
                          ('(click)', "{handler}({obj_param})".format(
                              handler=self.function_node.function_name,
                              obj_param=self.object_param))
                          ):
            text_landmark(self.button_text)
