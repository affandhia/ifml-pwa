from main.utils.ast.base import Node
from main.utils.ast.language.typescript import VarDeclType, ImportStatementType, FunctionDeclType
from main.utils.jinja.angular import angular_html_writer
from main.utils.naming_management import dasherize, camel_function_style, \
    creating_title_sentence_from_dasherize_word, camel_classify


class DataBindingFunction(Node):

    def __init__(self, name, model_node):
        self.var_camel_name = camel_function_style(name)
        self.property_declaration = None
        self.import_statement = None
        self.build_import_statement_and_property_declaration(model_node)
        self.func_decl = FunctionDeclType('attach'+camel_classify(name))

    def build_import_statement_and_property_declaration(self, model_node):
        self.property_declaration = VarDeclType(self.var_camel_name, ';')
        self.property_declaration.variable_datatype = model_node.class_name
        self.property_declaration.acc_modifiers = 'public'

        self.import_statement = ImportStatementType()
        self.import_statement.add_imported_element(model_node.class_name)

        classifier_location = '../models/'+dasherize(model_node.class_name)+'.model'
        self.import_statement.set_main_module(classifier_location)

    def add_statement_to_body(self, statement):
        self.func_decl.add_statement_to_body(statement)

    def get_property_name(self):
        return self.property_declaration.variable_name

    def get_function_declaration(self):
        return self.func_decl.render()

    def get_function_call(self):
        return 'this.{func_name}();'.format(func_name=self.func_decl.function_name)

class InputField(Node):

    ANGULAR_TPYE_TO_HTML_CONVERSION = {'string': 'text', 'number': 'number', 'boolean': 'text'}

    def __init__(self, name, datatype='string'):
        self.dasherize_name = dasherize(name)
        self.title_name = creating_title_sentence_from_dasherize_word(name)
        self.var_camel_name = camel_function_style(name)
        self.placeholder = True
        self.value = ''
        self.type = self.build_type(datatype)
        self.ngmodel_property = VarDeclType(self.var_camel_name, semicolon=';')
        self.ngmodel_property.variable_datatype = datatype
        self.ngmodel_property.acc_modifiers = 'public'

    def build_type(self, type):
        returned_type = None
        try:
            returned_type = self.ANGULAR_TPYE_TO_HTML_CONVERSION[type]
        except KeyError:
            returned_type = 'text'
        return returned_type

    def get_ngmodel_property(self):
        return self.ngmodel_property

    def disable_placeholder(self):
        self.placeholder = False

    def set_default_value(self, value):
        self.value = value

    def render(self):
        return angular_html_writer('form_input.html.template', dasherize_name=self.dasherize_name,
                                   title_name=self.title_name, var_camel_name=self.var_camel_name,
                                   placeholder=self.placeholder, value=self.value, type=self.type)

class VisualizationWithSpan(Node):

    def __init__(self, name, structural_feature_name, data_binding_name=''):
        self.title_name = creating_title_sentence_from_dasherize_word(name)
        self.dasherize_name = dasherize(name)
        self.attribute_name = structural_feature_name
        self.class_name = data_binding_name

    def render(self):
        return angular_html_writer('visualization_with_span.html.template', title_name=self.title_name,
                                   dasherize_name=self.dasherize_name, attribute_name=self.attribute_name,
                                   class_name=self.class_name)