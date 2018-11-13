from .base import BooleanExpression

class ActivationExpression(BooleanExpression):
    ACTIVATION_EXPRESSION_ATTRIBUTE = 'activationExpression'
    MULTIPLE_ACT_EXP_IN_EVENT = "Event can't have more than one Activation Expression"

    def __init__(self, xmiSchema, uml_symbol_table, ifml_symbol_table):
        super().__init__(xmiSchema, uml_symbol_table, ifml_symbol_table)

class Constraint(BooleanExpression):

    def __init__(self, xmiSchema, uml_symbol_table, ifml_symbol_table):
        super().__init__(xmiSchema, uml_symbol_table, ifml_symbol_table)