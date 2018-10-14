import logging

from yattag import Doc

from ifml_parser.ifml_element.interaction_flow_elements.view_family.view_containers import ViewContainer, Menu
from main.core.angular.interpreter.view_family import BaseViewContainerInterpreter
from . import BaseInterpreter
from main.utils.naming_management import dasherize
from main.utils.ast.framework.angular.components import AngularComponent, AngularComponentTypescriptClass, AngularComponentHTML
from main.utils.ast.language.html import HTMLMenuTemplate

logger_ifml_angular_interpreter = logging.getLogger("main.core.angular.interpreter")


# Processing the all model and will return the AST of Angular that define the project structure of the IFML design
class IFMLtoAngularInterpreter(BaseInterpreter):

    def __init__(self, ifml_xmi, class_diagram_xmi):
        self.root_ifml = ifml_xmi
        self.root_class_diagram_xmi = class_diagram_xmi
        self.project_name = dasherize(self.root_ifml.name)
        self.component = {}
        self.service = {}
        self.angular_routing = {}
        self.root_html = AngularComponentHTML()
        self.root_typescript_class = self.build_root_class()

        logger_ifml_angular_interpreter.info("Interpreting {name} IFML Project".format(name=self.project_name))

        # Getting All IFML Elements
        self.ifml_expressing_ui_design = self.root_ifml.get_interaction_flow_model().get_interaction_flow_model_elements()

        # Getting All Domain Model Elements
        self.domain_model_used_by_ifml = self.root_ifml.get_domain_model()
        self.interpret_interaction_flow_model()
        self.interpret_domain_model()

    def build_root_class(self):
        # Angular Typescript Component for root component
        root_ts_class = AngularComponentTypescriptClass()
        root_ts_class.component_name = 'app'
        root_ts_class.class_name = 'App'
        root_ts_class.selector_name = 'app-root'

    def get_project_name(self):
        return self.project_name

    def interpret_interaction_flow_model(self):
        for key, interaction_flow_model_element in self.ifml_expressing_ui_design.items():
            # If the root have menu
            if isinstance(interaction_flow_model_element, Menu):
                self.interpret_menu(interaction_flow_model_element, self.root_html)
            elif isinstance(interaction_flow_model_element, ViewContainer):
                logger_ifml_angular_interpreter.info(
                    "Interpreting a {name}View Container".format(name=interaction_flow_model_element.get_name()))
                self.component[interaction_flow_model_element.get_id()] = BaseViewContainerInterpreter(
                    view_container=interaction_flow_model_element).build()

    def interpret_menu(self, menu_element, html_calling):

        #Name of element
        element_name = menu_element.get_name()

        # Prepare Typescript Class
        typescript_class = AngularComponentTypescriptClass()
        typescript_class.set_component_selector_class_name(menu_element.get_name())

        # Prepare HTML
        html = HTMLMenuTemplate()

        #Build All View Element Event Inside
        menu_buttons = menu_element.get_view_element_events()
        for button in menu_buttons:
            self.interpret_menu(button)

        #The Component Itself
        angular_component_node = AngularComponent(element_name,
                                                       component_typescript_class=typescript_class,
                                                       component_html=html)

        self.component[menu_element.get_id()] = angular_component_node

        #Calling Menu selector
        doc, tag, text = Doc().tagtext()

        with tag(typescript_class.selector_name):
            text('')
        html_calling.add_html_into_body(doc.getvalue())

    def interpret_event(self, event_menu, html_calling, typescript_calling):
        pass

    def interpret_domain_model(self):
        pass