class UMLSymbolTable(object):

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

    def __init__(self, uml_dom):
        self.uml_dom = uml_dom
        self.uml_symbol_table = UMLSymbolTable()
        self.build()

    def build(self):
        pass