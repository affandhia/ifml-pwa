from six import string_types


class NoObject(object):
    pass


_marker = NoObject()


def getElementsExceptTextNode(domElement):
    elements = domElement.childNodes

    cleaned_els = []

    for element in elements:
        if not (element.nodeType == element.TEXT_NODE):
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


class IFMLSymbolTable(object):

    def __init__(self):
        self.table = {}
        self.model_name = ''

    def insert(self, scope_table):
        self.table[scope_table.model_name] = scope_table

    def lookup(self, reference_in_list):

        symbol_found = None

        # Remove the first 3 character, and convert into array
        recursive_reference_array = reference_in_list[3:].split('/@')
        model_name = recursive_reference_array[0]
        scope_in_model = recursive_reference_array[1:]
        # Find it in the table, throw exception if it's not found
        try:
            symbol_found = self.table[model_name].lookup(scope_in_model)
        except KeyError:
            raise Exception('No {name} model in IFML, please fix the XMI file'.format(name=model_name))

        return symbol_found


class IFMLElementSymbolTable(IFMLSymbolTable):

    def __init__(self):
        super().__init__()

    def insert(self, symbol):
        try:
            array_of_appearance = self.table[symbol.tag_name]
            array_of_appearance.append(symbol)
        except KeyError:
            self.table[symbol.tag_name] = [symbol]

    def lookup(self, reference_list):

        current_scope_tag_name, current_scope_index = reference_list[0].split('.')
        next_scope_reference_list = reference_list[1:]
        symbol_found = None
        try:
            array_of_element_for_current_tag_name = self.table[current_scope_tag_name]
            symbol = array_of_element_for_current_tag_name[int(current_scope_index)]
            if len(reference_list) > 1:
                symbol_found = symbol.next_scope.lookup(next_scope_reference_list)
            else:
                symbol_found = symbol
        except IndexError:
            raise Exception(
                '{name} tag with index of appearance {index} is never been created in the IFML Model, please fix'.format(
                    name=current_scope_tag_name, index=current_scope_index))
        except KeyError:
            raise Exception(
                '{name} tag is never been created in the IFML Model, please fix'.format(
                    name=current_scope_tag_name))
        return symbol_found


class IFMLSymbol(object):
    ID_ATTRIBUTE = 'id'
    NAME_ATTRIBUTE = 'name'
    TYPE_ATTRIBUTE = 'xsi:type'

    def __init__(self, element_dom):
        self.id = element_dom.getAttribute(self.ID_ATTRIBUTE)
        self.name = element_dom.getAttribute(self.NAME_ATTRIBUTE)
        self.type = element_dom.getAttribute(self.TYPE_ATTRIBUTE)
        self.tag_name = element_dom.tagName
        self.next_scope = None

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


class DomainConceptSymbol(IFMLSymbol):

    def __init__(self, element):
        super().__init__(element)
        self.classifier_reference = getElementByTagName(element, 'classifier').getAttribute('href')
        self.classifier_symbol = None

    def build_classifier_symbol(self, uml_symbol_table):
        self.classifier_symbol = uml_symbol_table.lookup(self.classifier_reference)


class StructuralFeatureSymbol(IFMLSymbol):

    def __init__(self, element):
        super().__init__(element)
        self.struct_feature_reference = getElementByTagName(element, 'structuralFeature').getAttribute('href')
        self.struct_feature_symbol = None

    def build_struct_feature_symbol(self, uml_symbol_table):
        self.struct_feature_symbol = uml_symbol_table.lookup(self.struct_feature_reference)


class BehavioralFeature(IFMLSymbol):

    def __init__(self, element):
        super().__init__(element)
        self.behavioral_feature_reference = getElementByTagName(element, 'behavioralFeature').getAttribute('href')
        self.behavioral_feature_symbol = None

    def build_behavioral_feature_symbol(self, uml_symbol_table):
        self.behavioral_feature_symbol = uml_symbol_table.lookup(self.behavioral_feature_reference)


class Behavior(IFMLSymbol):

    def __init__(self, element):
        super().__init__(element)
        self.behavior_reference = getElementByTagName(element, 'behavior').getAttribute('href')
        self.behavior_symbol = None

    def build_behavior_symbol(self, uml_symbol_table):
        self.behavior_symbol = uml_symbol_table.lookup(self.behavior_reference)


class IFMLSymbolTableBuilder(object):
    DOMAIN_MODEL_TAG = 'domainModel'
    INTERACTION_FLOW_MODEL_TAG = 'interactionFlowModel'
    IFML_MODEL_TAG = 'core:IFMLModel'
    TYPE_ATTRIBUTE = 'xsi:type'

    def __init__(self, ifml_dom):
        self.ifml_dom = getElementByTagName(ifml_dom, self.IFML_MODEL_TAG)
        self.ifml_symbol_table = IFMLSymbolTable()

    def build(self):
        self.build_domain_model()
        self.build_interaction_flow_model()
        return self.ifml_symbol_table

    def build_domain_model(self):

        DOMAIN_CONCEPT = 'core:UMLDomainConcept'
        STRUCTURAL_FEATURE = 'core:UMLStructuralFeature'
        BEHAVIOR_FEATURE = 'core:UMLBehaviorFeature'
        BEHAVIOR = 'core:UMLBehavior'

        domain_model = getElementByTagName(self.ifml_dom, self.DOMAIN_MODEL_TAG)
        domain_model_table = IFMLElementSymbolTable()
        domain_model_table.model_name = self.DOMAIN_MODEL_TAG

        for child in getElementsExceptTextNode(domain_model):
            symbol_type = child.getAttribute(self.TYPE_ATTRIBUTE)
            if symbol_type == DOMAIN_CONCEPT:
                domain_model_table.insert(DomainConceptSymbol(child))
            elif symbol_type == STRUCTURAL_FEATURE:
                domain_model_table.insert(StructuralFeatureSymbol(child))
            elif symbol_type == BEHAVIOR_FEATURE:
                domain_model_table.insert(BehavioralFeature(child))
            elif symbol_type == BEHAVIOR:
                domain_model_table.insert(Behavior(child))

        self.ifml_symbol_table.insert(domain_model_table)

    def build_interaction_flow_model(self):
        interaction_flow_model = getElementByTagName(self.ifml_dom, self.INTERACTION_FLOW_MODEL_TAG)
        interaction_flow_model_table = IFMLElementSymbolTable()
        interaction_flow_model_table.model_name = self.INTERACTION_FLOW_MODEL_TAG

        for child in getElementsExceptTextNode(interaction_flow_model):
            pass
            # print(child)
