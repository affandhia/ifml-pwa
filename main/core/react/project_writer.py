from main.template.project_structure.react_structure import default_structure
from main.utils.jinja.react import base_file_writer
from main.utils.naming_management import camel_classify


class ReactProject(object):
    APP_FOLDER_KEY = 'App'
    SRC_FOLDER_KEY = 'src'
    PUBLIC_FOLDER_KEY = 'public'
    SERVICES_KEY = 'services'

    INDEX_KEY = 'index.js'
    PACKAGE_KEY = 'package.json'
    README_KEY = 'README.md'
    APP_COMPONENT_KEY = 'App.js'

    def __init__(self, app_name, structure=None, google_client_id=''):
        self.app_name = app_name
        self.project_structure = \
            default_structure if structure is None else structure
        self.app_folder = self.project_structure[self.SRC_FOLDER_KEY]
        self.services_folder = self.app_folder[self.SERVICES_KEY]
        self.google_client_id = google_client_id
        self.write_base_angular_project_file()

    def get_app_name(self):
        return self.app_name

    def write_base_angular_project_file(self):
        self.write_index()
        self.write_package_dependencies()
        self.write_readme()
        self.write_env()
        self.write_manifest()
        self.write_index_html()

    def write_index(self):
        self.project_structure[self.SRC_FOLDER_KEY][self.INDEX_KEY] = \
            base_file_writer(
                [
                    self.SRC_FOLDER_KEY,
                    self.INDEX_KEY + '.template'
                ])

    def write_package_dependencies(self):
        self.project_structure[self.PACKAGE_KEY] = base_file_writer(
            self.PACKAGE_KEY + '.template', app_name=self.get_app_name())

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
                "Authentication": {
                    "index.js": "main/template/file/react/assets/src/Authentication"
                }
            }

            self.project_structure[self.SRC_FOLDER_KEY].update(auth_modules)

    def return_project_structure(self):
        return {self.app_name: self.project_structure}

    def write_env(self):
        self.project_structure['.env'] = base_file_writer(
            '.env.template',
            google_client_id=self.google_client_id)

    def write_manifest(self):
        self.project_structure[self.PUBLIC_FOLDER_KEY][
            'manifest.json'] = base_file_writer(
            [self.PUBLIC_FOLDER_KEY, 'manifest.json.template'],
            app_name=camel_classify(self.get_app_name())
        )

    def write_index_html(self):
        self.project_structure[self.PUBLIC_FOLDER_KEY][
            'index.html'] = base_file_writer(
            [self.PUBLIC_FOLDER_KEY, 'index.html.template'],
            app_name=self.get_app_name(),
            google_client_id=self.google_client_id
        )
