from main.template.project_structure.angular_strcture import default_structure
from main.utils.jinja.angular import base_file_writer


class AngularProject:
    SRC_FOLDER_KEY = 'src'
    ENV_FOLDER_KEY = 'environments'
    E2E_KEY = 'e2e'
    APP_KEY = 'app'

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

    app_name = 'generated-template'

    def __init__(self, structure=None):
        self.project_structure = default_structure if structure == None else structure
        self.write_base_angular_project_file()
        self.write_base_app()

    def write_base_angular_project_file(self):
        self.write_editor_config()
        self.write_gitignore()
        self.write_angular_settings()
        self.write_service_worker_config()
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

    def write_editor_config(self):
        self.project_structure[self.EDITOR_CONFIG_KEY] = base_file_writer(self.EDITOR_CONFIG_KEY + '.template')

    def write_gitignore(self):
        self.project_structure[self.GITIGNORE_KEY] = base_file_writer(self.GITIGNORE_KEY + '.template')

    def write_angular_settings(self):
        self.project_structure[self.ANGULAR_KEY] = base_file_writer(self.ANGULAR_KEY + '.template',
                                                                    app_name=self.app_name)

    def write_service_worker_config(self):
        self.project_structure[self.NGSW_KEY] = base_file_writer(self.NGSW_KEY + '.template',
                                                                 app_name=self.app_name)

    def write_package_dependencies(self):
        self.project_structure[self.PACKAGE_KEY] = base_file_writer(self.PACKAGE_KEY + '.template',
                                                                    app_name=self.app_name)

    def write_readme(self):
        self.project_structure[self.README_KEY] = base_file_writer(self.README_KEY + '.template',
                                                                   app_name=self.app_name)

    def write_express_server(self):
        self.project_structure[self.SERVER_KEY] = base_file_writer(self.SERVER_KEY + '.template',
                                                                   app_name=self.app_name)

    def write_tsconfig_and_linter(self):
        self.project_structure[self.TSCONFIG_KEY] = base_file_writer(self.TSCONFIG_KEY + '.template')
        self.project_structure[self.TSLINT_KEY] = base_file_writer(self.TSLINT_KEY + '.template')
        self.project_structure[self.SRC_FOLDER_KEY][self.TSLINT_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.TSLINT_KEY + '.template')
        self.project_structure[self.SRC_FOLDER_KEY][self.TSCONFIG_SPEC_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.TSCONFIG_SPEC_KEY + '.template')
        self.project_structure[self.SRC_FOLDER_KEY][self.TSCONFIG_APP_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.TSCONFIG_APP_KEY + '.template')

    def write_src_test_template(self):
        self.project_structure[self.SRC_FOLDER_KEY][self.TEST_TS_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.TEST_TS_KEY + '.template')

    def write_global_style(self, content=None):
        self.project_structure[self.SRC_FOLDER_KEY][
            self.GLOBAL_STYLE_KEY] = '/* Style Here' if content == None else content

    def write_polyfills(self):
        self.project_structure[self.SRC_FOLDER_KEY][self.POLYFILLS_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.POLYFILLS_KEY + '.template')

    def write_manifest(self):
        self.project_structure[self.SRC_FOLDER_KEY][self.MANIFEST_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.MANIFEST_KEY + '.template', app_name=self.app_name)

    def write_main_ts(self):
        self.project_structure[self.SRC_FOLDER_KEY][self.MAIN_TS_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.MAIN_TS_KEY + '.template')

    def write_karma_configuration(self):
        self.project_structure[self.SRC_FOLDER_KEY][self.KARMA_CONF_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.KARMA_CONF_KEY + '.template')

    def write_index(self):
        self.project_structure[self.SRC_FOLDER_KEY][self.INDEX_HTML_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.INDEX_HTML_KEY + '.template', app_name=self.app_name)

    def write_browserlist(self):
        self.project_structure[self.SRC_FOLDER_KEY][self.BROWSERLIST_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.BROWSERLIST_KEY + '.template')

    def write_env_production(self, content=None):
        self.project_structure[self.SRC_FOLDER_KEY][self.ENV_FOLDER_KEY][self.ENV_PROD_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.ENV_FOLDER_KEY + '/' + self.ENV_PROD_KEY + '.template')

    def write_env_development(self, content=None):
        self.project_structure[self.SRC_FOLDER_KEY][self.ENV_FOLDER_KEY][self.ENV_DEV_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.ENV_FOLDER_KEY + '/' + self.ENV_DEV_KEY + '.template')

    def write_e2e_tsconfig(self):
        self.project_structure[self.E2E_KEY][self.E2E_TSCONFIG_KEY] = base_file_writer(
            self.E2E_KEY + '/' + self.E2E_TSCONFIG_KEY + '.template')

    def write_e2e_protractor(self):
        self.project_structure[self.E2E_KEY][self.E2E_PROTRACTOR_KEY] = base_file_writer(
            self.E2E_KEY + '/' + self.E2E_PROTRACTOR_KEY + '.template')

    def write_e2e_protractor_definition(self):
        self.project_structure[self.E2E_KEY][self.SRC_FOLDER_KEY][self.E2E_PO_KEY] = base_file_writer(
            self.E2E_KEY + '/' + self.SRC_FOLDER_KEY + '/' + self.E2E_PO_KEY + '.template')

    def write_e2e_spec_definition(self):
        self.project_structure[self.E2E_KEY][self.SRC_FOLDER_KEY][self.E2E_SPEC_KEY] = base_file_writer(
            self.E2E_KEY + '/' + self.SRC_FOLDER_KEY + '/' + self.E2E_SPEC_KEY + '.template')

    def write_base_app(self):
        app_folder = self.project_structure[self.SRC_FOLDER_KEY][self.APP_KEY]

        app_folder[self.APP_COMPONENT_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.APP_KEY + '/' + self.APP_COMPONENT_KEY + '.template',
            app_name=self.app_name)

        app_folder[self.APP_HTML_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.APP_KEY + '/' + self.APP_HTML_KEY + '.template')

        app_folder[self.APP_MODULE_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.APP_KEY + '/' + self.APP_MODULE_KEY + '.template', app_name=self.app_name)

        app_folder[self.APP_ROUTING_KEY] = base_file_writer(
            self.SRC_FOLDER_KEY + '/' + self.APP_KEY + '/' + self.APP_ROUTING_KEY + '.template')

    def return_project_structure(self):
        return {self.app_name: self.project_structure}
