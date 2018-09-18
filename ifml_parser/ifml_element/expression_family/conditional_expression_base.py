from .base import Expression
from ifml_parser.ifml_element.interaction_flow_elements.view_family.view_component_parts import ViewComponentPart

class ConditionalExpression(Expression, ViewComponentPart):
    CONDITIONAL_EXPRESSION_TAGNAME = 'conditionalExpression'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)