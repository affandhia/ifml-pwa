import click
import logging

logging.basicConfig(level=logging.DEBUG)

from main.core.angular import generate_project

@click.group()
def main():
    pass

@main.command()
@click.option('--target-directory', default='', help='Target Directory to generate the Angular PWA Project')
@click.argument('ifml_path', type=click.Path(exists=True))
@click.argument('class_diagram_path', type=click.Path(exists=True))
def generate(ifml_path, class_diagram_path, target_directory=None):
    generate_project(ifml_path, class_diagram_path, target_directory)

if __name__ == '__main__':
    main()