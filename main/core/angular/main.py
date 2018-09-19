import logging
import sys
from main.utils.project_generator import create_structure
from main.core.angular.project_writer import AngularProject
from main.utils.ast.framework.angular.base import AngularMainModule
from main.utils.ast.framework.angular.routers import AngularDefaultRouterDefinition

logger_angular = logging.getLogger("core.angular")

def generate_project(path_to_ifml_file, path_to_class_diagram, target_directory=''):
    ifml = open(path_to_ifml_file, "rt")
    class_diagram = open(path_to_class_diagram, "rt")
    target_project_directory = sys.path[0] if target_directory == '' else target_directory
    basic_template = AngularProject()

    #Adding App Module
    basic_app_module = AngularMainModule(app_name='generated-pwa')
    basic_template.add_app_module_file(basic_app_module.render())

    #Adding basic Routing Module
    basic_routing = AngularDefaultRouterDefinition()
    basic_template.add_app_module_routing(basic_routing.render())

    create_structure(basic_template.return_project_structure(), target_directory)
    logger_angular.debug('Target directory is ' + target_directory)

def write_base_project_content(ifml, class_diagram, target_directory, default_structure):
    pass



