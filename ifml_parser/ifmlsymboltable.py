class IFMLSymbolTable(object):

    def __init__(self):
        self.table = {}

    def insert(self, scope_table):
        pass

    def lookup(self, reference_in_list):
        pass

class DomainModelSymbolTable(IFMLSymbolTable):

    def __init__(self):
        super().__init__()

    def insert(self, symbol):
        pass


class InteractionFlowModelSymbolTable(IFMLSymbolTable):

    def __init__(self):
        super().__init__()

    def insert(self, symbol):
        pass

class IFMLSymbol(object):

    ID_ATTRIBUTE = 'id'
    NAME_ATTRIBUTE = 'name'
    TYPE_ATTRIBUTE = 'xsi:type'

    def __init__(self, element_dom):
        self.id = element_dom.getAttribute(self.ID_ATTRIBUTE)
        self.name = element_dom.getAttribute(self.NAME_ATTRIBUTE)
        self.next_scope = element_dom.getAttribute(self.TYPE_ATTRIBUTE)
        self.tag_name = element_dom.tagName

    def set_next_scope(self, symbol_table):
        self.next_scope = symbol_table

class ViewContainer(IFMLSymbol):

    def __init__(self, element_dom):
        super().__init__(element_dom)


class Menu(IFMLSymbol):

    def __init__(self, element_dom):
        super().__init__(element_dom)

class Windows(IFMLSymbol):

    IS_MODAL_ATTRIBUTE = 'isModal'

    def __init__(self, element_dom):
        super().__init__(element_dom)
        self.is_modal = element_dom.getAttribute(self.IS_MODAL_ATTRIBUTE)

class List(IFMLSymbol):

    def __init__(self, element_dom):
        super().__init__(element_dom)


class Detail(IFMLSymbol):

    def __init__(self, element_dom):
        super().__init__(element_dom)


class Form(IFMLSymbol):

    def __init__(self, element_dom):
        super().__init__(element_dom)

class Action(IFMLSymbol):

    def __init__(self, element_dom):
        super().__init__(element_dom)

class Parameter(IFMLSymbol):

    def __init__(self, element_dom):
        super().__init__(element_dom)
        self.type = None

class VisualizationAttribute(IFMLSymbol):

    def __init__(self, element_dom):
        super().__init__(element_dom)
        self.type = None

class SimpleField(IFMLSymbol):

    def __init__(self, element_dom):
        super().__init__(element_dom)
        self.type = None

class DataBinding(IFMLSymbol):

    def __init__(self, element_dom):
        super().__init__(element_dom)
        self.classifier = None

class IFMLSymbolTableBuilder(object):

    def __init__(self, ifml_dom):
        self.uml_dom = ifml_dom
        self.ifml_symbol_table = IFMLSymbolTable()
        self.build_domain_model()
        self.build_interaction_flow_model()

    def build_domain_model(self):
        domain_model_table = DomainModelSymbolTable()
        pass

    def build_interaction_flow_model(self):
        interaction_flow_model_table = InteractionFlowModelSymbolTable()
        pass