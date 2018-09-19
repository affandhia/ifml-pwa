import logging
import sys

from custom_xmi_parser.xmiparser_2 import parse as uml_parse
from ifml_parser.ifmlxmiparser import parse as ifml_parse
from main.core.angular.interpreter.base import IFMLtoAngularInterpreter
from main.core.angular.project_writer import AngularProject
from main.utils.project_generator import create_structure
from main.utils.ast.framework.angular.base import AngularMainModule
from main.utils.ast.framework.angular.components import AngularComponentTypescriptClass
from main.utils.ast.framework.angular.routers import AngularDefaultRouterDefinition
from main.utils.jinja.angular import base_file_writer

logger_angular = logging.getLogger("main.core.angular.main")


def generate_project(path_to_ifml_file, path_to_class_diagram, target_directory=''):
    ifml = open(path_to_ifml_file, "rt")
    class_diagram = open(path_to_class_diagram, "rt")
    target_project_directory = sys.path[0] if target_directory == '' else target_directory



    ifml_interpreter = IFMLtoAngularInterpreter(ifml_xmi=ifml_parse(path_to_ifml_file),
                                                class_diagram_xmi=uml_parse(path_to_class_diagram))
    '''
    basic_template = AngularProject()

    # Adding App Module
    basic_app_module = AngularMainModule(app_name='generated-pwa')
    basic_template.add_app_module_file(basic_app_module.render())

    # Adding basic Routing Module
    basic_routing = AngularDefaultRouterDefinition()
    basic_template.add_app_module_routing(basic_routing.render())

    # Adding app.component.ts
    root_component_name = 'app'
    root_class_name = 'App'

    # Angular Typescript Component for root component
    root_ts_class = AngularComponentTypescriptClass()
    root_ts_class.component_name = root_component_name
    root_ts_class.class_name = root_class_name
    root_ts_class.selector_name = root_component_name + '-root'
    basic_template.add_default_app_component(root_ts_class.render())

    root_html = base_file_writer('src/app/app.component.html.template')
    basic_template.add_app_html_template(root_html)

    create_structure(basic_template.return_project_structure(), target_directory)
    logger_angular.debug('Target directory is ' + target_directory)
    '''


def write_base_project_content(ifml, class_diagram, target_directory, default_structure):
    pass
