import click
import logging
from woodhouse.notebooks import strip_solutions_from_notebook
from woodhouse.images import crunch_images
from woodhouse.code import code
from pathlib import Path

logging.getLogger("anthropic").setLevel(logging.WARNING)


@click.group()
def cli():
    """woodhouse: A collection of personal tools."""
    pass


@cli.group()
def notebook():
    """Notebook-related tools."""
    pass


@notebook.command("strip-answers")
@click.argument("input_path")
@click.argument("output_path", required=False)
def strip_answers(input_path, output_path):
    """Strip solution blocks from a Jupyter notebook."""
    input_path = Path(input_path)
    output_path = Path(output_path) if output_path else None

    if input_path.is_dir():
        if not output_path:
            output_path = input_path
        output_path.mkdir(parents=True, exist_ok=True)
        for file_path in input_path.glob("*-complete.ipynb"):
            output_filename = file_path.name.replace("-complete.ipynb", ".ipynb")
            output_file_path = output_path / output_filename
            print(f"Processing {file_path} -> {output_file_path}")
            strip_solutions_from_notebook(str(file_path), str(output_file_path))
    else:
        if not output_path:
            if input_path.name.endswith("-complete.ipynb"):
                output_filename = input_path.name.replace("-complete.ipynb", ".ipynb")
                output_path = input_path.parent / output_filename
            else:
                click.echo(
                    "Error: When input is a single file not ending in '-complete.ipynb', "
                    "output_path must be specified.",
                    err=True,
                )
                return

        if not output_path.parent.exists():
            output_path.parent.mkdir(parents=True, exist_ok=True)
        strip_solutions_from_notebook(str(input_path), str(output_path))


@cli.command()
@click.argument("pattern")
def crunch(pattern):
    """Compresses PNG files using crunch and renames them."""
    crunch_images(pattern)


cli.add_command(code)

if __name__ == "__main__":
    cli()
