import logging

from yattag import Doc

from custom_xmi_parser.umlsymboltable import ClassSymbol
from ifml_parser.ifml_element.interaction_flow.base import NavigationFlow, DataFlow
from ifml_parser.ifml_element.interaction_flow_elements.action_family.base import Action
from ifml_parser.ifml_element.interaction_flow_elements.event_family.catching_event_extension import ViewElementEvent
from ifml_parser.ifml_element.interaction_flow_elements.event_family.view_element_event_extension import OnSubmitEvent, \
    OnSelectEvent
from ifml_parser.ifml_element.interaction_flow_elements.view_family.view_component_parts import SimpleField, \
    DataBinding, VisualizationAttribute, ConditionalExpression
from ifml_parser.ifml_element.interaction_flow_elements.view_family.view_components import Form, Details, List
from ifml_parser.ifml_element.interaction_flow_elements.view_family.view_containers import ViewContainer, Menu, Window
from ifml_parser.ifmlsymboltable import ViewContainerSymbol, WindowSymbol, ActionSymbol
from main.utils.ast.framework.angular.buttons import AngularButtonWithFunctionHandler, AngularSubmitButtonType, \
    AngularOnclickType, AngularModalButtonAndFunction
from main.utils.ast.framework.angular.component_parts import InputField, DataBindingFunction, VisualizationWithSpan
from main.utils.ast.framework.angular.components import AngularComponent, AngularComponentTypescriptClass, \
    AngularComponentHTML, AngularFormHTML, AngularDetailHTMLCall, AngularListHTMLCall, AngularListHTMLLayout, \
    AngularModalHTMLLayout, AngularComponentForModal, AngularComponentWithInputTypescriptClass
from main.utils.ast.framework.angular.models import ModelFromUMLClass
from main.utils.ast.framework.angular.parameters import InParameter, OutParameter
from main.utils.ast.framework.angular.routers import RouteToModule, RedirectToAnotherPath, RootRoutingNode, \
    RouteToComponentPage
from main.utils.ast.framework.angular.services import AngularService
from main.utils.ast.language.html import HTMLMenuTemplate
from main.utils.ast.language.typescript import VarDeclType
from main.utils.naming_management import dasherize, camel_function_style
from . import BaseInterpreter

logger_ifml_angular_interpreter = logging.getLogger("main.core.angular.interpreter")


# Processing the all model and will return the AST of Angular that define the project structure of the IFML design
class IFMLtoAngularInterpreter(BaseInterpreter):

    def __init__(self, ifml_xmi, ifml_symbol_table, class_diagram_xmi, class_diagram_symbol_table):
        self.root_ifml, self.ifml_symbol_table = ifml_xmi, ifml_symbol_table
        self.root_class_diagram_xmi, self.uml_symbol_table = class_diagram_xmi, class_diagram_symbol_table
        self.project_name = dasherize(self.root_ifml.name)
        self.components = {}
        self.services = {}
        self.models = {}
        self.action_events = []
        self.view_element_events = []
        self.list_service_worker_config = []
        self.angular_routing = RootRoutingNode('')
        self.root_html = self.get_root_html()
        self.root_typescript_class = self.get_root_class()

        logger_ifml_angular_interpreter.info("Interpreting {name} IFML Project".format(name=self.project_name))

        # Getting All IFML Elements
        self.ifml_expressing_ui_design = self.root_ifml.get_interaction_flow_model().get_interaction_flow_model_elements()

        # Interpret all Domain Model Elements
        self.interpret_domain_model()

        # Interpret all Interaction Flow Model Elements
        self.interpret_interaction_flow_model()

        # Interpret all Action Event Elements with it's corresponding navigation
        self.interpret_all_action_events()

        # Interpret all View Element Elements with it's corresponding navigation
        self.interpret_all_view_element_events()

        # Decide whether router-outlet is needed or not
        self.append_router_outlet(self.angular_routing, self.root_html)

    def router_outlet_html(self):
        doc_outlet, tag_outlet, text_outlet = Doc().tagtext()

        with tag_outlet('router-outlet'):
            text_outlet('')
        return doc_outlet.getvalue()

    def append_router_outlet(self, angular_routing, html_call):
        if len(angular_routing.angular_children_routes) > 0:
            html_call.append_html_into_body(self.router_outlet_html())

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
            # If the root have Windows
            elif isinstance(interaction_flow_model_element, Window):
                self.check_if_windows_is_different_than_view_container(interaction_flow_model_element, self.root_html,
                                                                       self.root_typescript_class, self.angular_routing)
            # If the root have menu
            elif isinstance(interaction_flow_model_element, Menu):
                self.interpret_menu(interaction_flow_model_element, self.root_html)
            elif isinstance(interaction_flow_model_element, ViewContainer):
                self.interpret_view_container(interaction_flow_model_element, self.root_html,
                                              self.root_typescript_class, self.angular_routing)

    def check_if_windows_is_different_than_view_container(self, window_element, html_calling, typescript_calling,
                                                          routing_parent):
        # Check if there is no difference with view container
        is_new_window = window_element.get_new_window_att()
        is_modal = window_element.get_modal_att()
        if not (is_modal or is_new_window):
            self.interpret_view_container(window_element, html_calling, typescript_calling, routing_parent)
        else:
            self.interpret_windows(window_element, html_calling, typescript_calling, routing_parent)

    def interpret_windows(self, window_element, html_calling, typescript_calling, routing_parent):
        # Name of element
        element_name = window_element.get_name()
        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} Windows".format(name=element_name))

        # Modal Typescript class and HTML
        typescript_class = AngularComponentTypescriptClass()
        typescript_class.set_component_selector_class_name(element_name)

        html = AngularModalHTMLLayout(element_name)

        # Build All View Element Event Inside
        for _, event in window_element.get_view_element_events().items():
            self.view_element_events.append(event)

        # TODO Implement
        # Check if it is a XOR

        # Check if it is a landmark
        if (window_element.get_is_landmark()):
            # Append the Button into root HTML
            func_and_html_event_node = AngularModalButtonAndFunction(element_name, type='async')
            func_and_html_event_node.set_target_modal(html.var_camel_name)

            # Import the service, create the constructor param
            typescript_calling.add_import_statement_using_import_node(
                func_and_html_event_node.import_ngx_modal_service_node)
            typescript_calling.set_constructor_param(func_and_html_event_node.ngx_service_constructor)

            # Get the function and HTML
            button_html, typescript_function = func_and_html_event_node.render()

            # Append the Button
            html_calling.append_html_into_body(button_html)

            # Append the function
            typescript_calling.body.append(typescript_function)

        # Check if there are any interaction flow, but no need to define anything

        # Creating the Angular Component Node
        angular_component_node = AngularComponentForModal(typescript_class, html)

        # Register the Modal Selector the parent HTML
        doc_selector, tag_selector, text_selector = Doc().tagtext()
        with tag_selector(typescript_class.selector_name):
            text_selector('')
        html_calling.append_html_into_body(doc_selector.getvalue())

        # Registering to Components Container
        self.components[window_element.get_id()] = angular_component_node

    def interpret_menu(self, menu_element, html_calling):

        # Name of element
        element_name = menu_element.get_name()

        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} Menu".format(name=element_name))

        # Prepare Typescript Class
        typescript_class = AngularComponentTypescriptClass()
        typescript_class.set_component_selector_class_name(element_name)

        # Prepare HTML
        html = HTMLMenuTemplate(typescript_class.selector_name)

        # Build All View Element Event Inside
        for _, event in menu_element.get_view_element_events().items():
            self.view_element_events.append(event)

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

        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} View Container".format(name=element_name))

        html, typescript_class, routing_node = self.view_container_definition()

        typescript_class.set_component_selector_class_name(element_name)

        # Decide if this container is callable or using router
        # Checking if its is a Landmark or having an interaction flow
        if view_container.get_is_xor():
            routing_node = RouteToModule(typescript_class)
            routing_node.enable_children_routing()

        if self.check_if_there_is_an_interaction_flow(view_container) and routing_node is None:
            routing_node = RouteToModule(typescript_class) if routing_node is None else routing_node

        if (view_container.get_is_landmark()):
            landmark_path_var_name = camel_function_style(typescript_class.class_name) + 'path'

            doc_landmark, tag_landmark, text_landmark = Doc().tagtext()
            with tag_landmark('button', ('class', 'landmark-event'), ('id', typescript_class.selector_name),
                              ('[routerLink]', landmark_path_var_name)):
                text_landmark(typescript_class.class_name)

            routing_node = RouteToModule(typescript_class) if routing_node is None else routing_node

            absolute_path = routing_node.path

            landmark_path_var_decl = VarDeclType(landmark_path_var_name, ';')
            landmark_path_var_decl.acc_modifiers = 'public'
            landmark_path_var_decl.value = "\'{value}\'".format(value=absolute_path)
            landmark_path_var_decl.variable_datatype = 'string'

            typescript_calling.set_property_decl(landmark_path_var_decl)
            html_calling.append_html_into_body(doc_landmark.getvalue())

        # Adding Path from root
        if not (routing_node is None):
            routing_node.path_from_root = routing_parent.path_from_root + '/' + routing_node.path

        # TODO Implement, Delete below line after testing use
        doc_test, tag_test, text_test = Doc().tagtext()

        with tag_test('h2'):
            text_test(typescript_class.selector_name + ' Works Fine')

        html.append_html_into_body(doc_test.getvalue())
        # End TODO

        # TODO Implement
        # Build All View Element Event Inside
        for _, event in view_container.get_view_element_events().items():
            if isinstance(event, ViewElementEvent):
                # self.interpret_view_element_event(event, html, typescript_class)
                self.view_element_events.append(event)

        # TODO Implement
        # Build All Action inside the Container
        for _, action in view_container.get_action().items():
            self.action_events.append(action)

        # Build All Associated View Element
        for key, view_element in view_container.get_assoc_view_element().items():
            if isinstance(view_element, List):
                self.interpret_list(view_element, html, typescript_class, routing_node)
            elif isinstance(view_element, Details):
                self.interpret_detail(view_element, html, typescript_class, routing_node)
            elif isinstance(view_element, Form):
                self.interpret_form(view_element, html, typescript_class, routing_node)
            elif isinstance(view_element, Window):
                self.check_if_windows_is_different_than_view_container(view_element, html, typescript_class,
                                                                       routing_node)
            elif isinstance(view_element, Menu):
                self.interpret_menu(view_element, html)
            elif isinstance(view_element, ViewContainer):
                self.interpret_view_container(view_element, html, typescript_class, routing_node)

        # Decide if this container is default in its XOR
        if view_container.get_is_default():
            routing_parent.add_children_routing(RedirectToAnotherPath('', typescript_class.selector_name))

        # The Component Itself
        angular_component_node = AngularComponent(component_typescript_class=typescript_class,
                                                  component_html=html)

        # Add Routing Node and (If exist) any children route
        try:
            routing_parent.add_children_routing(routing_node)
            angular_component_node.set_routing_node(routing_node.path_from_root)
            self.append_router_outlet(routing_node, html)
        # If this container must be called
        except Exception:
            # Calling ViewContainer selector
            doc_selector, tag_selector, text_selector = Doc().tagtext()

            with tag_selector(typescript_class.selector_name):
                text_selector('')
            html_calling.append_html_into_body(doc_selector.getvalue())

        # Register to components container
        self.components[view_container.get_id()] = angular_component_node

    def interpret_action(self, action_element):
        # Name of element
        element_name = action_element.get_name()

        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} Action".format(name=element_name))

        # Defining service typescript, and add the name into AngularService
        service_typescript = AngularService()
        service_typescript.set_endpoint_class_name_and_worker(element_name)

        # TODO Implement
        # Calling ActionEvent and build it
        for _, action_event in action_element.get_action_event().items():
            self.interpret_action_event(action_event, service_typescript)

        # Register to services container
        self.services[action_element.get_id()] = service_typescript

        # Register service worker config
        self.list_service_worker_config.append(service_typescript.worker_config.render())

    def interpret_form(self, form_element, html_calling, typescript_calling, routing_parent):
        # Name of element
        element_name = form_element.get_name()

        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} Form".format(name=element_name))

        # Only need the routing node and typescript_class
        _, typescript_class, routing_node = self.view_component_definition()
        typescript_class.set_component_selector_class_name(element_name)

        # The HTML for Form
        html = AngularFormHTML(element_name)

        # Defining Routing Node
        routing_node = None

        # Determine if there are any incoming interaction flow
        if self.check_if_there_is_an_interaction_flow(form_element) and routing_node is None:
            routing_node = RouteToModule(typescript_class)
            routing_node.path_from_root = routing_parent.path_from_root + '/' + routing_node.path

        # TODO Implement
        # Build all View Component Part
        for _, view_component_part in form_element.get_assoc_view_component_parts().items():
            if isinstance(view_component_part, SimpleField):
                self.interpret_simple_field(view_component_part, html, typescript_class)
            elif isinstance(view_component_part, DataBinding):
                self.interpret_data_binding(view_component_part, html, typescript_class)

        # TODO Implement
        # Build All View Element Event Inside
        for _, event in form_element.get_view_element_events().items():
            self.view_element_events.append(event)

        # Creating the component node
        # The Component Itself
        angular_component_node = AngularComponent(component_typescript_class=typescript_class,
                                                  component_html=html)

        # Add Routing Node and (If exist) any children route
        try:
            routing_parent.add_children_routing(routing_node)
            angular_component_node.set_routing_node(routing_node.path_from_root)
        # If this container must be called
        except Exception:
            # Calling Form selector
            doc_selector, tag_selector, text_selector = Doc().tagtext()

            with tag_selector('div', id='div-form-{name}'.format(name=html.form_dasherize),
                              klass='div-form view-component'):
                with tag_selector(typescript_class.selector_name):
                    text_selector('')
            html_calling.append_html_into_body(doc_selector.getvalue())

        # Register to components container
        self.components[form_element.get_id()] = angular_component_node

    def interpret_detail(self, detail_element, html_calling, typescript_calling, routing_parent):
        # Name of element
        element_name = detail_element.get_name()

        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} Detail".format(name=element_name))

        # HTML, Typescript Class, and Routing Node
        html, typescript_class, routing_node = self.view_component_definition()
        typescript_class.set_component_selector_class_name(element_name)

        # HTML Call for Detail
        # Preparation to Call Detail
        detail_call = AngularDetailHTMLCall(typescript_class.selector_name)

        # Defining Routing Node
        routing_node = None

        # Determine if there are any incoming interaction flow
        if self.check_if_there_is_an_interaction_flow(detail_element) and routing_node is None:
            routing_node = RouteToModule(typescript_class)
            routing_node.path_from_root = detail_element.path_from_root + '/' + routing_node.path

        # TODO Implement
        list_in_param = []
        for _, parameter in detail_element.get_parameters().items():
            self.interpret_parameter(parameter, html, typescript_class, list_in_param)

        # TODO Implement Building all In Direction Parameter
        self.build_in_parameter_for_parent(detail_call, typescript_calling, list_in_param)

        # TODO Implement
        # Build All View Element Event Inside
        for _, event in detail_element.get_view_element_events().items():
            self.view_element_events.append(event)

        # TODO Implement
        # Build all View Component Part
        for _, view_component_part in detail_element.get_assoc_view_component_parts().items():
            if isinstance(view_component_part, DataBinding):
                self.interpret_data_binding(view_component_part, html, typescript_class)

        # Creating the component node
        # The Component Itself
        angular_component_node = AngularComponent(component_typescript_class=typescript_class,
                                                  component_html=html)

        # Add Routing Node and (If exist) any children route
        try:
            routing_parent.add_children_routing(routing_node)
            angular_component_node.set_routing_node(routing_node.path_from_root)
        # If this container must be called
        except Exception:
            # Calling Detail selector
            doc_selector, tag_selector, text_selector = Doc().tagtext()
            with tag_selector('div', id='div-detail-{name}'.format(name=typescript_class.selector_name),
                              klass='div-detail view-component'):
                doc_selector.asis(detail_call.render())
            html_calling.append_html_into_body(doc_selector.getvalue())

        # Register to components container
        self.components[detail_element.get_id()] = angular_component_node

    def interpret_list(self, list_element, html_calling, typescript_calling, routing_parent):
        # Name of element
        element_name = list_element.get_name()

        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} List".format(name=element_name))

        # Typescript Class, and Routing Node
        _, typescript_class, routing_node = self.view_component_definition()
        typescript_class.set_component_selector_class_name(element_name)

        # List HTML Layout
        html = AngularListHTMLLayout()

        # Preparation to Call List selector in parent
        list_call = AngularListHTMLCall(typescript_class.selector_name)

        # Defining Routing Node
        routing_node = None

        # Determine if there are any incoming interaction flow
        if self.check_if_there_is_an_interaction_flow(list_element) and routing_node is None:
            routing_node = RouteToModule(typescript_class)
            routing_node.path_from_root = list_element.path_from_root + '/' + routing_node.path

        # TODO Implement
        list_in_param = []
        for _, parameter in list_element.get_parameters().items():
            self.interpret_parameter(parameter, html, typescript_class, list_in_param)

        # TODO Implement Building all In Direction Parameter
        self.build_in_parameter_for_parent(list_call, typescript_calling, list_in_param)

        # TODO Implement
        # Build All View Element Event Inside
        for _, event in list_element.get_view_element_events().items():
            self.view_element_events.append(event)

        # TODO Implement
        # Build all View Component Part
        for _, view_component_part in list_element.get_assoc_view_component_parts().items():
            if isinstance(view_component_part, DataBinding):
                self.interpret_data_binding(view_component_part, html, typescript_class)

        # Creating the component node
        # The Component Itself
        angular_component_node = AngularComponent(component_typescript_class=typescript_class,
                                                  component_html=html)

        # Add Routing Node and (If exist) any children route
        try:
            routing_parent.add_children_routing(routing_node)
            angular_component_node.set_routing_node(routing_node.path_from_root)
        # If this container must be called
        except Exception:
            # Calling Detail selector
            doc_selector, tag_selector, text_selector = Doc().tagtext()
            with tag_selector('div', id='div-list-{name}'.format(name=typescript_class.selector_name),
                              klass='div-list view-component'):
                doc_selector.asis(list_call.render())
            html_calling.append_html_into_body(doc_selector.getvalue())

        # Register to components container
        self.components[list_element.get_id()] = angular_component_node

    # TODO Implement
    def interpret_view_element_event(self, view_element_event, html_calling, typescript_calling):
        # Get the name
        element_name = view_element_event.get_name()

        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} View Element Event".format(name=element_name))

        # Interpret, Defining Typescript function and HTML button
        func_and_html_event_node = AngularButtonWithFunctionHandler(element_name, type='async')

        # TODO Implement Delete this after test
        func_and_html_event_node.add_statement_into_function_body('console.log(\'Click Activated\');')

        # Build all child
        for _, interaction_flow in view_element_event.get_out_interaction_flow().items():
            self.interpret_interaction_flow(interaction_flow, func_and_html_event_node)

        # Call it to the parent HTML
        button_html, typescript_function = func_and_html_event_node.render()
        html_calling.append_html_into_body(button_html)

        # Call it to typescript body, and possibly add import node and constructor param to the class
        typescript_calling.body.append(typescript_function)

        for import_node in func_and_html_event_node.needed_import:
            typescript_calling.add_import_statement_using_import_node(import_node)

        for constructor_param in func_and_html_event_node.needed_constructor_param:
            typescript_calling.set_constructor_param(constructor_param)

    # TODO Implement
    def interpret_onsubmit_event(self, onsubmit_event, html_calling, typescript_calling):

        # Get the name
        element_name = onsubmit_event.get_name()

        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} OnSubmit Event".format(name=element_name))

        # Interpret, Defining Typescript function and HTML button
        func_and_html_event_node = AngularSubmitButtonType(element_name, type='async')

        # TODO Implement Delete this after test
        func_and_html_event_node.add_statement_into_function_body('console.log(\'Click Activated\');')

        # Build all child
        for _, interaction_flow in onsubmit_event.get_out_interaction_flow().items():
            self.interpret_interaction_flow(interaction_flow, func_and_html_event_node)

        # Call it to the parent by binding it to HTML Form on submit method, add_submit_event
        button_html, typescript_function, ngsubmit = func_and_html_event_node.render()
        html_calling.append_html_into_body(button_html)
        html_calling.add_submit_event(ngsubmit)

        # Call it to typescript body, and possibly add import node and constructor param to the class
        typescript_calling.body.append(typescript_function)

        for import_node in func_and_html_event_node.needed_import:
            typescript_calling.add_import_statement_using_import_node(import_node)

        for constructor_param in func_and_html_event_node.needed_constructor_param:
            typescript_calling.set_constructor_param(constructor_param)

    # TODO Implement
    def interpret_onselect_event(self, onselect_event, html_calling, typescript_calling):

        # Get the name
        element_name = onselect_event.get_name()

        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} OnSelect Event".format(name=element_name))

        # Interpret, Defining Typescript function and HTML button
        func_and_html_event_node = AngularOnclickType(element_name, type='async')

        # TODO Implement Delete this after test
        func_and_html_event_node.add_statement_into_function_body('console.log(\'Click Activated\');')

        # Build all child
        for _, interaction_flow in onselect_event.get_out_interaction_flow().items():
            self.interpret_interaction_flow(interaction_flow, func_and_html_event_node)

        # Call it to the parent and onclick html named add_onclick
        onclick_html, typescript_function = func_and_html_event_node.render()
        html_calling.add_onclick(onclick_html)

        # Call it to typescript body, and possibly add import node and constructor param to the class
        typescript_calling.body.append(typescript_function)

        for import_node in func_and_html_event_node.needed_import:
            typescript_calling.add_import_statement_using_import_node(import_node)

        for constructor_param in func_and_html_event_node.needed_constructor_param:
            typescript_calling.set_constructor_param(constructor_param)

    # TODO Implement
    def interpret_action_event(self, action_event_element, typescript_call):
        # Get the name
        element_name = action_event_element.get_name()

        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} ActionEvent".format(name=element_name))
        pass

    # TODO Implement
    def interpret_data_binding(self, data_binding_element, html_calling, typescript_calling):
        # Get the name
        element_name = data_binding_element.get_name()

        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} DataBinding".format(name=element_name))
        # Get the classifier
        classifier = self.ifml_symbol_table.lookup(data_binding_element.get_domain_concept()).classifier_symbol

        # Find it in the models container, and use it for declaring Data Binding Property
        intended_model = self.models.get(classifier.id)

        # Interpreting Data Binding
        data_binding_function = DataBindingFunction(element_name, intended_model)

        # Build all Conditional Expression
        for _, conditional_expression in data_binding_element.get_conditional_expressions().items():
            self.interpret_conditional_expression(conditional_expression, data_binding_function.func_decl)

        # Build (If any) Visualization Attribute or Simple Field
        for _, sub_view_component_part in data_binding_element.get_sub_view_component_parts().items():
            if isinstance(sub_view_component_part, VisualizationAttribute):
                self.interpret_visualization_attribute(sub_view_component_part, html_calling, typescript_calling,
                                                       data_binding_function.property_declaration)
            elif isinstance(sub_view_component_part, SimpleField):
                self.interpret_simple_field(sub_view_component_part, html_calling, typescript_calling)
            elif isinstance(sub_view_component_part, ConditionalExpression):
                self.interpret_conditional_expression(sub_view_component_part, data_binding_function.func_decl)

        # Add the import statement
        typescript_calling.add_import_statement_using_import_node(data_binding_function.import_statement)

        # Add the property from Data Binding
        typescript_calling.set_property_decl(data_binding_function.property_declaration)

        # Call the function in the constructor
        typescript_calling.constructor_body.append(data_binding_function.get_function_call())

        # Create the function
        typescript_calling.body.append(data_binding_function.get_function_declaration())

    # TODO Implement
    def interpret_visualization_attribute(self, visualization_attribute_element, html_calling, typescript_calling,
                                          data_binding_property):
        # Get the name
        element_name = visualization_attribute_element.get_name()
        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} VisualizationAttribute".format(name=element_name))

        # Get the structural feature
        structural_feature = self.ifml_symbol_table.lookup(
            visualization_attribute_element.get_feature_concept()).struct_feature_symbol

        # Interpret the notation
        visualization_span = VisualizationWithSpan(element_name, structural_feature.name,
                                                   data_binding_property.variable_name)

        # Append to the HTML
        html_calling.append_html_into_body(visualization_span.render())

    # TODO Implement
    def interpret_simple_field(self, simple_field_element, html_calling, typescript_calling):

        # Get the name and type
        element_name = simple_field_element.get_name()
        uml_model_name, id_of_type = simple_field_element.get_type().split('#')

        # Find the type in the UML Symbol Table
        datatype_of_field = self.uml_symbol_table.lookup(uml_model_name, id_of_type)

        logger_ifml_angular_interpreter.info(
            "Interpreting a {name} SimpleField".format(name=element_name))

        # Check if this field is under the DataBinding
        # TODO Implement

        # Create the Input Field
        input_html = InputField(element_name, datatype_of_field)

        # Call Into the HTML
        html_calling.append_html_into_body(input_html.render())

        # Declare property in class, for ngModel two way biding
        typescript_calling.set_property_decl(input_html.get_ngmodel_property())

    # TODO Implement
    def interpret_conditional_expression(self, conditional_expression_element, data_binding_function_declaration):

        # Get the language and body from the element
        element_name = conditional_expression_element.get_name()
        body = conditional_expression_element.get_body()

        # Append Conditional Expression body into statement inside Data Binding Function
        data_binding_function_declaration.add_statement_to_body(body)

    # TODO Implement
    def interpret_slot(self, view_element_event, html_calling, typescript_calling):
        pass

    # TODO Implement
    def interpret_parameter(self, parameter_element, html_calling, typescript_calling, list_in_direction_parameter):

        # Get element name, and parameter direction
        element_name = parameter_element.get_name()
        direction = parameter_element.get_direction()

        if direction == 'in':
            self.interpret_in_parameter(parameter_element, typescript_calling, list_in_direction_parameter)
        elif direction == 'out':
            self.interpret_out_parameter(parameter_element, html_calling, typescript_calling)
        elif direction == 'inout':
            parameter_element.name = 'in' + element_name
            self.interpret_in_parameter(parameter_element, typescript_calling, list_in_direction_parameter)
            parameter_element.name = 'out' + element_name
            self.interpret_out_parameter(parameter_element, html_calling, typescript_calling)
        else:
            raise TypeError(
                'No Parameter will have {direction} direction, Please verify the validity of your IFML'.format(
                    direction=direction))

    # TODO Implement
    def interpret_in_parameter(self, in_parameter_element, typescript_calling, list_in_direction_parameter):

        # Get element name and type
        element_name = in_parameter_element.get_name()
        uml_name, id_of_symbol = in_parameter_element.get_type().split('#')
        type_used_by_parameter = self.uml_symbol_table.lookup(uml_name, id_of_symbol)

        # If type is class then take the model frommodel container, else just take the string name
        if isinstance(type_used_by_parameter, ClassSymbol):
            type_used_by_parameter = self.models[type_used_by_parameter.id]

        # Creating @Input Property Declaration in child
        input_node = InParameter(element_name, type_used_by_parameter)

        # Declare it in the child typescript, and if the type is class, import the class
        typescript_calling.set_property_decl(input_node.child_property)
        if input_node.needed_import:
            typescript_calling.add_import_statement_using_import_node(input_node.needed_import)

        # Add it into InDirectionInput List at Child Component
        list_in_direction_parameter.append(input_node)

    # TODO Implement
    def interpret_out_parameter(self, out_parameter_calling, child_html_calling, child_typescript_calling):
        # Get element name and type
        element_name = out_parameter_calling.get_name()
        uml_name, id_of_symbol = out_parameter_calling.get_type().split('#')
        type_used_by_parameter = self.uml_symbol_table.lookup(uml_name, id_of_symbol)

        # If type is class then take the model frommodel container, else just take the string name
        if isinstance(type_used_by_parameter, ClassSymbol):
            type_used_by_parameter = self.models[type_used_by_parameter.id]

        # Creating Output Parameter in child
        output_node = OutParameter(element_name, type_used_by_parameter)

        # Declare it in the child typescript, and if the type is class, import the class
        child_typescript_calling.set_property_decl(output_node.property)

        if output_node.needed_import:
            child_typescript_calling.add_import_statement_using_import_node(output_node.needed_import)

    def view_container_definition(self):

        # Defining variable for routing node, intialized if this container have inInteractionFlow or isLandmark
        routing_node = None

        # Prepare Typescript Class
        typescript_class = AngularComponentTypescriptClass()

        # Prepare HTML
        html = AngularComponentHTML()

        return html, typescript_class, routing_node

    def view_component_definition(self):

        html, _, routing_node = self.view_container_definition()
        typescript_class = AngularComponentWithInputTypescriptClass()
        return html, typescript_class, routing_node

    def check_if_there_is_an_interaction_flow(self, element):
        exist = False

        # Check length of array
        in_flow = element.get_in_interaction_flow()
        length = len(in_flow)
        first_element = in_flow[0]

        # If array is not empty and first element is not an empty string
        if length > 0 and len(first_element) > 0:
            exist = True

        return exist

    def build_in_parameter_for_parent(self, call_html, parent_typescript, list_param):

        # TODO Implement
        # This logic is only good for parameter inside form and detail
        # Improve this logic for list
        for param in list_param:

            # Adding the parameter to HTML Call
            call_html.add_parameter_and_property_pair(param.child_property, param.parent_property)

            # Adding needed property for parent component
            parent_typescript.set_property_decl(param.parent_property)

            # Check if the declaration of property need to import a model class
            if param.needed_import:
                parent_typescript.add_import_statement_using_import_node(param.needed_import)

    # TODO Implement
    def interpret_all_action_events(self):
        for action_event in self.action_events:
            print(action_event)

    # TODO Implement
    def interpret_all_view_element_events(self):
        for view_element_event in self.view_element_events:
            view_element_parent_symbol = self.ifml_symbol_table.lookup(
                view_element_event.get_parent_view_element_reference())
            component_node = self.components[view_element_parent_symbol.id]
            if isinstance(view_element_event, OnSelectEvent):
                self.interpret_onselect_event(view_element_event, component_node.component_html,
                                              component_node.component_typescript_class)
            elif isinstance(view_element_event, OnSubmitEvent):
                self.interpret_onsubmit_event(view_element_event, component_node.component_html,
                                              component_node.component_typescript_class)
            elif isinstance(view_element_event, ViewElementEvent):
                self.interpret_view_element_event(view_element_event, component_node.component_html,
                                              component_node.component_typescript_class)


    def interpret_interaction_flow(self, interaction_flow_element, func_and_html_calling):
        if isinstance(interaction_flow_element, NavigationFlow):
            self.interpret_navigation_flow(interaction_flow_element, func_and_html_calling)
        elif isinstance(interaction_flow_element, DataFlow):
            self.interpret_data_flow(interaction_flow_element, func_and_html_calling)

    #TODO Implement
    def interpret_navigation_flow(self, navigation_flow_element, func_and_html_calling):

        #Get element target
        element_target = navigation_flow_element.get_target_interaction_flow_element()
        target_symbol = self.ifml_symbol_table.lookup(element_target)

        if isinstance(target_symbol, ViewContainerSymbol) or isinstance(target_symbol, WindowSymbol):
            self.interaction_with_container_as_target(self.components.get(target_symbol.id), func_and_html_calling)
        elif isinstance(target_symbol, ActionSymbol):
            self.interaction_with_action_as_target(self.services.get(target_symbol.id), func_and_html_calling)

    #TODO Implement
    def interaction_with_container_as_target(self, container_node, function_and_html_of_event):

        if isinstance(container_node, AngularComponentForModal):
            self.route_to_component_modal(container_node, function_and_html_of_event)
        elif isinstance(container_node, AngularComponent):
            self.route_to_component_page(container_node, function_and_html_of_event)

    #TODO implement
    def route_to_component_page(self, component_page_node, function_and_html_of_event):

        #Get routing path of that page
        route_path_from_root = component_page_node.get_routing_path()

        #Build the param binding group

        #Creating statement for navigation into page
        router_statement = RouteToComponentPage(route_path_from_root)

        #Append to the event function handler
        function_and_html_of_event.add_statement_into_function_body(router_statement.render())

    #TODO Implement, improve this logic
    def route_to_component_modal(self, component_modal_node, function_and_html_of_event):
        # Get modal identifier for that page
        modal_identifier = component_modal_node.modal_identifier

        #Add Open Modal Statement and import ngxmodal service
        modal_handler_template = AngularModalButtonAndFunction(modal_identifier, 'async')
        modal_handler_template.set_target_modal(modal_identifier)

        # Build the param binding group

        #Append to the event function handler. add import and constructor param
        function_and_html_of_event.add_needed_import(modal_handler_template.import_ngx_modal_service_node)
        function_and_html_of_event.add_needed_constructor_param(modal_handler_template.ngx_service_constructor)
        function_and_html_of_event.add_statements_into_function_body(modal_handler_template.function_node.function_body)

    #TODO Implement
    def interaction_with_action_as_target(self, service_node, function_and_html_of_event):
        pass

    # TODO Implement
    def interpret_data_flow(self, data_flow_element, func_and_html_calling):

        # Get element target
        element_target = data_flow_element.get_target_interaction_flow_element()
        pass

    # TODO Implement
    def interpret_domain_model(self):
        # Build all Class used
        for _, class_xmi in self.root_class_diagram_xmi.get_classes().items():
            self.interpret_uml_class(class_xmi)

    def interpret_uml_class(self, class_xmi):
        # Get class name
        element_name = class_xmi.get_model_name()

        # Interpret it
        model_from_class = ModelFromUMLClass(element_name)

        # Build the owned attribute
        for _, attribute in class_xmi.get_properties().items():
            self.interpret_owned_attribute(attribute, model_from_class)

        # TODO Implement
        # Build the owned operation

        # Register to models container
        self.models[class_xmi.get_model_id()] = model_from_class

    def interpret_owned_attribute(self, class_attribute_xmi, model_element):
        # Get attribute name, and type of the attribute
        element_name = class_attribute_xmi.get_model_name()
        id_of_type_symbol = class_attribute_xmi.get_type()
        uml_filename = self.root_class_diagram_xmi.get_filename()
        element_type = self.uml_symbol_table.lookup(uml_filename, id_of_type_symbol).name

        # Interpret it
        model_element.add_owned_attribute_to_class(element_name, element_type)
