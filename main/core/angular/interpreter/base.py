import logging

from yattag import Doc

from ifml_parser.ifml_element.interaction_flow_elements.action_family.base import Action
from ifml_parser.ifml_element.interaction_flow_elements.view_family.view_containers import ViewContainer, Menu
from main.utils.ast.framework.angular.components import AngularComponent, AngularComponentTypescriptClass, \
    AngularComponentHTML
from main.utils.ast.framework.angular.routers import RouteToModule, RedirectToAnotherPath, RootRoutingNode
from main.utils.ast.framework.angular.services import AngularService
from main.utils.ast.language.html import HTMLMenuTemplate
from main.utils.ast.language.typescript import VarDeclType
from main.utils.naming_management import dasherize
from . import BaseInterpreter

logger_ifml_angular_interpreter = logging.getLogger("main.core.angular.interpreter")


# Processing the all model and will return the AST of Angular that define the project structure of the IFML design
class IFMLtoAngularInterpreter(BaseInterpreter):

    def __init__(self, ifml_xmi, class_diagram_xmi):
        self.root_ifml = ifml_xmi
        self.root_class_diagram_xmi = class_diagram_xmi
        self.project_name = dasherize(self.root_ifml.name)
        self.components = {}
        self.services = {}
        self.list_service_worker_config = []
        self.angular_routing = RootRoutingNode('')
        self.root_html = self.get_root_html()
        self.root_typescript_class = self.get_root_class()

        logger_ifml_angular_interpreter.info("Interpreting {name} IFML Project".format(name=self.project_name))

        # Getting All IFML Elements
        self.ifml_expressing_ui_design = self.root_ifml.get_interaction_flow_model().get_interaction_flow_model_elements()

        # Getting All Domain Model Elements
        self.domain_model_used_by_ifml = self.root_ifml.get_domain_model()
        self.interpret_interaction_flow_model()
        self.interpret_domain_model()

        # Decide whether router-outlet is needed or not
        self.append_router_outlet()

    def append_router_outlet(self):
        if len(self.angular_routing.angular_children_routes) > 0:
            doc_outlet, tag_outlet, text_outlet = Doc().tagtext()

            with tag_outlet('router-outlet'):
                text_outlet('')
            self.root_html.append_html_into_body(doc_outlet.getvalue())

    def get_root_class(self):
        # Angular Typescript Component for root component
        root_ts_class = AngularComponentTypescriptClass()
        root_ts_class.component_name = 'app'
        root_ts_class.class_name = 'App'
        root_ts_class.selector_name = 'app-root'
        return root_ts_class

    def get_root_html(self):
        root_html_node = AngularComponentHTML()
        return root_html_node

    def get_project_name(self):
        return self.project_name

    def interpret_interaction_flow_model(self):
        for key, interaction_flow_model_element in self.ifml_expressing_ui_design.items():
            # If the root have actions
            if isinstance(interaction_flow_model_element, Action):
                self.interpret_action(interaction_flow_model_element)
            # If the root have menu
            elif isinstance(interaction_flow_model_element, Menu):
                logger_ifml_angular_interpreter.info(
                    "Interpreting a {name} Menu".format(name=interaction_flow_model_element.get_name()))
                self.interpret_menu(interaction_flow_model_element, self.root_html)
            elif isinstance(interaction_flow_model_element, ViewContainer):
                logger_ifml_angular_interpreter.info(
                    "Interpreting a {name} View Container".format(name=interaction_flow_model_element.get_name()))
                self.interpret_view_container(interaction_flow_model_element, self.root_html,
                                              self.root_typescript_class, self.angular_routing)

    def interpret_menu(self, menu_element, html_calling):

        # Name of element
        element_name = menu_element.get_name()

        # Prepare Typescript Class
        typescript_class = AngularComponentTypescriptClass()
        typescript_class.set_component_selector_class_name(element_name)

        # Prepare HTML
        html = HTMLMenuTemplate(typescript_class.selector_name)

        # Build All View Element Event Inside
        events = menu_element.get_view_element_events()
        for event in events:
            self.interpret_view_element_event(event, html, typescript_class)

        # The Component Itself
        angular_component_node = AngularComponent(component_typescript_class=typescript_class,
                                                  component_html=html)

        # Calling Menu selector
        doc_selector, tag_selector, text_selector = Doc().tagtext()

        with tag_selector(typescript_class.selector_name):
            text_selector('')

        # Menu always appended into first element
        html_calling.append_html_into_body(doc_selector.getvalue())

        # Register to components container
        self.components[menu_element.get_id()] = angular_component_node

    def interpret_view_container(self, view_container, html_calling, typescript_calling, routing_parent):

        # Name of element
        element_name = view_container.get_name()

        # Defining variable for routing node, intialized if this container have inInteractionFlow or isLandmark
        routing_node = None

        # Prepare Typescript Class
        typescript_class = AngularComponentTypescriptClass()
        typescript_class.set_component_selector_class_name(element_name)

        # Prepare HTML
        html = AngularComponentHTML()

        # Decide if this container is callable or using router
        # Checking if its is a Landmark or having an interaction flow

        if view_container.get_is_xor():
            routing_node = RouteToModule(typescript_class)
            routing_node.enable_children_routing()

        if (view_container.get_is_landmark() or len(
                view_container.get_in_interaction_flow()) > 0) and routing_node is None:

            landmark_path_var_name = typescript_class.class_name+'path'

            doc_landmark, tag_landmark, text_landmark = Doc().tagtext()
            with tag_landmark('button', ('class', 'landmark-event'), ('id', typescript_class.selector_name),
                              ('[routerLink]', typescript_class.class_name+'path')):
                text_landmark(typescript_class.class_name)
            routing_node = RouteToModule(typescript_class)

            absolute_path = routing_parent.path + '/' + routing_node.path

            landmark_path_var_decl = VarDeclType(landmark_path_var_name,';')
            landmark_path_var_decl.acc_modifiers = 'public'
            landmark_path_var_decl.value = absolute_path
            landmark_path_var_decl.variable_datatype = 'string'

            typescript_calling.set_property_decl(landmark_path_var_decl)
            html_calling.append_html_into_body(doc_landmark.getvalue())

        # TODO Implement, Delete below line after testing use
        doc_test, tag_test, text_test = Doc().tagtext()

        with tag_test('h2'):
            text_test(typescript_class.selector_name + ' Works Fine')

        html.append_html_into_body(doc_test.getvalue())
        # End TODO

        #Build All Action inside the Container
        for action in view_container.get_action():
            self.interpret_action(action)

        # Build All Associated View Element
        for key, view_element in view_container.get_assoc_view_element().items():
            if isinstance(view_element, Menu):
                self.interpret_menu(view_element, html)
            elif isinstance(view_element, ViewContainer):
                self.interpret_view_container(view_element, html, typescript_class, routing_node)

        # The Component Itself
        angular_component_node = AngularComponent(component_typescript_class=typescript_class,
                                                  component_html=html)

        # Decide if this container is default in its XOR
        if view_container.get_is_default():
            routing_parent.add_children_routing(RedirectToAnotherPath('', typescript_class.selector_name))

        # Add Routing Node and (If exist) any children route
        try:
            routing_parent.add_children_routing(routing_node)
            angular_component_node.set_routing_node(routing_parent.path + '/' + routing_node.path)
        # If this container must be called
        except Exception:
            # Calling ViewContainer selector
            doc_selector, tag_selector, text_selector = Doc().tagtext()

            with tag_selector(typescript_class.selector_name):
                text_selector('')
            html_calling.append_html_into_body(doc_selector.getvalue())

        #Register to components container
        self.components[view_container.get_id()] = angular_component_node

    def interpret_view_element_event(self, view_element_event, html_calling, typescript_calling):
        pass

    def interpret_action(self, action_element):
        # Name of element
        element_name = action_element.get_name()

        #Defining service typescript, and add the name into AngularService
        service_typescript = AngularService()
        service_typescript.set_endpoint_class_name_and_worker(element_name)

        #Calling ActionEvent and build it
        for action_event in action_element.get_action_event():
            self.interpret_action_event(action_event, service_typescript)

        #Register to services container
        self.services[action_element.get_id()] = service_typescript

        # Register service worker config
        self.list_service_worker_config.append(service_typescript.worker_config.render())

    def interpret_action_event(self, action_event_element, typescript_call):
        pass

    def interpret_domain_model(self):
        pass
