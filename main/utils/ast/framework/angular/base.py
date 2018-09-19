from main.utils.ast.base import Node
from main.utils.ast.language.typescript import ImportStatementType, TypescriptClassType
from main.utils.jinja.angular import base_file_writer

ANGULAR_CORE_MODULE = '@angular/core'
ANGULAR_PLATFORM_BROWSER_MODULE = '@angular/platform-browser'
APP_ROUTING_MODULE_LOCATION = './app-routing.module'
APP_COMPONENT_LOCATION = './app.component'
ANGULAR_SERVICE_WORKER_MODULE = '@angular/service-worker'
ENVIRONMENTS_LOCATION = '../environments/environment'
ANGULAR_ROUTER_MODULE = '@angular/router'

IMPORTED_NG_MODULE = 'NgModule'
IMPORTED_ROUTES = 'Routes'
IMPORTED_ROUTER_MODULE = 'RouterModule'

class AngularMainModule(TypescriptClassType):
    IMPORTED_BROWSER_MODULE = 'BrowserModule'
    IMPORTED_APP_ROUTING_MODULE = 'AppRoutingModule'
    IMPORTED_APP_COMPONENT = 'AppComponent'
    IMPORTED_SERVICE_WORKER_MODULE = 'ServiceWorkerModule'
    IMPORTED_ENVIRONMENT = 'environment'

    def __init__(self, app_name):
        super().__init__()

        # Importing basic requirement of app module
        self.base_element_import_statement_for_module()

        service_worker_initialization = "ServiceWorkerModule.register('/" + app_name + "/ngsw-worker.js', { enabled: environment.production })"
        self.ngmodule_declarations = ['AppComponent']
        self.ngmodule_imports = ['BrowserModule', 'AppRoutingModule', service_worker_initialization]
        self.ngmodule_providers = ['']
        self.ngmodule_bootstraps = ['AppComponent']

    def add_element_into_ngmodule_declarations(self, element=None, elements=None):
        if element:
            self.ngmodule_declarations.append(element)
        elif elements:
            self.ngmodule_declarations += elements
        else:
            raise TypeError('Need at least an element or list of elements to be added into NgModule Declarations')

    def add_element_into_ngmodule_imports(self, element=None, elements=None):
        if element:
            self.ngmodule_imports.append(element)
        elif elements:
            self.ngmodule_imports += elements
        else:
            raise TypeError('Need at least an element or list of elements to be added into NgModule Imports')

    def add_element_into_ngmodule_providers(self, element=None, elements=None):
        if element:
            self.ngmodule_providers.append(element)
        elif elements:
            self.ngmodule_providers += elements
        else:
            raise TypeError('Need at least an element or list of elements to be added into NgModule Providers')

    def add_element_into_ngmodule_bootstraps(self, element=None, elements=None):
        if element:
            self.ngmodule_bootstraps.append(element)
        elif elements:
            self.ngmodule_bootstraps += elements
        else:
            raise TypeError('Need at least an element or list of elements to be added into NgModule Bootstraps')

    def base_element_import_statement_for_module(self):
        self.add_import_statement(main_module=ANGULAR_PLATFORM_BROWSER_MODULE,
                                  element_imported=self.IMPORTED_BROWSER_MODULE)
        self.add_import_statement(main_module=ANGULAR_CORE_MODULE, element_imported=IMPORTED_NG_MODULE)
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
                                ngmodule_bootstrap=',\n'.join(self.ngmodule_bootstraps), import_statement_list='\n'.join(import_statement_list))
