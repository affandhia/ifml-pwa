from ifml_parser.ifml_element.expression_family.boolean_expression_extension import ActivationExpression
from ifml_parser.ifml_element.interaction_flow_elements.event_family.catching_event_extension import ViewElementEvent
from ifml_parser.ifml_element.interaction_flow_elements.event_family.view_element_event_extension import OnSubmitEvent, \
    OnSelectEvent
from ifml_parser.ifml_element.interaction_flow_elements.interaction_flow_base import InteractionFlowElement


class ViewElement(InteractionFlowElement):
    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._view_element_events = self.build_view_element_event()
        self._activation_expression = self.build_activation_expression()

    def build_view_element_event(self):
        dict_view_el_event = {}
        list_view_el_event_node = self.getElementsByTagName(
            ViewElementEvent.VIEW_ELEMENT_EVENT_TAGNAME)
        for view_el_event_element in list_view_el_event_node:
            view_el_type = view_el_event_element.getAttribute(self.XSI_TYPE)

            # If it's On Select Event
            if view_el_type == OnSelectEvent.ON_SELECT_EVENT_TYPE:
                on_select_event_instance = OnSelectEvent(view_el_event_element)
                dict_view_el_event.update({on_select_event_instance.get_id(): on_select_event_instance})

            # If it's On Submit Event
            if view_el_type == OnSubmitEvent.ON_SUBMIT_EVENT_TYPE:
                on_submit_event_instance = OnSubmitEvent(view_el_event_element)
                dict_view_el_event.update({on_submit_event_instance.get_id(): on_submit_event_instance})

            # If it's View Element Event
            else:
                view_el_event_instance = ViewElementEvent(view_el_event_element)
                dict_view_el_event.update({view_el_event_instance.get_id(): view_el_event_instance})
        return dict_view_el_event

    def get_view_element_events(self):
        return self._view_element_events

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
                print("There's something wrong in " + self.__class__.__name__ + ", to get Activation Expression")

    def get_activation_expression(self):
        return self._activation_expression
