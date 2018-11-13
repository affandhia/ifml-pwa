from ifml_parser.ifml_element.ifml_elements_general import InteractionFlowModelElement
from ifml_parser.ifml_element.parameter_family.parameters import ParameterBindingGroup


class InteractionFlow(InteractionFlowModelElement):

    INTERACTION_FLOW_TAGNAME = 'interactionFlow'
    INTERACTION_FLOW_TYPE = 'core:InteractionFlow'

    OUT_INTERACTION_FLOWS_TAGNAME = 'outInteractionFlows'
    IN_INTERACTION_FLOWS_TAGNAME = 'inInteractionFlows'

    TARGET_INTERACTION_FLOW_ELEMENT_ATTRIBUTE = 'targetInteractionFlowElement'

    def __init__(self, xmiSchema, uml_symbol_table, ifml_symbol_table):
        super().__init__(xmiSchema, uml_symbol_table, ifml_symbol_table)
        self._parameter_binding_group = None
        self.build_param_binding_group()
        self._target_interaction_flow_element = xmiSchema.getAttribute(self.TARGET_INTERACTION_FLOW_ELEMENT_ATTRIBUTE)
        self.check_ifml_reference(self._target_interaction_flow_element)

    def build_param_binding_group(self):
        list_param_binding_groups = self.getElementsByTagName(ParameterBindingGroup.PARAMETER_BINDING_GROUP_TAGNAME)
        for instance in list_param_binding_groups:
            param_binding_group = ParameterBindingGroup(instance, self.uml_symbol_table, self.ifml_symbol_table)
            self._parameter_binding_group = param_binding_group

    def get_parameter_binding_groups(self):
        return self._parameter_binding_group

    def get_target_interaction_flow_element(self):
        return self._target_interaction_flow_element


class NavigationFlow(InteractionFlow):
    NAVIGATION_FLOW_TYPE = 'core:NavigationFlow'

    def __init__(self, xmiSchema, uml_symbol_table, ifml_symbol_table):
        super().__init__(xmiSchema, uml_symbol_table, ifml_symbol_table)


class DataFlow(InteractionFlow):
    DATA_FLOW_TYPE = 'core:DataFlow'

    def __init__(self, xmiSchema, uml_symbol_table, ifml_symbol_table):
        super().__init__(xmiSchema, uml_symbol_table, ifml_symbol_table)
