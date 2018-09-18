from .base import CatchingEvent
from ifml_parser.ifml_element.expression_family.base import Expression

class SystemEvent(CatchingEvent):

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._triggering_expression = self.build_triggering_expression()

    def build_triggering_expression(self):
        dict_triggering_expression = {}
        list_triggering_expression_node = self._schema.getElementsByTagName(
            Expression.TRIGGERING_EXPRESSION_TAGNAME)

        for trig_exp_element in list_triggering_expression_node:
            trig_exp_instance = Expression(trig_exp_element)
            dict_triggering_expression[trig_exp_instance.get_id()] = trig_exp_instance
        return dict_triggering_expression

    def get_triggering_expression(self):
        return self._triggering_expression

class ActionEvent(CatchingEvent):

    ACTION_EVENT_TAGNAME =  'actionEvents'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)

class ViewElementEvent(CatchingEvent):

    VIEW_ELEMENT_EVENT_TAGNAME = 'viewElementEvents'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)

class LandingEvent(CatchingEvent):

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
