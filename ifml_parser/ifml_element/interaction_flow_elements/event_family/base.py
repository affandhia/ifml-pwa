from ifml_parser.ifml_element.interaction_flow_elements.interaction_flow_base import InteractionFlowElement
from ifml_parser.ifml_element.expression_family.base import InteractionFlowExpression
from ifml_parser.ifml_element.expression_family.boolean_expression_extension import ActivationExpression

class Event(InteractionFlowElement):

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._interaction_flow_expression = self.build_int_flow_expression()
        self._activation_expression = self.build_activation_expression()

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
