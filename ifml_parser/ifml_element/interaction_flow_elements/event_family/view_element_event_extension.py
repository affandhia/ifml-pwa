from .catching_event_extension import ViewElementEvent


class OnSelectEvent(ViewElementEvent):
    ON_SELECT_EVENT_TYPE = 'ext:OnSelectEvent'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)


class OnSubmitEvent(ViewElementEvent):
    ON_SUBMIT_EVENT_TYPE = 'ext:OnSubmitEvent'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
