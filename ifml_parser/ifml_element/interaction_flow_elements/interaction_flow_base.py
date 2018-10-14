from ifml_parser.ifml_element.ifml_elements_general import InteractionFlowModelElement
from ifml_parser.ifml_element.interaction_flow.base import InteractionFlow, NavigationFlow, DataFlow
from ifml_parser.ifml_element.parameter_family.parameters import Parameter


class InteractionFlowElement(InteractionFlowModelElement):

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._in_interaction_flows = self.build_interaction_flow(
            self._schema.getAttribute(InteractionFlow.IN_INTERACTION_FLOWS_TAGNAME))
        self._out_interaction_flows = self.build_interaction_flow(
            self._schema.getAttribute(InteractionFlow.OUT_INTERACTION_FLOWS_TAGNAME))
        self._parameter = self.build_parameters()

    def build_interaction_flow(self, selectedSchema):
        list_interaction_flows = selectedSchema.split(' ')
        return list_interaction_flows

    def get_in_interaction_flow(self):
        return self._in_interaction_flows

    def get_out_interaction_flow(self):
        return self._out_interaction_flows

    def build_parameters(self):
        dict_parameter = {}
        list_parameters = self.getElementsByTagName(Parameter.PARAMETER_TAGNAME)
        for param in list_parameters:
            instance_param = Parameter(param)
            dict_parameter.update({instance_param.get_id() : instance_param})
        return dict_parameter

    def get_parameters(self):
        return self._parameter
