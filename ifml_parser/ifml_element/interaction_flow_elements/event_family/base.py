from ifml_parser.ifml_element.interaction_flow_elements.interaction_flow_base import InteractionFlowElement, InteractionFlow, NavigationFlow, DataFlow
from ifml_parser.ifml_element.expression_family.base import InteractionFlowExpression
from ifml_parser.ifml_element.expression_family.boolean_expression_extension import ActivationExpression

class Event(InteractionFlowElement):

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._interaction_flow_expression = self.build_int_flow_expression()
        self._activation_expression = self.build_activation_expression()
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

    def build_int_flow_expression(self):
        int_flow_exp_instance = None
        try:
            node_int_flow_expression = self._schema.getAttribute(InteractionFlowExpression.INTERACTION_FLOW_EXPRESSION_ATTRIBUTE)
            if len(node_int_flow_expression) < 2:
                int_flow_exp_instance = InteractionFlowExpression(node_int_flow_expression[0])
            else:
                raise Exception(InteractionFlowExpression.MULTIPLE_INT_FLOW_EXP_IN_EVENT)
        except IndexError:
            pass
        except Exception as e:
            if str(e) == InteractionFlowExpression.MULTIPLE_INT_FLOW_EXP_IN_EVENT:
                print(e)
            else:
                print("There's something wrong in "+ self.__class__.__name__+", to get Interaction Flow Expression")
        return int_flow_exp_instance

    def get_int_flow_expression(self):
        return self._interaction_flow_expression

    def build_activation_expression(self):
        act_exp_instance = None
        try:
            node_int_flow_expression = self._schema.getAttribute(ActivationExpression.ACTIVATION_EXPRESSION_ATTRIBUTE)
            if len(node_int_flow_expression) < 2:
                int_flow_exp_instance = ActivationExpression(node_int_flow_expression[0])
            else:
                raise Exception(ActivationExpression.MULTIPLE_ACT_EXP_IN_EVENT)
        except IndexError:
            pass
        except Exception as e:
            if str(e) == ActivationExpression.MULTIPLE_ACT_EXP_IN_EVENT:
                print(e)
            else:
                print("There's something wrong in "+ self.__class__.__name__+", to get Activation Expression")


    def get_activation_expression(self):
        return self._activation_expression

class CatchingEvent(Event):

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)


class ThrowingEvent(Event):

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
