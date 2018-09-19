from jinja2 import Environment, PackageLoader

base_env = Environment(loader=PackageLoader('main.template', 'file/angular/base'), autoescape=[''])
component_env = Environment(loader=PackageLoader('main.template', 'file/angular/component'), autoescape=[''],
                            variable_start_string='{$', variable_end_string='$}')
service_env = Environment(loader=PackageLoader('main.template', 'file/angular/service'), autoescape=[''],
                          variable_start_string='{$', variable_end_string='$}')
model_env = Environment(loader=PackageLoader('main.template', 'file/angular/model'), autoescape=[''])


def base_file_writer(template_name, *args, **kwargs):
    template = base_env.get_template(template_name)
    return template.render(*args, **kwargs)


def component_file_writer(template_name, *args, **kwargs):
    template = component_env.get_template(template_name)
    return template.render(*args, **kwargs)


def service_file_writer(template_name, *args, **kwargs):
    template = service_env.get_template(template_name)
    return template.render(*args, **kwargs)


def model_file_writer(template_name, *args, **kwargs):
    template = model_env.get_template(template_name)
    return template.render(*args, **kwargs)