from main.utils.ast.base import Node
from main.utils.ast.language.typescript import VarDeclType, ImportStatementType, FunctionDeclType
from main.utils.jinja.angular import angular_html_writer
from main.utils.naming_management import dasherize, camel_function_style, \
    creating_title_sentence_from_dasherize_word, camel_classify


class DataBindingFunction(Node):

    def __init__(self, name, classfier_name):
        self.var_camel_name = camel_function_style(name)
        self.property_declaration = None
        self.import_statement = None
        self.build_import_statement_and_property_declaration(classfier_name)
        self.func_decl = FunctionDeclType('attach'+camel_classify(name))

    def build_import_statement_and_property_declaration(self, classifier_name):
        self.property_declaration = VarDeclType(self.var_camel_name, ';')
        self.property_declaration.variable_datatype = classifier_name
        self.property_declaration.acc_modifiers = 'public'

        self.import_statement = ImportStatementType()
        self.import_statement.add_imported_element(classifier_name)

        classifier_location = '../'+dasherize(classifier_name)+'/'+dasherize(classifier_name)+'.model.ts'
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

    def __init__(self, name, type='text'):
        self.dasherize_name = dasherize(name)
        self.title_name = creating_title_sentence_from_dasherize_word(name)
        self.var_camel_name = camel_function_style(name)
        self.placeholder = True
        self.value = ''
        self.type = self.build_type(type)
        self.ngmodel_property = VarDeclType(self.var_camel_name, semicolon=';')
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
