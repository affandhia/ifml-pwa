import functools
import logging

from main.utils.ast.base import Node
from main.utils.ast.framework.angular.worker_configs import WorkerConfig
from main.utils.ast.language.eseight import EseightClassType, \
    MethodAsInstanceVarDeclType, FunctionType
from main.utils.jinja.react import service_file_writer
from main.utils.naming_management import dasherize, camel_classify, \
    change_slash_and_dot_into_dash, camel_function_style

logger = logging.getLogger("main.utils.ast.framework.react.services")


def function_logger(function):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        logger.debug(function.__name__)
        return function(*args, **kwargs)

    return wrapper


class ReactAPICall(EseightClassType):
    SERVICE_FILE_NAME = '{service_filename}.service.js'

    def __init__(self, enable_auth=False):
        super().__init__()
        self.api_endpoint = ''
        self.call_param = ''
        self.filename = ''
        self.enable_auth_token_for_calling_api = enable_auth

        # TODO Implement
        # Improve this logic to handle multiple action event
        self.action_event = None

    def add_action_event(self, action_event_behavior):
        self.action_event = action_event_behavior

    def set_endpoint_class_name_and_worker(self, name):
        """
        Setting API endpoint and the Service Worker configuration. Setting
        class name by the API endpoint.

        :param name: supposed to be the API endpoint
        :return: None
        """

        self.api_endpoint = dasherize(name)
        # define class name
        self.filename = change_slash_and_dot_into_dash(self.api_endpoint)
        self.class_name = camel_classify(self.filename)

    def param_exist(self):
        self.call_param = 'param'

    def render(self):
        # Rendering all import statement
        import_statement_list = []
        for _, import_statement in self.import_dict.items():
            import_statement_list.append(import_statement.render())

        # Rendering all constructor param statement
        constructor_param_list = []
        for _, param in self.constructor_param.items():
            constructor_param_list.append(param.render())

        # Rendering all property decl statement
        property_decl_list = []
        for _, prop in self.property_decl.items():
            property_decl_list.append(prop.render())

        return {
            self.SERVICE_FILE_NAME.format(
                service_filename=self.filename
            ): service_file_writer(
                'basic.service.js.template',
                class_name=self.class_name,
                api_endpoint=self.api_endpoint,
                call_param=self.call_param,
                constructor_param=', '.join(constructor_param_list),
                import_statement_list='\n'.join(import_statement_list),
                property_decl='\n'.join(property_decl_list),
                enable_auth=self.enable_auth_token_for_calling_api)
        }


class ActionEventInterpretation(FunctionType):

    def __init__(self, name):
        super().__init__(name)


class ActionInterpretation(Node):
    def __init__(self, action: str, auth_guard: bool):
        self.auth_guard = auth_guard
        self.action = action
        self.function = MethodAsInstanceVarDeclType(
            camel_function_style(
                change_slash_and_dot_into_dash(action)))
        self.function.enable_async()

    def extract_action(self, action: str) -> str:
        fun = "NOT_FOUND"
        action_type = self.extract_action_type(action)
        fun = action_type if action_type != fun else fun
        return fun

    def extract_action_type(self, text: str) -> str:
        arr = text.split('/')
        temp = arr[len(arr) - 1]
        suffix = '.abs'
        is_end_with_dot_abs = temp.endswith(suffix)

        return temp[:len(suffix)] if is_end_with_dot_abs else temp

    def action_reducer(self, action: str):
        action_type: str = self.extract_action_type(action)
        parsed = ""

        if action_type == 'retrieve':
            parsed = self.action_type_retrieve_parser()
        elif action_type == 'create':
            parsed = 'this aciton is: create'
        elif action_type == 'delete':
            parsed = 'this aciton is: delete'
        elif action_type == 'list':
            parsed = 'this aciton is: list'

        return parsed

    def action_type_retrieve_parser(self):

        return service_file_writer(
            'action_retrieve.js.template',
            function_name=self.function.variable_name,
            auth_guard=self.auth_guard,
            action_api=self.action
        )

    def render(self):
        return self.action_reducer(self.action)
