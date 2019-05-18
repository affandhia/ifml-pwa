import logging

from main.utils.ast.base import Node
from main.utils.ast.framework.react.components import \
    ReactComponentEseightClass
from main.utils.ast.language.typescript import TypescriptClassType, \
    VarDeclType, ImportStatementType
from main.utils.ast.language.eseight import EseightClassType
from main.utils.jinja.react import base_file_writer, router_file_writer
from main.utils.naming_management import camel_function_style, dasherize
from .base import ANGULAR_CORE_MODULE, IMPORTED_ROUTER_MODULE, IMPORTED_ROUTES, \
    IMPORTED_NG_MODULE, \
    ANGULAR_ROUTER_MODULE
from yattag import Doc

logger_routers = logging.getLogger("main.utils.ast.framework.react.routers")


class ReactDefaultRouterDefinition(EseightClassType):
    def __init__(self):
        super().__init__()
        self.route_hierarchy = None
        self.ngmodule_imports = ["RouterModule.forRoot(routes)"]
        self.ngmodule_exports = ["RouterModule"]
        self.base_element_import_statement_for_router()

    def enable_authentication_service(self):
        self.add_import_statement('./guard/auth.guard', 'AuthGuard')

    def add_routing_hierarchy(self, routing_hierarchy):
        self.route_hierarchy = routing_hierarchy

    def register_component_with_router(self, component):
        selector_name = component.component_typescript_class.selector_name
        class_name = component.component_typescript_class.class_name + 'Component'
        if not (component.get_routing_path() is None):
            component_location = './' + selector_name + '/' + selector_name + '.component'
            self.add_import_statement(main_module=component_location,
                                      element_imported=class_name)

    def base_element_import_statement_for_router(self):
        self.add_import_statement(main_module=ANGULAR_CORE_MODULE,
                                  element_imported=IMPORTED_NG_MODULE)
        self.add_import_statement_for_multiple_element(
            main_module=ANGULAR_ROUTER_MODULE,
            elements_imported=[IMPORTED_ROUTES, IMPORTED_ROUTER_MODULE])

    def render(self):
        # Rendering all import statement

        import_statement_list = []
        for _, import_statement in self.import_dict.items():
            import_statement_list.append(import_statement.render())
        return base_file_writer('src/app/app-routing.module.ts.template',
                                ngmodule_imports=',\n'.join(
                                    self.ngmodule_imports),
                                ngmodule_exports=',\n'.join(
                                    self.ngmodule_exports),
                                list_routes=self.route_hierarchy.render(),
                                import_statement_list='\n'.join(
                                    import_statement_list))


class BaseRoutingNode(Node):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def get_target_path(self):
        return self.path

    def render(self):
        pass


class RootRoutingNode(BaseRoutingNode):
    """
    Represent route for root node based on the base routing node.
    """

    def __init__(self, path):
        super().__init__(path)
        self.children_routes = {}
        self.path_from_root = ''
        self.flag = False

    def add_children_routing(self, children_route_node: BaseRoutingNode):
        if not (
                children_route_node.path in self.children_routes.keys()):
            self.children_routes[
                children_route_node.path] = children_route_node
        else:
            raise KeyError('Path {path} is already exists'.format(
                path=children_route_node.path))

    def add_list_of_children_routing(self, list_of_children_route_node):
        for route_node in list_of_children_route_node:
            self.add_children_routing(route_node)

    def get_routing_hierarchy(self):
        return self.children_routes

    def enable_children_routing(self):
        self.flag = True

    def render(self):
        # Rendering Children route
        children_routes = []
        for _, route_node in self.children_routes.items():
            children_routes.append(route_node.render())
        return ','.join(children_routes)


class RouteToModule(RootRoutingNode):
    ROUTE_TO_MODULE_TEMPLATE = 'route_to_module.jsx.template'

    def __init__(self,
                 component_class: ReactComponentEseightClass,
                 enable_guard=False):
        component_kebab_case = dasherize(component_class.component_name)
        super().__init__(component_kebab_case)
        self.component = component_class.class_name + 'Component'
        self.enable_guard = enable_guard

    def add_component_to_route(self, component):
        """
        Add component to Route.

        FIXME: Right now no one uses this method

        :param component:
        :return:
        """
        self.component = component.component_typescript_class.class_name + 'Component'

    def render(self):
        # Rendering Children route
        logger_routers.info(
            'Rendering RouteToModule {name}'.format(name=self.path))
        children_routes = []
        for _, route_node in self.children_routes.items():
            children_routes.append(route_node.render())
        return router_file_writer(self.ROUTE_TO_MODULE_TEMPLATE,
                                  flag=self.flag, path=self.path,
                                  component=self.component,
                                  childrens=',\n'.join(children_routes),
                                  enable_guard=self.enable_guard)


class RedirectToAnotherPath(BaseRoutingNode):
    REDIRECT_TO_PATH_TEMPLATE = 'redirect_to_path.ts.template'

    def __init__(self, path, target_redirect, path_match='exact'):
        super().__init__(path)
        self.path_match = path_match
        self.target_redirect = target_redirect

    def set_target_redirect(self, target_redirect):
        self.target_redirect = target_redirect

    def render(self):
        return router_file_writer(self.REDIRECT_TO_PATH_TEMPLATE,
                                  path=self.path,
                                  target_redirect=self.target_redirect,
                                  path_match=self.path_match)


class RouteUsingInteractionFlow(Node):

    def __init__(self):
        self.param_binding_group = None

    def add_param_binding_group(self, param_binding_group):
        self.param_binding_group = param_binding_group


class RouteToComponentPage(RouteUsingInteractionFlow):
    ROUTE_TO_COMPONENT_PAGE_TEMPLATE = 'route_to_component_page.ts.template'

    def __init__(self, routing_path):
        super().__init__()
        self.routing_path = routing_path

    def render(self):
        return router_file_writer(self.ROUTE_TO_COMPONENT_PAGE_TEMPLATE,
                                  routing_path=self.routing_path,
                                  param_binding_group=self.param_binding_group)


class RouteToAction(RouteUsingInteractionFlow):
    ROUTE_TO_ACTION_PAGE_TEMPLATE = 'route_to_action.ts.template'

    def __init__(self, service_class_name, service_filename):
        super().__init__()
        self.service_class_name = service_class_name + 'Service'
        self.service_filename = service_filename
        self.after_statement = []
        self.import_statement = None
        self.constructor_param = None
        self.build_import_statement()
        self.build_constructor_param()

    def build_import_statement(self):
        self.import_statement = ImportStatementType()
        # Service location
        service_location = '../services/{service_filename}.service'.format(
            service_filename=self.service_filename)
        self.import_statement.set_main_module(service_location)
        self.import_statement.add_imported_element(self.service_class_name)

    def build_constructor_param(self):
        self.constructor_param = VarDeclType(
            camel_function_style(self.service_class_name))
        self.constructor_param.acc_modifiers = 'public'
        self.constructor_param.variable_datatype = self.service_class_name

    def render(self):
        return router_file_writer(self.ROUTE_TO_ACTION_PAGE_TEMPLATE,
                                  service_name=camel_function_style(
                                      self.service_class_name),
                                  param_binding_group=self.param_binding_group,
                                  after_statement='\n'.join(
                                      self.after_statement))


class GettingQueryParam(Node):

    def __init__(self):
        self.list_query_param_and_property_pair = []

    def add_statement_for_saving_query_param_value_into_property(self,
                                                                 query_param_name,
                                                                 property_name):
        self.list_query_param_and_property_pair.append(
            'this.{property_name} = JSON.parse(params.{query_param_name});'.format(
                query_param_name=query_param_name,
                property_name=property_name))

    def add_statement_for_saving_query_param_value_into_property_typed_class(
            self, query_param_name, property_name, class_type):
        self.list_query_param_and_property_pair.append(
            'this.{property_name} = new {class_type}(JSON.parse(params.{query_param_name}));'.format(
                query_param_name=query_param_name,
                property_name=property_name, class_type=class_type))

    def render(self):
        return router_file_writer('getting_query_params.ts.template',
                                  list_of_param='\n'.join(
                                      self.list_query_param_and_property_pair))
