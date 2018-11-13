from .boolean_expression_extension import Constraint

class ValidationRule(Constraint):

    def __init__(self, xmiSchema, uml_symbol_table, ifml_symbol_table):
        super().__init__(xmiSchema, uml_symbol_table, ifml_symbol_table)