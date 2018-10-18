from enum import Enum
import logging

from main.utils.ast.base import Node
from main.utils.jinja.language_template_writer import typescript_writer
from main.utils.naming_management import camel_function_style

IMPORT_TYPESCRIPT_TEMPLATE = 'import.ts.template'
CLASS_TYPESCRIPT_TEMPLATE = 'class.ts.template'
VARIABLE_DECLARATION_TEMPLATE = 'variable.ts.template'
ARROW_FUNCTION_DECLARATION_TEMPLATE = 'arrow_function.ts.template'
FUNCTION_DECLARATION_TEMPLATE = 'function.ts.template'

class ImportStatementType(Node):

    def __init__(self):
        self.main_module = ''
        self.imported_elements = []

    def set_main_module(self, main_module):
        self.main_module = main_module

    def add_imported_elements(self, elements_that_want_to_be_imported):
        self.imported_elements += elements_that_want_to_be_imported

    def add_imported_element(self, element_that_want_to_be_imported):
        self.imported_elements.append(element_that_want_to_be_imported)

    def render(self):
        list_element_imported_in_module = ','.join(self.imported_elements)
        import_statement = typescript_writer(IMPORT_TYPESCRIPT_TEMPLATE,
                                             imported_element=', '.join(self.imported_elements),
                                             main_module=self.main_module)
        return import_statement

    def __str__(self):
        return self.main_module + ' with ' + '[' + ','.join(self.imported_elements) + ']'

class VarDeclType(Node):

    def __init__(self, name, semicolon=''):
        self.acc_modifiers = ''
        self.decorator = ''
        self.variable_type = ''
        self.variable_name = name
        self.variable_datatype = ''
        self.value = ''
        self.semicolon = semicolon

    def render(self):
        return typescript_writer(VARIABLE_DECLARATION_TEMPLATE,
                                     acc_modifiers=self.acc_modifiers, decorator=self.decorator,
                                     variable_type=self.variable_type, variable_name=self.variable_name,
                                     variable_datatype=self.variable_datatype, value=self.value, end=self.semicolon)

class ArrowFunctionType(Node):

    def __init__(self ,name):
        super().__init__()
        self.function_name = camel_function_style(name)
        self.parameter_dict = {}
        self.function_body = []

    def add_param(self, var_decl):
        self.parameter_dict[var_decl.variable_name] = var_decl

    def add_statement_to_body(self, statement):
        self.function_body.append(statement)

    def render(self):
        # Parameter list
        parameter_list = []
        for _, param in self.parameter_dict.items():
            parameter_list.append(param.render())

        return typescript_writer(ARROW_FUNCTION_DECLARATION_TEMPLATE,
                                 function_name=self.function_name,
                                 function_body='\n'.join(self.function_body), parameter_list=', '.join(parameter_list))

class FunctionDeclType(ArrowFunctionType):

    def __init__(self, name):
        super().__init__(name)
        self.function_type = ''
        self.function_return_type = ''

    def add_param(self, var_decl):
        self.parameter_dict[var_decl.variable_name] = var_decl

    def render(self):

        #Parameter list
        parameter_list = []
        for _, param in self.parameter_dict.items():
            parameter_list.append(param.render())

        return typescript_writer(FUNCTION_DECLARATION_TEMPLATE,
                                 function_name=self.function_name, function_type=self.function_type,
                                 function_body='\n'.join(self.function_body), parameter_list=', '.join(parameter_list),
                                 function_return_type=self.function_return_type)


class TypescriptClassType(Node):

    def __init__(self):
        self.class_name = ''
        self.constructor_param = {}
        self.property_decl = {}
        self.constructor_body = []
        self.body = []
        self.import_dict = {}

    def set_class_name(self, class_name):
        self.class_name = class_name

    def get_class_name(self):
        return self.class_name

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

    def set_constructor_param(self, var_decl):
        self.constructor_param[var_decl.variable_name] = var_decl

    def set_property_decl(self, var_decl):
        self.property_decl[var_decl.variable_name] = var_decl

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

        return typescript_writer(CLASS_TYPESCRIPT_TEMPLATE,
                                     class_name=self.class_name,
                                     constructor_param=','.join(constructor_param_list), body='\n'.join(self.body),
                                     import_statement_list='\n'.join(import_statement_list))

