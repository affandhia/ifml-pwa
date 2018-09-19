import logging

from main.utils.ast.framework.angular.components import AngularComponent, AngularComponentTypescriptClass, AngularComponentHTML

view_container_interpreter_logging = logging.getLogger("main.core.angular.interpreter.view_family")

#Class that receive a view container notation as instantiation and return an AngularComponent Class
class ViewContainerIntepreter(object):

    def __init__(self, view_container):
        self.view_container = view_container

#Class that receive Base View Container, meaning that this View Container is located at the 1st level
class BaseViewContainerInterpreter(ViewContainerIntepreter):

    def __init__(self, view_container):
        super().__init__(view_container)
        view_container_interpreter_logging.debug("{name} is being interpreted".format(name=view_container.get_name()))