import click
import questionary
import pkg_resources
from pathlib import Path


@click.group()
def code():
    """Code-related tools."""
    pass


@code.command()
def weaviate():
    """Generate Weaviate code examples."""
    examples_path = Path(pkg_resources.resource_filename('jphtools', 'weaviate_examples'))
    example_files = sorted(list(examples_path.glob("*.py")))

    example_choices = [f.stem for f in example_files]
    ai_choice = "Ask AI to generate an example"

    selected_example = questionary.select(
        "Which Weaviate example would you like?",
        choices=example_choices + [ai_choice],
    ).ask()

    if selected_example == ai_choice:
        prompt = questionary.text("What would you like the AI to do?").ask()
        if prompt:
            print(f"AI Prompt: {prompt}")
    elif selected_example:
        for example_file in example_files:
            if example_file.stem == selected_example:
                print(f"--- {example_file.name} ---")
                print(example_file.read_text())
                break
