from jinja2 import Environment, PackageLoader

base_env = Environment(
    loader=PackageLoader('main.template', 'file/language/markup/jsx'),
    autoescape=[''],
    variable_start_string='{$', variable_end_string='$}')


def base_jsx_writer(template_name, *args, **kwargs):
    template = base_env.get_template(template_name)
    return template.render(*args, **kwargs)
