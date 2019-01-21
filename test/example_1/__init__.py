from main.core.angular.main import generate_project
import logging
from ifml_parser.ifmlxmiparser import parse
from custom_xmi_parser.xmiparser_2 import parse as uml_parse
logging.basicConfig(level=logging.DEBUG)

generate_project('abs_bankaccount.core','abs_bankaccount.uml', target_directory="D:\\results", enable_login=True)