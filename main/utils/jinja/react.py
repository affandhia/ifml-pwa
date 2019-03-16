from jinja2 import Environment, PackageLoader

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

DELIMITER = '/'


def __path_joiner(path):
    final_path = ''
    if isinstance(path, list):
        for section in path:
            final_path = final_path + DELIMITER + section

        final_path = final_path[1:]
    elif isinstance(path, str):
        final_path = path
    return final_path


def base_file_writer(template_name, *args, **kwargs):
    template = base_env.get_template(__path_joiner(template_name))
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
