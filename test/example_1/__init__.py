from main.core.angular.main import generate_project
from main.template.project_structure.angular_strcture import default_structure
from main.utils.jinja.angular import base_file_writer

import logging

logging.basicConfig(level=logging.DEBUG)

#target_structure = {"generated-angular-python": default_structure}

generate_project('test1.txt','test2.txt',"D:/testing/")