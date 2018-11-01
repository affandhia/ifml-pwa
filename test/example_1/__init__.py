from main.core.angular.main import generate_project
import logging
from ifml_parser.ifmlxmiparser import parse
from custom_xmi_parser.xmiparser_2 import parse as uml_parse
logging.basicConfig(level=logging.DEBUG)

#target_structure = {"generated-angular-python": default_structure}

#generate_project('movies.core','movies.xmi',"/Users/hafiyyansayyidfadhlillah/generated-pwa/")
generate_project('abs_bankaccount.core','abs_bankaccount.uml', target_directory="D:\\testing", enable_login=True)

#uml_movies, uml_symbol_table = uml_parse('movies.uml')
#ifml_movies, ifml_symbol_table = parse(xmiFileName='practice_2.core', umlSymbolTable=uml_symbol_table)
#print(symbol_table.table)

#print('-------------')
#print(ifml_movies.get_domain_model())
#print('-------------')
#print(uml_movies.get_classes()['_Gt2cYE7REeSt-rUToYoH4A'].get_properties())


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

