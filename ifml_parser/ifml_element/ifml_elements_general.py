from ifml_parser.general_model import Element


class InteractionFlowModelElement(Element):
    IFML_ELEMENTS_TAGNAME = 'interactionFlowModelElements'

    """
    General Class for Interaction Flow Model Element in XMI Document for IFML
    """
    def __init__(self, xmiSchema, uml_symbol_table, ifml_symbol_table):
        super().__init__(xmiSchema)
        self.uml_symbol_table = uml_symbol_table
        self.ifml_symbol_table = ifml_symbol_table

    def check_uml_reference(self, reference_string):
        reference_list = reference_string.split('#')
        uml_name = reference_list[0]
        id_symbol = reference_list[1]
        self.uml_symbol_table.lookup(uml_name, id_symbol)

    def check_ifml_reference(self, reference_string):
        self.ifml_symbol_table.lookup(reference_string)