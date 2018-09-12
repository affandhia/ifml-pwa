from jinja2 import Environment, PackageLoader, select_autoescape

base_env = Environment(loader=PackageLoader('main.template', 'file/angular/base'), autoescape=[''])


def base_file_writer(template_name, *args, **kwargs):
    template = base_env.get_template(template_name)
    return template.render(*args, **kwargs)