from main.utils.ast.base import Node
from main.utils.ast.language.typescript import ImportStatementType, TypescriptClassType
from main.utils.jinja.angular import base_file_writer, component_file_writer

ANGULAR_CORE_MODULE = '@angular/core'
ANGULAR_PLATFORM_BROWSER_MODULE = '@angular/platform-browser'
APP_ROUTING_MODULE_LOCATION = './app-routing.module'
APP_COMPONENT_LOCATION = './app.component'
ANGULAR_SERVICE_WORKER_MODULE = '@angular/service-worker'
ENVIRONMENTS_LOCATION = '../environments/environment'


class AngularMainModule(TypescriptClassType):
    IMPORTED_BROWSER_MODULE = 'BrowserModule'
    IMPORTED_NG_MODULE = 'NgModule'
    IMPORTED_APP_ROUTING_MODULE = 'AppRoutingModule'
    IMPORTED_APP_COMPONENT = 'AppComponent'
    IMPORTED_SERVICE_WORKER_MODULE = 'ServiceWorkerModule'
    IMPORTED_ENVIRONMENT = 'environment'

    def __init__(self, app_name):
        super().__init__()

        # Importing basic requirement of app module
        self.base_element_import_statement_for_module()

        service_worker_initialization = "ServiceWorkerModule.register('/" + app_name + "/ngsw-worker.js', { enabled: environment.production }"
        self.ngmodule_declarations = ['AppComponent']
        self.ngmodule_imports = ['BrowserModule', 'AppRoutingModule', service_worker_initialization]
        self.ngmodule_providers = ['']
        self.ngmodule_bootstrap = ['AppComponent']

    def base_element_import_statement_for_module(self):
        self.add_import_statement(main_module=ANGULAR_PLATFORM_BROWSER_MODULE,
                                  element_imported=self.IMPORTED_BROWSER_MODULE)
        self.add_import_statement(main_module=ANGULAR_CORE_MODULE, element_imported=self.IMPORTED_NG_MODULE)
        self.add_import_statement(main_module=APP_ROUTING_MODULE_LOCATION,
                                  element_imported=self.IMPORTED_APP_ROUTING_MODULE)
        self.add_import_statement(main_module=APP_COMPONENT_LOCATION, element_imported=self.IMPORTED_APP_COMPONENT)
        self.add_import_statement(main_module=ANGULAR_SERVICE_WORKER_MODULE,
                                  element_imported=self.IMPORTED_SERVICE_WORKER_MODULE)
        self.add_import_statement(main_module=ENVIRONMENTS_LOCATION, element_imported=self.IMPORTED_ENVIRONMENT)

    def render(self):
        # Rendering all import statement
        import_statement_list = []
        for _, import_statement in self.import_dict.items():
            import_statement_list.append(import_statement.render())

        return base_file_writer('src/app/app.module.ts.template', ngmodule_declarations=',\n'.join(self.ngmodule_declarations),
                                ngmodule_imports=',\n'.join(self.ngmodule_imports), ngmodule_providers=',\n'.join(self.ngmodule_providers),
                                ngmodule_bootstrap=',\n'.join(self.ngmodule_bootstrap), import_statement_list='\n'.join(import_statement_list))


class AngularComponent(Node):
    SUFFIX_TYPESCRIPT_COMPONENT_FILENAME = '.component.ts'
    SUFFIX_HTML_COMPONENT_FILENAME = '.component.html'

    def __init__(self, component_name, component_typescript_class, component_html):
        self.component_name = component_name
        self.component_typescript_class = component_typescript_class
        self.component_html = component_html

    def build(self):
        typescript_component_name = self.component_name + self.SUFFIX_TYPESCRIPT_COMPONENT_FILENAME
        typescript_html_name = self.component_name + self.SUFFIX_HTML_COMPONENT_FILENAME
        return {self.component_name: {typescript_component_name: self.component_typescript_class.render(),
                                      typescript_html_name: self.component_html.render()}}


class AngularComponentTypescriptClass(TypescriptClassType):
    def __init__(self):
        super().__init__()
        self.selector_name = ''
        self.component_name = ''

        # Adding import statement for Basic Component
        import_component_from_angular_core = ImportStatementType()
        import_component_from_angular_core.set_main_module(ANGULAR_CORE_MODULE)
        import_component_from_angular_core.add_imported_element('Component')
        self.import_dict[ANGULAR_CORE_MODULE] = import_component_from_angular_core

    def set_selector_name(self, selector_name):
        self.selector_name = selector_name

    def set_component_name(self, component_name):
        self.component_name = component_name

    def render(self):
        # Rendering all import statement
        import_statement_list = []
        for _, import_statement in self.import_dict.items():
            import_statement_list.append(import_statement.render())

        return component_file_writer('basic.component.ts.template', selector_name=self.selector_name,
                                     class_name=self.class_name, component_name=self.component_name,
                                     constructor=self.constructor, body='',
                                     import_statement_list='\n'.join(import_statement_list))


class AngularComponentHTML(Node):
    def __init__(self):
        self.body = []

    def render(self):
        return component_file_writer('basic.component.html.template', body='\n'.join(self.body))
