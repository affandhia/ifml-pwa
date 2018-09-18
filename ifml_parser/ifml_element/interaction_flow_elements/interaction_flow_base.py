from ifml_parser.ifml_element.ifml_elements_general import InteractionFlowModelElement
from ifml_parser.ifml_element.interaction_flow.base import InteractionFlow, NavigationFlow, DataFlow
from ifml_parser.ifml_element.parameter_family.parameters import Parameter


class InteractionFlowElement(InteractionFlowModelElement):

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._in_interaction_flows = self.build_interaction_flow(
            self.getElementsByTagName(InteractionFlow.IN_INTERACTION_FLOWS_TAGNAME))
        self._out_interaction_flows = self.build_interaction_flow(
            self.getElementsByTagName(InteractionFlow.OUT_INTERACTION_FLOWS_TAGNAME))
        self._parameter = self.build_parameters()

    def build_interaction_flow(self, selectedSchema):
        dict_interaction_flows = {}
        list_interaction_flows = selectedSchema
        for int_flow_element in list_interaction_flows:
            instance = int_flow_element.getAttribute(self.XSI_TYPE)
            # If it's navigation flow
            if instance == NavigationFlow.NAVIGATION_FLOW_TYPE:
                nav_flow = NavigationFlow(int_flow_element)
                dict_interaction_flows.update({nav_flow.get_id(): nav_flow})

            # If it's data flow
            elif instance == DataFlow.DATA_FLOW_TYPE:
                data_flow = DataFlow(int_flow_element)
                dict_interaction_flows.update({data_flow.get_id(): data_flow})

            # If it's interaction flow
            elif instance == InteractionFlow.INTERACTION_FLOW_TYPE:
                int_flow_instance = InteractionFlow(int_flow_element)
                dict_interaction_flows.update({int_flow_instance.get_id(): int_flow_instance})
        return dict_interaction_flows

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
