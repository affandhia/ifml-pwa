from ifml_parser.ifml_element.interaction_flow_elements.interaction_flow_base import InteractionFlowElement
from ifml_parser.ifml_element.expression_family.boolean_expression_extension import ActivationExpression
from ifml_parser.ifml_element.interaction_flow_elements.event_family.catching_event_extension import ViewElementEvent
from ifml_parser.ifml_element.parameter_family.parameters import Parameter


class ViewComponentPart(InteractionFlowElement):
    TYPE_TAGNAME = 'type'
    TYPE_ATTRIBUTE = 'type'
    HREF_ATTRIBUTE = 'href'
    VIEW_COMPONENT_PARTS_TYPE = 'core:ViewComponentPart'
    SUB_VIEW_COMPONENT_PARTS_TAGNAME = 'subViewComponentParts'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._type = self.set_type()
        self._activation_expression = self.build_activation_expression()
        self._view_element_events = self.build_view_element_event()
        self._name = self.set_name()
        self._sub_view_component_parts = self.build_view_component_parts()

    def build_view_component_parts(self):
        dict_view_component_parts = {}
        list_view_component_parts_node = self.getElementsByTagName(
            self.SUB_VIEW_COMPONENT_PARTS_TAGNAME)
        for view_comp_part in list_view_component_parts_node:
            view_comp_part_type = view_comp_part.getAttribute(self.XSI_TYPE)

            if view_comp_part_type == self.VIEW_COMPONENT_PARTS_TYPE:
                view_comp_part_element = ViewComponentPart(view_comp_part)
                dict_view_component_parts.update({view_comp_part_element.get_id(): view_comp_part_element})

            elif view_comp_part_type == SimpleField.SIMPLE_FIELD_TYPE:
                simple_field_element = SimpleField(view_comp_part)
                dict_view_component_parts.update({simple_field_element.get_id(): simple_field_element})

            elif view_comp_part_type == Slot.SLOT_TYPE:
                slot_element = Slot(view_comp_part)
                dict_view_component_parts.update({slot_element.get_id(): slot_element})

            elif view_comp_part_type == DataBinding.DATA_BINDING_TYPE:
                data_binding_element = DataBinding(view_comp_part)
                dict_view_component_parts.update({data_binding_element.get_id(): data_binding_element})

            elif view_comp_part_type == DynamicBehavior.DYNAMIC_BEHAVIOUR_TYPE:
                dynamic_behaviour_element = DynamicBehavior(view_comp_part)
                dict_view_component_parts.update({dynamic_behaviour_element.get_id(): dynamic_behaviour_element})

            elif view_comp_part_type == VisualizationAttribute.VISUALIZATION_ATTRIBUTE_TYPE:
                visualization_attribute_element = VisualizationAttribute(view_comp_part)
                dict_view_component_parts.update(
                    {visualization_attribute_element.get_id(): visualization_attribute_element})

        return dict_view_component_parts

    def get_sub_view_component_parts(self):
        return self._sub_view_component_parts

    def set_type(self):
        # Check if have child node
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
            uml_type = type_node.getAttribute(self.XSI_TYPE)
            href = type_node.getAttribute('href')
            type_returned = href
        except IndexError:
            pass
        return type_returned

    def get_type(self):
        return self._type

    def set_name(self):
        return self._schema.getAttribute('name')

    def get_name(self):
        return self._name

    def build_triggering_expression(self):
        dict_activation_expression = {}
        list_activation_expression_node = self.getElementsByTagName(
            ActivationExpression.ACTIVATION_EXPRESSION_ATTRIBUTE)

        for act_exp_element in list_activation_expression_node:
            act_exp_instance = ActivationExpression(act_exp_element)
            dict_activation_expression[act_exp_instance.get_id()] = act_exp_instance
        return dict_activation_expression

    def build_activation_expression(self):
        act_exp_instance = None
        try:
            node_int_flow_expression = self._schema.getAttribute(ActivationExpression.ACTIVATION_EXPRESSION_ATTRIBUTE)
            if len(node_int_flow_expression) < 2:
                int_flow_exp_instance = ActivationExpression(node_int_flow_expression[0])
            else:
                raise Exception(ActivationExpression.MULTIPLE_ACT_EXP_IN_EVENT)
        except IndexError:
            pass
        except Exception as e:
            if str(e) == ActivationExpression.MULTIPLE_ACT_EXP_IN_EVENT:
                print(e)
            else:
                print("There's something wrong in " + self.__class__.__name__ + ", to get Activation Expression")

    def get_activation_expression(self):
        return self._activation_expression

    def build_view_element_event(self):
        dict_view_el_event = {}
        list_view_el_event_node = self.getElementsByTagName(
            ViewElementEvent.VIEW_ELEMENT_EVENT_TAGNAME)

        for view_el_event_element in list_view_el_event_node:
            view_el_event_instance = ViewElementEvent(view_el_event_element)
            dict_view_el_event[view_el_event_instance.get_id()] = view_el_event_instance
        return dict_view_el_event

    def get_view_element_events(self):
        return self._view_element_events

class Field(ViewComponentPart, Parameter):

    FIELD_TYPE = 'ext:Field'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)

class SimpleField(Field):
    SIMPLE_FIELD_TYPE = 'ext:SimpleField'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)

class SelectionField(Field):
    SIMPLE_FIELD_TYPE = 'ext:SimpleField'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._is_multi_selection = self._schema.getAttribute('isMultiSelection')

class Slot(Field, Parameter):
    SLOT_TYPE = 'ext:Slot'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)


class VisualizationAttribute(ViewComponentPart):
    VISUALIZATION_ATTRIBUTE_TAGNAME = 'visualizationAttribute'
    VISUALIZATION_ATTRIBUTE_TYPE = 'core:VisualizationAttribute'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._name = self._schema.getAttribute('name')
        self._feature_concept = self._schema.getAttribute('featureConcept')

    def get_name(self):
        return self._name

    def get_feature_concept(self):
        return self._feature_concept


# ---------------------------------------------------#
'''Below is the implementation of Content Binding Base'''


# ---------------------------------------------------#

class ContentBinding(ViewComponentPart):

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._uniform_resource_identifier = self.build_uri()

    def build_uri(self):
        uri = None
        return uri


class DataBinding(ContentBinding):

    DATA_BINDING_TYPE = 'core:DataBinding'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._domain_concept = self._schema.getAttribute('domainConcept')
        self._conditional_expressions = self.build_conditional_expressions()
        self._data_context_variable = self.build_data_context_variable()

    def build_data_context_variable(self):
        from ifml_parser.ifml_element.context_family.base import DataContextVariable
        dict_data_context_variable = {}
        list_data_context_variable_node = self.getElementsByTagName(DataContextVariable.DATA_CONTEXT_VARIABLE_TYPE)
        for data_context_variable in list_data_context_variable_node:
            data_context_variable_element = DataContextVariable(data_context_variable)
            dict_data_context_variable.update({data_context_variable_element.get_id() : data_context_variable_element})
        return dict_data_context_variable

    def get_data_context_variable(self):
        return self._data_context_variable

    def build_conditional_expressions(self):
        from ifml_parser.ifml_element.expression_family.conditional_expression_base import ConditionalExpression
        dict_conditional_expressions = {}
        list_conditional_expressions_node = self.getElementsByTagName(
            ConditionalExpression.CONDITIONAL_EXPRESSION_TAGNAME)

        for cond_exp in list_conditional_expressions_node:
            cond_exp_element = ConditionalExpression(cond_exp)
            dict_conditional_expressions.update({cond_exp_element.get_id(): cond_exp_element})
        return dict_conditional_expressions

    def get_conditional_expressions(self):
        return self._conditional_expressions

    def get_domain_concept(self):
        return self._domain_concept

class DynamicBehavior(ContentBinding):
    from ifml_parser.ifml_element.interaction_flow_elements.action_family.base import Action

    DYNAMIC_BEHAVIOUR_TYPE = 'core:DynamicBehavior'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._action = self._schema.getAttribute('action')
        self._behavioral_feature_concept = self._schema.getAttribute('behavioralFeatureConcept')
        self._behavior_concept = self._schema.getAttribute('behaviorConcept')

    def get_action(self):
        return self._action
