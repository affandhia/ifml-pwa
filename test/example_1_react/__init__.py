import sys
import logging

sys.path.append('/Users/affandhia/Documents/Affan/skripsi/ifml-angular-pwa')

from main.core.react.main import generate_project

logging.basicConfig(level=logging.DEBUG)

generate_project('abs_bankaccount.core', 'abs_bankaccount.uml',
                 target_directory="./result", enable_login=True,
                 remove_folder_content=True)
