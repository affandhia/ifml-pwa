import logging
import sys

from custom_xmi_parser.xmiparser_2 import parse as uml_parse
from ifml_parser.ifmlxmiparser import parse as ifml_parse
from main.core.angular.interpreter.base import IFMLtoAngularInterpreter
from main.core.angular.project_writer import AngularProject
from main.utils.ast.framework.angular.base import AngularMainModule
from main.utils.ast.framework.angular.routers import AngularDefaultRouterDefinition
from main.utils.project_generator import create_structure

logger_angular = logging.getLogger("main.core.angular.main")


def generate_project(path_to_ifml_file, path_to_class_diagram, target_directory='', enable_login=False):
    target_project_directory = sys.path[0] if target_directory == '' else target_directory
    uml_structure, uml_symbol_table = uml_parse(path_to_class_diagram)
    ifml_structure, ifml_symbol_table = ifml_parse(path_to_ifml_file, uml_symbol_table)
    interpreting_result = IFMLtoAngularInterpreter(ifml_structure, ifml_symbol_table, uml_structure, uml_symbol_table,
                                                   enable_authentication_guard=enable_login)
    basic_template = AngularProject(app_name=interpreting_result.get_project_name())

    # Adding app.component.ts
    root_component_name = 'app'
    root_class_name = 'App'

    # Angular Typescript Component for root component
    basic_template.add_default_app_component(interpreting_result.root_typescript_class.render())
    basic_template.add_app_html_template(interpreting_result.root_html.render())

    # Defining Angular Main Module
    basic_app_module = AngularMainModule(app_name=interpreting_result.get_project_name())

    # Adding basic Routing Module
    basic_routing = AngularDefaultRouterDefinition()
    basic_routing.add_routing_hierarchy(interpreting_result.angular_routing)

    # Adding service worker config
    basic_template.write_service_worker_config(interpreting_result.list_service_worker_config)

    # Adding each service into the AngularProject
    for _, model_node in interpreting_result.models.items():
        basic_template.add_model_inside_models_folder(model_node.render())

    # Adding each component of interpreting into the AngularProject
    for _, component_node in interpreting_result.components.items():
        # Insert the component into main module
        basic_app_module.add_component_to_module(component_node)

        # Importing all component to the routing node
        basic_routing.register_component_with_router(component_node)

        # Insert the component definition into src folder
        basic_template.add_new_component_using_basic_component_folder(component_node.build())

    # Adding each service into the AngularProject
    for _, service_node in interpreting_result.services.items():
        # Insert the service into the services folder
        basic_template.add_service_inside_services_folder(service_node.render())

    # If user wants the predefined login to be used, then it will generate the predefined Authentication by Google
    if enable_login:
        basic_app_module.enable_authentication_service()
        basic_template.enable_authentication_service()
        basic_routing.enable_authentication_service()

    # Adding App Module
    basic_template.add_app_module_file(basic_app_module.render())

    basic_template.add_app_module_routing(basic_routing.render())
    # print(basic_template.return_project_structure())
    #create_structure(basic_template.return_project_structure(), target_directory)
    logger_angular.info('Angular PWA Project successfully generated at ' + target_directory)
