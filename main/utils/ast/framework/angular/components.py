from main.utils.ast.base import Node
from main.utils.ast.language.typescript import ImportStatementType, TypescriptClassType
from main.utils.jinja.angular import component_file_writer
from main.utils.naming_management import dasherize, classify

from .base import ANGULAR_CORE_MODULE

class AngularComponent(Node):
    SUFFIX_TYPESCRIPT_COMPONENT_FILENAME = '.component.ts'
    SUFFIX_HTML_COMPONENT_FILENAME = '.component.html'

    def __init__(self, component_name, component_typescript_class, component_html):
        self.component_name = component_name
        self.component_typescript_class = component_typescript_class
        self.component_html = component_html

    def build(self):
        typescript_component_name = self.component_name + self.SUFFIX_TYPESCRIPT_COMPONENT_FILENAME
        typescript_html_name = self.component_name + self.SUFFIX_HTML_COMPONENT_FILENAME
        return {self.component_name: {typescript_component_name: self.component_typescript_class.render(),
                                      typescript_html_name: self.component_html.render()}}


class AngularComponentTypescriptClass(TypescriptClassType):
    def __init__(self):
        super().__init__()
        self.selector_name = ''
        self.component_name = ''

        # Adding import statement for Basic Component
        import_component_from_angular_core = ImportStatementType()
        import_component_from_angular_core.set_main_module(ANGULAR_CORE_MODULE)
        import_component_from_angular_core.add_imported_element('Component')
        self.import_dict[ANGULAR_CORE_MODULE] = import_component_from_angular_core

    def set_component_selector_class_name(self, name):
        self.selector_name = dasherize(name)
        self.class_name = classify(name)
        self.component_name = dasherize(name)

    def set_selector_name(self, selector_name):
        self.selector_name = selector_name

    def set_component_name(self, component_name):
        self.component_name = component_name

    def render(self):
        # Rendering all import statement
        import_statement_list = []
        for _, import_statement in self.import_dict.items():
            import_statement_list.append(import_statement.render())

        return component_file_writer('basic.component.ts.template', selector_name=self.selector_name,
                                     class_name=self.class_name, component_name=self.component_name,
                                     constructor=', '.join(self.constructor), body='\n'.join(self.body),
                                     import_statement_list='\n'.join(import_statement_list))


class AngularComponentHTML(Node):
    def __init__(self):
        self.body = []

    def render(self):
        return component_file_writer('basic.component.html.template', body='\n'.join(self.body))