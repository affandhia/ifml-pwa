from six import string_types

class NoObject(object):
    pass

_marker = NoObject()

def getElementsExceptTextNode(domElement):

    elements = domElement.childNodes

    cleaned_els = []

    for element in elements:
        if not(element.nodeType == element.TEXT_NODE):
            cleaned_els.append(element)

    return cleaned_els

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


class UMLSymbolTable(object):

    def __init__(self):
        self.table = {}
        self.model_name = ''

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

    ID_ATTRIBUTE = 'xmi:id'
    NAME_ATTRIBUTE = 'name'
    TYPE_ATTRIBUTE = 'xmi:type'

    def __init__(self):
        self.id = None
        self.name = None

class ClassSymbol(Symbol):

    def __init__(self, class_dom):
        super().__init__()
        self.id = class_dom.getAttribute(self.ID_ATTRIBUTE)
        self.name = class_dom.getAttribute(self.NAME_ATTRIBUTE)

class TypeSymbol(Symbol):

    def __init__(self, type_dom):
        super().__init__()
        self.id = type_dom.getAttribute(self.ID_ATTRIBUTE)
        self.name = type_dom.getAttribute(self.NAME_ATTRIBUTE)
        self.type = type_dom.getAttribute(self.TYPE_ATTRIBUTE)


class PropertySymbol(Symbol):

    def __init__(self, property_element):
        super().__init__()
        self.id = property_element.getAttribute(self.ID_ATTRIBUTE)
        self.name = property_element.getAttribute(self.NAME_ATTRIBUTE)
        self.type = property_element.getAttribute(self.TYPE_ATTRIBUTE)

class OperationSymbol(Symbol):

    def __init__(self, operation_element):
        super().__init__()
        self.id = operation_element.getAttribute(self.ID_ATTRIBUTE)
        self.name = operation_element.getAttribute(self.NAME_ATTRIBUTE)

class UMLSymbolTableBuilder(object):

    OWNED_ATTRIBUTE = 'ownedAttribute'  # Attribute in element
    OWNED_OPERATION = 'ownedOperation'  # Opertaion in that element
    CLASS = 'uml:Class'  # Class tag
    PRIMITIVE_TYPE = 'uml:PrimitiveType'  # Creating a datatype
    DATA_TYPE = 'uml:DataType'

    def __init__(self, uml_dom):
        self.uml_dom = getElementByTagName(uml_dom, 'uml:Model')
        self.uml_symbol_table = UMLSymbolTable()
        self.uml_symbol_table.model_name = self.uml_dom.getAttribute('name')
        self.build()

    def build(self):
        for child in getElementsByTagName(self.uml_dom, 'packagedElement'):
            type_of_symbol = child.getAttribute('xmi:type')

            if type_of_symbol == self.CLASS:
                self.build_class(child)
                self.uml_symbol_table.insert(ClassSymbol(child))
            elif type_of_symbol == self.PRIMITIVE_TYPE or type_of_symbol == self.DATA_TYPE:
                self.uml_symbol_table.insert(TypeSymbol(child))
            else:
                raise Exception('{name} Not Yet Implemented, please Fix'.format(name=type_of_symbol))

        return self.uml_symbol_table

    def build_class(self, class_dom):
        for child in getElementsExceptTextNode(class_dom):
            if child.tagName == self.OWNED_ATTRIBUTE:
                self.uml_symbol_table.insert(PropertySymbol(child))
            elif child.tagName == self.OWNED_OPERATION:
                self.uml_symbol_table.insert(OperationSymbol(child))
