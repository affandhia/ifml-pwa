from main.utils.ast.base import Node
from main.utils.ast.language.eseight import InstanceVarDeclType, \
    ImportStatementType, NormalMethodType
from main.utils.jinja.react import react_jsx_writer
from main.utils.naming_management import dasherize, camel_function_style, \
    creating_title_sentence_from_dasherize_word, camel_classify


class DataBindingFunction(Node):

    def __init__(self, name):
        self.var_camel_name = camel_function_style(name)
        self.property_declaration = None
        self.import_statement = None
        self.build_import_statement_and_property_declaration()
        self.func_decl = NormalMethodType('attach' + camel_classify(name))

    def build_import_statement_and_property_declaration(self):
        self.property_declaration = InstanceVarDeclType(self.var_camel_name)

    def add_statement_to_body(self, statement):
        self.func_decl.add_statement_to_body(statement)

    def get_property_name(self):
        return self.property_declaration.variable_name

    def get_function_declaration(self):
        return self.func_decl.render()

    def get_function_call(self):
        return 'this.{func_name}();'.format(
            func_name=self.func_decl.function_name)


class InputField(Node):
    """

    defaultValue: is javascript assignment statement, this will be the
    source of the element default value.
    """
    ANGULAR_TPYE_TO_HTML_CONVERSION = {'string': 'text', 'number': 'number',
                                       'boolean': 'text'}

    def __init__(self, name, datatype='string'):
        self.dasherize_name = dasherize(name)
        self.title_name = creating_title_sentence_from_dasherize_word(name)
        self.var_camel_name = camel_function_style(name)
        self.placeholder = True
        self.value = ''
        self.type = self.build_type(datatype)

    def build_type(self, input_type: str):
        try:
            return self.ANGULAR_TPYE_TO_HTML_CONVERSION[input_type]
        except KeyError:
            return 'text'

    def disable_placeholder(self):
        self.placeholder = False

    def set_default_value(self, value):
        self.value = value

    def render(self):
        return react_jsx_writer('form_input_field.jsx.template',
                                dasherize_name=self.dasherize_name,
                                title_name=self.title_name,
                                var_camel_name=self.var_camel_name + 'Input',
                                placeholder=self.placeholder, value=self.value,
                                type=self.type)


class VisualizationWithSpan(Node):

    def __init__(self, name, structural_feature_name, data_binding_name=''):
        self.title_name = creating_title_sentence_from_dasherize_word(name)
        self.dasherize_name = dasherize(name)
        self.attribute_name = structural_feature_name
        self.class_name = data_binding_name

    def render(self):
        return react_jsx_writer('visualization_with_span.jsx.template',
                                title_name=self.title_name,
                                dasherize_name=self.dasherize_name,
                                attribute_name=self.attribute_name,
                                class_name=self.class_name)
