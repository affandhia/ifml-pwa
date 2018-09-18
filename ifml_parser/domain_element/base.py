from ifml_parser.general_model import NamedElement


class DomainElement(NamedElement):
    """
    to create concrete syntax for Domain Element in XMI Document for IFML
    """
    DATA_BINDING_ATTRIBUTE = 'dataBinding'
    CLASSIFIER_ATTRIBUTE = 'classifier'
    VISUALIZATION_ATTRIBUTE = 'visualizationAttribute'
    STRUCTURAL_FEATURE_ATTRIBUTE = 'structuralFeature'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)