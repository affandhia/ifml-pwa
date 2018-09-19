from main.utils.ast.base import Node
from main.utils.jinja.angular import base_file_writer
from main.utils.ast.language.typescript import TypescriptClassType
from .base import ANGULAR_CORE_MODULE, IMPORTED_ROUTER_MODULE, IMPORTED_ROUTES, IMPORTED_NG_MODULE, ANGULAR_ROUTER_MODULE
from main.utils.naming_management import dasherize

class AngularDefaultRouterDefinition(TypescriptClassType):

    def __init__(self):
        super().__init__()

        self.route_definition = {}
        self.ngmodule_imports = ["RouterModule.forRoot(routes)"]
        self.ngmodule_exports = ["RouterModule"]
        self.base_element_import_statement_for_router()

    def add_routing_definition(self, routing_element):
        if self.route_definition[routing_element.get_target_path()]:
            raise ValueError('Path {path} is already used, please use another path configuration'.format(path=routing_element.get_target_path()))
        else:
            self.route_definition[routing_element.get_target_path()] = routing_element.render()

    def base_element_import_statement_for_router(self):
        self.add_import_statement(main_module=ANGULAR_CORE_MODULE, element_imported=IMPORTED_NG_MODULE)
        self.add_import_statement_for_multiple_element(main_module=ANGULAR_ROUTER_MODULE, elements_imported=[IMPORTED_ROUTES, IMPORTED_ROUTER_MODULE])

    def render(self):
        # Rendering all import statement
        import_statement_list = []
        for _, import_statement in self.import_dict.items():
            import_statement_list.append(import_statement.render())

        #Rendering all configuration definition
        routing_configuration_list = []
        for _, routing_configuration in self.route_definition.items():
            routing_configuration_list.append(routing_configuration.render())

        return base_file_writer('src/app/app-routing.module.ts.template',
                                ngmodule_imports=',\n'.join(self.ngmodule_imports), ngmodule_exports=',\n'.join(self.ngmodule_exports),
                                list_routes='\n'.join(routing_configuration_list),
                                import_statement_list='\n'.join(import_statement_list))

class RoutingElement(Node):

    def __init__(self, path):
        self.path = ''

    def add_component_to_route(self, component):
        self.component = component.component_typescript_class.class_name

    def add_redirect_to(self, redirect):
        self.redirect_to = redirect

    def add_path_match(self, path_match_pattern):
        self.path_match = path_match_pattern

    def add_children_routing(self, children_routes_configuration):
        self.list_of_children_routes = children_routes_configuration.render()

    def get_target_path(self):
        return self.path
    
    def render(self):
        all_routing_element_attributes = self.__dict__
        returned_dict = {}
        for key, value in all_routing_element_attributes.items():
            returned_dict[dasherize(key)] = value
        return returned_dict
