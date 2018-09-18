from enum import Enum
from main.utils.ast.base import Node
from main.utils.jinja.language_template_writer import typescript_writer

IMPORT_TYPESCRIPT_TEMPLATE = 'import.ts.template'

class NodeType(Enum):
    TEXT = 0
    VAR = 1
    FUNCTION = 2
    CLASS = 3
    COMMENT = 4

class ImportStatementType(Node):

    def __init__(self):
        self.main_module = ''
        self.imported_elements = []

    def set_main_module(self, main_module):
        self.main_module = main_module

    def add_imported_element(self, element_that_want_to_be_imported):
        self.imported_elements.append(element_that_want_to_be_imported)

    def render_import_dict(self):
        list_element_imported_in_module = ','.join(self.imported_elements)
        import_statement = typescript_writer(IMPORT_TYPESCRIPT_TEMPLATE,
                                                 imported_element=list_element_imported_in_module,
                                                 main_module=self.main_module)
        return import_statement
