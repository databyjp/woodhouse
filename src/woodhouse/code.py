import asyncio
import click
import questionary
import importlib.resources
from pathlib import Path
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel


async def generate_weaviate_code_from_prompt(prompt: str) -> str:
    """Generate Weaviate code from a prompt using Pydantic AI."""
    reference_path = importlib.resources.files("woodhouse") / "references" / "weaviate.py"
    reference_code = reference_path.read_text()

    system_prompt = f"""You are a Weaviate code generation assistant.
    Generate a Python code example based on the user's prompt.
    THe following is a correct, up-to-date Weaviate reference code.
    Use this as context. If the required example is not in the reference code,
    let the user know that the example is not in the reference code,
    and what is missing.

    ---
    {reference_code}
    ---
    """

    model = AnthropicModel('claude-3-5-sonnet-latest')
    agent = Agent(model, system_prompt=system_prompt)

    result = await agent.run_async(prompt)
    return result.output


@click.group()
def code():
    """Code-related tools."""
    pass


@code.command()
def weaviate():
    """Generate Weaviate code examples."""
    asyncio.run(weaviate_async())

async def weaviate_async():
    """Generate Weaviate code examples."""
    examples_path = importlib.resources.files("woodhouse") / "weaviate_examples"
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
            generated_code = await generate_weaviate_code_from_prompt(prompt)
            print("--- Generated Code ---")
            print(generated_code)
    elif selected_example:
        for example_file in example_files:
            if example_file.stem == selected_example:
                print(f"--- {example_file.name} ---")
                print(example_file.read_text())
                break
