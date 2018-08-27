import click


@click.group()
@click.option('--debug', default=False, help='Activating Debug Log (Default is False)')
def main(debug):
    click.echo('Debug is {debug}'.format(debug=debug))


@main.command()
@click.argument('ifml', type=click.Path(exists=True))
@click.argument('class_diagram', type=click.Path(exists=True))
#@click.option('--target-directory', default='', help='Target Directory to generate the Angular PWA Project')
def generate(ifml, class_diagram):
    click.echo('IFML model is: '+click.format_filename(ifml))

if __name__ == '__main__':
    main()
