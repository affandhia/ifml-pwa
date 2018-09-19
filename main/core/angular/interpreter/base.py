from ifml_parser.ifml_element.interaction_flow_elements.view_family.view_containers import ViewContainer, Menu, Window
import logging

logger_ifml_angular_interpreter = logging.getLogger("main.core.angular.interpreter")

class IFMLtoAngularInterpreter(object):

    def __init__(self, ifml_xmi, class_diagram_xmi):
        self.root_ifml = ifml_xmi
        self.root_class_diagram_xmi = class_diagram_xmi
        self.project_name = self.root_ifml.name
        logger_ifml_angular_interpreter.debug("Interpreting {name} IFML Project".format(name=self.project_name))

        #Getting All IFML Elements
        self.ifml_expressing_ui_design = self.root_ifml.get_interaction_flow_model().get_interaction_flow_model_elements()

        #Getting All Domain Model Elements
        self.domain_model_used_by_ifml = self.root_ifml.get_domain_model()
        self.interpret_interaction_flow_model()

    def interpret_interaction_flow_model(self):
        for key, interaction_flow_model_element in self.ifml_expressing_ui_design.items():
            logger_ifml_angular_interpreter.debug(isinstance(interaction_flow_model_element,ViewContainer))


    def interpret_domain_model(self):
        pass