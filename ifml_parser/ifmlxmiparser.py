# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Name:        IFMLXMIParser.py
# Purpose:     Parse XMI (IFML-model) and provide a logical model of it
#
# Author:      Hafiyyan Sayyid Fadhlillah
#
# Created:     2018/02/28
# Licence:     GPL
# -----------------------------------------------------------------------------

import logging
import os.path
from xml.dom import minidom

from ifml_parser.domain_element.base import DomainElement
from ifml_parser.ifml_element.interaction_flow_elements.view_family.view_component_parts import ViewComponentPart, \
    SimpleField, Slot
from ifml_parser.ifml_element.interaction_flow_elements.view_family.view_components import ViewComponent, Details, List, \
    Form
from ifml_parser.ifml_element.interaction_flow_elements.view_family.view_containers import ViewContainer, Menu, Window
from ifml_parser.ifml_element.interaction_flow_elements.action_family.base import Action
from ifml_parser.ifml_element.ifml_elements_general import InteractionFlowModelElement
from ifml_parser.ifml_element.parameter_family.parameters import Parameter, ParameterBinding, ParameterBindingGroup
from ifml_parser.ifml_element.expression_family.base import Expression, InteractionFlowExpression, BooleanExpression
from ifml_parser.ifml_element.expression_family.boolean_expression_extension import ActivationExpression, Constraint
from ifml_parser.ifml_element.expression_family.conditional_expression_base import ConditionalExpression
from ifml_parser.ifml_element.expression_family.constraint_extension import ValidationRule
from ifml_parser.ifml_element.interaction_flow.base import InteractionFlow, DataFlow, NavigationFlow
from .general_model import Element, NamedElement

log = logging.getLogger('IFMLparser')


class InteractionFlowModel(Element):
    """
    to create concrete syntax for Interaction Flow Model in XMI Document for IFML
    """
    INTERACTION_FLOW_ATTRIBUTE = 'interactionFlowModel'


    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._interaction_flow_model_elements = self.build_ifml_elements()

    def build_ifml_elements(self):
        dict_ifml_elements = {}
        list_ifml_elements = self.getElementsByTagName(InteractionFlowModelElement.IFML_ELEMENTS_TAGNAME)
        for element in list_ifml_elements:
            element_type = element.getAttribute(self.XSI_TYPE)

            # If element is Menu (Ext)
            if element_type == Menu.MENU_TYPE:
                menu_element = Menu(element)
                dict_ifml_elements.update({menu_element.get_id(): menu_element})

            # If element is Windows (Ext)
            elif element_type == Window.WINDOWS_TYPE:
                windows_element = Window(element)
                dict_ifml_elements.update({windows_element.get_id(): windows_element})

            #If element is View Container
            elif element_type == ViewContainer.VIEW_CONTAINER_TYPE:
                view_container_element = ViewContainer(element)
                dict_ifml_elements.update({view_container_element.get_id(): view_container_element})

            #If element is List (Ext)
            elif element_type == List.LIST_TYPE:
                element_list = List(element)
                dict_ifml_elements.update({element_list.get_id(): element_list})

            #If element is Form (Ext)
            elif element_type == Form.FORM_TYPE:
                element_form = Form(element)
                dict_ifml_elements.update({element_form.get_id(): element_form})

            #If element is Detail (Ext)
            elif element_type == Details.DETAIL_TYPE:
                details_element = Details(element)
                dict_ifml_elements.update({details_element.get_id(): details_element})

            # If element is View Component
            elif element_type == ViewComponent.VIEW_COMPONENT_TYPE:
                view_component_element = ViewComponent(element)
                dict_ifml_elements.update({view_component_element.get_id(): view_component_element})

            #If element is View Component Part
            elif element_type == ViewComponentPart.VIEW_COMPONENT_PARTS_TYPE:
                view_component_part_element = ViewComponentPart(element)
                dict_ifml_elements.update({view_component_part_element.get_id(): view_component_part_element})

            #If element is SimpleField (Ext)
            elif element_type == SimpleField.SIMPLE_FIELD_TYPE:
                simple_field_element = SimpleField(element)
                dict_ifml_elements.update({simple_field_element.get_id(): simple_field_element})

            #If element is Slot (Ext)
            elif element_type == Slot.SLOT_TYPE:
                slot_element = Slot(element)
                dict_ifml_elements.update({slot_element.get_id(): slot_element})

            # If element is Slot (Ext)
            elif element_type == Action.ACTION_TYPE:
                action_element = Action(element)
                dict_ifml_elements.update({action_element.get_id(): action_element})

            # If element is Interaction Flow
            elif element_type == InteractionFlow.INTERACTION_FLOW_TYPE:
                interaction_flow_element = InteractionFlow(element)
                dict_ifml_elements.update({interaction_flow_element.get_id(): interaction_flow_element})

            # If element is Navigation Flow
            elif element_type == NavigationFlow.NAVIGATION_FLOW_TYPE:
                navigation_flow_element = NavigationFlow(element)
                dict_ifml_elements.update({navigation_flow_element.get_id(): navigation_flow_element})

            # If element is Navigation Flow
            elif element_type == DataFlow.DATA_FLOW_TYPE:
                data_flow_element = DataFlow(element)
                dict_ifml_elements.update({data_flow_element.get_id(): data_flow_element})

            # If element is Parameter
            elif element_type == Parameter.PARAMETER_TYPE:
                parameter_element = Parameter(element)
                dict_ifml_elements.update({parameter_element.get_id(): parameter_element})

            # If element is Parameter Binding
            elif element_type == ParameterBinding.PARAMETER_BINDING_TYPE:
                parameter_binding_element = ParameterBinding(element)
                dict_ifml_elements.update({parameter_binding_element.get_id(): parameter_binding_element})

            # If element is Parameter Binding Group
            elif element_type == ParameterBindingGroup.PARAMETER_BINDING_GROUP_TYPE:
                parameter_binding_group_element = ParameterBindingGroup(element)
                dict_ifml_elements.update({parameter_binding_group_element.get_id(): parameter_binding_group_element})

            else:
                pass
                # raise ValueError("Invalid Structure, needs Interaction Flow Model Element")

            '''
            # If element is Expression
            elif element_type == Expression.EXPRESSION_TYPE:
                expression_element = Expression(element)
                dict_ifml_elements.update({expression_element.get_id(): expression_element}
            
            # If element is Interaction Flow Expression
            elif element_type == InteractionFlowExpression.INTERACTION_FLOW_TYPE:
                interaction_flow_expression_element = InteractionFlowExpression(element)
                dict_ifml_elements.update({interaction_flow_expression_element.get_id(): interaction_flow_expression_element}
            
            # If element is Boolean Expression
            elif element_type == BooleanExpression.BOOLEAN_EXPRESSION_TYPE:
                boolean_expression_element = BooleanExpression(element)
                dict_ifml_elements.update({boolean_expression_element.get_id(): boolean_expression_element}
            
            # If element is Activation Expression
            elif element_type == ActivationExpression.ACTIVATION_EXPRESSION_TYPE:
                activation_expression_element = ActivationExpression(element)
                dict_ifml_elements.update({activation_expression_element.get_id(): activation_expression_element}
            
            # If element is Constraint
            elif element_type == Constraint.CONSTRAINT_TYPE:
                constraint_element = Constraint(element)
                dict_ifml_elements.update({constraint_element.get_id(): constraint_element}
            
            # If element is Conditional Expression
            elif element_type == ConditionalExpression.CONDITIONAL_EXPRESSION_TYPE:
                conditional_expression_element = ConditionalExpression(element)
                dict_ifml_elements.update({conditional_expression_element.get_id(): conditional_expression_element}
            
            # If element is Validation Rule
            elif element_type == ValidationRule.VALIDATION_RULE_TYPE:
                validation_rule_element = ValidationRule(element)
                dict_ifml_elements.update({validation_rule_element.get_id(): validation_rule_element}
            
            '''

        return dict_ifml_elements

    def get_interaction_flow_model_elements(self):
        return self._interaction_flow_model_elements


class DomainModel(NamedElement):
    """
    to create concrete syntax for Domain Model in XMI Document for IFML
    """
    DOMAIN_MODEL_ATTRIBUTE = 'domainModel'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._domain_concept = self.build_domain_concept()

    def build_domain_concept(self):
        dict_domain_concept = {}
        list_schema_domain_concept = self.getElementsByTagName('domainElements')
        for domain_element in list_schema_domain_concept:
            domain_element_instance = DomainElement(domain_element)
            dict_domain_concept[domain_element_instance.get_id()] = domain_element_instance

        return dict_domain_concept

    def get_list_domain_concept(self):
        return self._domain_concept


class IFMLModel(NamedElement):
    """
    to create concrete syntax for IFML Model in XMI Document for IFML
    """

    CORE_ATTRIBUTE = 'xmlns:core'
    EXT_ATTRIBUTE = 'xmlns:ext'

    #Add parameter of UML symbol table to be used in the process of parsing
    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self.core_version = str(self._schema.getAttribute(self.CORE_ATTRIBUTE)) if len(
            str(self._schema.getAttribute(self.CORE_ATTRIBUTE))) > 0 else "No Version Found"
        self.ext_version = str(self._schema.getAttribute(self.EXT_ATTRIBUTE)) if len(
            str(self._schema.getAttribute(self.EXT_ATTRIBUTE))) > 0 else "No Version Found"
        self._interaction_flow_model = self.build_interaction_flow_model()
        self._domain_model = self.build_domain_model()

    def build_interaction_flow_model(self):
        interaction_flow_model = None
        list_schema_interaction_flow_model = self.getElementsByTagName(InteractionFlowModel.INTERACTION_FLOW_ATTRIBUTE)
        if len(list_schema_interaction_flow_model) > 1:
            raise ValueError('XMI FIle invalid, Cannot have More than 1 InteractionFlowModel')
        else:
            if_model = InteractionFlowModel(list_schema_interaction_flow_model[0])
        return if_model

    def build_domain_model(self):
        domain_model = None
        list_schema_domain_model = self.getElementsByTagName(DomainModel.DOMAIN_MODEL_ATTRIBUTE)
        if len(list_schema_domain_model) > 1:
            raise ValueError('XMI FIle invalid, Cannot have More than 1 DomainModel')
        else:
            domain_model = DomainModel(list_schema_domain_model[0])
        return domain_model

    def get_interaction_flow_model(self):
        return self._interaction_flow_model

    def get_domain_model(self):
        return self._domain_model


def build_ifml_model(doc=None):
    """
        This method used for build IFMLModel Structure

        buildIFMLModel(doc) -> IFMLModel
    """
    #Parse the UML Model here and become input for IFML Model
    model = IFMLModel(doc.getElementsByTagName('core:IFMLModel')[0])

    return model


def parse(xmiFileName=None, xmiSchema=None, **kw):
    """
    This method used for initializing IFML parser

    parse(xmiFileName, xmiSchema) -> IFMLModel

    """

    # doc is variable that will store XMI strcuture that has been parsed
    doc = None
    log.info("Parsing...")
    if xmiFileName:
        suff = os.path.splitext(xmiFileName)[1].lower()

        '''
        IFML Model is OMG Standard Modeling Language, so to interchange data it will be using XMI Format.
        Because of that, file type for XMI Format usually is .xmi, .xml, or .core (Eclipse editor format)
        '''
        if suff in ('.xmi', '.xml', '.core'):
            log.debug("Opening %s ..." % suff)
            doc = minidom.parse(xmiFileName)
        else:
            raise TypeError('Input file not of the following types: .xmi, .xml, .core')
    else:
        doc = minidom.parseString(xmiSchema)

    root = build_ifml_model(doc=doc)
    log.debug("Created a root IFML parser.")
    return root
