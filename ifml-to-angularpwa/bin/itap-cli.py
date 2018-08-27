import click


@click.group()
def greet():
    pass


@greet.command()
def hello(**kwargs):
    click.echo('Hello')


@greet.command()
def goodbye(**kwargs):
    click.echo('Goodbye')

if __name__ == '__main__':
    greet()