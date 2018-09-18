from .boolean_expression_extension import Constraint

class ValidationRule(Constraint):

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)