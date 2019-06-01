# this file is supposed to be used as a project initializer

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
        #     self.write_editor_config()
        #     self.write_gitignore()
        #     self.write_angular_settings()
        self.write_package_dependencies()
        self.write_readme()

    #     self.write_express_server()
    #     self.write_tsconfig_and_linter()
    #     self.write_src_test_template()
    #     self.write_global_style()
    #     self.write_polyfills()
    #     self.write_manifest()
    #     self.write_main_ts()
    #     self.write_karma_configuration()
    #     self.write_index()
    #     self.write_env_production()
    #     self.write_env_development()
    #     self.write_e2e_tsconfig()
    #     self.write_e2e_protractor()
    #     self.write_e2e_protractor_definition()
    #     self.write_e2e_spec_definition()
    #     self.enable_authentication_service()
    #     self.write_build_and_run_script()
    #

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

    # def write_editor_config(self):
    #     self.project_structure[self.EDITOR_CONFIG_KEY] = base_file_writer(self.EDITOR_CONFIG_KEY + '.template')
    #
    # def write_gitignore(self):
    #     self.project_structure[self.GITIGNORE_KEY] = base_file_writer(self.GITIGNORE_KEY + '.template')
    #
    # def write_angular_settings(self):
    #     self.project_structure[self.ANGULAR_KEY] = base_file_writer(self.ANGULAR_KEY + '.template',
    #                                                                 app_name=self.app_name)
    #
    # def write_service_worker_config(self, list_of_config):
    #     self.project_structure[self.NGSW_KEY] = base_file_writer(self.NGSW_KEY + '.template',
    #                                                              app_name=self.app_name,
    #                                                              data_config=','.join(list_of_config))
    #
    # def write_package_dependencies(self):
    #     self.project_structure[self.PACKAGE_KEY] = base_file_writer(self.PACKAGE_KEY + '.template',
    #                                                                 app_name=self.app_name)
    #
    # def write_readme(self):
    #     self.project_structure[self.README_KEY] = base_file_writer(self.README_KEY + '.template',
    #                                                                app_name=self.app_name)
    #
    # def write_express_server(self):
    #     self.project_structure[self.SERVER_KEY] = base_file_writer(self.SERVER_KEY + '.template',
    #                                                                app_name=self.app_name)
    #
    # def write_tsconfig_and_linter(self):
    #     self.project_structure[self.TSCONFIG_KEY] = base_file_writer(self.TSCONFIG_KEY + '.template')
    #     self.project_structure[self.TSLINT_KEY] = base_file_writer(self.TSLINT_KEY + '.template')
    #     self.project_structure[self.SRC_FOLDER_KEY][self.TSLINT_KEY] = base_file_writer(
    #         self.SRC_FOLDER_KEY + '/' + self.TSLINT_KEY + '.template')
    #     self.project_structure[self.SRC_FOLDER_KEY][self.TSCONFIG_SPEC_KEY] = base_file_writer(
    #         self.SRC_FOLDER_KEY + '/' + self.TSCONFIG_SPEC_KEY + '.template')
    #     self.project_structure[self.SRC_FOLDER_KEY][self.TSCONFIG_APP_KEY] = base_file_writer(
    #         self.SRC_FOLDER_KEY + '/' + self.TSCONFIG_APP_KEY + '.template')
    #
    # def write_src_test_template(self):
    #     self.project_structure[self.SRC_FOLDER_KEY][self.TEST_TS_KEY] = base_file_writer(
    #         self.SRC_FOLDER_KEY + '/' + self.TEST_TS_KEY + '.template')
    #
    # def write_global_style(self, content=None):
    #     self.project_structure[self.SRC_FOLDER_KEY][
    #         self.GLOBAL_STYLE_KEY] = '/* Style Here */\n@import \"~ngx-smart-modal/ngx-smart-modal.css\";' if content == None else content
    #
    # def write_polyfills(self):
    #     self.project_structure[self.SRC_FOLDER_KEY][self.POLYFILLS_KEY] = base_file_writer(
    #         self.SRC_FOLDER_KEY + '/' + self.POLYFILLS_KEY + '.template')
    #
    # def write_manifest(self):
    #     self.project_structure[self.SRC_FOLDER_KEY][self.MANIFEST_KEY] = base_file_writer(
    #         self.SRC_FOLDER_KEY + '/' + self.MANIFEST_KEY + '.template', app_name=self.app_name)
    #
    # def write_main_ts(self):
    #     self.project_structure[self.SRC_FOLDER_KEY][self.MAIN_TS_KEY] = base_file_writer(
    #         self.SRC_FOLDER_KEY + '/' + self.MAIN_TS_KEY + '.template')
    #
    # def write_karma_configuration(self):
    #     self.project_structure[self.SRC_FOLDER_KEY][self.KARMA_CONF_KEY] = base_file_writer(
    #         self.SRC_FOLDER_KEY + '/' + self.KARMA_CONF_KEY + '.template')
    #
    # def write_index(self):
    #     self.project_structure[self.SRC_FOLDER_KEY][self.INDEX_HTML_KEY] = base_file_writer(
    #         self.SRC_FOLDER_KEY + '/' + self.INDEX_HTML_KEY + '.template', app_name=self.app_name)
    #
    # def write_browserlist(self):
    #     self.project_structure[self.SRC_FOLDER_KEY][self.BROWSERLIST_KEY] = base_file_writer(
    #         self.SRC_FOLDER_KEY + '/' + self.BROWSERLIST_KEY + '.template')
    #
    # def write_env_production(self, content=None):
    #     self.project_structure[self.SRC_FOLDER_KEY][self.ENV_FOLDER_KEY][self.ENV_PROD_KEY] = base_file_writer(
    #         self.SRC_FOLDER_KEY + '/' + self.ENV_FOLDER_KEY + '/' + self.ENV_PROD_KEY + '.template')
    #
    # def write_env_development(self, content=None):
    #     self.project_structure[self.SRC_FOLDER_KEY][self.ENV_FOLDER_KEY][self.ENV_DEV_KEY] = base_file_writer(
    #         self.SRC_FOLDER_KEY + '/' + self.ENV_FOLDER_KEY + '/' + self.ENV_DEV_KEY + '.template')
    #
    # def write_e2e_tsconfig(self):
    #     self.project_structure[self.E2E_KEY][self.E2E_TSCONFIG_KEY] = base_file_writer(
    #         self.E2E_KEY + '/' + self.E2E_TSCONFIG_KEY + '.template')
    #
    # def write_e2e_protractor(self):
    #     self.project_structure[self.E2E_KEY][self.E2E_PROTRACTOR_KEY] = base_file_writer(
    #         self.E2E_KEY + '/' + self.E2E_PROTRACTOR_KEY + '.template')
    #
    # def write_e2e_protractor_definition(self):
    #     self.project_structure[self.E2E_KEY][self.SRC_FOLDER_KEY][self.E2E_PO_KEY] = base_file_writer(
    #         self.E2E_KEY + '/' + self.SRC_FOLDER_KEY + '/' + self.E2E_PO_KEY + '.template')
    #
    # def write_e2e_spec_definition(self):
    #     self.project_structure[self.E2E_KEY][self.SRC_FOLDER_KEY][self.E2E_SPEC_KEY] = base_file_writer(
    #         self.E2E_KEY + '/' + self.SRC_FOLDER_KEY + '/' + self.E2E_SPEC_KEY + '.template')
    #
    #
    def add_default_app_component(self, app_component):
        self.app_folder.update(app_component)

    #
    # def add_app_module_routing(self, app_routing_file):
    #     self.app_folder[self.APP_ROUTING_KEY] = app_routing_file
    #
    # def add_app_module_file(self, app_module_file):
    #     self.app_folder[self.APP_MODULE_KEY] = app_module_file
    #
    def add_new_component_using_basic_component_folder(self,
                                                       inserted_component_folder):
        self.app_folder.update(inserted_component_folder)

    #
    def add_service_inside_services_folder(self, inserted_service_file):
        self.services_folder.update(inserted_service_file)
    #
    # def add_model_inside_models_folder(self, inserted_model_file):
    #     self.models_folder.update(inserted_model_file)
    #
    # def enable_authentication_service(self):
    #     # Adding Auth Guard
    #     content_of_auth_guard = base_file_writer(
    #         self.SRC_FOLDER_KEY + '/' + self.APP_KEY + '/' + self.GUARD_KEY + '/' + self.AUTH_GUARD_KEY + '.template')
    #     self.app_folder.update({self.GUARD_KEY: {self.AUTH_GUARD_KEY: content_of_auth_guard}})
    #
    # def write_build_and_run_script(self):
    #
    #     #Build Script
    #     self.project_structure[self.BUILD_SCRIPT_KEY+'.bat'] = base_file_writer(self.BUILD_SCRIPT_KEY+'.bat.template', app_name=self.app_name)
    #     self.project_structure[self.BUILD_SCRIPT_KEY+'.sh'] = base_file_writer(self.BUILD_SCRIPT_KEY + '.sh.template', app_name=self.app_name)
    #
    #     #Run Script
    #     self.project_structure[self.RUN_SCRIPT_KEY + '.bat'] = base_file_writer(
    #         self.RUN_SCRIPT_KEY + '.bat.template', app_name=self.app_name)
    #     self.project_structure[self.RUN_SCRIPT_KEY + '.sh'] = base_file_writer(self.RUN_SCRIPT_KEY + '.sh.template', app_name=self.app_name)
    #

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


class AngularProject(object):
    SRC_FOLDER_KEY = 'src'
    ENV_FOLDER_KEY = 'environments'
    E2E_KEY = 'e2e'
    APP_KEY = 'app'
    SERVICES_KEY = 'services'
    MODELS_KEY = 'models'
    GUARD_KEY = 'guard'
    LOGIN_KEY = 'login'

    BUILD_SCRIPT_KEY = 'build'
    RUN_SCRIPT_KEY = 'run'
    EDITOR_CONFIG_KEY = '.editorconfig'
    GITIGNORE_KEY = '.gitignore'
    ANGULAR_KEY = 'angular.json'
    NGSW_KEY = 'ngsw-config.json'
    PACKAGE_KEY = 'package.json'
    README_KEY = 'README.md'
    SERVER_KEY = 'server.js'
    TSCONFIG_KEY = 'tsconfig.json'
    TSCONFIG_APP_KEY = 'tsconfig.app.json'
    TSCONFIG_SPEC_KEY = 'tsconfig.spec.json'
    TSLINT_KEY = 'tslint.json'
    TEST_TS_KEY = 'test.ts'
    GLOBAL_STYLE_KEY = 'styles.css'
    POLYFILLS_KEY = 'polyfills.ts'
    MANIFEST_KEY = 'manifest.json'
    MAIN_TS_KEY = 'main.ts'
    KARMA_CONF_KEY = 'karma.conf.js'
    INDEX_HTML_KEY = 'index.html'
    BROWSERLIST_KEY = 'browserlist'
    ENV_PROD_KEY = 'environment.prod.ts'
    ENV_DEV_KEY = 'environment.ts'
    E2E_TSCONFIG_KEY = 'tsconfig.e2e.json'
    E2E_PROTRACTOR_KEY = 'protractor.conf.js'
    E2E_PO_KEY = 'app.po.ts'
    E2E_SPEC_KEY = 'app.e2e-spec.ts'
    APP_HTML_KEY = 'app.component.html'
    APP_COMPONENT_KEY = 'app.component.ts'
    APP_MODULE_KEY = 'app.module.ts'
    APP_ROUTING_KEY = 'app-routing.module.ts'
    AUTH_GUARD_KEY = 'auth.guard.ts'
    LOGIN_COMPONENT_KEY = 'login.component.ts'
    LOGIN_HTML_KEY = 'login.component.html'

    def __init__(self, app_name, structure=None):
        self.app_name = app_name
        self.project_structure = default_structure if structure == None else structure
        self.app_folder = self.project_structure[self.SRC_FOLDER_KEY][
            self.APP_KEY]
        self.services_folder = self.app_folder[self.SERVICES_KEY]
        self.models_folder = self.app_folder[self.MODELS_KEY]
        self.write_base_angular_project_file()

    def get_app_name(self):
        return self.app_name

    def write_base_angular_project_file(self):
        self.write_editor_config()
        self.write_gitignore()
        self.write_angular_settings()
        self.write_package_dependencies()
        self.write_readme()
        self.write_express_server()
        self.write_tsconfig_and_linter()
        self.write_src_test_template()
        self.write_global_style()
        self.write_polyfills()
        self.write_manifest()
        self.write_main_ts()
        self.write_karma_configuration()
        self.write_index()
        self.write_env_production()
        self.write_env_development()
        self.write_e2e_tsconfig()
        self.write_e2e_protractor()
        self.write_e2e_protractor_definition()
        self.write_e2e_spec_definition()
        self.enable_authentication_service()
        self.write_build_and_run_script()

    def write_editor_config(self):
        self.project_structure[self.EDITOR_CONFIG_KEY] = base_file_writer(
            self.EDITOR_CONFIG_KEY + '.template')

    def write_gitignore(self):
        self.project_structure[self.GITIGNORE_KEY] = base_file_writer(
            self.GITIGNORE_KEY + '.template')

    def write_angular_settings(self):
        self.project_structure[self.ANGULAR_KEY] = base_file_writer(
            self.ANGULAR_KEY + '.template',
            app_name=self.app_name)

    def write_service_worker_config(self, list_of_config):
        self.project_structure[self.NGSW_KEY] = base_file_writer(
            self.NGSW_KEY + '.template',
            app_name=self.app_name,
            data_config=','.join(list_of_config))

    def write_package_dependencies(self):
        self.project_structure[self.PACKAGE_KEY] = base_file_writer(
            self.PACKAGE_KEY + '.template',
            app_name=self.app_name)

    def write_readme(self):
        self.project_structure[self.README_KEY] = base_file_writer(
            self.README_KEY + '.template',
            app_name=self.app_name)

    def write_express_server(self):
        self.project_structure[self.SERVER_KEY] = base_file_writer(
            self.SERVER_KEY + '.template',
            app_name=self.app_name)

    def write_tsconfig_and_linter(self):
        self.project_structure[self.TSCONFIG_KEY] = base_file_writer(
            self.TSCONFIG_KEY + '.template')
        self.project_structure[self.TSLINT_KEY] = base_file_writer(
            self.TSLINT_KEY + '.template')
        self.project_structure[self.SRC_FOLDER_KEY][
            self.TSLINT_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.TSLINT_KEY + '.template')
        self.project_structure[self.SRC_FOLDER_KEY][
            self.TSCONFIG_SPEC_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.TSCONFIG_SPEC_KEY + '.template')
        self.project_structure[self.SRC_FOLDER_KEY][
            self.TSCONFIG_APP_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.TSCONFIG_APP_KEY + '.template')

    def write_src_test_template(self):
        self.project_structure[self.SRC_FOLDER_KEY][
            self.TEST_TS_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.TEST_TS_KEY + '.template')

    def write_global_style(self, content=None):
        self.project_structure[self.SRC_FOLDER_KEY][
            self.GLOBAL_STYLE_KEY] = '/* Style Here */\n@import \"~ngx-smart-modal/ngx-smart-modal.css\";' if content == None else content

    def write_polyfills(self):
        self.project_structure[self.SRC_FOLDER_KEY][
            self.POLYFILLS_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.POLYFILLS_KEY + '.template')

    def write_manifest(self):
        self.project_structure[self.SRC_FOLDER_KEY][
            self.MANIFEST_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.MANIFEST_KEY + '.template',
            app_name=self.app_name)

    def write_main_ts(self):
        self.project_structure[self.SRC_FOLDER_KEY][
            self.MAIN_TS_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.MAIN_TS_KEY + '.template')

    def write_karma_configuration(self):
        self.project_structure[self.SRC_FOLDER_KEY][
            self.KARMA_CONF_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.KARMA_CONF_KEY + '.template')

    def write_index(self):
        self.project_structure[self.SRC_FOLDER_KEY][
            self.INDEX_HTML_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.INDEX_HTML_KEY + '.template',
            app_name=self.app_name)

    def write_browserlist(self):
        self.project_structure[self.SRC_FOLDER_KEY][
            self.BROWSERLIST_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.BROWSERLIST_KEY + '.template')

    def write_env_production(self, content=None):
        self.project_structure[self.SRC_FOLDER_KEY][self.ENV_FOLDER_KEY][
            self.ENV_PROD_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.ENV_FOLDER_KEY + '/' + self.ENV_PROD_KEY + '.template')

    def write_env_development(self, content=None):
        self.project_structure[self.SRC_FOLDER_KEY][self.ENV_FOLDER_KEY][
            self.ENV_DEV_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.ENV_FOLDER_KEY + '/' + self.ENV_DEV_KEY + '.template')

    def write_e2e_tsconfig(self):
        self.project_structure[self.E2E_KEY][
            self.E2E_TSCONFIG_KEY] = base_file_writer(
            self.E2E_KEY + '/' + self.E2E_TSCONFIG_KEY + '.template')

    def write_e2e_protractor(self):
        self.project_structure[self.E2E_KEY][
            self.E2E_PROTRACTOR_KEY] = base_file_writer(
            self.E2E_KEY + '/' + self.E2E_PROTRACTOR_KEY + '.template')

    def write_e2e_protractor_definition(self):
        self.project_structure[self.E2E_KEY][self.SRC_FOLDER_KEY][
            self.E2E_PO_KEY] = base_file_writer(
            self.E2E_KEY + '/' + self.SRC_FOLDER_KEY + '/' + self.E2E_PO_KEY + '.template')

    def write_e2e_spec_definition(self):
        self.project_structure[self.E2E_KEY][self.SRC_FOLDER_KEY][
            self.E2E_SPEC_KEY] = base_file_writer(
            self.E2E_KEY + '/' + self.SRC_FOLDER_KEY + '/' + self.E2E_SPEC_KEY + '.template')

    def add_app_html_template(self, html_template):
        self.app_folder[self.APP_HTML_KEY] = html_template

    def add_default_app_component(self, app_component_typescript):
        self.app_folder[self.APP_COMPONENT_KEY] = app_component_typescript

    def add_app_module_routing(self, app_routing_file):
        self.app_folder[self.APP_ROUTING_KEY] = app_routing_file

    def add_app_module_file(self, app_module_file):
        self.app_folder[self.APP_MODULE_KEY] = app_module_file

    def add_new_component_using_basic_component_folder(self,
                                                       inserted_component_folder):
        self.app_folder.update(inserted_component_folder)

    def add_service_inside_services_folder(self, inserted_service_file):
        self.services_folder.update(inserted_service_file)

    def add_model_inside_models_folder(self, inserted_model_file):
        self.models_folder.update(inserted_model_file)

    def enable_authentication_service(self):
        # Adding Auth Guard
        content_of_auth_guard = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.APP_KEY + '/' + self.GUARD_KEY + '/' + self.AUTH_GUARD_KEY + '.template')
        self.app_folder.update(
            {self.GUARD_KEY: {self.AUTH_GUARD_KEY: content_of_auth_guard}})

    def write_build_and_run_script(self):
        # Build Script
        self.project_structure[
            self.BUILD_SCRIPT_KEY + '.bat'] = base_file_writer(
            self.BUILD_SCRIPT_KEY + '.bat.template', app_name=self.app_name)
        self.project_structure[
            self.BUILD_SCRIPT_KEY + '.sh'] = base_file_writer(
            self.BUILD_SCRIPT_KEY + '.sh.template', app_name=self.app_name)

        # Run Script
        self.project_structure[
            self.RUN_SCRIPT_KEY + '.bat'] = base_file_writer(
            self.RUN_SCRIPT_KEY + '.bat.template', app_name=self.app_name)
        self.project_structure[self.RUN_SCRIPT_KEY + '.sh'] = base_file_writer(
            self.RUN_SCRIPT_KEY + '.sh.template', app_name=self.app_name)

    def return_project_structure(self):
        return {self.app_name: self.project_structure}
