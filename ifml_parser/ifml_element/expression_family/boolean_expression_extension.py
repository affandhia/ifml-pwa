from .base import BooleanExpression

class ActivationExpression(BooleanExpression):
    ACTIVATION_EXPRESSION_ATTRIBUTE = 'activationExpression'
    MULTIPLE_ACT_EXP_IN_EVENT = "Event can't have more than one Activation Expression"

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)

class Constraint(BooleanExpression):

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)