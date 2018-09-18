from .base import DomainElement


class BehaviorFeatureConcept(DomainElement):

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)


class UMLBehaviorFeature(BehaviorFeatureConcept):
    UML_DOMAIN_CONCEPT_TYPE = 'core:UMLBehaviourFeature'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._name = self._schema.getAttribute('name')
        self._data_binding = self._schema.getAttribute('behavioralFeature')

    def get_name(self):
        return self._name

    def get_data_binding(self):
        return self._data_binding
