import logging
import sys
import shutil
import os
import json

from custom_xmi_parser.xmiparser_2 import parse as uml_parse
from ifml_parser.ifmlxmiparser import parse as ifml_parse
from main.core.react.interpreter.base import IFMLtoReactInterpreter
from main.core.react.project_writer import ReactProject
from main.utils.project_generator import create_structure

logger_react = logging.getLogger("main.core.react.main")


# receive two required params: ifml file & uml, others two: generated web, enable login
def generate_project(path_to_ifml_file, path_to_class_diagram,
                     target_directory='', enable_login=False,
                     remove_folder_content=False):
    # handle output folder
    target_project_directory = sys.path[
        0] if target_directory == '' else target_directory

    if remove_folder_content:
        shutil.rmtree(target_project_directory,
                      ignore_errors=True)
        os.mkdir(target_project_directory)

    # parse uml, the data is supposed to be related with UI, because of ifml has no relation of each UI so we use the UML
    # the output will be used to generate the IFML [SKIP]
    uml_structure, uml_symbol_table = uml_parse(path_to_class_diagram)

    # parse ifml by using the relation provided by the UML [SKIP]
    ifml_structure, ifml_symbol_table = ifml_parse(path_to_ifml_file,
                                                   uml_symbol_table)

    # the result of those two parser will be used to generate the angular
    interpreting_result = IFMLtoReactInterpreter(
        ifml_structure,
        ifml_symbol_table,
        uml_structure,
        uml_symbol_table,
        enable_authentication_guard=enable_login
    )

    basic_template = ReactProject(
        app_name=interpreting_result.get_project_name())

    # Adding app.component.ts
    root_component_name = 'app'
    root_class_name = 'App'

    # Angular Typescript Component for root component
    basic_template.add_default_app_component(
        interpreting_result.root_eseight_class.render())
    # basic_template.add_app_html_template(
    #     interpreting_result.root_html.render())

    # # Defining Angular Main Module
    # basic_app_module = AngularMainModule(app_name=interpreting_result.get_project_name())

    # # Adding basic Routing Module
    # basic_routing = AngularDefaultRouterDefinition()
    # basic_routing.add_routing_hierarchy(interpreting_result.angular_routing)
    #
    # # Adding service worker config
    # basic_template.write_service_worker_config(interpreting_result.list_service_worker_config)
    #
    # # Adding each service into the AngularProject
    # for _, model_node in interpreting_result.models.items():
    #     basic_template.add_model_inside_models_folder(model_node.render())
    #
    # # Adding each component of interpreting into the AngularProject
    # for _, component_node in interpreting_result.components.items():
    #     # Insert the component into main module
    #     basic_app_module.add_component_to_module(component_node)
    #
    #     # Importing all component to the routing node
    #     basic_routing.register_component_with_router(component_node)
    #
    #     # Insert the component definition into src folder
    #     basic_template.add_new_component_using_basic_component_folder(component_node.build())
    #
    # # Adding each service into the AngularProject
    # for _, service_node in interpreting_result.services.items():
    #     # Insert the service into the services folder
    #     basic_template.add_service_inside_services_folder(service_node.render())
    #
    # # If user wants the predefined login to be used, then it will generate the predefined Authentication by Google
    # if enable_login:
    #     basic_app_module.enable_authentication_service()
    #     basic_template.enable_authentication_service()
    #     basic_routing.enable_authentication_service()
    #
    # # Adding App Module
    # basic_template.add_app_module_file(basic_app_module.render())
    #
    # basic_template.add_app_module_routing(basic_routing.render())

    logger_react.debug(
        json.dumps(basic_template.return_project_structure(), sort_keys=True,
                   indent=4))

    create_structure(basic_template.return_project_structure(),
                     target_directory)
    logger_react.info(
        'React PWA Project successfully generated at ' + target_directory)
    return
    ###################################
