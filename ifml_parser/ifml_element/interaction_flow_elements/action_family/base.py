from ifml_parser.ifml_element.interaction_flow_elements.interaction_flow_base import InteractionFlowElement
from ifml_parser.ifml_element.interaction_flow_elements.event_family.catching_event_extension import ActionEvent

class Action(InteractionFlowElement):

    ACTION_TYPE = 'core:IFMLAction'


    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._name = self.set_name()
        self._action_events = self.build_action_event()

    def set_name(self):
        return self._schema.getAttribute('name')

    def get_name(self):
        return self._name

    def build_action_event(self):
        dict_action_event = {}
        list_action_event = self.getElementsByTagName(ActionEvent.ACTION_EVENT_TAGNAME)
        for action_event_element in list_action_event:
            action_event_instance = ActionEvent(action_event_element)
            dict_action_event[action_event_instance.get_id()] = action_event_instance

        return dict_action_event

    def get_action_event(self):
        return self._action_events