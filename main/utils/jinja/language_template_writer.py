from jinja2 import Environment, PackageLoader, select_autoescape
from main.utils.file_and_folder_management import path_joiner

typescript_env = Environment(
    loader=PackageLoader('main.template', 'file/language/typescript'),
    autoescape=[''],
    variable_start_string='{$', variable_end_string='$}')
eseight_env = Environment(
    loader=PackageLoader('main.template', 'file/language/eseight'),
    autoescape=[''],
    variable_start_string='{$', variable_end_string='$}')


def typescript_writer(template_name, *args, **kwargs):
    template = typescript_env.get_template(template_name)
    return template.render(*args, **kwargs)


def eseight_writer(template_name, *args, **kwargs):
    template = eseight_env.get_template(path_joiner(template_name))
    return template.render(*args, **kwargs)
