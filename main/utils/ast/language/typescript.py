from enum import Enum

from main.utils.ast.base import Node
from main.utils.jinja.language_template_writer import typescript_writer

IMPORT_TYPESCRIPT_TEMPLATE = 'import.ts.template'
CLASS_TYPESCRIPT_TEMPLATE = 'class.ts.template'

class ImportStatementType(Node):

    def __init__(self):
        self.main_module = ''
        self.imported_elements = []

    def set_main_module(self, main_module):
        self.main_module = main_module

    def add_imported_elements(self, elements_that_want_to_be_imported):
        self.imported_elements + elements_that_want_to_be_imported

    def add_imported_element(self, element_that_want_to_be_imported):
        self.imported_elements.append(element_that_want_to_be_imported)

    def render(self):
        list_element_imported_in_module = ','.join(self.imported_elements)
        import_statement = typescript_writer(IMPORT_TYPESCRIPT_TEMPLATE,
                                             imported_element=','.join(self.imported_elements),
                                             main_module=self.main_module)
        return import_statement

    def __str__(self):
        return self.main_module + ' with ' + '[' + ','.join(self.imported_elements) + ']'

class TypescriptClassType(Node):

    def __init__(self):
        self.class_name = ''
        self.constructor = []
        self.body = []
        self.import_dict = {}

    def set_class_name(self, class_name):
        self.class_name = class_name

    def add_import_statement_for_multiple_element(self, main_module, elements_imported):
        try:
            self.import_dict[main_module].add_imported_elements(elements_imported)
        except KeyError:
            new_import_statement_node = ImportStatementType()
            new_import_statement_node.set_main_module(main_module)
            new_import_statement_node.add_imported_elements(elements_imported)
            self.import_dict[main_module] = new_import_statement_node

    def add_import_statement(self, main_module, element_imported):
        try:
            self.import_dict[main_module].add_imported_element(element_imported)
        except KeyError:
            new_import_statement_node = ImportStatementType()
            new_import_statement_node.set_main_module(main_module)
            new_import_statement_node.add_imported_element(element_imported)
            self.import_dict[main_module] = new_import_statement_node

    def render(self):
        # Rendering all import statement
        import_statement_list = []
        for _, import_statement in self.import_dict.items():
            import_statement_list.append(import_statement.render())

        return typescript_writer('class.ts.template',
                                     class_name=self.class_name,
                                     constructor=self.constructor, body='\n'.join(self.body),
                                     import_statement_list='\n'.join(import_statement_list))

