from ifml_parser.ifml_element.interaction_flow_elements.action_family.base import Action
from .base import ViewElement
from .view_components import ViewComponent, Form, Details, List


class ViewContainer(ViewElement):
    VIEW_ELEMENT_TAGNAME = 'viewElements'
    ACTION_TAGNAME = 'actions'

    LANDMARK_ATTRIBUTE = 'isLandmark'
    XOR_ATTRIBUTE = 'isXOR'
    DEFAULT_ATTRIBUTE = 'isDefault'
    NAME_ATTRIBUTE = 'name'

    # Core Type
    VIEW_CONTAINER_TYPE = 'core:ViewContainer'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._is_landmark = self.set_landmark_att()
        self._is_xor = self.set_xor_att()
        self._is_default = self.set_default_att()
        self._name = self.set_name()
        self._associated_view_element = self.build_assoc_view_element()
        self._action = self.build_action()

    def set_landmark_att(self):
        return self._schema.getAttribute(self.LANDMARK_ATTRIBUTE)

    def get_is_landmark(self):
        return self._is_landmark

    def set_xor_att(self):
        return self._schema.getAttribute(self.XOR_ATTRIBUTE)

    def get_is_xor(self):
        return self._is_xor

    def set_default_att(self):
        return self._schema.getAttribute(self.DEFAULT_ATTRIBUTE)

    def get_is_default(self):
        return self._is_default

    def set_name(self):
        return self._schema.getAttribute(self.NAME_ATTRIBUTE)

    def get_name(self):
        return self._name

    def build_assoc_view_element(self):
        dict_view_elements_associated = {}
        list_view_elements_associated = self.getElementsByTagName(self.VIEW_ELEMENT_TAGNAME)
        for element in list_view_elements_associated:
            element_type = element.getAttribute(self.XSI_TYPE)
            # If element is View Container
            if element_type == ViewContainer.VIEW_CONTAINER_TYPE:
                view_container_element = ViewContainer(element)
                dict_view_elements_associated.update({view_container_element.get_id(): view_container_element})

            # If element is Menu (Ext)
            elif element_type == Menu.MENU_TYPE:
                menu_element = Menu(element)
                dict_view_elements_associated.update({menu_element.get_id(): menu_element})

            # If element is Windows (Ext)
            elif element_type == Window.WINDOWS_TYPE:
                windows_element = Window(element)
                dict_view_elements_associated.update({windows_element.get_id(): windows_element})

            # If element is View Component
            elif element_type == ViewComponent.VIEW_COMPONENT_TYPE:
                view_component_element = ViewComponent(element)
                dict_view_elements_associated.update({view_component_element.get_id(): view_component_element})

            # If element is List (Ext)
            elif element_type == List.LIST_TYPE:
                element_list = List(element)
                dict_view_elements_associated.update({element_list.get_id(): element_list})

            # If element is Form (Ext)
            elif element_type == Form.FORM_TYPE:
                element_form = Form(element)
                dict_view_elements_associated.update({element_form.get_id(): element_form})

            # If element is Detail (Ext)
            elif element_type == Details.DETAIL_TYPE:
                details_element = Details(element)
                dict_view_elements_associated.update({details_element.get_id(): details_element})

            else:
                pass
                # raise ValueError("Invalid Structure for Defining Association in View Element")
        return dict_view_elements_associated

    def get_assoc_view_element(self):
        return self._associated_view_element

    def build_action(self):
        dict_actions = {}
        list_action_associated = self.getElementsByTagName(self.ACTION_TAGNAME)
        for action in list_action_associated:
            action_instance = Action(action)
            dict_actions.update({action_instance.get_id(): action_instance})
        return dict_actions

    def get_action(self):
        return self._action


class Menu(ViewContainer):
    MENU_TYPE = 'ext:IFMLMenu'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)


class Window(ViewContainer):
    WINDOWS_TYPE = 'ext:IFMLWindow'
    MODAL_ATTRIBUTE = 'isModal'
    NEW_WINDOW_ATTRIBUTE = 'isNewWindow'

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self._is_modal = self.set_modal_att()
        self._is_new_window = self.set_new_window_att()

    def set_modal_att(self):
        return self._schema.getAttribute(self.MODAL_ATTRIBUTE)

    def set_new_window_att(self):
        return self._schema.getAttribute(self.NEW_WINDOW_ATTRIBUTE)
