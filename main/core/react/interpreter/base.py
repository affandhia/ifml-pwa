import logging

from yattag import Doc

from custom_xmi_parser.umlsymboltable import ClassSymbol, UMLSymbolTable
from custom_xmi_parser.xmiparser_2 import XMIClass, XMIModel
from ifml_parser.ifml_element.interaction_flow.base import NavigationFlow, \
    DataFlow
from ifml_parser.ifml_element.interaction_flow_elements.action_family.base import \
    Action
from ifml_parser.ifml_element.interaction_flow_elements.event_family.catching_event_extension import \
    ViewElementEvent
from ifml_parser.ifml_element.interaction_flow_elements.event_family.view_element_event_extension import \
    OnSubmitEvent, \
    OnSelectEvent
from ifml_parser.ifml_element.interaction_flow_elements.view_family.view_component_parts import \
    SimpleField, \
    DataBinding, VisualizationAttribute, ConditionalExpression
from ifml_parser.ifml_element.interaction_flow_elements.view_family.view_components import \
    Form, Details, List
from ifml_parser.ifml_element.interaction_flow_elements.view_family.view_containers import \
    ViewContainer, Menu, Window
from ifml_parser.ifmlsymboltable import ViewContainerSymbol, WindowSymbol, \
    ActionSymbol, MenuSymbol, IFMLSymbolTable
from ifml_parser.ifmlxmiparser import IFMLModel
from main.utils.ast.framework.angular.buttons import \
    AngularButtonWithFunctionHandler, AngularSubmitButtonType, \
    AngularOnclickType, AngularModalButtonAndFunction, AngularMenuButton
from main.utils.ast.framework.angular.component_parts import InputField, \
    DataBindingFunction, VisualizationWithSpan
from main.utils.ast.framework.angular.components import AngularComponent, \
    AngularComponentTypescriptClass, \
    AngularComponentHTML, AngularFormHTML, AngularDetailHTMLCall, \
    AngularListHTMLCall, AngularListHTMLLayout, \
    AngularModalHTMLLayout, AngularComponentForModal, \
    AngularComponentWithInputTypescriptClass, AngularFormHTMLCall
from main.utils.ast.framework.angular.google_sign_in import LoginHTML, \
    LoginTypescriptClass
from main.utils.ast.framework.angular.models import ModelFromUMLClass, \
    OwnedOperation
from main.utils.ast.framework.angular.parameters import InParameter, \
    OutParameter, ParamGroup, \
    ParameterBindingInterpretation
from main.utils.ast.framework.react.routers import RouteToModule, \
    RedirectToAnotherPath, RootRoutingNode, \
    RouteToComponentPage, RouteToAction, GettingQueryParam
from main.utils.ast.framework.angular.services import AngularService, \
    ActionEventInterpretation
from main.utils.ast.framework.react.base import REACT_ROUTER_DOM_MODULE, \
    REACT_COOKIES_MODULE
from main.utils.ast.language.eseight import ImportStatementType
from main.utils.ast.language.html import HTMLMenuTemplate
from main.utils.ast.language.typescript import VarDeclType
from main.utils.naming_management import dasherize, camel_function_style
from . import BaseInterpreter

from main.utils.ast.framework.react.components import \
    ReactComponentEseightClass, ReactJSX, ReactComponent, MenuJSX

logger_ifml_angular_interpreter = logging.getLogger(
    "main.core.angular.interpreter")

logger_react = logging.getLogger("main.core.react.interpreter")


class IFMLtoReactInterpreter(BaseInterpreter):
    def __init__(self, ifml_xmi: IFMLModel, ifml_symbol_table: IFMLSymbolTable,
                 class_diagram_xmi: XMIModel,
                 class_diagram_symbol_table: UMLSymbolTable,
                 enable_authentication_guard=False):

        self.root_ifml, self.ifml_symbol_table = ifml_xmi, ifml_symbol_table
        self.root_class_diagram_xmi, self.uml_symbol_table = class_diagram_xmi, class_diagram_symbol_table

        # set project name to dashed case, i.e. abs-projectname
        self.project_name = dasherize(self.root_ifml.name)

        self.enable_authentication_guard = enable_authentication_guard
        self.components = {}
        self.services = {}

        # save all model interpreted from UML Class.
        # The first one will be filled.
        self.models = {}
        self.action_events = []
        self.view_element_events = []
        self.list_service_worker_config = []

        # setup initial route for the project.
        # this route will be constructed nested as the XML & IFML interpreted.
        # this root has one must have property called "path"
        self.root_routing = RootRoutingNode('')

        # NOTE: react doesn't have explicit external HTML file or structure.
        # But there's a tool called Babel which transformed the JSX (HTML-like)
        # structure into JS instruction then construct the VDOM based on.
        self.root_template = self.get_root_template()

        # initial root class for the current project.
        self.root_eseight_class = self.get_root_class()

        logger_react.info(
            "Interpreting {name} IFML Project".format(name=self.project_name))

        # Get all the IFML element/node/notation model IFML
        self.ifml_expressing_ui_design = \
            self.root_ifml \
                .get_interaction_flow_model() \
                .get_interaction_flow_model_elements()

        # interpret domain model means the app will process all the class
        # within UML.

        # TODO: do something with model in React
        # react treat data as literal JSON. there is no need to
        # create a specific class and serialized it on.
        # self.interpret_domain_model()

        # Interpret all Interaction Flow Model Elements
        self.interpret_interaction_flow_model()

    def interpret_domain_model(self):
        """
        Interpret all the corresponding class in UML into a model which
        contain its properties.

        class Customer in UML --> Customer: Model

        :return:
        """
        # Build all Class used
        for _, class_xmi in self.root_class_diagram_xmi.get_classes().items():
            self.interpret_uml_class(class_xmi)

    def interpret_uml_class(self, class_xmi: XMIClass):
        """
        Create a model based on given class.

        :param class_xmi:
        :return:
        """

        # Get class name based on UML class.
        element_name = class_xmi.get_model_name()

        logger_react.info("UML name: {element}".format(element=element_name))

        # Interpret it
        model_from_class = ModelFromUMLClass(element_name)

        # Build the owned attribute
        for _, attribute in class_xmi.get_properties().items():
            self.interpret_owned_attribute(attribute, model_from_class)

        # TODO Implement
        # Build the owned operation
        for _, operation in class_xmi.get_operations().items():
            self.interpret_owned_operation(operation, model_from_class)

        # Register to models container
        self.models[class_xmi.get_model_id()] = model_from_class

    def router_outlet_html(self, name):
        doc_outlet, tag_outlet, text_outlet = Doc().tagtext()
        with tag_outlet('div', id=name, klass='div-content-router'):
            with tag_outlet('router-outlet'):
                text_outlet('')
        return doc_outlet.getvalue()

    def append_router_outlet(self, angular_routing, html_call,
                             typescipt_class):
        if len(angular_routing.angular_children_routes) > 0:
            html_call.append_html_into_body(
                self.router_outlet_html(typescipt_class.selector_name))
            angular_routing.enable_children_routing()

    def get_root_class(self):
        root_react_class = ReactComponentEseightClass()
        root_react_class.class_name = 'App'
        root_react_class.component_name = 'App'

        react_router_dom_import = ImportStatementType()
        react_router_dom_import.set_main_module(REACT_ROUTER_DOM_MODULE)
        react_router_dom_import.add_imported_elements([
            'BrowserRouter',
            'Route'
        ])

        react_cookie_import = ImportStatementType()
        react_cookie_import.set_main_module(REACT_COOKIES_MODULE)
        react_cookie_import.add_imported_element('CookiesProvider')

        root_react_class.add_import_statement_using_import_node(
            react_router_dom_import)
        root_react_class.add_import_statement_using_import_node(
            react_cookie_import)

        return root_react_class

    def get_root_template(self):
        root_template_node = ReactJSX()
        return root_template_node

    def get_project_name(self):
        return self.project_name

    def interpret_interaction_flow_model(self):
        """
        Interpret all the expressed ui design in IFML. There are four kind
        of element exist in the IFML, they are Action, Window, Menu,
        View Container.

        :return: None
        """

        for key, interaction_flow_model_element in \
                self.ifml_expressing_ui_design.items():
            # If the root have actions
            if isinstance(interaction_flow_model_element, Action):
                pass
                # self.interpret_action(interaction_flow_model_element)
            # If the root have Windows

            elif isinstance(interaction_flow_model_element, Window):
                # Note: this IFML haven't be used due to lack of things.
                # TODO: remove this one due to unused
                # self.check_if_windows_is_different_than_view_container(
                #     interaction_flow_model_element, self.root_template,
                #     self.root_eseight_class, self.angular_routing)
                pass
            # If the root have menu
            # TODO: after viewcontainer has been implemented, implement this one [SECOND ONE]
            elif isinstance(interaction_flow_model_element, Menu):
                self.interpret_menu(interaction_flow_model_element,
                                    self.root_template)
            # TODO: FOCUS ON THIS ONE FIRST
            elif isinstance(interaction_flow_model_element, ViewContainer):
                pass
                # self.interpret_view_container(interaction_flow_model_element,
                #                               self.root_template,
                #                               self.root_eseight_class,
                #                               self.root_routing)

    def check_if_windows_is_different_than_view_container(self, window_element,
                                                          html_calling,
                                                          typescript_calling,
                                                          routing_parent):
        # Check if there is no difference with view container
        is_new_window = window_element.get_new_window_att()
        is_modal = window_element.get_modal_att()
        if not (is_modal or is_new_window):
            self.interpret_view_container(window_element, html_calling,
                                          typescript_calling, routing_parent)
        else:
            self.interpret_windows(window_element, html_calling,
                                   typescript_calling, routing_parent)

    def interpret_windows(self, window_element, html_calling,
                          typescript_calling, routing_parent):
        # Name of element
        element_name = window_element.get_name()
        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} Windows".format(name=element_name))

        # Modal Typescript class and HTML
        typescript_class = AngularComponentTypescriptClass()
        typescript_class.set_component_selector_class_name(element_name)

        html = AngularModalHTMLLayout(element_name)

        # Build All Associated View Element
        for key, view_element in window_element.get_assoc_view_element().items():
            if isinstance(view_element, List):
                self.interpret_list(view_element, html, typescript_class)

        # Build All View Element Event Inside
        for _, event in window_element.get_view_element_events().items():
            self.view_element_events.append(event)

        # Check if it is a XOR

        # Check if it is a landmark
        if (window_element.get_is_landmark()):
            # Append the Button into root HTML
            func_and_html_event_node = AngularModalButtonAndFunction(
                element_name, type='async')
            func_and_html_event_node.set_target_modal(html.var_camel_name)

            # Import the service, create the constructor param
            typescript_calling.add_import_statement_using_import_node(
                func_and_html_event_node.import_ngx_modal_service_node)
            typescript_calling.set_constructor_param(
                func_and_html_event_node.ngx_service_constructor)

            # Get the function and HTML
            button_html, typescript_function = func_and_html_event_node.render()

            # Append the Button
            html_calling.append_html_into_body(button_html)

            # Append the function
            typescript_calling.body.append(typescript_function)

        # Check if there are any interaction flow, but no need to define anything

        # Creating the Angular Component Node
        angular_component_node = AngularComponentForModal(typescript_class,
                                                          html)

        # Register the Modal Selector the parent HTML
        doc_selector, tag_selector, text_selector = Doc().tagtext()
        with tag_selector(typescript_class.selector_name):
            text_selector('')
        html_calling.append_html_into_body(doc_selector.getvalue())

        # Registering to Components Container
        self.components[window_element.get_id()] = angular_component_node

    def interpret_menu(self, menu_element: Menu,
                       html_calling: ReactJSX):
        """
        Create new ReactComponent for menu element.

        :param menu_element: a menu representative
        :param html_calling: the html block where the menu mounted on
        :return: None
        """

        # Name of element
        element_name = menu_element.get_name()

        logger_react.info(
            "Interpreting a {name} Menu".format(name=element_name))

        # Prepare Component Class
        component_class = ReactComponentEseightClass()
        component_class.set_component_selector_class_name(element_name)

        # Set import for Link element from React Router DOM
        react_router_dom = ImportStatementType()
        react_router_dom.set_main_module('react-router-dom')
        react_router_dom.add_imported_element('Link')

        # add to Component Class imported module list
        component_class.add_import_statement_using_import_node(
            react_router_dom)

        # Prepare HTML
        html = MenuJSX(component_class.selector_name,
                       self.enable_authentication_guard)

        # Build All View Element Event Inside
        # TODO: Why should enlist event globally?
        for _, event in menu_element.get_view_element_events().items():
            self.view_element_events.append(event)

        # The Component Itself
        component_node = ReactComponent(
            component_class=component_class,
            component_markup_language=html)

        # Calling Menu selector
        doc_selector, tag_selector, text_selector = Doc().tagtext()

        with tag_selector(component_class.component_name):
            text_selector('')

        # Menu always appended into first element
        html_calling.append_html_into_body(doc_selector.getvalue())

        # Register to components container
        self.components[menu_element.get_id()] = component_node


    def interpret_view_container(self, view_container: ViewContainer,
                                 html_calling: ReactJSX,
                                 typescript_calling, routing_parent):
        """
        Handle View Container interpretation.

        :param view_container: given IFML element
        :param html_calling: the parent jsx of the view container
        :param typescript_calling: the parent component of the view container
        :param routing_parent: the parent route of the view container
        :return: None
        """
        # Name of element that will be a component name
        element_name = view_container.get_name()

        logger_react.info(
            "Interpreting a {name} View Container".format(name=element_name))

        # prepare the initial component requirements
        html, container_class, routing_node = self.view_container_definition()

        # React treats a component class as a directive selector which means
        # there is no need to re-state the directive name.
        # note: directive is just like an importing component in React.
        container_class.set_component_selector_class_name(element_name)

        # Decide if this container is callable or using router
        # Checking if its is a Landmark or having an interaction flow
        if view_container.get_is_xor():
            routing_node = RouteToModule(container_class,
                                         enable_guard=self.enable_authentication_guard)
            routing_node.enable_children_routing()

        if view_container.get_is_landmark():
            landmark_path_var_name = camel_function_style(
                container_class.class_name) + 'path'

            doc_landmark, tag_landmark, text_landmark = Doc().tagtext()
            with tag_landmark('button', ('class', 'landmark-event'),
                              ('id', container_class.selector_name),
                              ('[routerLink]', landmark_path_var_name)):
                text_landmark(container_class.class_name)

            routing_parent.enable_children_routing()
            routing_node = RouteToModule(container_class,
                                         enable_guard=self.enable_authentication_guard) if routing_node is None else routing_node

            absolute_path = routing_node.path

            landmark_path_var_decl = VarDeclType(landmark_path_var_name, ';')
            landmark_path_var_decl.acc_modifiers = 'public'
            landmark_path_var_decl.value = "\'{value}\'".format(
                value=absolute_path)
            landmark_path_var_decl.variable_datatype = 'string'

            typescript_calling.set_property_decl(landmark_path_var_decl)
            html_calling.append_html_into_body(doc_landmark.getvalue())

        if self.check_if_there_is_an_interaction_flow(
                view_container) and routing_node is None:
            # Enable the parent child routing
            routing_parent.enable_children_routing()
            routing_node = RouteToModule(
                container_class,
                enable_guard=
                self.enable_authentication_guard) if routing_node is None else routing_node

        # Decide if this container is default in its XOR
        if view_container.get_is_default():
            routing_parent.add_children_routing(
                RedirectToAnotherPath('', container_class.selector_name))

        # Build All View Element Event Inside
        for _, event in view_container.get_view_element_events().items():
            if isinstance(event, ViewElementEvent):
                # self.interpret_view_element_event(event, html,
                # typescript_class)
                self.view_element_events.append(event)

        for _, parameter in view_container.get_parameters().items():
            self.interpret_parameter(parameter, container_class, [])

        # Build All Action inside the Container
        for _, action in view_container.get_action().items():
            self.interpret_action(action)

        if routing_node:
            routing_node.path_from_root = routing_parent.path_from_root + '/' + routing_node.path

        # Build All Associated View Element
        for key, view_element in view_container.get_assoc_view_element().items():
            if isinstance(view_element, List):
                self.interpret_list(view_element, html, container_class)
            elif isinstance(view_element, Details):
                self.interpret_detail(view_element, html, container_class)
            elif isinstance(view_element, Form):
                self.interpret_form(view_element, html, container_class)
            elif isinstance(view_element, Window):
                self.check_if_windows_is_different_than_view_container(
                    view_element, html, container_class,
                    routing_node)
            elif isinstance(view_element, Menu):
                self.interpret_menu(view_element, html)
            elif isinstance(view_element, ViewContainer):
                self.interpret_view_container(view_element, html,
                                              container_class, routing_node)

        # The Component Itself
        angular_component_node = AngularComponent(
            component_typescript_class=container_class,
            component_html=html)
        # Add Routing Node and (If exist) any children route
        try:
            routing_parent.add_children_routing(routing_node)
            angular_component_node.set_routing_node(
                routing_node.path_from_root)
            logger_react.debug(routing_node.path_from_root)
            self.append_router_outlet(routing_node, html, container_class)
        # If this container must be called
        except Exception:
            # This exeption catch a component without routing_node.
            # Calling ViewContainer selector
            doc_selector, tag_selector, text_selector = Doc().tagtext()

            with tag_selector(container_class.selector_name):
                text_selector('')
            html_calling.append_html_into_body(doc_selector.getvalue())

        # Register to components container
        self.components[view_container.get_id()] = angular_component_node

    def interpret_action(self, action_element):
        """
        Interpret the given action.

        :param action_element:
        :return:
        """
        # Name of element, the name in a form of API endpoint.
        # e.g. api/myentity/myaction.abs
        element_name = action_element.get_name()

        logger_react.info(
            "Interpreting a {name} Action".format(name=element_name))

        # TODO: what this is variable for
        any_in_param = False

        # TODO: what exactly the condition loop guard on
        # Check if there are any in parameter being defined
        all_param_inside_action = action_element.get_parameters()
        while len(all_param_inside_action) and not any_in_param:
            arbitary_param_inside_action = all_param_inside_action.popitem()[1]
            any_in_param = arbitary_param_inside_action.get_direction() == 'in'

        # Defining service typescript, and add the name into AngularService
        service_typescript = AngularService(
            enable_auth=self.enable_authentication_guard)
        service_typescript.set_endpoint_class_name_and_worker(element_name)

        if any_in_param:
            service_typescript.param_exist()

        # Calling ActionEvent and build it
        for _, action_event in action_element.get_action_event().items():
            self.action_events.append((action_element.get_id(), action_event))

        # Register to services container
        self.services[action_element.get_id()] = service_typescript

        # Register service worker config
        self.list_service_worker_config.append(
            service_typescript.worker_config.render())

    def interpret_form(self, form_element, html_calling, typescript_calling):
        # Name of element
        element_name = form_element.get_name()

        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} Form".format(name=element_name))

        # Only need the routing node and typescript_class
        _, typescript_class, _ = self.view_component_definition()
        typescript_class.set_component_selector_class_name(element_name)

        # The HTML for Form
        html = AngularFormHTML(element_name)

        # Preparing HTML Call template for form
        form_call = AngularFormHTMLCall(typescript_class.selector_name)

        list_in_param = []
        for _, parameter in form_element.get_parameters().items():
            self.interpret_parameter(parameter, typescript_class,
                                     list_in_param)

        # Build all View Component Part
        for _, view_component_part in form_element.get_assoc_view_component_parts().items():
            if isinstance(view_component_part, SimpleField):
                self.interpret_simple_field(view_component_part, html,
                                            typescript_class, list_in_param)
            elif isinstance(view_component_part, DataBinding):
                self.interpret_data_binding(view_component_part, html,
                                            typescript_class, list_in_param)

        # TODO Implement Building all In Direction Parameter
        self.build_in_parameter_for_parent(form_call, typescript_calling,
                                           list_in_param)

        # Build All View Element Event Inside
        for _, event in form_element.get_view_element_events().items():
            self.view_element_events.append(event)

        # Creating the component node
        # The Component Itself
        angular_component_node = AngularComponent(
            component_typescript_class=typescript_class,
            component_html=html)

        # Calling Form selector
        doc_selector, tag_selector, text_selector = Doc().tagtext()

        with tag_selector('div', id='div-form-{name}'.format(
                name=html.form_dasherize),
                          klass='div-form view-component'):
            doc_selector.asis(form_call.render())
        html_calling.append_html_into_body(doc_selector.getvalue())

        # Register to components container
        self.components[form_element.get_id()] = angular_component_node

    def interpret_detail(self, detail_element, html_calling,
                         typescript_calling):
        # Name of element
        element_name = detail_element.get_name()

        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} Detail".format(name=element_name))

        # HTML, Typescript Class, and Routing Node
        html, typescript_class, _ = self.view_component_definition()
        typescript_class.set_component_selector_class_name(element_name)

        # HTML Call for Detail
        # Preparation to Call Detail
        detail_call = AngularDetailHTMLCall(typescript_class.selector_name)

        list_in_param = []
        for _, parameter in detail_element.get_parameters().items():
            self.interpret_parameter(parameter, typescript_class,
                                     list_in_param)

        # Build All View Element Event Inside
        for _, event in detail_element.get_view_element_events().items():
            self.view_element_events.append(event)

        # Build all View Component Part
        for _, view_component_part in detail_element.get_assoc_view_component_parts().items():
            if isinstance(view_component_part, SimpleField):
                self.interpret_simple_field(view_component_part, html,
                                            typescript_class, list_in_param)
            elif isinstance(view_component_part, DataBinding):
                self.interpret_data_binding(view_component_part, html,
                                            typescript_class, list_in_param)

        # TODO Implement Building all In Direction Parameter
        self.build_in_parameter_for_parent(detail_call, typescript_calling,
                                           list_in_param)

        # Creating the component node
        # The Component Itself
        angular_component_node = AngularComponent(
            component_typescript_class=typescript_class,
            component_html=html)

        # Calling Detail selector
        doc_selector, tag_selector, text_selector = Doc().tagtext()
        with tag_selector('div', id='div-detail-{name}'.format(
                name=typescript_class.selector_name),
                          klass='div-detail view-component'):
            doc_selector.asis(detail_call.render())
        html_calling.append_html_into_body(doc_selector.getvalue())

        # Register to components container
        self.components[detail_element.get_id()] = angular_component_node

    def interpret_list(self, list_element, html_calling, typescript_calling):
        # Name of element
        element_name = list_element.get_name()

        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} List".format(name=element_name))

        # Typescript Class, and Routing Node
        _, typescript_class, _ = self.view_component_definition()
        typescript_class.set_component_selector_class_name(element_name)

        # List HTML Layout
        html = AngularListHTMLLayout()

        # Preparation to Call List selector in parent
        list_call = AngularListHTMLCall(typescript_class.selector_name)

        list_in_param = []
        for _, parameter in list_element.get_parameters().items():
            self.interpret_parameter(parameter, typescript_class,
                                     list_in_param)

        # Build All View Element Event Inside
        for _, event in list_element.get_view_element_events().items():
            self.view_element_events.append(event)

        # Build all View Component Part
        for _, view_component_part in list_element.get_assoc_view_component_parts().items():
            if isinstance(view_component_part, SimpleField):
                self.interpret_simple_field(view_component_part, html,
                                            typescript_class, list_in_param)
            elif isinstance(view_component_part, DataBinding):
                self.interpret_data_binding(view_component_part, html,
                                            typescript_class, list_in_param)

        # TODO Implement Building all In Direction Parameter
        self.build_in_parameter_for_parent(list_call, typescript_calling,
                                           list_in_param)

        # Creating the component node
        # The Component Itself
        angular_component_node = AngularComponent(
            component_typescript_class=typescript_class,
            component_html=html)

        # Calling Detail selector
        doc_selector, tag_selector, text_selector = Doc().tagtext()
        with tag_selector('div', id='div-list-{name}'.format(
                name=typescript_class.selector_name),
                          klass='div-list view-component'):
            doc_selector.asis(list_call.render())
        html_calling.append_html_into_body(doc_selector.getvalue())

        # Register to components container
        self.components[list_element.get_id()] = angular_component_node

    def interpret_view_element_event(self, view_element_event, html_calling,
                                     typescript_calling, parent_symbol):
        # Get the name
        element_name = view_element_event.get_name()

        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} View Element Event".format(
                name=element_name))

        # Defining variable for view element event interpreter
        func_and_html_event_node = AngularButtonWithFunctionHandler(
            element_name)

        # Interpret if this is a special menu button
        if isinstance(parent_symbol, MenuSymbol):
            func_and_html_event_node = AngularMenuButton(element_name)

        # Build all child
        for _, interaction_flow in view_element_event.get_out_interaction_flow().items():
            self.interpret_interaction_flow(interaction_flow,
                                            func_and_html_event_node.function_node)

        # Call it to the parent HTML
        button_html, typescript_function = func_and_html_event_node.render()
        html_calling.append_html_into_body(button_html)

        # Call it to typescript body, and possibly add import node and constructor param to the class
        typescript_calling.body.append(typescript_function)

        for import_node in func_and_html_event_node.function_node.needed_import:
            typescript_calling.add_import_statement_using_import_node(
                import_node)

        for constructor_param in func_and_html_event_node.function_node.needed_constructor_param:
            typescript_calling.set_constructor_param(constructor_param)

    def interpret_onsubmit_event(self, onsubmit_event, html_calling,
                                 typescript_calling):

        # Get the name
        element_name = onsubmit_event.get_name()

        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} OnSubmit Event".format(name=element_name))

        # Interpret, Defining Typescript function and HTML button
        func_and_html_event_node = AngularSubmitButtonType(element_name)

        # Build all child
        for _, interaction_flow in onsubmit_event.get_out_interaction_flow().items():
            self.interpret_interaction_flow(interaction_flow,
                                            func_and_html_event_node.function_node)

        # Call it to the parent by binding it to HTML Form on submit method, add_submit_event
        button_html, typescript_function, ngsubmit = func_and_html_event_node.render()
        html_calling.append_html_into_body(button_html)
        html_calling.add_submit_event(ngsubmit)

        # Call it to typescript body, and possibly add import node and constructor param to the class
        typescript_calling.body.append(typescript_function)

        for import_node in func_and_html_event_node.function_node.needed_import:
            typescript_calling.add_import_statement_using_import_node(
                import_node)

        for constructor_param in func_and_html_event_node.function_node.needed_constructor_param:
            typescript_calling.set_constructor_param(constructor_param)

    def interpret_onselect_event(self, onselect_event, html_calling,
                                 typescript_calling):

        # Get the name
        element_name = onselect_event.get_name()

        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} OnSelect Event".format(name=element_name))

        # Interpret, Defining Typescript function and HTML button
        func_and_html_event_node = AngularOnclickType(element_name)

        # Build all child
        for _, interaction_flow in onselect_event.get_out_interaction_flow().items():
            self.interpret_interaction_flow(interaction_flow,
                                            func_and_html_event_node.function_node)

        # Call it to the parent and onclick html named add_onclick
        onclick_html, typescript_function = func_and_html_event_node.render()
        html_calling.add_onclick(onclick_html)

        # Call it to typescript body, and possibly add import node and constructor param to the class
        typescript_calling.body.append(typescript_function)

        for import_node in func_and_html_event_node.function_node.needed_import:
            typescript_calling.add_import_statement_using_import_node(
                import_node)

        for constructor_param in func_and_html_event_node.function_node.needed_constructor_param:
            typescript_calling.set_constructor_param(constructor_param)

    def interpret_action_event(self, action_id_action_event_tuple):
        # Get the name
        action_id = action_id_action_event_tuple[0]
        action_event_element = action_id_action_event_tuple[1]
        element_name = action_event_element.get_name()

        action_event_container = self.services.get(action_id)

        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} ActionEvent".format(name=element_name))

        # The idea is to create fake button and HTML handler
        action_event_node = ActionEventInterpretation(element_name)

        # Build the interaction flow inside this element
        for _, interaction_flow in action_event_element.get_out_interaction_flow().items():
            self.interpret_interaction_flow(interaction_flow,
                                            action_event_node,
                                            from_action=True)

        # Register to the Action Container
        action_event_container.add_action_event(action_event_node)

    def interpret_data_binding(self, data_binding_element, html_calling,
                               typescript_calling, list_in_param):
        # Get the name
        element_name = data_binding_element.get_name()

        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} DataBinding".format(name=element_name))
        # Get the classifier
        classifier = self.ifml_symbol_table.lookup(
            data_binding_element.get_domain_concept()).classifier_symbol

        # Find it in the models container, and use it for declaring Data Binding Property
        intended_model = self.models.get(classifier.id)

        # Interpreting Data Binding
        data_binding_function = DataBindingFunction(element_name,
                                                    intended_model)

        # Build (If any) Visualization Attribute or Simple Field
        for _, sub_view_component_part in data_binding_element.get_sub_view_component_parts().items():
            if isinstance(sub_view_component_part, VisualizationAttribute):
                self.interpret_visualization_attribute(sub_view_component_part,
                                                       html_calling,
                                                       data_binding_function.property_declaration)
            elif isinstance(sub_view_component_part, SimpleField):
                self.interpret_simple_field(sub_view_component_part,
                                            html_calling, typescript_calling,
                                            list_in_param)
            elif isinstance(sub_view_component_part, ConditionalExpression):
                self.interpret_conditional_expression(sub_view_component_part,
                                                      data_binding_function.func_decl)

        # Add the import statement
        typescript_calling.add_import_statement_using_import_node(
            data_binding_function.import_statement)

        # Add the property from Data Binding
        typescript_calling.set_property_decl(
            data_binding_function.property_declaration)

        # Call the function in the constructor
        typescript_calling.constructor_body.append(
            data_binding_function.get_function_call())

        # Create the function
        typescript_calling.body.append(
            data_binding_function.get_function_declaration())

    def interpret_visualization_attribute(self,
                                          visualization_attribute_element,
                                          html_calling,
                                          data_binding_property):
        # Get the name
        element_name = visualization_attribute_element.get_name()
        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} VisualizationAttribute".format(
                name=element_name))

        # Get the structural feature
        structural_feature = self.ifml_symbol_table.lookup(
            visualization_attribute_element.get_feature_concept()).struct_feature_symbol

        # Interpret the notation
        visualization_span = VisualizationWithSpan(element_name,
                                                   structural_feature.name,
                                                   data_binding_property.variable_name)

        # Append to the HTML
        html_calling.append_html_into_body(visualization_span.render())

    def interpret_simple_field(self, simple_field_element, html_calling,
                               typescript_calling, list_in_param):

        # Get the name and type
        element_name = simple_field_element.get_name()
        uml_model_name, id_of_type = simple_field_element.get_type().split('#')
        direction = simple_field_element.get_direction()

        # Find the type in the UML Symbol Table
        datatype_of_field = self.uml_symbol_table.lookup(uml_model_name,
                                                         id_of_type).name

        # Interpreting the parameter, because part of Simple Field is Parameter
        self.interpret_parameter(simple_field_element, typescript_calling,
                                 list_in_param)

        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} SimpleField".format(name=element_name))

        # Create the Input Field
        input_html = InputField(element_name, datatype_of_field)

        # Call Into the HTML, because the property already declared by interpreting the parameter
        # The two way data binding angular ready to be implemented
        html_calling.append_html_into_body(input_html.render())

    def interpret_conditional_expression(self, conditional_expression_element,
                                         data_binding_function_declaration):

        # Get body from the element
        body = conditional_expression_element.get_body()

        # Append Conditional Expression body into statement inside Data Binding Function
        data_binding_function_declaration.add_statement_to_body(body)

    def interpret_slot(self, view_element_event, html_calling,
                       typescript_calling):
        pass

    def interpret_parameter(self, parameter_element, typescript_calling,
                            list_in_direction_parameter):

        # Get element name, and parameter direction
        element_name = parameter_element.get_name()
        direction = parameter_element.get_direction()

        if direction == 'in':
            self.interpret_in_parameter(parameter_element, typescript_calling,
                                        list_in_direction_parameter)
        elif direction == 'out':
            self.interpret_out_parameter(parameter_element, typescript_calling)
        elif direction == 'inout':
            self.interpret_in_parameter(parameter_element, typescript_calling,
                                        list_in_direction_parameter)
        else:
            raise TypeError(
                'No Parameter will have {direction} direction, Please verify the validity of your IFML'.format(
                    direction=direction))

    def interpret_in_parameter(self, in_parameter_element, typescript_calling,
                               list_in_direction_parameter):

        # Get element name and type
        element_name = in_parameter_element.get_name()
        uml_name, id_of_symbol = in_parameter_element.get_type().split('#')
        type_used_by_parameter = self.uml_symbol_table.lookup(uml_name,
                                                              id_of_symbol)

        # If type is class then take the model frommodel container, else just take the string name
        if isinstance(type_used_by_parameter, ClassSymbol):
            type_used_by_parameter = self.models[type_used_by_parameter.id]

        # Creating @Input Property Declaration in child
        input_node = InParameter(element_name, type_used_by_parameter)

        # Declare it in the child typescript, and if the type is class, import the class
        typescript_calling.set_property_decl(input_node.child_property)

        if input_node.needed_import:
            typescript_calling.add_import_statement_using_import_node(
                input_node.needed_import)

        # Adding Input decorator import statement
        typescript_calling.add_import_statement_using_import_node(
            input_node.input_import_statement)

        # Add it into InDirectionInput List at Child Component
        list_in_direction_parameter.append(input_node)

    def interpret_out_parameter(self, out_parameter_calling,
                                child_typescript_calling):
        # Get element name and type
        element_name = out_parameter_calling.get_name()
        uml_name, id_of_symbol = out_parameter_calling.get_type().split('#')
        type_used_by_parameter = self.uml_symbol_table.lookup(uml_name,
                                                              id_of_symbol)

        # If type is class then take the model frommodel container, else just take the string name
        if isinstance(type_used_by_parameter, ClassSymbol):
            type_used_by_parameter = self.models[type_used_by_parameter.id]

        # Creating Output Parameter in child
        output_node = OutParameter(element_name, type_used_by_parameter)

        # Declare it in the child typescript, and if the type is class, import the class
        child_typescript_calling.set_property_decl(output_node.property)

        if output_node.needed_import:
            child_typescript_calling.add_import_statement_using_import_node(
                output_node.needed_import)

    def view_container_definition(self):
        """
        Prepare a component requirements such the react component, JSX,
        and routing from this page.

        :return: ReactComponentJSX, EseightClassType, Route
        """

        # Defining variable for routing node, initialized if this container
        # have inInteractionFlow OR isLandmark
        routing_node = None

        # Prepare React Component Class
        react_class = ReactComponentEseightClass()

        # Prepare JSX
        html = ReactJSX()

        return html, react_class, routing_node

    def view_component_definition(self):

        html, _, routing_node = self.view_container_definition()
        typescript_class = AngularComponentWithInputTypescriptClass()
        return html, typescript_class, routing_node

    def check_if_there_is_an_interaction_flow(self, element):
        """
        Inpect if there is any interaction flow contained in the element.

        :param element: the IFML element
        :return:
        """
        exist = False

        # Check length of array
        in_flow: [str] = element.get_in_interaction_flow()
        length = len(in_flow)
        first_element: str = in_flow[0]

        # If array is not empty and first element is not an empty string
        if length > 0 and len(first_element) > 0:
            exist = True

        return exist

    def build_in_parameter_for_parent(self, call_html, parent_typescript,
                                      list_param):

        # This logic is only good for parameter inside form and detail
        # Improve this logic for list
        constructor_body_statement = GettingQueryParam()
        for param in list_param:

            # Adding the parameter to HTML Call
            call_html.add_parameter_and_property_pair(param.child_property,
                                                      param.parent_property)

            # Adding needed property for parent component
            parent_typescript.set_property_decl(param.parent_property)

            # Check if the declaration of property need to import a model class, else no import needed
            if param.needed_import:
                query_param_name, property_name, class_type = param.parent_property.variable_name, param.parent_property.variable_name, param.parent_property.variable_datatype
                parent_typescript.add_import_statement_using_import_node(
                    param.needed_import)
                constructor_body_statement.add_statement_for_saving_query_param_value_into_property_typed_class(
                    query_param_name, property_name, class_type)
            else:
                query_param_name, property_name = param.parent_property.variable_name, param.parent_property.variable_name
                constructor_body_statement.add_statement_for_saving_query_param_value_into_property(
                    query_param_name, property_name)

        parent_typescript.constructor_body.append(
            constructor_body_statement.render())

    def interpret_all_action_events(self):
        for action_id_action_event_tuple in self.action_events:
            self.interpret_action_event(action_id_action_event_tuple)

    def interpret_all_view_element_events(self):
        for view_element_event in self.view_element_events:
            view_element_parent_symbol = self.ifml_symbol_table.lookup(
                view_element_event.get_parent_view_element_reference())
            component_node = self.components[view_element_parent_symbol.id]
            if isinstance(view_element_event, OnSelectEvent):
                self.interpret_onselect_event(view_element_event,
                                              component_node.component_html,
                                              component_node.component_typescript_class)
            elif isinstance(view_element_event, OnSubmitEvent):
                self.interpret_onsubmit_event(view_element_event,
                                              component_node.component_html,
                                              component_node.component_typescript_class)
            elif isinstance(view_element_event, ViewElementEvent):
                self.interpret_view_element_event(view_element_event,
                                                  component_node.component_html,
                                                  component_node.component_typescript_class,
                                                  view_element_parent_symbol)

    def interpret_interaction_flow(self, interaction_flow_element,
                                   function_node, from_action=False):

        param_binding_group = interaction_flow_element.get_parameter_binding_groups()

        if isinstance(interaction_flow_element, NavigationFlow):
            self.interpret_navigation_flow(interaction_flow_element,
                                           function_node, param_binding_group,
                                           from_action)
        elif isinstance(interaction_flow_element, DataFlow):
            self.interpret_data_flow(interaction_flow_element, function_node,
                                     param_binding_group, from_action)

    def interpret_navigation_flow(self, navigation_flow_element, function_node,
                                  param_binding_group, from_action=False):

        # Get element target
        element_target = navigation_flow_element.get_target_interaction_flow_element()
        target_symbol = self.ifml_symbol_table.lookup(element_target)

        if isinstance(target_symbol, ViewContainerSymbol) or isinstance(
                target_symbol, WindowSymbol):
            self.interaction_with_container_as_target(
                self.components.get(target_symbol.id), function_node,
                param_binding_group, from_action)
        elif isinstance(target_symbol, ActionSymbol):
            self.interaction_with_action_as_target(
                self.services.get(target_symbol.id), function_node,
                param_binding_group)

    def interaction_with_container_as_target(self, container_node,
                                             function_node,
                                             param_binding_group, from_action):

        if isinstance(container_node, AngularComponentForModal):
            self.route_to_component_modal(container_node, function_node,
                                          param_binding_group, from_action)
        elif isinstance(container_node, AngularComponent):
            self.route_to_component_page(container_node, function_node,
                                         param_binding_group, from_action)

    def route_to_component_page(self, component_page_node, function_node,
                                param_binding_group, from_action):

        # Get routing path of that page
        route_path_from_root = component_page_node.get_routing_path()

        # Creating statement for navigation into page
        router_statement = RouteToComponentPage(route_path_from_root)

        # Build the param binding group
        if param_binding_group:
            param_binding_group_node = self.interpret_param_binding(
                param_binding_group, from_action, is_query_param=True)
            router_statement.add_param_binding_group(
                param_binding_group_node.render())

        # Append to the event function handler
        function_node.add_statement_to_body(router_statement.render())

    def route_to_component_modal(self, component_modal_node, function_node,
                                 param_binding_group, from_action):
        # Get modal identifier for that page
        modal_identifier = component_modal_node.modal_identifier

        # Add Open Modal Statement and import ngxmodal service
        modal_handler_template = AngularModalButtonAndFunction(
            modal_identifier)
        modal_handler_template.set_target_modal(modal_identifier)

        # Build the param binding group
        if param_binding_group:
            param_binding_group_node = self.interpret_param_binding(
                param_binding_group, from_action)

        # Append to the event function handler. add import and constructor param
        function_node.add_needed_import(
            modal_handler_template.import_ngx_modal_service_node)
        function_node.add_needed_constructor_param(
            modal_handler_template.ngx_service_constructor)
        function_node.add_statements_to_body(
            modal_handler_template.function_node.function_body)

    def interaction_with_action_as_target(self, service_node, function_node,
                                          param_binding_group):
        # Get the service name, and filename
        service_class_name = service_node.class_name
        service_filename = service_node.filename

        # Improve this logic to handle multiple action event
        service_action_event = service_node.action_event

        # Creating statement for navigation into service
        service_call_statement = RouteToAction(service_class_name,
                                               service_filename)

        # Build the param binding group
        if param_binding_group:
            param_binding_group_node = self.interpret_param_binding(
                param_binding_group)
            service_call_statement.add_param_binding_group(
                param_binding_group_node.render())

        # Build the after effect of calling service, if None, then there are no after effect
        try:
            service_call_statement.after_statement = service_action_event.function_body
        except AttributeError:
            pass

        # Append to the event function handler. add import and constructor param
        function_node.add_needed_import(
            service_call_statement.import_statement)
        function_node.add_needed_constructor_param(
            service_call_statement.constructor_param)
        function_node.add_statement_to_body(service_call_statement.render())

    def interpret_data_flow(self, data_flow_element, function_node,
                            param_binding_group, from_action):

        # Get element target
        element_target = data_flow_element.get_target_interaction_flow_element()
        pass

    def interpret_param_binding(self, param_binding_group, from_action=False,
                                is_query_param=False):

        # Create ParamGroup Node
        param_group = ParamGroup()

        # Build all Parameter Binding inside Parameter Binding Group
        for _, param_binding in param_binding_group.get_parameter_bindings().items():
            source_param_symbol = self.ifml_symbol_table.lookup(
                param_binding.get_source_parameter())
            target_param_symbol = self.ifml_symbol_table.lookup(
                param_binding.get_target_parameter())

            param_binding_statement = ParameterBindingInterpretation(
                source_param_symbol.name, target_param_symbol.name,
                from_action, is_query_param)
            param_group.add_param_statement(param_binding_statement)

        # Let the Interaction Flow Render the node
        return param_group

    def interpret_owned_attribute(self, class_attribute_xmi,
                                  model_element: ModelFromUMLClass):
        # Get attribute name, and type of the attribute
        element_name = class_attribute_xmi.get_model_name()
        id_of_type_symbol = class_attribute_xmi.get_type()

        uml_filename = self.root_class_diagram_xmi.get_filename()
        element_type = self.uml_symbol_table.lookup(uml_filename,
                                                    id_of_type_symbol).name
        # Interpret it
        model_element.add_owned_attribute_to_class(element_name, element_type)

    #
    def interpret_owned_operation(self, class_operation_xmi, model_element):
        # Get attribute name, and type of the attribute
        element_name = class_operation_xmi.get_model_name()

        # Create Owned Operation Node
        operation_node = OwnedOperation(element_name)

        for _, owned_param in class_operation_xmi.get_parameters().items():
            self.interpret_owned_param(owned_param, operation_node)

        model_element.add_owned_operation_to_class(operation_node)

    def interpret_owned_param(self, operation_param_xmi, operation_element):
        # Get attribute name, and type of the attribute
        element_name = operation_param_xmi.get_model_name()
        id_of_type_symbol = operation_param_xmi.get_type()
        uml_filename = self.root_class_diagram_xmi.get_filename()
        element_type = self.uml_symbol_table.lookup(uml_filename,
                                                    id_of_type_symbol)

        is_class = isinstance(element_type, ClassSymbol)
        operation_element.add_owned_param(element_name, element_type.name,
                                          is_class=is_class)

    def show_login_button_in_root(self):
        # If there are any navigation inside, then create a login page in the routing, else, call the button
        if len(self.root_routing.children_routes) > 0:

            # Create dummy AngularComponent
            html, typescript_class = LoginHTML(), LoginTypescriptClass()
            angular_component_node = AngularComponent(typescript_class, html)
            routing_node = RouteToModule(typescript_class)
            self.root_routing.add_children_routing(routing_node)
            self.components['login'] = angular_component_node
        else:
            doc_google_sign_in_button, tag_google_sign_in_button, text_google_sign_in_button = Doc().tagtext()
            with tag_google_sign_in_button('login'):
                text_google_sign_in_button('Google Sign In')
            self.root_template.append_html_into_body(
                doc_google_sign_in_button.getvalue())
