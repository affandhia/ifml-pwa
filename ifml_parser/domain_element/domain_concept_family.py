from .base import DomainElement


class DomainConcept(DomainElement):

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)


class UMLDomainConcept(DomainConcept):
    UML_DOMAIN_CONCEPT_TYPE = 'core:UMLDomainConcept'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
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
        return type + ' ' + href
