class ViewContainerIntepreter(object):

    def __init__(self, view_container):
        self.view_container = view_container

class BaseViewContainerInterpreter(ViewContainerIntepreter):

    def __init__(self, view_container):
        super().__init__(view_container)