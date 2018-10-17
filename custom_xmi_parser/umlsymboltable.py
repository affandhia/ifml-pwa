
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

    def __init__(self):
        self.id = None

class ClassSymbol(Symbol):

    def __init__(self, class_dom):
        super().__init__()
        self.id = ''
        self.name = ''

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

class UMLSymbolTableBuilder(object):

    def __init__(self, uml_dom):
        self.uml_dom = uml_dom
        self.uml_symbol_table = UMLSymbolTable()
        self.build()

    def build(self):
        pass