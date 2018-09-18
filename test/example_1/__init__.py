from main.core.angular.main import generate_project
from main.template.project_structure.angular_strcture import default_structure
from main.utils.jinja.angular import base_file_writer
from ifml_parser.ifmlxmiparser import parse
from custom_xmi_parser.xmiparser_2 import parse as uml_parse
from main.utils.ast.framework.angular import AngularComponent
import logging

logging.basicConfig(level=logging.DEBUG)

#target_structure = {"generated-angular-python": default_structure}

#generate_project('test1.txt','test2.txt',"/Users/hafiyyansayyidfadhlillah/generated-pwa/")

'''
ifml_movies = parse('movies.core')
uml_movies = uml_parse('movies.xmi')

print(ifml_movies.get_list_interaction_flow_model()['_740hok7SEeSvsr3-_MjFew'].get_interaction_flow_model_elements())
print('-------------')
print(uml_movies.get_classes()['_Gt2cYE7REeSt-rUToYoH4A'].get_properties())
'''

first_component = AngularComponent()
first_component.component_name = 'coba'
first_component.class_name = 'Coba'
first_component.selector_name = 'app-coba'
first_component.constructor = 'constructor(){}'

print(first_component.render())
