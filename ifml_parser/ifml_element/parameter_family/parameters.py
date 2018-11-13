from ifml_parser.ifml_element.interaction_flow_elements.interaction_flow_base import InteractionFlowModelElement
from ifml_parser.general_model import NamedElement, Element

class Parameter(InteractionFlowModelElement, NamedElement):
    NAME_ATTRIBUTE = 'name'
    DIRECTION_ATTRIBUTE = 'direction'
    TYPE_ATTRIBUTE = 'type'
    PARAMETER_TAGNAME = 'parameters'
    SOURCE_PARAMETER_ATTRIBUTE = 'sourceParameter'
    TARGET_PARAMETER_ATTRIBUTE = 'targetParameter'

    def __init__(self, xmiSchema, uml_symbol_table, ifml_symbol_table):
        super().__init__(xmiSchema, uml_symbol_table, ifml_symbol_table)
        self._direction = 'in' if len(self.set_direction()) < 1 else self.set_direction()
        self._default_value = self.build_expression()
        self._name = self.set_name()
        self._type = self.set_type()
        self.set_direction()

    def set_name(self):
        return self._schema.getAttribute(self.NAME_ATTRIBUTE)

    def get_name(self):
        return self._name

    def set_type(self):
        #Check if have child node
        correct_type = None
        flag_has_child = len(self._schema.childNodes) > 0
        if flag_has_child:
            correct_type = self.set_type_as_child_nodes()
        else:
            correct_type = self.set_type_as_attribute()
        return correct_type

    def set_type_as_attribute(self):
        return self._schema.getAttribute('type')

    def set_type_as_child_nodes(self):
        type_returned = ''
        try:
            type_node = self.getElementByTagName('type')
            #uml_type = type_node.getAttribute(self.XSI_TYPE)
            #href = type_node.getAttribute('href')
            type_returned = type_node.getAttribute('href')
        except IndexError:
            pass
        return type_returned

    def get_type(self):
        return self._type

    def set_direction(self):
        return self._schema.getAttribute(self.DIRECTION_ATTRIBUTE)

    def get_direction(self):
        return self._direction

    def build_expression(self):
        pass

class ParameterBinding(Element):

    PARAMETER_BINDINGS_TAGNAME = 'parameterBindings'

    def __init__(self, xmiSchema, uml_symbol_table, ifml_symbol_table):
        super().__init__(xmiSchema)
        self._source_parameter = self._schema.getAttribute(Parameter.SOURCE_PARAMETER_ATTRIBUTE)
        self._target_parameter = self._schema.getAttribute(Parameter.TARGET_PARAMETER_ATTRIBUTE)
        self.uml_symbol_table = uml_symbol_table
        self.ifml_symbol_table = ifml_symbol_table

    def get_source_parameter(self):
        return self._source_parameter

    def get_target_parameter(self):
        return self._target_parameter

class ParameterBindingGroup(Element):


    PARAMETER_BINDING_GROUP_TAGNAME = 'parameterBindingGroup'

    def __init__(self, xmiSchema, uml_symbol_table, ifml_symbol_table):
        super().__init__(xmiSchema)
        self.uml_symbol_table = uml_symbol_table
        self.ifml_symbol_table = ifml_symbol_table
        self._parameter_bindings = self.build_parameter_bindings()


    def build_parameter_bindings(self):
        dict_param_binding = {}
        list_param_binding = self._schema.getElementsByTagName(ParameterBinding.PARAMETER_BINDINGS_TAGNAME)
        for param in list_param_binding:
            param_binding = ParameterBinding(param, self.uml_symbol_table, self.ifml_symbol_table)
            dict_param_binding.update({param_binding.get_id() : param_binding})
        return dict_param_binding

    def get_parameter_bindings(self):
        return self._parameter_bindings