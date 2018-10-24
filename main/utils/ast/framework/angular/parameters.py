from custom_xmi_parser.umlsymboltable import TypeSymbol
from main.utils.ast.base import Node
from main.utils.ast.language.typescript import VarDeclType, ImportStatementType
from main.utils.naming_management import camel_function_style, dasherize


class Parameter(Node):

    def __init__(self, name, type_node):
        self.var_camel_name = camel_function_style(name)

        # Checking the type
        self.is_primitive_type = self.check_if_parameter_type_is_primitive_type(type_node)

        self.type_name = self.build_parameter_type(type_node)

        # Needed Import Statement
        self.needed_import = self.build_needed_import(type_node)

    def build_parameter_type(self, type_node):
        returned_type = None
        if self.is_primitive_type:
            returned_type = type_node.name
        else:
            returned_type = type_node.class_name
        return returned_type

    def check_if_parameter_type_is_primitive_type(self, type_node):
        return isinstance(type_node, TypeSymbol)

    def build_needed_import(self, model_node):
        returned_import_node = None
        if not self.is_primitive_type:
            returned_import_node = ImportStatementType()
            returned_import_node.add_imported_element(model_node.class_name)

            classifier_location = '../models/' + dasherize(model_node.class_name) + '.model'
            returned_import_node.set_main_module(classifier_location)

        return returned_import_node

class OutParameter(Parameter):

    def __init__(self, name, type_node):
        super().__init__(name, type_node)


class InParameter(Parameter):

    def __init__(self, name, type_node):
        super().__init__(name, type_node)

        # Creating typescript code for defining proprty in child and parent
        self.parent_property = None
        self.child_property = None

        self.build_parent_and_child_param()

    def build_parent_and_child_param(self):
        self.build_parent_param()
        self.build_child_param()

    def build_parent_param(self):
        # Declaring the property
        self.parent_property = VarDeclType(self.var_camel_name, ';')
        self.parent_property.acc_modifiers = 'public'
        self.parent_property.variable_datatype = self.type_name

    def build_child_param(self):
        self.child_property = VarDeclType(self.var_camel_name, ';')
        self.child_property.acc_modifiers = 'public'
        self.child_property.variable_datatype = self.type_name
        self.child_property.decorator = '@Input()'
