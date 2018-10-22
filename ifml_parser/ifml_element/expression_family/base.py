from ifml_parser.ifml_element.ifml_elements_general import InteractionFlowModelElement
from ifml_parser.ifml_element.interaction_flow.base import InteractionFlow, DataFlow, NavigationFlow


class Expression(InteractionFlowModelElement):

    LANGUAGE_ATTRIBUTE = 'language'
    BODY_ATTRIBUTE = 'body'
    TRIGGERING_EXPRESSION_TAGNAME = 'triggeringExpressions'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._language = self._schema.getAttribute(self.LANGUAGE_ATTRIBUTE)
        self._body = self._schema.getAttribute(self.BODY_ATTRIBUTE)

    def get_language(self):
        return self._language

    def get_body(self):
        return self._body

class InteractionFlowExpression(Expression):
    INTERACTION_FLOW_EXPRESSION_ATTRIBUTE = 'interactionFlowExpression'
    MULTIPLE_INT_FLOW_EXP_IN_EVENT = "Event can't have more than one Interaction Flow Expression"

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._interaction_flow = self.build_interaction_flow()

    def build_interaction_flow(self):
        dict_interaction_flows = {}
        list_interaction_flows = self._schema.getAttribute(InteractionFlow.INTERACTION_FLOW_TAGNAME)
        for int_flow in list_interaction_flows:
            int_flow_type = int_flow.getAttribute(self.XSI_TYPE)

            #If it's navigation flow
            if int_flow_type == NavigationFlow.NAVIGATION_FLOW_TYPE:
                nav_flow = NavigationFlow(int_flow_type)
                dict_interaction_flows.update({nav_flow.get_id() : nav_flow})

            # If it's data flow
            elif int_flow_type == DataFlow.DATA_FLOW_TYPE:
                data_flow = DataFlow(int_flow_type)
                dict_interaction_flows.update({data_flow.get_id() : data_flow})

            # If it's interaction flow
            elif int_flow_type == InteractionFlow.INTERACTION_FLOW_TYPE:
                int_flow_instance = InteractionFlow(int_flow_type)
                dict_interaction_flows.update({int_flow_instance.get_id() : int_flow_instance})

        return dict_interaction_flows

class BooleanExpression(Expression):

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)


