import functools
import logging

from main.utils.ast.base import Node
from main.utils.ast.framework.angular.worker_configs import WorkerConfig
from main.utils.ast.language.eseight import EseightClassType
from main.utils.ast.language.typescript import TypescriptClassType, \
    FunctionDeclType
from main.utils.jinja.react import service_file_writer
from main.utils.naming_management import dasherize, camel_classify, \
    change_slash_and_dot_into_dash

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
    SERVICE_FILE_NAME = '{service_filename}.service.ts'

    def __init__(self, enable_auth=False):
        super().__init__()
        self.api_endpoint = ''
        self.call_param = ''
        self.filename = ''
        self.enable_auth_token_for_calling_api = enable_auth

        # TODO Implement
        # Improve this logic to handle multiple action event
        self.action_event = None

    @function_logger
    def add_action_event(self, action_event_behavior):
        self.action_event = action_event_behavior

    @function_logger
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

    @function_logger
    def param_exist(self):
        self.call_param = 'param'

    @function_logger
    def render(self):

        return {
            "property": self.property_decl,
            "function": self.methods
        }


class ActionEventInterpretation(FunctionDeclType):

    def __init__(self, name):
        super().__init__(name)
