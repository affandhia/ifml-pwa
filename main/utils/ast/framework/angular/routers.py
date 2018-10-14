from main.utils.ast.base import Node
from main.utils.jinja.angular import base_file_writer, router_file_writer
from main.utils.ast.language.typescript import TypescriptClassType
from .base import ANGULAR_CORE_MODULE, IMPORTED_ROUTER_MODULE, IMPORTED_ROUTES, IMPORTED_NG_MODULE, ANGULAR_ROUTER_MODULE

class AngularDefaultRouterDefinition(TypescriptClassType):

    def __init__(self):
        super().__init__()

        self.route_definition = {}
        self.ngmodule_imports = ["RouterModule.forRoot(routes)"]
        self.ngmodule_exports = ["RouterModule"]
        self.base_element_import_statement_for_router()

    def add_routing_definition_for_component(self, component_that_have_routing):
        routing_node = component_that_have_routing.get_routing_node()
        try:
            check_if_path_already_being_used = self.route_definition[routing_node.get_target_path()] != None
            raise ValueError('Path {path} is already used, please use another path configuration'.format(path=routing_node.get_target_path()))
        except KeyError:
            # Import into Module
            folder_name = component_that_have_routing.get_component_name()
            component_class_name = component_that_have_routing.get_typescript_class_node().get_class_name() + 'Component'
            self.add_import_statement(main_module='./' + folder_name + '/' + folder_name + '.component',
                                      element_imported=component_class_name)
            self.route_definition[routing_node.get_target_path()] = routing_node

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
                                list_routes=',\n'.join(routing_configuration_list),
                                import_statement_list='\n'.join(import_statement_list))

class BaseRoutingNode(Node):

    def __init__(self, path):
        self.path = path

    def add_children_routing(self, children_routes_configuration):
        self.list_of_children_routes = children_routes_configuration.render()

    def get_target_path(self):
        return self.path
    
    def render(self):
        pass

class RouteToModule(BaseRoutingNode):

    ROUTE_TO_MODULE_TEMPLATE = 'route_to_component.ts.template'

    def __init__(self, path, component):
        super().__init__(path)
        self.add_component_to_route(component)
    def add_component_to_route(self, component):
        self.component = component.component_typescript_class.class_name+'Component'

    def render(self):
        return router_file_writer(self.ROUTE_TO_MODULE_TEMPLATE, path=self.path, component=self.component)

class RedirectToAnotherPath(BaseRoutingNode):

    def __init__(self, path, target_redirect, path_match=None):
        super().__init__(path)
        self.set_path_match(path_match)
        self.set_target_redirect(target_redirect)

    def set_target_redirect(self, target_redirect):
        self.target_redirect = target_redirect

    def set_path_match(self, path_match):
        self.path_match = path_match

