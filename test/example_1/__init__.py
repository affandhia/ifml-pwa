from main.core.angular.main import generate_project
from main.template.project_structure.angular_strcture import default_structure
from main.utils.jinja.angular import base_file_writer
from ifml_parser.ifmlxmiparser import parse
from custom_xmi_parser.xmiparser_2 import parse as uml_parse
from main.utils.ast.framework.angular import AngularComponent, AngularComponentTypescriptClass, AngularComponentHTML
import logging

logging.basicConfig(level=logging.DEBUG)

#target_structure = {"generated-angular-python": default_structure}

generate_project('test1.txt','test2.txt',"/Users/hafiyyansayyidfadhlillah/generated-pwa/")

'''
ifml_movies = parse('movies.core')
uml_movies = uml_parse('movies.xmi')

print(ifml_movies.get_list_interaction_flow_model()['_740hok7SEeSvsr3-_MjFew'].get_interaction_flow_model_elements())
print('-------------')
print(uml_movies.get_classes()['_Gt2cYE7REeSt-rUToYoH4A'].get_properties())
'''

'''
component_name = 'coba'
class_name = 'Coba'
selector_name = 'app-coba'
constructor = 'constructor(){}'

first_typescript_component = AngularComponentTypescriptClass()
first_typescript_component.component_name = component_name
first_typescript_component.class_name = class_name
first_typescript_component.selector_name = selector_name
first_typescript_component.constructor = constructor

first_html_component = AngularComponentHTML()

first_component = AngularComponent(component_name='coba', component_typescript_class=first_typescript_component, component_html=first_html_component)

print(first_component.build())
'''

