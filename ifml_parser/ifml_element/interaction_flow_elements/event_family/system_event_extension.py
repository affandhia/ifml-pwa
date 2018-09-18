from .catching_event_extension import SystemEvent

class OnLoadEvent(SystemEvent):

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)