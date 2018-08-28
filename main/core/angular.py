import logging
import sys
from main.template.project_structure.angular_strcture import default_structure
from main.utils.project_generator import create_structure
logger_angular = logging.getLogger("core.angular")

def generate_project(path_to_ifml_file, path_to_class_diagram, target_directory=''):
    ifml = open(path_to_ifml_file, "rt")
    class_diagram = open(path_to_class_diagram, "rt")
    target_project_directory = sys.path[0] if target_directory == '' else target_directory
    create_structure(default_structure,target_project_directory)
    logger_angular.debug('Target directory is '+target_project_directory)