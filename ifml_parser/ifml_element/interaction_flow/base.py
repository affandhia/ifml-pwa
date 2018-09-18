from ifml_parser.ifml_element.ifml_elements_general import InteractionFlowModelElement
from ifml_parser.ifml_element.parameter_family.parameters import ParameterBindingGroup


class InteractionFlow(InteractionFlowModelElement):

    INTERACTION_FLOW_TAGNAME = 'interactionFlow'
    INTERACTION_FLOW_TYPE = 'core:InteractionFlow'

    OUT_INTERACTION_FLOWS_TAGNAME = 'outInteractionFlows'
    IN_INTERACTION_FLOWS_TAGNAME = 'inInteractionFlows'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._parameter_binding_group = self.build_param_binding_group()

    def build_param_binding_group(self):
        dict_param_binding_groups = {}
        list_param_binding_groups = self.getElementsByTagName(ParameterBindingGroup.PARAMETER_BINDING_GROUP_TAGNAME)
        for instance in list_param_binding_groups:
            param_binding_group = ParameterBindingGroup(instance)
            dict_param_binding_groups.update({param_binding_group.get_id(): param_binding_group})
        return dict_param_binding_groups

    def get_parameter_binding_groups(self):
        return self._parameter_binding_group


class NavigationFlow(InteractionFlow):
    NAVIGATION_FLOW_TYPE = 'core:NavigationFlow'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)


class DataFlow(InteractionFlow):
    DATA_FLOW_TYPE = 'core:DataFlow'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
