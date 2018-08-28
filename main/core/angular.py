import logging
import sys
logger_angular = logging.getLogger("core.angular")

def generate_project(path_to_ifml_file, path_to_class_diagram, target_directory=''):
    ifml = open(path_to_ifml_file, "rt")
    class_diagram = open(path_to_class_diagram, "rt")
    target_project_directory = sys.path[0] if target_directory == '' else target_directory
    logger_angular.debug('Target directory is '+target_project_directory)

if __name__ == '__main__':
    print('\n'.join(sys.path))