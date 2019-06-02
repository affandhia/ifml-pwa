from main.template.project_structure.react_structure import default_structure
from main.utils.jinja.react import base_file_writer


class ReactProject(object):
    APP_FOLDER_KEY = 'App'
    SRC_FOLDER_KEY = 'src'
    SERVICES_KEY = 'services'

    INDEX_KEY = 'index.js'
    PACKAGE_KEY = 'package.json'
    README_KEY = 'README.md'
    APP_COMPONENT_KEY = 'App.js'

    def __init__(self, app_name, structure=None):
        self.app_name = app_name
        self.project_structure = \
            default_structure if structure is None else structure
        self.app_folder = self.project_structure[self.SRC_FOLDER_KEY]
        self.services_folder = self.app_folder[self.SERVICES_KEY]

        self.write_base_angular_project_file()

    def get_app_name(self):
        return self.app_name

    def write_base_angular_project_file(self):
        self.write_index()
        self.write_package_dependencies()
        self.write_readme()

    def write_index(self):
        self.project_structure[self.SRC_FOLDER_KEY][self.INDEX_KEY] = \
            base_file_writer(
                [
                    self.SRC_FOLDER_KEY,
                    self.INDEX_KEY + '.template'
                ])

    def write_package_dependencies(self):
        self.project_structure[self.PACKAGE_KEY] = base_file_writer(
            self.PACKAGE_KEY + '.template')

    def write_readme(self):
        self.project_structure[self.README_KEY] = base_file_writer(
            self.README_KEY + '.template')

    def add_default_app_component(self, app_component):
        self.app_folder.update(app_component)

    def add_new_component_using_basic_component_folder(
            self,
            inserted_component_folder):
        self.app_folder.update(inserted_component_folder)

    def add_service_inside_services_folder(self, inserted_service_file):
        self.services_folder.update(inserted_service_file)

    def add_auth_modules_if_needed(self, auth_enabled: bool):
        """
        Import necessary modules for authentication purpose.

        :param auth_enabled: the status whether authentication is enabled or not
        :return: None
        """
        if auth_enabled:
            auth_modules = {
                "utils": {
                    "token.js": "main/template/file/react/assets/src/utils",
                    "environment.js": "main/template/file/react/assets/src/utils"
                },
                "containers": {
                    "Authentication": {
                        "index.js": "main/template/file/react/assets/src/containers/Authentication"
                    }
                }
            }

            self.project_structure[self.SRC_FOLDER_KEY].update(auth_modules)

    def return_project_structure(self):
        return {self.app_name: self.project_structure}
