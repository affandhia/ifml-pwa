import logging

from ifml_parser.ifml_element.interaction_flow_elements.view_family.view_containers import ViewContainer
from main.core.angular.interpreter.view_family import BaseViewContainerInterpreter
from . import BaseInterpreter
from main.utils.naming_management import dasherize

logger_ifml_angular_interpreter = logging.getLogger("main.core.angular.interpreter")


# Processing the all model and will return the AST of Angular that define the project structure of the IFML design
class IFMLtoAngularInterpreter(BaseInterpreter):

    def __init__(self, ifml_xmi, class_diagram_xmi):
        self.root_ifml = ifml_xmi
        self.root_class_diagram_xmi = class_diagram_xmi
        self.project_name = dasherize(self.root_ifml.name)
        self.component = {}
        logger_ifml_angular_interpreter.info("Interpreting {name} IFML Project".format(name=self.project_name))

        # Getting All IFML Elements
        self.ifml_expressing_ui_design = self.root_ifml.get_interaction_flow_model().get_interaction_flow_model_elements()

        # Getting All Domain Model Elements
        self.domain_model_used_by_ifml = self.root_ifml.get_domain_model()
        self.interpret_interaction_flow_model()
        self.interpret_domain_model()

    def get_project_name(self):
        return self.project_name

    def interpret_interaction_flow_model(self):
        for key, interaction_flow_model_element in self.ifml_expressing_ui_design.items():
            if isinstance(interaction_flow_model_element, ViewContainer):
                logger_ifml_angular_interpreter.info(
                    "Interpreting a {name}View Container".format(name=interaction_flow_model_element.get_name()))
                self.component[interaction_flow_model_element.get_id()] = BaseViewContainerInterpreter(
                    view_container=interaction_flow_model_element).build()

    def interpret_domain_model(self):
        pass