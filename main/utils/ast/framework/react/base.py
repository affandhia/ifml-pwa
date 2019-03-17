from main.utils.ast.language.typescript import TypescriptClassType
from main.utils.jinja.angular import base_file_writer

ANGULAR_CORE_MODULE = '@angular/core'
ANGULAR_PLATFORM_BROWSER_MODULE = '@angular/platform-browser'
APP_ROUTING_MODULE_LOCATION = './app-routing.module'
APP_COMPONENT_LOCATION = './app.component'
ANGULAR_SERVICE_WORKER_MODULE = '@angular/service-worker'
ENVIRONMENTS_LOCATION = '../environments/environment'
ANGULAR_ROUTER_MODULE = '@angular/router'
FORMS_MODULE_LOCATION = '@angular/forms'
HTTP_MODULE_LOCATION = '@angular/common/http'
NGX_SMART_MODAL_LOCATION = 'ngx-smart-modal'
ANGULAR_6_SOCIAL_LOGIN = 'angular-6-social-login-v2'

IMPORTED_NG_MODULE = 'NgModule'
IMPORTED_ROUTES = 'Routes'
IMPORTED_ROUTER_MODULE = 'RouterModule'
IMPORTED_GOOGLE_LOGIN_PROVIDER = 'GoogleLoginProvider'


class AngularMainModule(TypescriptClassType):
    IMPORTED_BROWSER_MODULE = 'BrowserModule'
    IMPORTED_APP_ROUTING_MODULE = 'AppRoutingModule'
    IMPORTED_APP_COMPONENT = 'AppComponent'
    IMPORTED_SERVICE_WORKER_MODULE = 'ServiceWorkerModule'
    IMPORTED_ENVIRONMENT = 'environment'
    IMPORTED_FORMS_MODULE = 'FormsModule'
    IMPORTED_HTTP_CLIENT_MODULE = 'HttpClientModule'
    IMPORTED_SMART_MODAL_MODULE = 'NgxSmartModalModule'
    IMPORTED_SMART_MODAL_SERVICE = 'NgxSmartModalService'
    IMPORTED_AUTH_SERVICE_CONFIG = 'AuthServiceConfig'
    IMPORTED_SOCIAL_LOGIN_MODULE = 'SocialLoginModule'

    # Edit this to change Google Client ID
    GOOGLE_CLIENT_ID = '\"980984936575-0lo321pevqjlul7nsdk441ccjah11b1f.apps.googleusercontent.com\"'

    def __init__(self, app_name):
        super().__init__()
        self.google_sign_in_config = False
        # Importing basic requirement of app module
        self.base_element_import_statement_for_module()

        service_worker_initialization = "ServiceWorkerModule.register('/" + app_name + "/ngsw-worker.js', { enabled: environment.production })"
        self.ngmodule_declarations = [self.IMPORTED_APP_COMPONENT]
        self.ngmodule_imports = [self.IMPORTED_BROWSER_MODULE,
                                 self.IMPORTED_HTTP_CLIENT_MODULE,
                                 '{smart_modal}.forRoot()'.format(
                                     smart_modal=self.IMPORTED_SMART_MODAL_MODULE),
                                 self.IMPORTED_APP_ROUTING_MODULE,
                                 self.IMPORTED_FORMS_MODULE,
                                 service_worker_initialization]
        self.ngmodule_providers = [self.IMPORTED_SMART_MODAL_SERVICE]
        self.ngmodule_bootstraps = [self.IMPORTED_APP_COMPONENT]

    def enable_authentication_service(self):
        # Adding import statement for Social Login
        self.add_import_statement(main_module=ANGULAR_6_SOCIAL_LOGIN,
                                  element_imported=IMPORTED_GOOGLE_LOGIN_PROVIDER)
        self.add_import_statement(main_module=ANGULAR_6_SOCIAL_LOGIN,
                                  element_imported=self.IMPORTED_AUTH_SERVICE_CONFIG)
        self.add_import_statement(main_module=ANGULAR_6_SOCIAL_LOGIN,
                                  element_imported=self.IMPORTED_SOCIAL_LOGIN_MODULE)

        # Angular Social Login Provider Setting
        social_login_provider = '{ provide: ' + self.IMPORTED_AUTH_SERVICE_CONFIG + ', useFactory: getAuthServiceConfigs }'
        self.ngmodule_providers.append(social_login_provider)

        # Adding Social Login Module
        self.ngmodule_imports.append(self.IMPORTED_SOCIAL_LOGIN_MODULE)

        # Enabling Google Sign In Configuration
        self.google_sign_in_config = True

        # Adding Login Component to NgModule
        login_component_location = './login/login.component'
        login_component_class_name = 'LoginComponent'
        self.add_import_statement(login_component_location,
                                  login_component_class_name)
        self.ngmodule_declarations.append(login_component_class_name)

    def add_element_into_ngmodule_declarations(self, element=None,
                                               elements=None):
        if element:
            self.ngmodule_declarations.append(element)
        elif elements:
            self.ngmodule_declarations += elements
        else:
            raise TypeError(
                'Need at least an element or list of elements to be added into NgModule Declarations')

    def add_component_to_module(self, component_node):

        # Import into Module
        folder_name = component_node.get_component_name()
        component_class_name = component_node.get_typescript_class_node().get_class_name() + 'Component'
        self.add_import_statement(
            main_module='./' + folder_name + '/' + folder_name + '.component',
            element_imported=component_class_name)

        # Add to Declarations
        self.add_element_into_ngmodule_declarations(component_class_name)

    def add_element_into_ngmodule_imports(self, element=None, elements=None):
        if element:
            self.ngmodule_imports.append(element)
        elif elements:
            self.ngmodule_imports += elements
        else:
            raise TypeError(
                'Need at least an element or list of elements to be added into NgModule Imports')

    def add_element_into_ngmodule_providers(self, element=None, elements=None):
        if element:
            self.ngmodule_providers.append(element)
        elif elements:
            self.ngmodule_providers += elements
        else:
            raise TypeError(
                'Need at least an element or list of elements to be added into NgModule Providers')

    def add_element_into_ngmodule_bootstraps(self, element=None,
                                             elements=None):
        if element:
            self.ngmodule_bootstraps.append(element)
        elif elements:
            self.ngmodule_bootstraps += elements
        else:
            raise TypeError(
                'Need at least an element or list of elements to be added into NgModule Bootstraps')

    def base_element_import_statement_for_module(self):
        self.add_import_statement(main_module=ANGULAR_PLATFORM_BROWSER_MODULE,
                                  element_imported=self.IMPORTED_BROWSER_MODULE)
        self.add_import_statement(main_module=ANGULAR_CORE_MODULE,
                                  element_imported=IMPORTED_NG_MODULE)
        self.add_import_statement(main_module=APP_ROUTING_MODULE_LOCATION,
                                  element_imported=self.IMPORTED_APP_ROUTING_MODULE)
        self.add_import_statement(main_module=APP_COMPONENT_LOCATION,
                                  element_imported=self.IMPORTED_APP_COMPONENT)
        self.add_import_statement(main_module=ANGULAR_SERVICE_WORKER_MODULE,
                                  element_imported=self.IMPORTED_SERVICE_WORKER_MODULE)
        self.add_import_statement(main_module=ENVIRONMENTS_LOCATION,
                                  element_imported=self.IMPORTED_ENVIRONMENT)
        self.add_import_statement(main_module=HTTP_MODULE_LOCATION,
                                  element_imported=self.IMPORTED_HTTP_CLIENT_MODULE)
        self.add_import_statement(main_module=FORMS_MODULE_LOCATION,
                                  element_imported=self.IMPORTED_FORMS_MODULE)
        self.add_import_statement(main_module=NGX_SMART_MODAL_LOCATION,
                                  element_imported=self.IMPORTED_SMART_MODAL_MODULE)
        self.add_import_statement(main_module=NGX_SMART_MODAL_LOCATION,
                                  element_imported=self.IMPORTED_SMART_MODAL_SERVICE)

    def render(self):
        # Rendering all import statement
        import_statement_list = []
        for _, import_statement in self.import_dict.items():
            import_statement_list.append(import_statement.render())

        return base_file_writer('src/app/app.module.ts.template',
                                ngmodule_declarations=',\n'.join(
                                    self.ngmodule_declarations),
                                ngmodule_imports=',\n'.join(
                                    self.ngmodule_imports),
                                ngmodule_providers=',\n'.join(
                                    self.ngmodule_providers),
                                ngmodule_bootstrap=',\n'.join(
                                    self.ngmodule_bootstraps),
                                import_statement_list='\n'.join(
                                    import_statement_list),
                                google_client_id=self.GOOGLE_CLIENT_ID,
                                google_sign_in_config=self.google_sign_in_config)
