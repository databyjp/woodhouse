import click
from jphtools.notebooks import strip_solutions_from_notebook
from jphtools.images import crunch_images


@click.group()
def cli():
    """jphtools: A collection of personal tools."""
    pass

@cli.group()
def notebook():
    """Notebook-related tools."""
    pass

@notebook.command("strip-answers")
@click.argument("input_path")
@click.argument("output_path")
def strip_answers(input_path, output_path):
    """Strip solution blocks from a Jupyter notebook."""
    strip_solutions_from_notebook(input_path, output_path)


@cli.command()
@click.argument("pattern")
def crunch(pattern):
    """Compresses PNG files using crunch and renames them."""
    crunch_images(pattern)


if __name__ == "__main__":
    cli()
