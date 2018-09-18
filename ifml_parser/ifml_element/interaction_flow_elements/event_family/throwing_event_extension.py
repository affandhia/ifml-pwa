from .base import ThrowingEvent

class SetContextEvent(ThrowingEvent):
    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)

class JumpEvent(ThrowingEvent):
    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)