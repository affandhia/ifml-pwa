from custom_xmi_parser.umlsymboltable import TypeSymbol
from main.utils.ast.base import Node
from main.utils.ast.language.eseight import ImportStatementType, InstanceVarDeclType
from main.utils.jinja.angular import router_file_writer
from main.utils.naming_management import camel_function_style, dasherize
from .base import ANGULAR_CORE_MODULE


class Parameter(Node):

    def __init__(self, name, type_node):
        self.var_camel_name = camel_function_style(name)

        # Checking the type
        self.is_primitive_type = self.check_if_parameter_type_is_primitive_type(
            type_node)

        self.type_name = self.build_parameter_type(type_node)

        # Needed Import Statement
        self.needed_import = self.build_needed_import(type_node)

    def build_parameter_type(self, type_node):
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

            classifier_location = '../models/' + dasherize(
                model_node.class_name) + '.model'
            returned_import_node.set_main_module(classifier_location)

        return returned_import_node


class OutParameter(Parameter):

    def __init__(self, name, type_node):
        super().__init__(name, type_node)
        self.property = None
        self.build_param()

    def build_param(self):
        # Declaring the property
        self.property = InstanceVarDeclType(self.var_camel_name)
        self.property.acc_modifiers = 'public'
        self.property.variable_datatype = self.type_name


class InParameter(Parameter):

    def __init__(self, name, type_node):
        super().__init__(name, type_node)
        # Creating typescript code for defining proprty in child and parent
        self.parent_property = None
        self.child_property = None
        self.build_parent_and_child_param()

    def build_import_statement_input(self):
        self.input_import_statement = ImportStatementType()
        self.input_import_statement.set_main_module(ANGULAR_CORE_MODULE)
        self.input_import_statement.add_imported_element('Input')

    def build_parent_and_child_param(self):
        self.build_parent_param()
        self.build_child_param()

    def build_parent_param(self):
        # Declaring the property
        self.parent_property = InstanceVarDeclType(self.var_camel_name)
        self.parent_property.variable_datatype = self.type_name

    def build_child_param(self):
        self.child_property = InstanceVarDeclType(self.var_camel_name)
        self.child_property.variable_datatype = self.type_name


class ParamGroup(Node):

    def __init__(self):
        self.list_param = []

    def add_param_statement(self, param_statement):
        self.list_param.append(param_statement.render())

    def render(self):
        object_json_template = '{' + ','.join(self.list_param) + '}'
        return object_json_template


class ParameterBindingInterpretation(Node):
    """
    Generate parameter data binding/assignment. There are several ways data
    being assigned. Those are: Query, Action, Instance Variable.
    """

    def __init__(self, source_param_name, dest_param_name, from_action,
                 is_sent_through_routing):
        self.source_param_is_a_result_of_action = from_action
        self.this_param_binding_is_query_param = is_sent_through_routing
        self.source_param_name = camel_function_style(source_param_name)
        self.dest_param_name = camel_function_style(dest_param_name)

    def render(self):
        if self.this_param_binding_is_query_param:
            # Stringify the date whatever that are. This json value will be
            # used as a parameter in Query.
            return router_file_writer(
                'query_parameter_binding_interpretation.ts.template',
                target_param=self.dest_param_name,
                source_param=self.source_param_name,
                from_action=self.source_param_is_a_result_of_action
            )
        else:
            # If its from action then just get the data[<param>] value
            # Otherwise, get from instance variable:
            #   <param>: this.getParamValue
            return router_file_writer(
                'parameter_binding_interpretation.ts.template',
                target_param=self.dest_param_name,
                source_param=self.source_param_name,
                from_action=self.source_param_is_a_result_of_action
            )
