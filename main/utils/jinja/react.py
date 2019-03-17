from jinja2 import Environment, PackageLoader
from main.utils.file_and_folder_management import path_joiner

base_env = Environment(
    loader=PackageLoader('main.template', 'file/react/base'),
    autoescape=[''])
component_env = Environment(
    loader=PackageLoader('main.template', 'file/react/component'),
    autoescape=[''],
    variable_start_string='{$', variable_end_string='$}')
service_env = Environment(
    loader=PackageLoader('main.template', 'file/react/service'),
    autoescape=[''],
    variable_start_string='{$', variable_end_string='$}')
router_env = Environment(
    loader=PackageLoader('main.template', 'file/react/router'),
    autoescape=[''],
    variable_start_string='{$', variable_end_string='$}')
model_env = Environment(
    loader=PackageLoader('main.template', 'file/react/model'),
    autoescape=[''],
    variable_start_string='{$', variable_end_string='$}')
react_html_env = Environment(
    loader=PackageLoader('main.template', 'file/react/html'),
    autoescape=[''],
    variable_start_string='{$', variable_end_string='$}')


def base_file_writer(template_name, *args, **kwargs):
    template = base_env.get_template(path_joiner(template_name))
    return template.render(*args, **kwargs)


def component_file_writer(template_name, *args, **kwargs):
    template = component_env.get_template(template_name)
    return template.render(*args, **kwargs)


def service_file_writer(template_name, *args, **kwargs):
    template = service_env.get_template(template_name)
    return template.render(*args, **kwargs)


def router_file_writer(template_name, *args, **kwargs):
    template = router_env.get_template(template_name)
    return template.render(*args, **kwargs)


def model_file_writer(template_name, *args, **kwargs):
    template = model_env.get_template(template_name)
    return template.render(*args, **kwargs)


def react_html_writer(template_name, *args, **kwargs):
    template = react_html_env.get_template(template_name)
    return template.render(*args, **kwargs)
