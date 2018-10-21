from .base import DomainElement


class BehavioralFeatureConcept(DomainElement):

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)


class UMLBehavioralFeatureConcept(BehavioralFeatureConcept):
    UML_DOMAIN_CONCEPT_TYPE = 'core:UMLBehavioralFeature'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._name = self._schema.getAttribute('name')
        self._data_binding = self._schema.getAttribute('behavioralFeature')

    def get_name(self):
        return self._name

    def get_data_binding(self):
        return self._data_binding
