import re

from yattag import Doc

from custom_xmi_parser.umlsymboltable import ClassSymbol, UMLSymbolTable
from custom_xmi_parser.xmiparser_2 import XMIClass, XMIModel
from ifml_parser.ifml_element.interaction_flow.base import NavigationFlow
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
    ViewContainer, Menu
from ifml_parser.ifmlsymboltable import ViewContainerSymbol, WindowSymbol, \
    ActionSymbol, MenuSymbol, IFMLSymbolTable
from ifml_parser.ifmlxmiparser import IFMLModel
from main.utils.ast.framework.react.base import REACT_ROUTER_DOM_MODULE, \
    REACT_COOKIES_MODULE
from main.utils.ast.framework.react.buttons import SubmitButtonType, \
    ButtonWithFunctionHandler, MenuButton, OnclickType
from main.utils.ast.framework.react.component_parts import InputField, \
    DataBindingFunction, VisualizationWithSpan
from main.utils.ast.framework.react.components import \
    ListJSXLayout, ListJSXCall, DetailJSXCall, DetailJSXLayout, RootJSX
from main.utils.ast.framework.react.components import \
    ReactComponentEseightClass, ReactJSX, ReactComponent, MenuJSX, FormJSX, \
    ReactComponentWithInputEseightClass, FormComponentJSXCall
from main.utils.ast.framework.react.google_sign_in import LoginClass
from main.utils.ast.framework.react.models import ModelFromUMLClass, \
    OwnedOperation
from main.utils.ast.framework.react.parameters import InParameter, \
    ParamGroup, \
    ParameterBindingInterpretation
from main.utils.ast.framework.react.routers import RouteToModule, \
    RedirectToAnotherPath, RootRoutingNode, \
    RouteToComponentPage, RouteToAction, GettingQueryParam
from main.utils.ast.framework.react.services import ReactAPICall, \
    ActionEventInterpretation
from main.utils.ast.language.eseight import ImportStatementType, \
    InstanceVarDeclType
from main.utils.logger_generator import get_logger
from main.utils.naming_management import dasherize, camel_function_style
from . import BaseInterpreter

logger = get_logger()


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

        # NOTE: react doesn't have explicit external jsx file or structure.
        # But there's a tool called Babel which transformed the JSX (jsx-like)
        # structure into JS instruction then construct the VDOM based on.
        self.root_template = self.get_root_template()

        # initial root class for the current project.
        self.root_eseight_class = self.get_root_class()

        self.root_react_node = ReactComponent(self.root_eseight_class,
                                              self.root_template)

        logger.info(
            "Interpreting {name} IFML Project".format(name=self.project_name))

        # Get all the IFML element/node/notation model IFML
        self.ifml_expressing_ui_design = \
            self.root_ifml \
                .get_interaction_flow_model() \
                .get_interaction_flow_model_elements()

        # interpret domain model means the app will process all the class
        # within UML.

        # react treat data as literal JSON. there is no need to
        # create a specific class and serialized it on.
        self.interpret_domain_model()

        # Interpret all Interaction Flow Model Elements
        self.interpret_interaction_flow_model()

        # Interpret all Action Event Elements with it's corresponding navigation
        self.interpret_all_action_events()

        # Interpret all View Element Elements with it's corresponding navigation
        self.interpret_all_view_element_events()

        # Deciding How to show Login Button
        self.show_login_button_in_root()

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

        logger.info("UML name: {element}".format(element=element_name))

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

    def router_outlet_jsx(self, name):
        doc_outlet, tag_outlet, text_outlet = Doc().tagtext()
        with tag_outlet('div', id=name, klass='div-content-router'):
            with tag_outlet('router-outlet'):
                text_outlet('')
        return doc_outlet.getvalue()

    def get_root_class(self):
        """
        Create a root class where will be the gateway of the apps.

        :return: an react component class without JSX.
        """
        root_react_class = ReactComponentEseightClass()
        root_react_class.class_name = 'App'
        root_react_class.component_name = 'App'

        react_router_dom_import = ImportStatementType()
        react_router_dom_import.set_main_module(REACT_ROUTER_DOM_MODULE)
        react_router_dom_import.add_imported_elements([
            'BrowserRouter',
            'Route'
        ])

        root_react_class.add_import_statement_for_multiple_element(
            '../Authentication',
            ['AuthProvider']
        )

        react_cookie_import = ImportStatementType()
        react_cookie_import.set_main_module(REACT_COOKIES_MODULE)
        react_cookie_import.add_imported_element('CookiesProvider')

        root_react_class.add_import_statement_using_import_node(
            react_router_dom_import)
        root_react_class.add_import_statement_using_import_node(
            react_cookie_import)

        return root_react_class

    def get_root_template(self):
        """
        create a root jsx.

        :return: jsx representation
        """

        root_template_node = RootJSX(self.enable_authentication_guard)
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
                self.interpret_action(interaction_flow_model_element)
            # If the root have menu
            elif isinstance(interaction_flow_model_element, Menu):
                self.interpret_menu(interaction_flow_model_element,
                                    self.root_template,
                                    self.root_eseight_class,
                                    auth_guard=True)
            elif isinstance(interaction_flow_model_element, ViewContainer):
                self.interpret_view_container(interaction_flow_model_element,
                                              self.root_template,
                                              self.root_eseight_class,
                                              self.root_routing)

    def interpret_menu(self, menu_element: Menu,
                       jsx_calling: ReactJSX,
                       component_calling: ReactComponentEseightClass,
                       auth_guard: bool = False):
        """
        Create new ReactComponent for menu element.

        :param menu_element: a menu representative
        :param jsx_calling: the jsx block where the menu mounted on
        :return: None
        """

        # Name of element
        element_name = menu_element.get_name()

        logger.info(
            "Interpreting a {name} Menu".format(name=element_name))

        # Prepare Component Class
        component_class = ReactComponentEseightClass()
        component_class.set_component_selector_class_name(element_name)

        # Set import for Link element from React Router DOM
        if auth_guard:
            react_router_dom = ImportStatementType()
            react_router_dom.set_main_module('react-router-dom')
            react_router_dom.add_imported_element('Link')

            # add to Component Class imported module list
            component_class.add_import_statement_using_import_node(
                react_router_dom)

        # add logout method

        logout_event_clicked = InstanceVarDeclType("onLogoutClicked")
        logout_event_clicked.value = \
            "e => { e.preventDefault(); this.props.logout(); }"

        component_class.set_property_decl(logout_event_clicked)

        # Prepare jsx
        jsx = MenuJSX(component_class.selector_name,
                      auth_guard)

        # Build All View Element Event Inside
        for _, event in menu_element.get_view_element_events().items():
            self.view_element_events.append(event)

        # The Component Itself
        component_node = ReactComponent(
            component_class=component_class,
            component_markup_language=jsx)

        # Calling Menu selector
        compose_menu_component = f'''\
        const Component = withRouter({component_class.component_name + 'Component'});
        return <Component {{...values}} />
        '''

        # Menu always appended into first element
        jsx_calling.append_jsx_into_body(
            "<AuthConsumer>{{ (values) => {{ {} }} }}</AuthConsumer>".format(
                compose_menu_component
            )
        )

        component_calling.add_import_statement(
            '../Authentication',
            'AuthConsumer'
        )
        component_calling.add_import_statement(
            'react-router-dom',
            'withRouter'
        )

        # add component to parent
        self.add_import_component_to_parent(component_calling, component_node)

        # Register to components container
        self.components[menu_element.get_id()] = component_node

    def interpret_view_container(self, view_container: ViewContainer,
                                 jsx_parent: ReactJSX,
                                 class_parent, routing_parent):
        """
        Handle View Container interpretation.

        :param view_container: given IFML element
        :param jsx_parent: the parent jsx of the view container
        :param class_parent: the parent component of the view container
        :param routing_parent: the parent route of the view container
        :return: None
        """
        # Name of element that will be a component name
        element_name = view_container.get_name()

        logger.info(
            "Interpreting a {name} View Container".format(name=element_name))

        # prepare the initial component requirements
        jsx, container_class, routing_node = self.view_container_definition()

        # React treats a component class as a directive selector which means
        # there is no need to re-state the directive name.
        # note: directive is just like an importing component in React.
        container_class.set_component_selector_class_name(element_name)

        # Decide if this container is callable or using router
        if view_container.get_is_xor():
            # means this ViewContainer is a layout placeholder
            routing_node = RouteToModule(
                container_class,
                enable_guard=self.enable_authentication_guard)
            routing_node.enable_children_routing()

        if self.check_if_there_is_an_interaction_flow(
                view_container) and routing_node is None:
            # Enable the parent child routing
            routing_node = RouteToModule(
                container_class,
                enable_guard=
                self.enable_authentication_guard
            ) if routing_node is None else routing_node

        if routing_node:
            routing_node.path_from_root = \
                routing_parent.path_from_root + '/' + routing_node.path

        # Build All View Element Event Inside
        for _, event in view_container.get_view_element_events().items():
            if isinstance(event, ViewElementEvent):
                self.view_element_events.append(event)

        for _, parameter in view_container.get_parameters().items():
            self.interpret_parameter(parameter, [])

        # Build All Action inside the Container
        for _, action in view_container.get_action().items():
            self.interpret_action(action)

        # Build All Associated View Element
        for _, view_element in view_container.get_assoc_view_element().items():
            if isinstance(view_element, List):
                self.interpret_list(view_element, jsx, container_class)
            elif isinstance(view_element, Details):
                self.interpret_detail(view_element, jsx, container_class)
            elif isinstance(view_element, Form):
                self.interpret_form(view_element, jsx, container_class)
            elif isinstance(view_element, Menu):
                self.interpret_menu(view_element, jsx, container_class)
            elif isinstance(view_element, ViewContainer):
                self.interpret_view_container(view_element, jsx,
                                              container_class, routing_node)

        # The Component Itself
        component_node = ReactComponent(
            component_class=container_class,
            component_markup_language=jsx)

        # Add Routing Node
        routing_parent.enable_children_routing()

        # Decide if this container is default in its XOR
        # import Redirect and append to body first before any Route
        if view_container.get_is_default():
            class_parent.add_import_statement('react-router-dom',
                                              'Redirect')
            redirect_node = RedirectToAnotherPath(
                routing_parent.path_from_root,
                routing_node.path_from_root)
            routing_parent.add_children_routing(redirect_node)
            if isinstance(jsx_parent, RootJSX):
                redirect_node.carry_param = False
            jsx_parent.append_route(redirect_node.render())

        self.add_import_component_to_parent(class_parent,
                                            component_node)

        # append this VC to parent jsx and import Route to parent
        routing_parent.add_children_routing(routing_node)
        jsx_parent.append_route(routing_node.render())
        class_parent.add_import_statement_for_multiple_element(
            'react-router-dom',
            ['Route', 'Switch'])

        # import withAuth HOC if login enabled
        if self.enable_authentication_guard:
            class_parent.add_import_statement(
                '../Authentication',
                'withAuth')

        component_node.set_routing_node(
            routing_node.path_from_root)

        # Register to components container
        self.components[view_container.get_id()] = component_node

    def interpret_action(self, action_element):
        """
        Interpret the given action. Mostly handle API call.

        :param action_element: IFML notation
        :return: None
        """

        # Name of element, the name in a form of API endpoint.
        # e.g. api/myentity/myaction.abs
        element_name = action_element.get_name()

        logger.info(
            "Interpreting a {name} Action".format(name=element_name))

        # Calling ActionEvent and build it
        for _, action_event in action_element.get_action_event().items():
            self.action_events.append((action_element.get_id(), action_event))

        # Defining service class, and add the name into it
        service_class = ReactAPICall(
            enable_auth=self.enable_authentication_guard)
        service_class.set_endpoint_class_name_and_worker(element_name)

        any_in_param = False

        # Check if there are any in parameter being defined
        all_param_inside_action = dict.copy(action_element.get_parameters())
        while len(all_param_inside_action) and not any_in_param:
            arbitary_param_inside_action = all_param_inside_action.popitem()[1]
            any_in_param = arbitary_param_inside_action.get_direction() == 'in'

        if any_in_param:
            service_class.param_exist()

        # Register to services container
        self.services[action_element.get_id()] = service_class

    def interpret_form(self, form_element, jsx_parent, class_parent):
        """
        Create a whole structure of form. Handle event later.

        :param form_element: IFML Notation
        :param jsx_parent: parent's JSX
        :param class_parent: parent's class
        :return: None
        """
        # Name of element
        element_name = form_element.get_name()

        logger.info(
            "Interpreting a {name} Form".format(name=element_name))

        # Only need the routing node and class
        _, component_class, _ = self.view_component_definition()
        component_class.set_component_selector_class_name(element_name)

        # The JSX for Form
        jsx = FormJSX(element_name)

        # Preparing JSX Call template for form
        form_call = FormComponentJSXCall(component_class.component_name)

        list_in_param = []
        for _, parameter in form_element.get_parameters().items():
            self.interpret_parameter(parameter, list_in_param)

        # Build All View Element Event Inside
        for _, event in form_element.get_view_element_events().items():
            self.view_element_events.append(event)

        # Build all View Component Part
        for _, view_component_part in \
                form_element.get_assoc_view_component_parts().items():
            if isinstance(view_component_part, SimpleField):
                self.interpret_simple_field(view_component_part, jsx,
                                            list_in_param)
            elif isinstance(view_component_part, DataBinding):
                self.interpret_data_binding(view_component_part, jsx,
                                            component_class, list_in_param)

        if len(list_in_param) > 0:
            self.build_in_parameter_for_parent(
                form_call,
                class_parent,
                list_in_param
            )

        # Creating the component node
        # The Component Itself
        component_module = ReactComponent(component_class, jsx)

        jsx_parent.append_jsx_into_body(form_call.render())

        self.add_import_component_to_parent(class_parent,
                                            component_module)

        # Register to components container
        self.components[form_element.get_id()] = component_module

    def interpret_detail(self, detail_element, jsx_parent,
                         class_parent):
        # Name of element
        element_name = detail_element.get_name()

        logger.info(
            "Interpreting a {name} Detail".format(name=element_name))

        # JSX, Class, and Routing Node
        _, component_class, _ = self.view_component_definition()
        component_class.set_component_selector_class_name(element_name)

        # JSX Layout for Detail
        jsx = DetailJSXLayout()

        # JSX Call for Detail
        # Preparation to Call Detail
        detail_call = DetailJSXCall(component_class.component_name)

        list_in_param = []
        for _, parameter in detail_element.get_parameters().items():
            self.interpret_parameter(parameter, list_in_param)

        # Build All View Element Event Inside
        for _, event in detail_element.get_view_element_events().items():
            self.view_element_events.append(event)

        # Build all View Component Part
        for _, view_component_part in detail_element.get_assoc_view_component_parts().items():
            if isinstance(view_component_part, SimpleField):
                self.interpret_simple_field(view_component_part, jsx,
                                            list_in_param)
            elif isinstance(view_component_part, DataBinding):
                self.interpret_data_binding(view_component_part, jsx,
                                            component_class, list_in_param)

        if len(list_in_param) > 0:
            self.build_in_parameter_for_parent(detail_call, class_parent,
                                               list_in_param)

        # Creating the component node
        # The Component Itself
        component_node = ReactComponent(
            component_class,
            jsx)

        # Calling Detail selector
        jsx_parent.append_jsx_into_body(detail_call.render())

        self.add_import_component_to_parent(class_parent, component_node)

        # Register to components container
        self.components[detail_element.get_id()] = component_node

    def interpret_list(self, list_element, jsx_parent, class_parent):
        """
        Interpret a list inside View Container.

        :param list_element: IFML node
        :param jsx_parent:  its jsx parent calling this component
        :param class_parent: its class parent calling this component
        :return: None
        """

        # Name of element
        element_name = list_element.get_name()

        logger.info(
            "Interpreting a {name} List".format(name=element_name))

        # component Class, and Routing Node
        _, component_class, _ = self.view_component_definition()
        component_class.set_component_selector_class_name(element_name)

        # List JSX Layout
        jsx = ListJSXLayout()

        # Preparation to JSX Call List in parent
        list_call = ListJSXCall(component_class.component_name)

        list_in_param = []
        for _, parameter in list_element.get_parameters().items():
            self.interpret_parameter(parameter, list_in_param)

        # Build All View Element Event Inside
        for _, event in list_element.get_view_element_events().items():
            self.view_element_events.append(event)

        # Build all View Component Part
        for _, view_component_part in \
                list_element.get_assoc_view_component_parts().items():
            if isinstance(view_component_part, SimpleField):
                self.interpret_simple_field(view_component_part, jsx,
                                            list_in_param)
            elif isinstance(view_component_part, DataBinding):
                self.interpret_data_binding(view_component_part, jsx,
                                            component_class, list_in_param)

        # TODO Implement Building all In Direction Parameter
        if len(list_in_param) > 0:
            self.build_in_parameter_for_parent(list_call, class_parent,
                                               list_in_param)

        # Creating the component node
        # The Component Itself
        component_node = ReactComponent(
            component_class,
            jsx)

        # Insert into parent JSX
        jsx_parent.append_jsx_into_body(list_call.render())

        self.add_import_component_to_parent(class_parent, component_node)

        # Register to components container
        self.components[list_element.get_id()] = component_node

    def add_import_component_to_parent(self, parent_class, component):
        form_import_statement = ImportStatementType()
        form_import_statement.set_default_element(
            component.component_class.component_name + 'Component'
        )
        form_import_statement.set_main_module(
            '../{}/{}'.format(
                component.component_class.component_name,
                component.get_component_filename()
            )
        )
        parent_class.add_import_statement_using_import_node(
            form_import_statement)

    def interpret_view_element_event(
            self,
            view_element_event,
            jsx_parent,
            class_parent: ReactComponentEseightClass,
            parent_symbol):
        # Get the name
        element_name = view_element_event.get_name()

        logger.info(
            "Interpreting a {name} View Element Event".format(
                name=element_name))

        # Defining variable for view element event interpreter
        # Interpret if this is a special menu button
        if isinstance(parent_symbol, MenuSymbol):
            func_and_jsx_event_node = MenuButton(element_name)
        else:
            func_and_jsx_event_node = ButtonWithFunctionHandler(
                element_name)

        # Build all child
        for _, interaction_flow in \
                view_element_event.get_out_interaction_flow().items():
            self.interpret_interaction_flow(
                interaction_flow,
                func_and_jsx_event_node.function_node)

        # Call it to the parent jsx
        button_jsx, component_function = func_and_jsx_event_node.render()
        jsx_parent.append_jsx_into_body(button_jsx)

        # Call it to parent class body, and possibly add import node and
        # constructor param to the class
        class_parent.set_property_decl(
            func_and_jsx_event_node.function_holder
        )

        # import needed Service/Action
        for import_node in func_and_jsx_event_node.function_node.needed_import:
            class_parent.add_import_statement_using_import_node(
                import_node)

    def interpret_onsubmit_event(self, onsubmit_event, jsx_calling,
                                 component_calling: ReactComponentEseightClass):
        """
        Once the form had been interpreted, there are left works to do. One
        of those may be interpreting Save/Submit button. This method will
        interpret that element and append it into the corresponding
        component class and jsx.

        :param onsubmit_event: the IFML submit element
        :param jsx_calling: the jsx where submit element JSX will be inserted into
        :param component_calling: the component class where submit event handler function will be inserted into
        :return: None
        """
        # Get the name
        element_name = onsubmit_event.get_name()

        logger.info(
            "Interpreting a {name} OnSubmit Event".format(name=element_name))

        # Interpret, Defining component function and jsx button
        func_and_jsx_event_node = SubmitButtonType(element_name)

        # Build all child
        for _, interaction_flow in onsubmit_event.get_out_interaction_flow().items():
            self.interpret_interaction_flow(interaction_flow,
                                            func_and_jsx_event_node.function_node)

        # Call it to the parent by binding it to jsx Form on submit method, add_submit_event
        button_jsx, component_function = func_and_jsx_event_node.render()
        jsx_calling.append_jsx_into_body(button_jsx)

        # Call it to component body, and possibly add import node and constructor param to the class
        # component_calling.body.append(component_function)
        # add handler function into component class body
        component_calling.set_property_decl(
            func_and_jsx_event_node.function_holder)

        for import_node in func_and_jsx_event_node.function_node.needed_import:
            component_calling.add_import_statement_using_import_node(
                import_node)

    def interpret_onselect_event(self, onselect_event, jsx_calling,
                                 component_calling):

        # Get the name
        element_name = onselect_event.get_name()

        logger.info(
            "Interpreting a {name} OnSelect Event".format(name=element_name))

        # Interpret, Defining component function and jsx button
        func_and_jsx_event_node = OnclickType(element_name)

        # Build all child
        for _, interaction_flow in onselect_event.get_out_interaction_flow().items():
            self.interpret_interaction_flow(interaction_flow,
                                            func_and_jsx_event_node.function_node)

        # Call it to the parent and onclick jsx named add_onclick
        onclick_jsx, component_function = func_and_jsx_event_node.render()
        jsx_calling.add_onclick(onclick_jsx)

        # Call it to component body, and possibly add import node and constructor param to the class
        component_calling.set_property_decl(
            func_and_jsx_event_node.function_holder)

        for import_node in func_and_jsx_event_node.function_node.needed_import:
            component_calling.add_import_statement_using_import_node(
                import_node)

    def interpret_action_event(self, action_id_action_event_tuple):
        # Get the name
        action_id = action_id_action_event_tuple[0]
        action_event_element = action_id_action_event_tuple[1]
        element_name = action_event_element.get_name()

        action_event_container = self.services.get(action_id)

        logger.info(
            "Interpreting a {name} ActionEvent".format(name=element_name))

        # The idea is to create fake button and jsx handler
        action_event_node = ActionEventInterpretation(element_name)

        # Build the interaction flow inside this element
        for _, interaction_flow in action_event_element.get_out_interaction_flow().items():
            self.interpret_interaction_flow(interaction_flow,
                                            action_event_node,
                                            from_action=True)

        # Register to the Action Container
        action_event_container.add_action_event(action_event_node)

    def interpret_data_binding(self, data_binding_element, jsx_parent,
                               class_parent, list_in_param):
        """
        Interpret the representation of content source comes from domain model.

        :param data_binding_element: IFML notation
        :param jsx_parent: parent's JSX
        :param class_parent: parent's class
        :param list_in_param: In parameter array container
        :return: None
        """
        # Get the name
        element_name = data_binding_element.get_name()

        logger.info(
            "Interpreting a {name} DataBinding".format(name=element_name))

        # Interpreting Data Binding
        data_binding_function = DataBindingFunction(element_name)

        # Build (If any) Visualization Attribute or Simple Field
        for _, sub_view_component_part in \
                data_binding_element.get_sub_view_component_parts().items():
            if isinstance(sub_view_component_part, VisualizationAttribute):
                self.interpret_visualization_attribute(
                    sub_view_component_part,
                    jsx_parent,
                    data_binding_function.property_declaration)
            elif isinstance(sub_view_component_part, SimpleField):
                self.interpret_simple_field(
                    sub_view_component_part,
                    jsx_parent,
                    list_in_param,
                    default_value_source=
                    data_binding_function.property_declaration
                )
            elif isinstance(sub_view_component_part, ConditionalExpression):
                self.interpret_conditional_expression(
                    sub_view_component_part,
                    data_binding_function,
                    class_parent)

        # IN params value assignment
        if len(list_in_param) > 0:
            param = list_in_param[0]
            if isinstance(param, InParameter):
                data_binding_function.property_declaration.value = \
                    'this.props.{}'.format(param.var_camel_name)

    def interpret_visualization_attribute(self,
                                          visualization_attribute_element,
                                          jsx_parent,
                                          data_binding_property):
        """
        Interpret an attribute will be shown to user.

        :param visualization_attribute_element: IFML notation
        :param jsx_parent: parent's JSX
        :param data_binding_property: data binding property object
        :return:
        """
        # Get the name
        element_name = visualization_attribute_element.get_name()
        logger.info(
            "Interpreting a {name} VisualizationAttribute".format(
                name=element_name))

        # Get the structural feature
        structural_feature = self.ifml_symbol_table.lookup(
            visualization_attribute_element.get_feature_concept()
        ).struct_feature_symbol

        # Note that data binding in React can be
        # retrieved from component's props
        visualization = VisualizationWithSpan(
            element_name,
            structural_feature.name,
            data_binding_property.variable_name)

        # Append to the JSX
        jsx_parent.append_jsx_into_body(visualization.render())

    def interpret_simple_field(
            self,
            simple_field_element,
            jsx_calling,
            list_in_param,
            default_value_source: InstanceVarDeclType = None
    ):
        """
        Parse simple field and append the result to its parent.

        :param simple_field_element: the ifml element
        :param jsx_calling: the parent markup language template
        :param list_in_param: list of all in param for next process
        :param default_value_source: variable for set field's default value
        :return: None
        """

        # Get the name and type
        element_name = simple_field_element.get_name()

        logger.info(
            "Interpreting a {name} SimpleField".format(name=element_name))

        # Find the type in the UML Symbol Table
        uml_model_name, id_of_type = simple_field_element.get_type().split('#')
        datatype_of_field = self.uml_symbol_table.lookup(uml_model_name,
                                                         id_of_type).name

        # Interpreting the parameter, because part of Simple Field is Parameter
        self.interpret_parameter(simple_field_element, list_in_param)

        # Create the Input Field
        input_jsx = InputField(element_name, datatype_of_field)

        direction = simple_field_element.get_direction()

        if default_value_source:
            input_jsx.set_default_value(
                'this.{property_name}'.format(
                    property_name=camel_function_style(element_name)
                )
            )
        elif direction == 'in' or direction == 'inout':
            input_jsx.set_default_value(
                'this.props.{property_name}'.format(
                    property_name=camel_function_style(element_name)
                )
            )

        # Call Into the JSX, because the property already declared by 
        # interpreting the parameter 
        jsx_calling.append_jsx_into_body(input_jsx.render())

    def interpret_conditional_expression(self, conditional_expression_element,
                                         data_binding_function, class_parent):
        """
        Interpret notation where it seems the body has been declared
        hardcoded in the IFML structure.

        :param conditional_expression_element: IFML notation
        :param data_binding_function: data binding object contain function
        :param class_parent: parent class which needs this binding
        :return: None
        """

        # Add the property from Data Binding
        # this should be placed in state
        all_props: [InstanceVarDeclType] = [
            data_binding_function.property_declaration]

        # Due to ConditionalExpression hardcoded, this is parsing way to
        # assign value to object source data in instance variable.
        statements = self.tokenized_conditional_expression_body(
            conditional_expression_element.get_body())
        for statement in statements:
            var, value = statement
            declaration = data_binding_function.property_declaration
            if var == declaration.variable_name and \
                    declaration.value != '':
                # Skip if the value is empty.
                continue
            elif var == declaration.variable_name:
                # Extract variable data source from component
                # serializations
                model = re.search('\((.*)\)', value, re.IGNORECASE)
                if model:
                    assignment = model.group(1)
                else:
                    assignment = value

                # Assign the data source value which has been passed via
                # props from parents.
                if 'this.' in assignment:
                    assignment = assignment.replace('this.', 'this.props.')
                else:
                    raise TypeError(
                        'Unrecognized "{}" value of {} variable'
                            .format(assignment, var))
                declaration.value = assignment
            else:
                # if the value is not empty then add to the all props
                # variables container
                instance_var = InstanceVarDeclType(var)
                instance_var.value = value
                all_props.append(instance_var)

        for prop in all_props:
            statement = "this.{} = {}".format(
                prop.variable_name,
                prop.value
            )
            class_parent.add_line_to_component_will_mount(statement)

    def tokenized_conditional_expression_body(self, text: str) -> [str]:
        arr = []

        statements = text.split(';')

        for statement in statements:
            if statement.strip() == '':
                continue

            areas: [str] = statement.split(' = ')
            var: str = areas[0].replace('this.', '').strip()
            value: str = areas[1].strip()
            arr.append((var, value))

        return arr

    def interpret_slot(self, view_element_event, jsx_calling,
                       component_calling):
        pass

    def interpret_parameter(self, parameter_element,
                            list_in_direction_parameter):
        # Get element name, and parameter direction
        direction = parameter_element.get_direction()

        if direction == 'in':
            self.interpret_in_parameter(parameter_element,
                                        list_in_direction_parameter)
        elif direction == 'out':
            # The implementation of this type will be done by those
            # component which need this param and will be processed as In
            # parameter.
            pass
        elif direction == 'inout':
            self.interpret_in_parameter(parameter_element,
                                        list_in_direction_parameter)
        else:
            raise TypeError(
                'No Parameter will have {direction} direction, Please verify '
                'the validity of your IFML'.format(
                    direction=direction))

    def interpret_in_parameter(self, in_parameter_element,
                               list_in_direction_parameter):
        """
        Handle input parameter to the component.

        :param in_parameter_element: IFML Notation
        :param list_in_direction_parameter: In Parameter Container
        :return:
        """
        # Get element name and type
        element_name = in_parameter_element.get_name()
        uml_name, id_of_symbol = in_parameter_element.get_type().split('#')
        type_used_by_parameter = self.uml_symbol_table.lookup(uml_name,
                                                              id_of_symbol)

        # UPDATE#1: Due to React mostly handle data in object so no need to
        # replace it with symbol.

        # If type is class then take the model from model container,
        # else just take the string name. But, still, this won't be
        # explicitly written in the generated code.
        if isinstance(type_used_by_parameter, ClassSymbol):
            type_used_by_parameter = self.models[type_used_by_parameter.id]

        # Creating Input Property Declaration in child
        input_node = InParameter(element_name, type_used_by_parameter)

        # Add it into InDirectionInput List at Child Component
        list_in_direction_parameter.append(input_node)

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
        jsx = ReactJSX()

        return jsx, react_class, routing_node

    def view_component_definition(self):

        jsx, _, routing_node = self.view_container_definition()
        component_class = ReactComponentWithInputEseightClass()
        return jsx, component_class, routing_node

    def check_if_there_is_an_interaction_flow(self, element):
        """
        Inspect if there is any interaction flow contained in the element.

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

    def build_in_parameter_for_parent(self, call_jsx, parent_component,
                                      list_param):
        """
        handle all input parameter. Gather the data from query param in the
        url. Implementing this way helps user to reload the page without
        re-fetch data.

        :param call_jsx:
        :param parent_component:
        :param list_param:
        :return:
        """
        # This logic is only good for parameter inside form and detail
        # Improve this logic for list
        constructor_body_statement = GettingQueryParam()
        for param in list_param:

            # Adding the parameter to jsx Call
            call_jsx.add_parameter_and_property_pair(param.child_property,
                                                     param.parent_property)

            # Check if the declaration of property need to import a model class, else no import needed
            if param.needed_import:
                query_param_name, property_name, class_type = param.parent_property.variable_name, param.parent_property.variable_name, param.parent_property.variable_datatype
                constructor_body_statement.add_statement_for_saving_query_param_value_into_property_typed_class(
                    query_param_name, property_name, class_type)
            else:
                query_param_name, property_name = param.parent_property.variable_name, param.parent_property.variable_name
                constructor_body_statement.add_statement_for_saving_query_param_value_into_property(
                    query_param_name, property_name)

        # React can just access the passed props without having issue with
        # type.

        # UPDATE#2: this statement is meant to parse the query param in URL
        # into a JSON data so that can be processed by the destination route.

        # UPDATE#3: to persist the data when user refresh the page so we
        # still need to use Query Param
        parent_component.add_default_element_import_statement(
            'query-string',
            'queryString'
        )
        parent_component.add_line_to_component_did_mount(
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
                self.interpret_onselect_event(
                    view_element_event,
                    component_node.component_jsx,
                    component_node.component_class)
            elif isinstance(view_element_event, OnSubmitEvent):
                self.interpret_onsubmit_event(
                    view_element_event,
                    component_node.component_jsx,
                    component_node.component_class)
            elif isinstance(view_element_event, ViewElementEvent):
                self.interpret_view_element_event(
                    view_element_event,
                    component_node.component_jsx,
                    component_node.component_class,
                    view_element_parent_symbol)

    def interpret_interaction_flow(self, interaction_flow_element,
                                   function_node, from_action=False):

        param_binding_group = \
            interaction_flow_element.get_parameter_binding_groups()

        if isinstance(interaction_flow_element, NavigationFlow):
            self.interpret_navigation_flow(interaction_flow_element,
                                           function_node, param_binding_group,
                                           from_action)
        else:
            raise TypeError("Unimplemented Interaction Flow {}".format(
                type(interaction_flow_element)
            ))

    def interpret_navigation_flow(self, navigation_flow_element, function_node,
                                  param_binding_group, from_action=False):

        # Get element target
        element_target = \
            navigation_flow_element.get_target_interaction_flow_element()
        target_symbol = self.ifml_symbol_table.lookup(element_target)

        if isinstance(target_symbol, ViewContainerSymbol) or isinstance(
                target_symbol, WindowSymbol):
            # handle flow for navigation to page
            self.interaction_with_container_as_target(
                self.components.get(target_symbol.id), function_node,
                param_binding_group, from_action)
        elif isinstance(target_symbol, ActionSymbol):
            # handle flow for API Call
            self.interaction_with_action_as_target(
                self.services.get(target_symbol.id), function_node,
                param_binding_group)

    def interaction_with_container_as_target(self, container_node,
                                             function_node,
                                             param_binding_group, from_action):
        # Get routing path of that page
        route_path_from_root = container_node.get_routing_path()

        # Creating statement for navigation into page
        router_statement = RouteToComponentPage(route_path_from_root)

        # Build the param binding group for data delivery via query url
        if param_binding_group:
            param_binding_group_node = self.interpret_param_binding(
                param_binding_group, from_action, is_query_param=True)
            router_statement.add_param_binding_group(
                param_binding_group_node.render())
            import_node = ImportStatementType()
            import_node.set_default_element('queryString')
            import_node.set_main_module('query-string')
            function_node.add_needed_import(import_node)

        # Append to the event function handler
        function_node.add_statement_to_body(router_statement.render())

    def interaction_with_action_as_target(self, service_node, function_node,
                                          param_binding_group):
        # set async
        function_node.is_async = True

        # Get the service name, and filename
        service_class_name = service_node.class_name
        service_filename = service_node.filename

        # Currently support only one event after action proceeded
        service_action_event = service_node.action_event

        # Creating statement for navigation into service
        service_call_statement = RouteToAction(service_class_name,
                                               service_filename)

        # Build the param binding group
        if param_binding_group:
            param_binding_group_node = self.interpret_param_binding(
                param_binding_group, from_input_text=True)
            service_call_statement.add_param_binding_group(
                param_binding_group_node.render())

        # Setup the following event after calling action, if None,
        # then nothing to be appended
        try:
            post_action_event = service_action_event.function_body
            service_call_statement.after_statement = post_action_event
            for import_statement in service_action_event.needed_import:
                function_node.add_needed_import(import_statement)
        except AttributeError:
            pass

        # Append to the event function handler. add import and constructor
        # param
        function_node.add_needed_import(
            service_call_statement.import_statement)

        # Doesn't need to add anything to constructor param class since
        # React just create the service as an object and call the function.
        function_node.add_statement_to_body(service_call_statement.render())

    def interpret_param_binding(self, param_binding_group, from_action=False,
                                is_query_param=False, from_input_text=False):

        # Create ParamGroup Node
        param_group = ParamGroup()

        # Build all Parameter Binding inside Parameter Binding Group
        for _, param_binding in \
                param_binding_group.get_parameter_bindings().items():
            source_param_symbol = self.ifml_symbol_table.lookup(
                param_binding.get_source_parameter())
            target_param_symbol = self.ifml_symbol_table.lookup(
                param_binding.get_target_parameter())

            param_binding_statement = ParameterBindingInterpretation(
                source_param_symbol.name, target_param_symbol.name,
                from_action, is_query_param)
            if from_input_text:
                param_binding_statement.source_param_name = \
                    param_binding_statement.source_param_name + 'Input.value'

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
        # Create dummy Component
        jsx, component_class = ReactJSX(), LoginClass()
        component_node = ReactComponent(component_class, jsx)
        routing_node = RouteToModule(component_class)
        routing_node.path = \
            routing_node.path_from_root = \
            component_node.routing_path = \
            self.root_routing.path_from_root + '/login'
        self.root_routing.add_children_routing(routing_node)
        self.root_routing.enable_children_routing()
        self.root_eseight_class.add_import_statement_for_multiple_element(
            'react-router-dom',
            ['Route', 'Switch']
        )
        self.root_eseight_class.add_default_element_import_statement(
            '../Login/login.js',
            'LoginComponent')
        self.root_template.append_route(routing_node.render())
        self.components['login'] = component_node
