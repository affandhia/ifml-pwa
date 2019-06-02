import sys
import shutil
import os
import json

from custom_xmi_parser.xmiparser_2 import parse as uml_parse
from ifml_parser.ifmlxmiparser import parse as ifml_parse
from main.core.react.interpreter.base import IFMLtoReactInterpreter
from main.core.react.project_writer import ReactProject
from main.utils.logger_generator import get_logger
from main.utils.project_generator import create_structure

logger_react = get_logger()


# receive two required params: ifml file & uml, others two: generated web,
# enable login
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

    # parse uml, the data is supposed to be related with UI, because of ifml
    # has no relation of each UI so we use the UML the output will be used
    # to generate the IFML [SKIP]
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

    basic_template.add_auth_modules_if_needed(enable_login)

    # Adding app.component.ts
    root_component_name = 'app'
    root_class_name = 'App'

    interpreting_result.root_eseight_class.set_component_selector_class_name(
        root_class_name)

    # Component for root component
    app_node = interpreting_result.root_react_node.build()
    basic_template.add_default_app_component(app_node)

    # Adding each component of interpreting into the Structure
    for _, component_node in interpreting_result.components.items():
        # Insert the component definition into src folder
        basic_template.add_new_component_using_basic_component_folder(
            component_node.build())

    # Adding each service into the AngularProject
    for _, service_node in interpreting_result.services.items():
        # Insert the service into the services folder
        basic_template.add_service_inside_services_folder(
            service_node.render())

    # logger_react.debug(
    #     json.dumps(basic_template.return_project_structure(), sort_keys=True,
    #                indent=4))

    project_structure_final = basic_template.return_project_structure()

    create_structure(project_structure_final,
                     target_directory)
    logger_react.info(
        'React PWA Project successfully generated at ' + target_directory)
