from ifml_parser.general_model import Element, NamedElement


class Context(Element):

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._context_dimensions = self.build_context_dimensions()
        self._context_variable = self.build_context_variable()

    def build_context_variable(self):
        dict_context_variable = {}
        list_context_variable_node = self.getElementsByTagName(ContextVariable.CONTEXT_VARIABLE_TAGNAME)
        for context_variable in list_context_variable_node:
            context_variable_type = context_variable.getAttribute(self.XSI_TYPE)

            if context_variable_type == ContextVariable.CONTEXT_VARIABLE_TYPE:
                context_variable_element = ContextVariable(context_variable)
                dict_context_variable.update({context_variable_element.get_id(): context_variable_element})

            elif context_variable_type == SimpleContextVariable.SIMPLE_CONTEXT_VARIABLE_TYPE:
                simple_context_variable_element = SimpleContextVariable(context_variable)
                dict_context_variable.update(
                    {simple_context_variable_element.get_id(): simple_context_variable_element})

            elif context_variable_type == DataContextVariable.DATA_CONTEXT_VARIABLE_TYPE:
                data_context_variable_element = DataContextVariable(context_variable)
                dict_context_variable.update(
                    {data_context_variable_element.get_id(): data_context_variable_element})

        return dict_context_variable

    def get_context_variable(self):
        return self._context_variable

    def build_context_dimensions(self):
        dict_context_dimensions = {}
        list_context_dimensions_node = self.getElementsByTagName(ContextDimension.CONTEXT_DIMENSION_TAGNAME)
        for context_dimension in list_context_dimensions_node:
            context_dimension_type = context_dimension.getAttribute(self.XSI_TYPE)

            if context_dimension_type == ContextDimension.CONTEXT_DIMENSION_TYPE:
                context_dimension_element = ContextDimension(context_dimension)
                dict_context_dimensions.update({context_dimension_element.get_id(): context_dimension_element})

            elif context_dimension_type == Position.POSITION_TYPE:
                position_element = Position(context_dimension)
                dict_context_dimensions.update({position_element.get_id(): position_element})

            elif context_dimension_type == UserRole.USER_ROLE_TYPE:
                user_role_element = UserRole(context_dimension)
                dict_context_dimensions.update({user_role_element.get_id(): user_role_element})

            elif context_dimension_type == Device.DEVICE_TYPE:
                device_element = Device(context_dimension)
                dict_context_dimensions.update({device_element.get_id(): device_element})

    def get_context_dimensions(self):
        return self._context_dimensions


class ContextDimension(Context):
    CONTEXT_DIMENSION_TAGNAME = 'contextDimensions'
    CONTEXT_DIMENSION_TYPE = 'core:ContextDimension'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)


class Position(ContextDimension):
    POSITION_TYPE = 'ext:Position'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)


class UserRole(ContextDimension):
    USER_ROLE_TYPE = 'ext:UserRole'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)


class Device(ContextDimension):
    DEVICE_TYPE = 'ext:Device'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)


class ContextVariable(NamedElement):
    CONTEXT_VARIABLE_TAGNAME = 'contextVariables'
    CONTEXT_VARIABLE_TYPE = 'core:ContextVariable'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)


class DataContextVariable(ContextVariable):
    DATA_CONTEXT_VARIABLE_TYPE = 'core:DataContextVariable'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)


class SimpleContextVariable(ContextVariable):
    SIMPLE_CONTEXT_VARIABLE_TYPE = 'core:SimpleContextVariable'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)


class Viewpoint(Element):

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._context = self._schema.getAttribute('context')
