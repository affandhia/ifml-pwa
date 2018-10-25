from main.utils.ast.framework.angular.worker_configs import WorkerConfig
from main.utils.ast.language.typescript import TypescriptClassType, FunctionDeclType
from main.utils.jinja.angular import service_file_writer
from main.utils.naming_management import dasherize, camel_classify, \
    change_slash_and_dot_into_dash


class AngularService(TypescriptClassType):

    SERVICE_FILE_NAME = '{service_filename}.service.ts'

    def __init__(self):
        super().__init__()
        self.api_endpoint = ''
        self.call_param = ''
        self.filename = ''
        self.typescript_call = None
        self.worker_config = None

        # TODO Implement
        #Improve this logic to handle multiple action event
        self.action_event = None

    def add_action_event(self, action_event_behavior):
        self.action_event = action_event_behavior

    def set_endpoint_class_name_and_worker(self, name):
        self.api_endpoint = dasherize(name)
        self.class_name = camel_classify(change_slash_and_dot_into_dash(name))
        self.worker_config = WorkerConfig(self.api_endpoint)
        self.worker_config.add_url(self.api_endpoint)
        self.filename = change_slash_and_dot_into_dash(self.api_endpoint)

    def param_exist(self):
        self.call_param = 'param'

    def calling_behaviour(self, typescript_call):
        self.typescript_call = typescript_call

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

        return {self.SERVICE_FILE_NAME.format(service_filename=self.filename) : service_file_writer('basic.service.ts.template', class_name=self.class_name,
                                     api_endpoint=self.api_endpoint, call_param=self.call_param,
                                     constructor_param=', '.join(constructor_param_list),
                                     import_statement_list='\n'.join(import_statement_list),
                                     property_decl='\n'.join(property_decl_list))}

class ActionEventInterpretation(FunctionDeclType):

    def __init__(self, name):
        super().__init__(name)