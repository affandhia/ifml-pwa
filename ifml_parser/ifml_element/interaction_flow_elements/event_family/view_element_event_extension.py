from .catching_event_extension import ViewElementEvent


class OnSelectEvent(ViewElementEvent):
    ON_SELECT_EVENT_TYPE = 'ext:OnSelectEvent'

    def __init__(self, xmiSchema, uml_symbol_table, ifml_symbol_table):
        super().__init__(xmiSchema, uml_symbol_table, ifml_symbol_table)


class OnSubmitEvent(ViewElementEvent):
    ON_SUBMIT_EVENT_TYPE = 'ext:OnSubmitEvent'

    def __init__(self, xmiSchema, uml_symbol_table, ifml_symbol_table):
        super().__init__(xmiSchema, uml_symbol_table, ifml_symbol_table)
