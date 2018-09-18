from main.core.angular.main import generate_project
from main.template.project_structure.angular_strcture import default_structure
from main.utils.jinja.angular import base_file_writer
from ifml_parser.ifmlxmiparser import parse
import logging

logging.basicConfig(level=logging.DEBUG)

#target_structure = {"generated-angular-python": default_structure}

#generate_project('test1.txt','test2.txt',"/Users/hafiyyansayyidfadhlillah/generated-pwa/")

ifml_movies = parse('movies.core')

print(ifml_movies.get_list_interaction_flow_model()['_740hok7SEeSvsr3-_MjFew'].get_interaction_flow_model_elements())