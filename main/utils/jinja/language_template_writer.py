from jinja2 import Environment, PackageLoader, select_autoescape

typescript_env = Environment(loader=PackageLoader('main.template', 'file/language/typescript'), autoescape=[''],
                             variable_start_string='{$', variable_end_string='$}')

def typescript_writer(template_name, *args, **kwargs):
    template = typescript_env.get_template(template_name)
    return template.render(*args, **kwargs)