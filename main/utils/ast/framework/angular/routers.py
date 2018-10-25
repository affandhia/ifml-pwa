import logging

from main.utils.ast.base import Node
from main.utils.ast.language.typescript import TypescriptClassType
from main.utils.jinja.angular import base_file_writer, router_file_writer
from .base import ANGULAR_CORE_MODULE, IMPORTED_ROUTER_MODULE, IMPORTED_ROUTES, IMPORTED_NG_MODULE, \
    ANGULAR_ROUTER_MODULE

logger_routers = logging.getLogger("main.utils.ast.framework.angular.routers")


class AngularDefaultRouterDefinition(TypescriptClassType):

    def __init__(self):
        super().__init__()
        self.route_hierarchy = None
        self.ngmodule_imports = ["RouterModule.forRoot(routes)"]
        self.ngmodule_exports = ["RouterModule"]
        self.base_element_import_statement_for_router()

    def add_routing_hierarchy(self, routing_hierarchy):
        self.route_hierarchy = routing_hierarchy

    def register_component_with_router(self, component):
        selector_name = component.component_typescript_class.selector_name
        class_name = component.component_typescript_class.class_name + 'Component'
        if not (component.get_routing_path() is None):
            component_location = './' + selector_name + '/' + selector_name + '.component'
            self.add_import_statement(main_module=component_location, element_imported=class_name)

    def base_element_import_statement_for_router(self):
        self.add_import_statement(main_module=ANGULAR_CORE_MODULE, element_imported=IMPORTED_NG_MODULE)
        self.add_import_statement_for_multiple_element(main_module=ANGULAR_ROUTER_MODULE,
                                                       elements_imported=[IMPORTED_ROUTES, IMPORTED_ROUTER_MODULE])

    def render(self):
        # Rendering all import statement

        import_statement_list = []
        for _, import_statement in self.import_dict.items():
            import_statement_list.append(import_statement.render())
        return base_file_writer('src/app/app-routing.module.ts.template',
                                ngmodule_imports=',\n'.join(self.ngmodule_imports),
                                ngmodule_exports=',\n'.join(self.ngmodule_exports),
                                list_routes=self.route_hierarchy.render(),
                                import_statement_list='\n'.join(import_statement_list))


class BaseRoutingNode(Node):

    def __init__(self, path):
        super().__init__()
        self.path = path

    def get_target_path(self):
        return self.path

    def render(self):
        pass


class RootRoutingNode(BaseRoutingNode):

    def __init__(self, path):
        super().__init__(path)
        self.angular_children_routes = {}
        self.path_from_root = ''

    def render(self):
        # Rendering Children route
        children_routes = []
        for _, route_node in self.angular_children_routes.items():
            children_routes.append(route_node.render())
        return ','.join(children_routes)

    def add_children_routing(self, children_route_node):
        if not (children_route_node.path in self.angular_children_routes.keys()):
            self.angular_children_routes[children_route_node.path] = children_route_node
        else:
            raise KeyError('Path {path} is already exists'.format(path=children_route_node.path))

    def add_list_of_children_routing(self, list_of_children_route_node):
        for route_node in list_of_children_route_node:
            self.add_children_routing(route_node)

    def get_routing_hierarchy(self):
        return self.angular_children_routes


class RouteToModule(RootRoutingNode):
    ROUTE_TO_MODULE_TEMPLATE = 'route_to_component.ts.template'

    def __init__(self, component_typescript_class):
        super().__init__(component_typescript_class.selector_name)
        self.component = component_typescript_class.class_name + 'Component'
        self.flag = False

    def enable_children_routing(self):
        self.flag = True

    def add_component_to_route(self, component):
        self.component = component.component_typescript_class.class_name + 'Component'

    def render(self):
        # Rendering Children route
        logger_routers.info('Rendering RouteToModule {name}'.format(name=self.path))
        children_routes = []
        for _, route_node in self.angular_children_routes.items():
            children_routes.append(route_node.render())
        return router_file_writer(self.ROUTE_TO_MODULE_TEMPLATE, flag=self.flag, path=self.path,
                                  component=self.component, childrens=',\n'.join(children_routes))


class RedirectToAnotherPath(BaseRoutingNode):
    REDIRECT_TO_PATH_TEMPLATE = 'redirect_to_path.ts.template'

    def __init__(self, path, target_redirect, path_match='full'):
        super().__init__(path)
        self.path_match = path_match
        self.target_redirect = target_redirect

    def set_target_redirect(self, target_redirect):
        self.target_redirect = target_redirect

    def render(self):
        return router_file_writer(self.REDIRECT_TO_PATH_TEMPLATE, path=self.path, target_redirect=self.target_redirect,
                                  path_match=self.path_match)


class RouteToComponentPage(Node):
    ROUTE_TO_COMPONENT_PAGE_TEMPLATE = 'route_to_component_page.ts.template'

    def __init__(self, routing_path):
        self.routing_path = routing_path
        self.param_binding_group = None

    def add_param_binding_group(self, param_binding_group):
        self.param_binding_group = param_binding_group

    def render(self):
        return router_file_writer(self.ROUTE_TO_COMPONENT_PAGE_TEMPLATE, routing_path=self.routing_path,
                                  param_binding_group=self.param_binding_group)
