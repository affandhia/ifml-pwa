from enum import Enum

from main.utils.ast.base import Node
from main.utils.jinja.angular import component_file_writer
from main.utils.ast.language.typescript import ImportStatementType

ANGULAR_CORE_MODULE = '@angular/core'

class NodeType(Enum):
    MODEL = 0
    COMPONENT = 1
    SERVICE = 2
    WORKER_FUNCTION = 3

class AngularComponent(Node):

    def __init__(self):
        self.selector_name = ''
        self.class_name = ''
        self.component_name = ''
        self.constructor = []
        self.body = []
        self.import_list = []

        #Adding import statement for Basic Component
        import_component_from_angular_core = ImportStatementType()
        import_component_from_angular_core.set_main_module(ANGULAR_CORE_MODULE)
        import_component_from_angular_core.add_imported_element('Component')

    def set_selector_name(self, selector_name):
        self.selector_name = selector_name

    def set_class_name(self, class_name):
        self.class_name = class_name

    def set_component_name(self, component_name):
        self.component_name = component_name

    def render(self):

        #Rendering all import statement
        import_statement_list = []
        for import_statement in self.import_list:
            import_statement_list.append(import_statement.render())

        return component_file_writer('basic.component.ts.template', selector_name=self.selector_name,
                              class_name=self.class_name, component_name=self.component_name,
                              constructor=self.constructor, body='', import_statement_list='\n'.join(import_statement_list))


