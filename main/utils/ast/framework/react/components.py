from main.utils.ast.base import Node
from main.utils.ast.language.eseight import ImportStatementType, \
    EseightClassType, VarDeclType
from main.utils.jinja.angular import component_file_writer, angular_html_writer
from main.utils.naming_management import camel_classify, dasherize, \
    camel_function_style, \
    creating_title_sentence_from_dasherize_word

from .base import ANGULAR_ROUTER_MODULE, REACT_MODULE


class ReactComponentEseightClass(EseightClassType):
    def __init__(self):
        super().__init__()
        self.component_name = ''
        self.set_import_and_constructor()

    def set_import_and_constructor(self):
        # Adding import statement for Basic Component
        import_component_from_react_core = ImportStatementType()
        import_component_from_react_core.set_main_module(REACT_MODULE)
        self.import_dict[
            REACT_MODULE] = import_component_from_react_core

        # Importing Routing Purpose
        import_component_from_angular_router = ImportStatementType()
        import_component_from_angular_router.set_main_module(
            ANGULAR_ROUTER_MODULE)
        import_component_from_angular_router.add_imported_element(
            'ActivatedRoute')
        import_component_from_angular_router.add_imported_element('Router')
        self.import_dict[
            ANGULAR_ROUTER_MODULE] = import_component_from_angular_router

        # Adding ActivatedRoute and Router in constructor
        activated_route_var = VarDeclType('route')
        activated_route_var.variable_datatype = 'ActivatedRoute'
        activated_route_var.acc_modifiers = 'private'

        router_var = VarDeclType('router')
        router_var.variable_datatype = 'Router'
        router_var.acc_modifiers = 'private'

        self.set_constructor_param(activated_route_var)
        self.set_constructor_param(router_var)

    def set_component_selector_class_name(self, name):
        self.class_name = camel_classify(name)
        self.component_name = dasherize(name)

    def set_component_name(self, component_name):
        self.component_name = component_name

    def render(self):
        pass


class AngularComponent(Node):
    SUFFIX_TYPESCRIPT_COMPONENT_FILENAME = '.component.ts'
    SUFFIX_HTML_COMPONENT_FILENAME = '.component.html'
    SUFFIX_CSS_COMPONENT_FILENAME = '.component.css'

    def __init__(self, component_typescript_class, component_html):
        self.component_typescript_class = component_typescript_class
        self.component_html = component_html
        self.component_name = self.component_typescript_class.selector_name
        self.typescript_component_name = self.component_name + self.SUFFIX_TYPESCRIPT_COMPONENT_FILENAME
        self.typescript_html_name = self.component_name + self.SUFFIX_HTML_COMPONENT_FILENAME
        self.typescript_css_name = self.component_name + self.SUFFIX_CSS_COMPONENT_FILENAME
        self.routing_path = ''

    def set_routing_node(self, routing_path):
        self.routing_path = routing_path

    def get_routing_path(self):
        return self.routing_path

    def get_component_name(self):
        return self.component_name

    def get_typescript_component_filename(self):
        return self.typescript_component_name

    def get_typescript_class_node(self):
        return self.component_typescript_class

    def get_component_html(self):
        return self.component_html

    def build(self):
        return {self.component_name: {
            self.typescript_component_name: self.component_typescript_class.render(),
            self.typescript_html_name: self.component_html.render(),
            self.typescript_css_name: ''}}


class AngularComponentForModal(AngularComponent):
    SUFFIX_TYPESCRIPT_COMPONENT_FILENAME = '.component.ts'
    SUFFIX_HTML_COMPONENT_FILENAME = '.component.html'
    SUFFIX_CSS_COMPONENT_FILENAME = '.component.css'

    def __init__(self, component_typescript_class, component_html):
        super().__init__(component_typescript_class, component_html)
        self.modal_identifier = self.component_html.var_camel_name


class AngularComponentTypescriptClass(EseightClassType):
    def __init__(self):
        super().__init__()
        self.selector_name = ''
        self.component_name = ''
        self.set_import_and_constructor()

    def set_import_and_constructor(self):
        # Adding import statement for Basic Component
        import_component_from_react_core = ImportStatementType()
        import_component_from_react_core.set_main_module(REACT_MODULE)
        import_component_from_react_core.add_imported_element('Component')
        import_component_from_react_core.add_imported_element('OnInit')
        self.import_dict[
            REACT_MODULE] = import_component_from_react_core

        # Importing Routing Purpose
        import_component_from_angular_router = ImportStatementType()
        import_component_from_angular_router.set_main_module(
            ANGULAR_ROUTER_MODULE)
        import_component_from_angular_router.add_imported_element(
            'ActivatedRoute')
        import_component_from_angular_router.add_imported_element('Router')
        self.import_dict[
            ANGULAR_ROUTER_MODULE] = import_component_from_angular_router

        # Adding ActivatedRoute and Router in constructor
        activated_route_var = VarDeclType('route')
        activated_route_var.variable_datatype = 'ActivatedRoute'
        activated_route_var.acc_modifiers = 'private'

        router_var = VarDeclType('router')
        router_var.variable_datatype = 'Router'
        router_var.acc_modifiers = 'private'

        self.set_constructor_param(activated_route_var)
        self.set_constructor_param(router_var)

    def set_component_selector_class_name(self, name):
        self.selector_name = dasherize(name)
        self.class_name = camel_classify(name)
        self.component_name = dasherize(name)

    def set_selector_name(self, selector_name):
        self.selector_name = selector_name

    def set_component_name(self, component_name):
        self.component_name = component_name

    def render(self):
        # Rendering all import statement
        import_statement_list = []
        for _, import_statement in self.import_dict.items():
            import_statement_list.append(import_statement.render())

        # Rendering all constructor param statement
        constructor_param_list = []
        for _, param in self.constructor_param.items():
            constructor_param_list.append(param.render())

        # Rendering all property decl statement
        property_decl_list = []
        for _, prop in self.property_decl.items():
            property_decl_list.append(prop.render())

        return component_file_writer('basic.component.ts.template',
                                     selector_name=self.selector_name,
                                     class_name=self.class_name,
                                     component_name=self.component_name,
                                     constructor_param=', '.join(
                                         constructor_param_list),
                                     body='\n'.join(self.body),
                                     import_statement_list='\n'.join(
                                         import_statement_list),
                                     property_decl='\n'.join(
                                         property_decl_list),
                                     constructor_body='\n'.join(
                                         self.constructor_body))


class AngularComponentWithInputTypescriptClass(
    AngularComponentTypescriptClass):
    def __init__(self):
        super().__init__()


class AngularComponentHTML(Node):
    def __init__(self):
        self.body = []

    def append_html_into_body(self, html_element):
        self.body.append(html_element)

    def render(self):
        return angular_html_writer('basic.component.html.template',
                                   body='\n'.join(self.body))


class AngularFormHTML(AngularComponentHTML):

    def __init__(self, name):
        super().__init__()
        self.on_submit_call = ''
        self.input_list = []
        self.form_varcamel = camel_function_style(name)
        self.form_dasherize = dasherize(name)
        self.form_title = creating_title_sentence_from_dasherize_word(
            self.form_dasherize)

    def append_html_into_body(self, input_html_string):
        self.input_list.append(input_html_string)

    def add_submit_event(self, on_submit):
        self.on_submit_call = on_submit

    def render(self):
        return angular_html_writer('angular_form.html.template',
                                   form_title=self.form_title,
                                   form_dasherize=self.form_dasherize,
                                   on_submit_call=self.on_submit_call,
                                   form_varcamel=self.form_varcamel,
                                   input_list='\n'.join(self.input_list))


class AngularDetailHTMLCall(Node):

    def __init__(self, name):
        super().__init__()
        self.selector_name = name
        self.parameter_and_property_pair_list = []

    def add_parameter_and_property_pair(self, parameter, property):
        parameter_name = parameter.variable_name
        property_name = property.variable_name
        self.parameter_and_property_pair_list.append(
            (parameter_name, property_name))

    def render(self):
        return angular_html_writer('detail_call.html.template',
                                   selector_name=self.selector_name,
                                   parameter_and_property_pair_list=self.parameter_and_property_pair_list)


class AngularFormHTMLCall(AngularDetailHTMLCall):

    def __init__(self, name):
        super().__init__(name)

    def render(self):
        return angular_html_writer('form_call.html.template',
                                   selector_name=self.selector_name,
                                   parameter_and_property_pair_list=self.parameter_and_property_pair_list)


class AngularListHTMLCall(Node):

    def __init__(self, name):
        super().__init__()
        self.selector_name = name
        self.parameter_and_property_pair_list = []

    def add_parameter_and_property_pair(self, parameter, property):
        tuple_param_prop_pair = (
            parameter.variable_name, property.variable_name)
        self.parameter_and_property_pair_list.append(tuple_param_prop_pair)

    def render(self):
        return angular_html_writer('list_call.html.template',
                                   selector_name=self.selector_name,
                                   parameter_and_property_pair_list=self.parameter_and_property_pair_list)


class AngularListHTMLLayout(AngularComponentHTML):

    def __init__(self):
        super().__init__()
        self.onclick = ''

    def add_onclick(self, onclick):
        self.onclick = onclick

    def render(self):
        return angular_html_writer('unordered_list_element.html.template',
                                   onclick=self.onclick,
                                   body='\n'.join(self.body))


class AngularModalHTMLLayout(AngularComponentHTML):

    def __init__(self, name):
        super().__init__()
        self.var_camel_name = camel_function_style(name)
        self.dasherize_name = dasherize(name)
        self.title_name = creating_title_sentence_from_dasherize_word(name)

    def render(self):
        return angular_html_writer('modal_layout.html.template',
                                   var_camel_name=self.var_camel_name,
                                   dasherize_name=self.title_name,
                                   title_name=self.title_name,
                                   body='\n'.join(self.body))
