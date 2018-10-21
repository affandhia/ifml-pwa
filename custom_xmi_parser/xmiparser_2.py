# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Name:        XMIParser.py
# Purpose:     Parse XMI (UML-model) and provide a logical model of it
#
# Author:      Philipp Auersperg
#
# Created:     2003/19/07
# Copyright:   (c) 2003-2008 BlueDynamics
# Licence:     GPL
# Modified By: Hafiyyan Sayyid Fadhlillah
# -----------------------------------------------------------------------------

import logging
import os.path
from xml.dom import minidom
from six import string_types
from .umlsymboltable import UMLSymbolTableBuilder

from enum import Enum

# Defining logging item
log = logging.getLogger('XMIparser')
XMI_25_version = '20131001'
# Set default wrap width
default_wrap_width = 64
has_stripogram = 1
try:
    from stripogram import html2text
except ImportError:
    has_stripogram = 0


    def html2text(s, *args, **kwargs):
        return s


class NoObject(object):
    pass


_marker = NoObject()
allObjects = {}


# START OF XMI UTILS METHOD#
def getSubElements(domElement):
    return [e for e in domElement.childNodes if e.nodeType == e.ELEMENT_NODE]


def getSubElement(domElement, default=_marker, ignoremult=0):
    els = getSubElements(domElement)
    if len(els) > 1 and not ignoremult:
        raise TypeError('more than 1 element found')
    try:
        return els[0]
    except IndexError:
        if default == _marker:
            raise
        else:
            return default


def getElementsByTagName(domElement, tagName, recursive=0):
    """Returns elements by tag name.

    The only difference from the original getElementsByTagName is
    the optional recursive parameter.
    """
    if isinstance(tagName, string_types):
        tagNames = [tagName]
    else:
        tagNames = tagName
    if recursive:
        els = []
        for tag in tagNames:
            els.extend(domElement.getElementsByTagName(tag))
    else:
        els = [el for el in domElement.childNodes
               if str(getattr(el, 'tagName', None)) in tagNames]
    return els


def getElementByTagName(domElement, tagName, default=_marker, recursive=0):
    """Returns a single element by name and throws an error if more
    than one exists.
    """
    els = getElementsByTagName(domElement, tagName, recursive=recursive)
    if len(els) > 1:
        raise TypeError('more than 1 element found')
    try:
        return els[0]
    except IndexError:
        if default == _marker:
            raise
        else:
            return default


def getAttributeValue(domElement, tagName=None, default=_marker, recursive=0, doReplace=False):
    el = domElement
    # el.normalize()
    if tagName:
        try:
            el = getElementByTagName(domElement, tagName, recursive=recursive)
        except IndexError:
            if default == _marker:
                raise
            else:
                return default
    if el.hasAttribute(XMI.VALUE):
        return el.getAttribute(XMI.VALUE)
    if not el.firstChild and default != _marker:
        return default


# END OF XMI UTILS METHOD#

class UMLSymbolTable:

    def __init__(self):
        self.table = {}

    def insert(self, symbol):
        self.table[symbol.id] = symbol

    def inserts(self, dict_symbol):
        for _, symbol in dict_symbol.items():
            self.insert(symbol)

    def lookup(self, symbol):
        try:
            return self.table[symbol.id]
        except KeyError:
            return None

class Symbol(object):

    def __init__(self):
        self.id = None

class ClassSymbol(Symbol):

    def __init__(self, class_element):
        super().__init__()
        self.id = class_element.get_model_id()
        self.name = class_element.get_model_name()

class DatatypeSymbol(Symbol):

    def __init__(self, id, name):
        super().__init__()
        self.id = id
        self.name = name

class PropertySymbol(Symbol):

    def __init__(self, property_element):
        super().__init__()
        self.id = property_element.get_model_id()
        self.name = property_element.get_model_name()
        self.type = property_element.get_type()

class OperationSymbol(Symbol):

    def __init__(self, operation_element):
        super().__init__()
        self.id = operation_element.get_model_id()
        self.name = operation_element.get_model_name()

class XMI2_0(object):
    # Main XML Tag
    PACKAGED_ELEMENT = 'packagedElement'  # Element in diagram
    OWNED_PARAMETER = 'ownedParameter'  # Parameter in element
    OWNED_ATTRIBUTE = 'ownedAttribute'  # Attribute in element
    PACKAGE_IMPORT = 'packageImport'  # Imported Package in element
    OWNED_RULE = 'ownedRule'  # Rule in element
    OWNED_COMMENT = 'ownedComment'  # Comment for that element
    OWNED_OPERATION = 'ownedOperation'  # Opertaion in that element
    MODEL = 'uml:Model'  # Model Tag in XMI UML
    GENERALIZATION = 'generalization'  # Id of generalization element
    MULT_MIN = 'lowerValue'
    MULT_MAX = 'upperValue'
    EANNOTATION = 'eAnnotations'
    OWNED_END = 'ownedEnd'  # Parameter in element
    TAG_TYPE = 'type'

    # XMI Attribute
    TYPE = 'xmi:type'  # Accessing attribute Packaged Element Type
    TYPE_XSI = 'xsi:type'
    NAME = 'name'  # Name of that tag
    AGGREGATION = 'aggregation'
    VALUE = 'value'
    ID = 'xmi:id'
    VISIBILITY = 'visibility'
    IS_ID = 'isID'
    IS_LEAF = 'isLeaf'
    IS_ABSTRACT = 'isAbstract'
    IS_STATIC = 'isStatic'
    IS_QUERY = 'isQuery'
    DIRECTION = 'direction'
    ATT_TYPE = 'type'

    # XMI Value
    PARAMETER = 'uml:Parameter'  # Parameter tag
    CONSTRAINT = 'uml:Constraint'  # Constraint tag
    CLASS = 'uml:Class'  # Class tag
    PACKAGE = 'uml:Package'  # Package tag
    PRIMITIVE_TYPE = 'uml:PrimitiveType'  # Creating a datatype
    OPERATION = 'uml:Operation'
    ASSOCIATION = 'uml:Association'
    DATA_TYPE = 'uml:DataType'
    INTERFACE = 'uml:Interface'
    ACTOR = "uml:Actor"
    STEREOTYPE = "uml:Stereotype"
    MEMBER_END = 'memberEnd'
    LITERAL_INTEGER = 'uml:LiteralInteger'
    LITERAL_BOOLEAN = 'uml:LiteralBoolean'
    LITERAL_STRING = 'uml:LiteralString'
    LITERAL_UNLIMITED_NATURAL = 'uml:LiteralUnlimitedNatural'

    def __init__(self, **kw):
        self.__dict__.update(kw)


class XMI2_5(XMI2_0):

    def get_content(self, doc, model_tag):

        content = getElementByTagName(doc, model_tag, recursive=0).childNodes
        return content

    def get_model(self, doc, model_tag):
        model = getElementByTagName(doc, model_tag, recursive=0)
        return model

    def get_type(self, doc):
        if doc.getAttribute(XMI.TYPE):
            return doc.getAttribute(XMI.TYPE)
        elif doc.getAttribute(XMI.TYPE_XSI):
            return doc.getAttribute(XMI.TYPE_XSI)
        else:
            raise ValueError('Attribute Type not Detected, possibly different tag value')


class EnumVisbility(Enum):
    none = 0


class XMIElement(object):
    model = None
    content = None

    def is_class(self, node):
        if node.nodeType != node.TEXT_NODE and XMI.get_type(node) == XMI.CLASS:
            return True
        else:
            return False

    def is_package(self, node):
        if node.nodeType != node.TEXT_NODE and XMI.get_type(node) == XMI.PACKAGE:
            return True
        else:
            return False

    def is_interface(self, node):
        if node.nodeType != node.TEXT_NODE and XMI.get_type(node) == XMI.INTERFACE:
            return True
        else:
            return False

    def is_primitive_types(self, node):
        if node.nodeType != node.TEXT_NODE and XMI.get_type(node) == XMI.PRIMITIVE_TYPE:
            return True
        else:
            return False

    def is_data_types(self, node):
        if node.nodeType != node.TEXT_NODE and XMI.get_type(node) == XMI.DATA_TYPE:
            return True
        else:
            return False

    def is_association(self, node):
        if node.nodeType != node.TEXT_NODE and XMI.get_type(node) == XMI.ASSOCIATION:
            return True
        else:
            return False

    def is_eannotation(self, node):
        if node.nodeType != node.TEXT_NODE and node.tagName == XMI.EANNOTATION:
            return True
        else:
            return False

    def is_package_import(self, node):
        if node.nodeType != node.TEXT_NODE and node.tagName == XMI.PACKAGE_IMPORT:
            return True
        else:
            return False

    def is_text_node(self, node):
        if node.nodeType == node.TEXT_NODE:
            return True
        else:
            return False

    def is_property(self, node):
        if node.nodeType != node.TEXT_NODE and node.tagName == XMI.OWNED_ATTRIBUTE:
            return True
        else:
            return False

    def is_operation(self, node):
        if node.nodeType != node.TEXT_NODE and node.tagName == XMI.OWNED_OPERATION:
            return True
        else:
            return False

    def is_generalization(self, node):
        if node.nodeType != node.TEXT_NODE and node.tagName == XMI.GENERALIZATION:
            return True
        else:
            return False

    def is_type_tag(self, node):
        if node.tagName == XMI.TAG_TYPE:
            return True
        else:
            return False

    def is_parameter(self, node):
        if node.nodeType != node.TEXT_NODE and node.tagName == XMI.OWNED_PARAMETER:
            return True
        else:
            return False

    def get_model_name(self):
        return self.model.getAttribute('name')

    def get_model_id(self):
        return self.model.getAttribute(XMI.ID)

    def get_value_visibility(self, node):
        return node.getAttribute(XMI.VISIBILITY)

    def set_is_query(self, node):
        return node.getAttribute(XMI.IS_QUERY)

    def set_is_abstract(self, node):
        return node.getAttribute(XMI.IS_ABSTRACT)

    def set_is_static(self, node):
        return node.getAttribute(XMI.IS_STATIC)

    def set_is_leaf(self, node):
        return node.getAttribute(XMI.IS_LEAF)


class XMIModel(XMIElement):
    global datatypes
    _isroot = 1
    _parent = None

    def __init__(self, doc):
        self.symtab = UMLSymbolTable()
        self._packages = {}
        self._classes = {}
        self._interfaces = {}
        self._data_types = {}
        self._association = {}
        self.document = doc
        self.model = XMI.get_model(doc, XMI.MODEL)
        self.content = XMI.get_content(doc, XMI.MODEL)
        self.build_diagrams()
        self._data_types = datatypes.copy()
        self.buildsymtab()

    def build_diagrams(self):
        diagram_els = self.content
        for el in diagram_els:
            if not (self.is_eannotation(el) or self.is_package_import(el) or self.is_text_node(el)):
                if self.is_class(el):
                    self._classes[str(el.getAttribute(XMI.ID))] = (XMIClass(el=el, package=None))
                elif self.is_package(el):
                    self._packages[str(el.getAttribute(XMI.ID))] = (XMIPackage(el=el, project=None))
                elif self.is_interface(el):
                    self._interfaces[str(el.getAttribute(XMI.ID))] = (XMIInterface(el=el))
                elif self.is_association(el):
                    self._association[str(el.getAttribute(XMI.ID))] = (XMIAssociation(el=el))
                elif self.is_primitive_types(el) or self.is_data_types(el):
                    pass
                else:
                    raise ValueError(XMI.get_type(el)+', not recognized in UML Class Diagram for Root Model')

    def get_packages(self):
        return self._packages

    def get_classes(self):
        return self._classes

    def get_association(self):
        return self._association

    def get_interfaces(self):
        return self._interfaces

    def get_datatypes(self):
        return self._data_types

    def find_class_from_packages(self, id, package_list):
        correct_class = None
        for package in package_list:
            correct_class = self.find_class_by_id(id, package.get_classes())
            if correct_class != None:
                break
        return correct_class

    def find_interface_from_packages(self, id, package_list):
        correct_interface = None
        for package in package_list:
            correct_class = self.find_interface_by_id(id, package.get_interfaces())
            if correct_class != None:
                break
        return correct_interface

    def find_class_by_id(self, id, class_list):
        try:
            return class_list[id]
        except KeyError:
            return None

    def find_interface_by_id(self, id, class_list):
        try:
            return class_list[id]
        except KeyError:
            return None

    def buildsymtab(self):
        for _, class_element in self._classes.items():
            self.symtab.insert(ClassSymbol(class_element))
            self.symtab.inserts(class_element.symtab.table)

        for _, datatype in self._data_types.items():
            self.symtab.insert(datatype)



class XMIPackage(XMIElement):
    isroot = 0

    def __init__(self, **kw):
        self._project = None
        self._visibility = 'public'
        self._is_abstract = 0
        self._classes = {}
        self._interfaces = {}
        self._packages = {}
        self._association = {}
        self.model = kw.get('el')
        self.content = self.model.childNodes
        self.set_project(kw.get('project'))
        self.build_diagrams()
        self._visibility = self.get_value_visibility(self.model) if self.get_value_visibility(
            self.model) != '' else 'public'

    def build_diagrams(self):
        package_name = self.get_model_name()
        diagram_els = self.content
        for el in diagram_els:
            # try:
            if not (self.is_eannotation(el) or self.is_text_node(el)):
                if self.is_class(el):
                    self._classes[str(el.getAttribute(XMI.ID))] = XMIClass(el=el, package=package_name)
                elif self.is_package(el):
                    self._packages[str(el.getAttribute(XMI.ID))] = XMIPackage(el=el, project=package_name)
                elif self.is_interface(el):
                    self._interfaces[str(el.getAttribute(XMI.ID))] = XMIInterface(el=el, package=package_name)
                elif self.is_association(el):
                    self._association[str(el.getAttribute(XMI.ID))] = (XMIAssociation(el=el))
                elif self.is_primitive_types(el) or self.is_data_types(el):
                    pass
                else:
                    raise ValueError(XMI.get_type(el)+', not recognized in UML Class Diagram for Package')

    def get_packages(self):
        return self._packages

    def get_classes(self):
        return self._classes

    def get_interfaces(self):
        return self._interfaces

    def get_visibility(self):
        return self._visibility

    def get_association(self):
        return self._association

    def set_project(self, new_project):
        self.project = new_project

    def get_project(self):
        return self.project

    def find_class_by_id(self, id, class_list):
        try:
            return class_list[id]
        except KeyError:
            return None

    def find_interface_by_id(self, id, class_list):
        try:
            return class_list[id]
        except KeyError:
            return None

    def find_class_from_packages(self, id, package_list):
        correct_class = None
        for package in package_list:
            correct_class = self.find_class_by_id(id, package.get_classes())
            if correct_class != None:
                break
        return correct_class

    def find_interface_from_packages(self, id, package_list):
        correct_interface = None
        for package in package_list:
            correct_class = self.find_interface_by_id(id, package.get_interfaces())
            if correct_class != None:
                break
        return correct_interface


class XMIClass(XMIElement):

    def __init__(self, *args, **kw):
        self.symtab = UMLSymbolTable()
        self._gen = {}
        self._package = None
        self._is_interface = 0
        self._is_abstract = 0
        self._is_leaf = 0
        self._visibility = 'public'
        self._properties = {}
        self._operations = {}
        log.debug("Initialising class.")
        # ugh, setPackage(). Handle this with some more generic zope3
        # parent() relation. [reinout]
        log.debug("Running XMIClass's init...")
        self.model = kw.get('el')
        self.content = self.model.childNodes
        self.build_class()
        self.set_package(kw.get('package'))
        self._visibility = self.get_value_visibility(self.model) if self.get_value_visibility(
            self.model) != '' else 'public'
        self._is_abstract = 1 if self.set_abstract(self.model) == 'true' else 0
        self._is_leaf = 1 if self.set_leaf(self.model) == 'true' else 0
        self.buildsymtab()

    def set_package(self, new_package):
        self._package = new_package

    def build_class(self):
        diagram_els = self.content
        for el in diagram_els:
            # try:
            if not (self.is_eannotation(el) or self.is_text_node(el)):
                if self.is_property(el):
                    self._properties[str(el.getAttribute(XMI.ID))] = XMIProperty(el=el)
                elif self.is_generalization(el):
                    self._gen[str(el.getAttribute(XMI.ID))] = str(self._set_generalization(el))
                elif self.is_operation(el):
                    self._operations[str(el.getAttribute(XMI.ID))] = XMIOperation(el=el)
                elif self.is_primitive_types(el) or self.is_data_types(el):
                    pass
                else:
                    raise ValueError(XMI.get_type(el)+', not recognized in UML Class Diagram')

    def buildsymtab(self):

        for _, property in self._properties.items():
            self.symtab.insert(PropertySymbol(property))

        for _, operation in self._operations.items():
            self.symtab.insert(OperationSymbol(operation))

    def _set_generalization(self, node):
        return node.getAttribute('general')

    def get_generalization(self):
        return self._gen

    def get_is_interface(self):
        return self._is_interface

    def get_visibility(self):
        return self._visibility

    def get_properties(self):
        return self._properties

    def get_operations(self):
        return self._operations

    def get_package(self):
        return self._package

    def set_abstract(self, node):
        return node.getAttribute(XMI.IS_ABSTRACT)

    def set_leaf(self, node):
        return node.getAttribute(XMI.IS_LEAF)


class XMIInterface(XMIClass):
    _is_interface = 1

class XMIOperation(XMIElement):

    def __init__(self, **kw):
        self._parameters = {}
        self.model = kw.get('el')
        self.content = self.model.childNodes
        self.set_parameters()

        self._is_ordered = False
        self._is_query = False
        self._is_unique = False
        self._upper = 1
        self._lower = 1
        self._is_static = False
        self._is_abstract = False
        self._is_leaf = False

        self._visibility = self.get_value_visibility(self.model) if self.get_value_visibility(
            self.model) != '' else False
        self._is_query = self.set_is_query(self.model) if self.set_is_query(self.model) != '' else False
        self._is_abstract = self.set_is_abstract(self.model) if self.set_is_abstract(self.model) != '' else False
        self._is_static = self.set_is_static(self.model) if self.set_is_static(self.model) != '' else False
        self._is_leaf = self.set_is_leaf(self.model) if self.set_is_leaf(self.model) != '' else False

    def set_parameters(self):
        diagram_els = self.content
        for el in diagram_els:
            if not (self.is_eannotation(el) or self.is_text_node(el)):
                if self.is_parameter(el):
                    self._parameters[str(el.getAttribute(XMI.ID))] = XMIParameter(el=el)
                else:
                    raise ValueError(XMI.get_type(el)+', not recognized in UML Class Diagram for Parameter')

    def is_parameter(self, node):
        if node.nodeType != node.TEXT_NODE and node.tagName == XMI.OWNED_PARAMETER:
            return True
        else:
            return False

    def get_parameters(self):
        return self._parameters

    def get_visibility(self):
        return self._visibility

    def get_is_query(self):
        return self._is_query

    def get_is_abstract(self):
        return self._is_abstract

    def get_is_static(self):
        return self._is_static

    def get_is_leaf(self):
        return self._is_leaf


class XMIParameter(XMIElement):

    def __init__(self, **kw):
        self._type = None
        self.model = kw.get('el')
        self._lower = XMIMultiplicity(type=XMI.LITERAL_INTEGER, value=1)
        self._upper = XMIMultiplicity(type=XMI.LITERAL_INTEGER, value=1)
        self.content = self.model.childNodes
        self._direction = self.model.getAttribute(XMI.DIRECTION) if self.model.getAttribute(
            XMI.DIRECTION) != None else None
        self.build_param()
        self.set_type(self.model)

    def build_param(self):
        diagram_els = self.content
        for el in diagram_els:
            if not (self.is_text_node(el) or self.is_eannotation(el) or self.is_type_tag(el)):
                self.set_mult(el)

    def set_type(self, el):
        global datatypes
        try:
            curr_type = el.getAttribute(XMI.ATT_TYPE) if el.getAttribute(XMI.ATT_TYPE) != '' else XMI.get_type(el)
            self._type = datatypes[curr_type]
        except (KeyError, ValueError):
            for tag in self.content:
                if not ((self.is_text_node(tag) or self.is_eannotation(tag))) and self.is_type_tag(tag):
                    self._type = self._get_type_in_using_uml_primitive_type(tag)

    def get_type(self):
        return self._type

    def _get_type_in_using_uml_primitive_type(self, node):
        if node.tagName == 'type':
            return node.getAttribute('href').split('//')[-1]

    def set_mult(self, node):
        if node.tagName == 'upperValue':
            self._upper = XMIMultiplicity(node)
        elif node.tagName == 'lowerValue':
            self._lower = XMIMultiplicity(node)

    def get_param_direction(self):
        return self._direction

    def get_upper_value(self):
        return self._upper

    def get_lower_value(self):
        return self._lower


class XMIProperty(XMIElement):
    global datatypes

    def __init__(self, *args, **kw):
        self._is_id = 0
        self._type = None
        self._lower = XMIMultiplicity(type=XMI.LITERAL_INTEGER, value=1)
        self._upper = XMIMultiplicity(type=XMI.LITERAL_INTEGER, value=1)
        log.debug("Initialising class.")
        log.debug("Running XMIProperty's init...")
        self.model = kw.get('el')
        self.content = self.model.childNodes
        self.build_property()
        self._visibility = self.get_value_visibility(self.model) if self.get_value_visibility(
            self.model) != '' else 'public'
        self._aggregation_type = self.model.getAttribute('aggregation') if self.model.getAttribute(
            'aggregation') != '' else None
        self.set_is_id()
        self.set_type(self.model)

    def build_property(self):
        diagram_els = self.content
        for el in diagram_els:
            if not (self.is_text_node(el) or self.is_eannotation(el) or self.is_type_tag(el)):
                self.set_mult(el)

    def get_visibility(self):
        return self._visibility

    def get_data_type(self):
        return self._data_type

    def get_upper_value(self):
        return self._upper

    def get_lower_value(self):
        return self._lower

    def is_type_tag(self, node):
        if node.tagName == XMI.TAG_TYPE:
            return True
        else:
            return False

    def set_type(self, el):
        global datatypes
        try:
            curr_type = el.getAttribute(XMI.ATT_TYPE) if el.getAttribute(XMI.ATT_TYPE) != '' else XMI.get_type(el)
            self._type = datatypes[curr_type]
        except (KeyError, ValueError):
            for tag in self.content:
                if not ((self.is_text_node(tag) or self.is_eannotation(tag))) and self.is_type_tag(tag):
                    self._type = self._get_type_in_using_uml_primitive_type(tag)

    def get_type(self):
        return self._type

    def _get_type_in_using_uml_primitive_type(self, node):
        if node.tagName == 'type':
            return node.getAttribute('href').split('//')[-1]

    def set_mult(self, node):
        if node.tagName == 'upperValue':
            self._upper = XMIMultiplicity(node)
        elif node.tagName == 'lowerValue':
            self._lower = XMIMultiplicity(node)

    def get_model_name(self):
        return self.model.getAttribute('name')

    def set_is_id(self):
        if self.model.getAttribute('isID') == 'true':
            self._is_id = 1
        else:
            self._is_id = 0

    def get_is_id(self):
        return self._is_id


class XMIMultiplicity(object):

    def __init__(self, el=None, type=None, value=None):
        self._type = type
        self._value = value
        self.model = el
        self.set_mult_type()
        self.set_value()

    def set_mult_type(self):
        if self.model != None:
            self._type = XMI.get_type(self.model)

    def set_value(self):
        if self.model != None:
            self._value = self.model.getAttribute(XMI.VALUE) if self.model.getAttribute(XMI.VALUE) != '' else 0

    def get_mult_type(self):
        return self._type

    def get_value(self):
        return self._value


class XMIAssociation(XMIElement):

    def __init__(self, **kw):
        self.model = kw.get('el')
        self._from_to = None
        self._end_to = None
        self._owned_end_desc = {}
        self.content = self.model.childNodes
        self.set_member()
        self.set_owned_end_desc()

    def get_from_to(self):
        return self._owned_end_desc[str(self._from_to)]

    def get_end_to(self):
        return self._owned_end_desc[str(self._end_to)]

    def get_model_name(self):
        return self.model.getAttribute('name')

    def set_member(self):
        member_end = self.model.getAttribute(XMI.MEMBER_END)
        self._from_to, self._end_to = member_end.split(' ')

    def set_owned_end_desc(self):
        list_of_end_element = self.content
        for child in list_of_end_element:
            if not self.is_text_node(child):
                if self.is_owned_end(child):
                    self._owned_end_desc[str(child.getAttribute(XMI.ID))] = XMIProperty(el=child)
                elif self.is_eannotation(child):
                    pass
                else:
                    raise ValueError(child.tagName+' type'+XMI.get_type(child)+' %s, not recognized in UML Class Diagram for Association')

    def is_owned_end(self, node):
        if node.nodeType != node.TEXT_NODE and node.tagName == XMI.OWNED_END:
            return True
        else:
            return False


# START XMI TOOLS UTILS#
def collectTagDefinitions(self, el, prefix=''):
    tagdefs = el.getElementsByTagName(self.TAG_DEFINITION)
    if self.tagDefinitions is None:
        self.tagDefinitions = {}
    for t in tagdefs:
        if t.hasAttribute('name'):
            self.tagDefinitions[prefix + t.getAttribute('xmi:id')] = t


def buildDataTypes(doc, profile=''):
    global datatypes
    global datatypenames
    if profile:
        log.debug("DataType profile: %s", profile)
        getId = lambda e: profile + "#" + str(e.getAttribute('xmi:id'))
        getName = lambda e: profile + "#" + str(e.getAttribute('name'))
    else:
        getId = lambda e: str(e.getAttribute('xmi:id'))
        getName = lambda e: str(e.getAttribute('name'))

    dts = doc.getElementsByTagName(XMI.PACKAGED_ELEMENT)  # doc.getElementsByTagName(XMI.DATATYPE)

    for dt in dts:
        '''
            If datatype is one of this category
            1. Created Primitive Type
            2. Created Class
            3. Created Interface
            4. Created Actor
        '''
        if (XMI.get_type(dt) == XMI.DATA_TYPE) or (XMI.get_type(dt) == XMI.CLASS) or \
                (XMI.get_type(dt) == XMI.INTERFACE) or (XMI.get_type(dt) == XMI.ACTOR) or \
                (XMI.get_type(dt) == XMI.PRIMITIVE_TYPE):

            id = getId(dt)
            name = getName(dt)

            datatypes[getId(dt)] = DatatypeSymbol(id, name)

    # prefix = profile and profile + "#" or ''
    # XMI.collectTagDefinitions(doc, prefix=prefix)


def buildStereoTypes(doc, profile=''):
    global stereotypes
    if profile:
        log.debug("Stereotype profile: %s", profile)
        getId = lambda e: profile + "#" + str(e.getAttribute('xmi:id'))
    else:
        getId = lambda e: str(e.getAttribute('xmi:id'))

    sts = doc.getElementsByTagName(XMI.STEREOTYPE)

    for st in sts:
        id = st.getAttribute('xmi:id')
        if not id:
            continue
        stereotypes[getId(st)] = st
        # print 'stereotype:', id, XMI.getName(st)


def buildHierarchy(doc):
    """Builds Hierarchy out of the doc."""
    global datatypes
    global stereotypes
    global datatypenames
    global packages

    datatypes = {}
    stereotypes = {}

    buildDataTypes(doc)
    buildStereoTypes(doc)
    symbol_table = UMLSymbolTableBuilder(doc).build()
    res = XMIModel(doc)
    return res, symbol_table


def parse(xschemaFileName):
    """ """
    global XMI
    try:
        doc = None
        if xschemaFileName:
            suff = os.path.splitext(xschemaFileName)[1].lower()
            if suff in ('.xmi', '.xml', '.uml'):
                log.debug("Opening %s ..." % suff)
                doc = minidom.parse(xschemaFileName)
            else:
                raise TypeError('Input file not of the following types: .xmi, .xml, .uml')
        xmi = doc.getElementsByTagName('uml:Model')[0]
        xmiver = str(xmi.getAttribute('xmi:version'))
        log.debug("XMI version: %s", xmiver)
        if xmiver == XMI_25_version:
            XMI = XMI2_5()
        # NEED TO FIX THIS ELSE
        else:
            XMI = XMI2_5()
    except IOError:
        print("There's no file like this, please check the path again")
    except Exception:
        log.debug("No version info found, taking XMI2_0.")

    # XMI.generator = generator

    root = buildHierarchy(doc)
    log.debug("Created a root XMI parser.")

    return root
# END XMI TOOLS UTILS#
