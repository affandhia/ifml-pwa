import logging

from . import BaseInterpreter
from main.utils.ast.framework.angular.components import AngularComponent, AngularComponentTypescriptClass, AngularComponentHTML
from main.utils.naming_management import dasherize

view_container_interpreter_logging = logging.getLogger("main.core.angular.interpreter.view_family")


# Class that receive a view container notation as instantiation and return an AngularComponent Class
class ViewContainerIntepreter(BaseInterpreter):

    def __init__(self, view_container):
        self.view_container = view_container


# Class that receive Base View Container, meaning that this View Container is located at the 1st level
class BaseViewContainerInterpreter(ViewContainerIntepreter):

    def __init__(self, view_container):
        super().__init__(view_container)
        self.dasherize_name = dasherize(self.view_container.get_name())
        self.angular_component_node = None
        view_container_interpreter_logging.info("{name} is being interpreted".format(name=view_container.get_name()))

    def creating_angular_component_node(self):
        component_typescript = self.creating_angular_typescript_component_node()
        component_html = self.creating_angular_html_component_node()
        self.angular_component_node = AngularComponent(self.dasherize_name,
                                                       component_typescript_class=component_typescript,
                                                       component_html=component_html)

    def creating_angular_typescript_component_node(self):
        typescript_class = AngularComponentTypescriptClass()
        typescript_class.set_component_selector_class_name(self.dasherize_name)
        return typescript_class

    def creating_angular_html_component_node(self):
        html = AngularComponentHTML()
        return html

    def build(self):
        self.creating_angular_component_node()
        return self.angular_component_node