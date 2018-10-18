from .base import ViewElement
from .view_component_parts import ViewComponentPart, SimpleField, Slot, DataBinding, DynamicBehavior, VisualizationAttribute


class ViewComponent(ViewElement):
    VIEW_COMPONENT_PARTS_TAGNAME = 'viewComponentParts'
    VIEW_COMPONENT_TYPE = 'core:ViewComponent'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._name = self.set_name()
        self._associated_view_component_part = self.build_assoc_view_component_parts()

    def build_assoc_view_component_parts(self):
        dict_view_component_parts_associated = {}
        list_view_component_parts_associated = self.getElementsByTagName(self.VIEW_COMPONENT_PARTS_TAGNAME)
        for part in list_view_component_parts_associated:
            element_type = part.getAttribute(self.XSI_TYPE)

            # If element is View Component Part
            if element_type == ViewComponentPart.VIEW_COMPONENT_PARTS_TYPE:
                view_component_part_element = ViewComponentPart(part)
                dict_view_component_parts_associated.update(
                    {view_component_part_element.get_id(): view_component_part_element})

            elif element_type == VisualizationAttribute.VISUALIZATION_ATTRIBUTE_TYPE:
                simple_field_element = VisualizationAttribute(part)
                dict_view_component_parts_associated.update(
                    {simple_field_element.get_id(): simple_field_element})

                # If element is SimpleField (Ext)
            elif element_type == SimpleField.SIMPLE_FIELD_TYPE:
                simple_field_element = SimpleField(part)
                dict_view_component_parts_associated.update(
                    {simple_field_element.get_id(): simple_field_element})

            # If element is Slot (Ext)
            elif element_type == Slot.SLOT_TYPE:
                slot_element = Slot(part)
                dict_view_component_parts_associated.update(
                    {slot_element.get_id(): slot_element})

            elif element_type == DataBinding.DATA_BINDING_TYPE:
                data_binding_element = DataBinding(part)
                dict_view_component_parts_associated.update({data_binding_element.get_id(): data_binding_element})

            elif element_type == DynamicBehavior.DYNAMIC_BEHAVIOUR_TYPE:
                dynamic_behaviour_element = DynamicBehavior(part)
                dict_view_component_parts_associated.update({dynamic_behaviour_element.get_id(): dynamic_behaviour_element})

            else:
                pass
                # raise ValueError("Invalid Structure for Defining Association in ViewComponent")
        return dict_view_component_parts_associated

    def get_assoc_view_component_parts(self):
        return self._associated_view_component_part

    def set_name(self):
        return self._schema.getAttribute('name')

    def get_name(self):
        return self._name


class List(ViewComponent):
    LIST_TYPE = 'ext:List'
    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)


class Details(ViewComponent):
    DETAIL_TYPE = 'ext:Details'
    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)


class Form(ViewComponent):
    FORM_TYPE = 'ext:Form'
    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
