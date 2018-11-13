from .catching_event_extension import SystemEvent

class OnLoadEvent(SystemEvent):

    def __init__(self, xmiSchema, uml_symbol_table, ifml_symbol_table):
        super().__init__(xmiSchema, uml_symbol_table, ifml_symbol_table)