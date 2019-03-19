from enum import Enum
import logging

from main.utils.ast.base import Node
from main.utils.jinja.language_template_writer import eseight_writer
from main.utils.naming_management import camel_function_style

IMPORT_ESEIGHT_TEMPLATE = 'import.js.template'
CLASS_ESEIGHT_TEMPLATE = 'class.js.template'
VARIABLE_DECLARATION_TEMPLATE = 'variable.js.template'
ARROW_FUNCTION_DECLARATION_TEMPLATE = 'arrow_function.js.template'
FUNCTION_DECLARATION_TEMPLATE = 'function.js.template'


class ImportStatementType(Node):

    def __init__(self):
        self.main_module = ''
        self.default_element = None
        self.imported_elements = []

    def set_main_module(self, main_module):
        self.main_module = main_module

    def set_default_element(self, default_element):
        self.default_element = default_element

    def add_imported_elements(self, elements_that_want_to_be_imported):
        self.imported_elements += elements_that_want_to_be_imported

    def add_imported_element(self, element_that_want_to_be_imported):
        self.imported_elements.append(element_that_want_to_be_imported)

    def render(self):
        import_statement = eseight_writer(IMPORT_ESEIGHT_TEMPLATE,
                                          default_element=self.default_element,
                                          imported_element=', '.join(
                                              self.imported_elements),
                                          main_module=self.main_module)
        return import_statement

    def __str__(self):
        return self.main_module + ' with ' + '[' + ','.join(
            self.imported_elements) + ']'


class VarDecl(Node):

    def __init__(self, name, semicolon=''):
        self.acc_modifiers = ''
        self.variable_name = name
        self.value = ''
        self.semicolon = semicolon

    def render(self):
        return eseight_writer(
            VARIABLE_DECLARATION_TEMPLATE,
            acc_modifiers=self.acc_modifiers,
            variable_name=self.variable_name,
            value=self.value,
            end=self.semicolon
        )


class ArrowFunctionType(Node):

    def __init__(self, name):
        super().__init__()
        self.function_name = camel_function_style(name)
        self.parameter_dict = {}
        self.function_body = []
        self.needed_constructor_param = []
        self.needed_import = []

    def add_needed_import(self, import_node):
        self.needed_import.append(import_node)

    def add_needed_constructor_param(self, constructor_param):
        self.needed_constructor_param.append(constructor_param)

    def add_param(self, var_decl):
        self.parameter_dict[var_decl.variable_name] = var_decl

    def add_statements_to_body(self, list_of_statements):
        for statement in list_of_statements:
            self.add_statement_to_body(statement)

    def add_statement_to_body(self, statement):
        self.function_body.append(statement)

    def render(self):
        # Parameter list
        parameter_list = []
        for _, param in self.parameter_dict.items():
            parameter_list.append(param.render())

        return eseight_writer(ARROW_FUNCTION_DECLARATION_TEMPLATE,
                              function_name=self.function_name,
                              function_body='\n'.join(self.function_body),
                              parameter_list=', '.join(parameter_list))


class FunctionDeclType(ArrowFunctionType):

    def __init__(self, name):
        super().__init__(name)
        self.function_type = ''
        self.function_return_type = ''

    def add_param(self, var_decl):
        self.parameter_dict[var_decl.variable_name] = var_decl

    def render(self):
        # Parameter list
        parameter_list = []
        for _, param in self.parameter_dict.items():
            parameter_list.append(param.render())

        return eseight_writer(FUNCTION_DECLARATION_TEMPLATE,
                              function_name=self.function_name,
                              function_type=self.function_type,
                              function_body='\n'.join(self.function_body),
                              parameter_list=', '.join(parameter_list),
                              function_return_type=self.function_return_type)


class EseightClassType(Node):

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

    def add_import_statement_using_import_node(self, import_node):
        try:
            # Check if the imported element already exist, if not then insert it
            for element in import_node.imported_elements:
                self.add_import_statement(import_node.main_module, element)
        except KeyError:
            # In case the import from the main module is never been declared before, then do the full import statement
            self.import_dict[import_node.main_module] = import_node

    def add_import_statement_for_multiple_element(self, main_module,
                                                  elements_imported):
        try:
            for element in elements_imported:
                self.add_import_statement(main_module, element)
        except KeyError:
            new_import_statement_node = ImportStatementType()
            new_import_statement_node.set_main_module(main_module)
            new_import_statement_node.add_imported_elements(elements_imported)
            self.import_dict[main_module] = new_import_statement_node

    def add_import_statement(self, main_module, element_imported):
        try:
            # Check if the imported element already exist, if not then insert it
            existing_import_node = self.import_dict[main_module]
            if not (
                    element_imported in existing_import_node.imported_elements):
                self.import_dict[main_module].add_imported_element(
                    element_imported)
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

        return eseight_writer(CLASS_ESEIGHT_TEMPLATE,
                              class_name=self.class_name,
                              constructor_param=','.join(
                                  constructor_param_list),
                              body='\n'.join(self.body),
                              import_statement_list='\n'.join(
                                  import_statement_list))
