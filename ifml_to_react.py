import sys
import logging
import coloredlogs
import os

logger_level = logging.DEBUG

logging.basicConfig(stream=sys.stdout, level=logger_level)
coloredlogs.install(level=logging._checkLevel(logger_level))

from main.core.react.main import generate_project

client_id = '588654354409-365mn3hbjvam5jp7ggnl7578ssp6otpi.apps.googleusercontent.com'

ifml_file = 'abs_bankaccount.core'

uml_file = 'abs_bankaccount.uml'

generate_project(ifml_file, uml_file,
                 target_directory='result', enable_login=True,
                 remove_folder_content=True, google_client_id=client_id)
