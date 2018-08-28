from main.utils.project_generator import create_structure
from main.template.project_structure.angular_strcture import default_structure

target_structure = {"generated-angular-python": default_structure}

create_structure(target_structure,"D:/testing/")
