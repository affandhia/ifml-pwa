class IFMLtoAngularInterpreter(object):

    def __init__(self, ifml_xmi, class_diagram_xmi):
        self.root_ifml = ifml_xmi
        self.root_class_diagram_xmi = class_diagram_xmi
        self.project_name = self.root_ifml.name

        #Getting All IFML Elements
        self.ifml_expressing_ui_design = self.root_ifml.get_interaction_flow_model()

        #Getting All Domain Model Elements
        self.domain_model_used_by_ifml = self.root_ifml.get_domain_model()