from main.utils.ast.language.typescript import TypescriptClassType, VarDeclType
from main.utils.jinja.angular import model_file_writer
from main.utils.naming_management import camel_classify, camel_function_style, dasherize


class ModelFromUMLClass(TypescriptClassType):
    FILENAME_TEMPLATE = '{filename}.model.ts'

    def __init__(self, class_name):
        super().__init__()
        self.class_name = camel_classify(class_name)
        self.filename = self.FILENAME_TEMPLATE.format(filename=dasherize(class_name))

    def add_owned_attribute_to_class(self, attribute_name, attribute_type):
        # Add Property Declaration for this attribute
        self.create_var_decl_for_owned_attribute(attribute_name, attribute_type)

        # Add constructor statement to add value from constructor
        self.create_constructor_body_to_add_value_based_on_constructor(attribute_name)

    def create_var_decl_for_owned_attribute(self, attribute_name, attribute_type):
        attribute_var_declaration = VarDeclType(camel_function_style(attribute_name), ';')
        attribute_var_declaration.variable_datatype = attribute_type
        attribute_var_declaration.acc_modifiers = 'public'
        self.set_property_decl(attribute_var_declaration)

    def create_constructor_body_to_add_value_based_on_constructor(self, attribute_name):
        # Template statement defined
        template_constructor_statement = 'this.{property_name} = obj && obj.{property_name} || null;'

        # Write statement based on the template
        intended_constructor_statement = template_constructor_statement.format(
            property_name=camel_function_style(attribute_name))

        # Add statement to constructor body
        self.constructor_body.append(intended_constructor_statement)

    def add_owned_operation_to_class(self, operation):
        print(operation)

    def render(self):
        # Rendering all property decl statement
        property_decl_list = []
        for _, prop in self.property_decl.items():
            property_decl_list.append(prop.render())

        return {self.filename: model_file_writer('basic.model.ts.template', class_name=self.class_name,
                                                 constructor_body=('\n'.join(self.constructor_body)),
                                                 body=('\n'.join(self.body)),
                                                 property_declaration='\n'.join(property_decl_list))}
