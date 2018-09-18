from .base import DomainElement


class FeatureConcept(DomainElement):

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)


class UMLStructuralFeature(FeatureConcept):
    UML_DOMAIN_CONCEPT_TYPE = 'core:UMLStructuralFeature'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
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
        return type + ' ' + href

    def get_structural_feature(self):
        return self._structural_feature
