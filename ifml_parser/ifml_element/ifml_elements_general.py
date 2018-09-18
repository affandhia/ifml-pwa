from ifml_parser.general_model import Element


class InteractionFlowModelElement(Element):
    IFML_ELEMENTS_TAGNAME = 'interactionFlowModelElements'

    """
    General Class for Interaction Flow Model Element in XMI Document for IFML
    """
    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)