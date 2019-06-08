import sys
import logging
import coloredlogs

logger_level = logging.DEBUG

logging.basicConfig(stream=sys.stdout, level=logger_level)
coloredlogs.install(level=logging._checkLevel(logger_level))

sys.path.append('/Users/affandhia/Documents/Affan/skripsi/ifml-angular-pwa')

from main.core.react.main import generate_project

client_id =\
    '588654354409-365mn3hbjvam5jp7ggnl7578ssp6otpi.apps.googleusercontent.com'

generate_project('abs_bankaccount.core', 'abs_bankaccount.uml',
                 target_directory="./result", enable_login=True,
                 remove_folder_content=True, google_client_id=client_id)
