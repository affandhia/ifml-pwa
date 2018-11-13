from ifml_parser.general_model import NamedElement


class DomainElement(NamedElement):
    """
    to create concrete syntax for Domain Element in XMI Document for IFML
    """
    DATA_BINDING_ATTRIBUTE = 'dataBinding'
    CLASSIFIER_ATTRIBUTE = 'classifier'
    VISUALIZATION_ATTRIBUTE = 'visualizationAttribute'
    STRUCTURAL_FEATURE_ATTRIBUTE = 'structuralFeature'

    def __init__(self, xmiSchema, uml_sym_tab):
        super().__init__(xmiSchema)
        self.uml_sym_tab = uml_sym_tab

    def check_reference(self, reference_string):
        reference_list = reference_string.split('#')
        uml_name = reference_list[0]
        id_symbol = reference_list[1]
        self.uml_sym_tab.lookup(uml_name, id_symbol)


class BehaviorConcept(DomainElement):

    def __init__(self, xmiSchema, uml_sym_tab):
        super().__init__(xmiSchema, uml_sym_tab)


class UMLBehavior(BehaviorConcept):
    UML_BEHAVIOR_TYPE = 'core:UMLBehavior'

    def __init__(self, xmiSchema, uml_sym_tab):
        super().__init__(xmiSchema, uml_sym_tab)
        self._name = self._schema.getAttribute('name')
        self._data_binding = self._schema.getAttribute('behavioralFeature')

    def get_name(self):
        return self._name

    def get_data_binding(self):
        return self._data_binding

class BehavioralFeatureConcept(DomainElement):

    def __init__(self, xmiSchema, uml_sym_tab):
        super().__init__(xmiSchema, uml_sym_tab)


class UMLBehavioralFeatureConcept(BehavioralFeatureConcept):
    UML_BEHAVIORAL_FEATURE_TYPE = 'core:UMLBehavioralFeature'

    def __init__(self, xmiSchema, uml_sym_tab):
        super().__init__(xmiSchema, uml_sym_tab)
        self._name = self._schema.getAttribute('name')
        self._data_binding = self._schema.getAttribute('behavioralFeature')

    def get_name(self):
        return self._name

    def get_data_binding(self):
        return self._data_binding

class DomainConcept(DomainElement):

    def __init__(self, xmiSchema, uml_sym_tab):
        super().__init__(xmiSchema, uml_sym_tab)


class UMLDomainConcept(DomainConcept):
    UML_DOMAIN_CONCEPT_TYPE = 'core:UMLDomainConcept'

    def __init__(self, xmiSchema, uml_sym_tab):
        super().__init__(xmiSchema, uml_sym_tab)
        self._name = self._schema.getAttribute('name')
        self._data_binding = self._schema.getAttribute('dataBinding')
        self._classifier = self.build_classifier_pointer()

    def get_name(self):
        return self._name

    def get_data_binding(self):
        return self._data_binding

    def build_classifier_pointer(self):
        classifier_node = self.getElementByTagName('classifier')
        type = classifier_node.getAttribute(self.XSI_TYPE)
        href = classifier_node.getAttribute('href')
        self.check_reference(href)
        return type + ' ' + href

class FeatureConcept(DomainElement):

    def __init__(self, xmiSchema, uml_sym_tab):
        super().__init__(xmiSchema, uml_sym_tab)


class UMLStructuralFeature(FeatureConcept):
    UML_STRUCTURAL_FEATURE_TYPE = 'core:UMLStructuralFeature'

    def __init__(self, xmiSchema, uml_sym_tab):
        super().__init__(xmiSchema, uml_sym_tab)
        self._name = self._schema.getAttribute('name')
        self._visualization_attribute = self._schema.getAttribute('visualizationAttribute')
        self._structural_feature = self.build_structural_feature()

    def get_name(self):
        return self._name

    def get_visualization_attribute(self):
        return self._visualization_attribute

    def build_structural_feature(self):
        structural_feature_node = self.getElementByTagName('structuralFeature')
        type = structural_feature_node.getAttribute(self.XSI_TYPE)
        href = structural_feature_node.getAttribute('href')
        self.check_reference(href)
        return type + ' ' + href

    def get_structural_feature(self):
        return self._structural_feature