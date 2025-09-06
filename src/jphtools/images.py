import glob
import subprocess
from pathlib import Path

import click


def crunch_images(pattern: str):
    """
    Compresses PNG files using crunch, renames original files to *-precrunch,
    and renames crunched files to the original filenames.
    """
    try:
        files = glob.glob(pattern, recursive=True)
    except Exception as e:
        click.echo(f"Error with pattern '{pattern}': {e}", err=True)
        return

    if not files:
        click.echo(f"No files found matching pattern: {pattern}")
        return

    for file_path_str in files:
        original_path = Path(file_path_str)

        if original_path.suffix.lower() != ".png":
            click.echo(f"Skipping non-PNG file: {original_path}")
            continue

        precrunch_path = original_path.with_stem(f"{original_path.stem}-precrunch")
        if precrunch_path.exists():
            click.echo(
                f"Skipping {original_path}: {precrunch_path} already exists.", err=True
            )
            continue

        crunched_path = original_path.with_stem(f"{original_path.stem}-crunch")

        click.echo(f"Processing {original_path}...")
        try:
            # Run crunch
            result = subprocess.run(
                ["crunch", str(original_path)],
                check=True,
                capture_output=True,
                text=True,
            )
            click.echo(result.stdout)
            if result.stderr:
                click.echo(result.stderr, err=True)

            if not crunched_path.exists():
                click.echo(
                    f"Error: '{crunched_path}' not found after running crunch.",
                    err=True,
                )
                continue

            # Rename original to -precrunch
            original_path.rename(precrunch_path)
            click.echo(f"Renamed {original_path} to {precrunch_path}")

            # Rename -crunch to original
            crunched_path.rename(original_path)
            click.echo(f"Renamed {crunched_path} to {original_path}")

        except FileNotFoundError:
            click.echo(
                "Error: 'crunch' command not found. Is it installed and in your PATH?",
                err=True,
            )
            return  # No point in continuing if crunch isn't installed
        except subprocess.CalledProcessError as e:
            click.echo(f"Error running crunch on {original_path}:", err=True)
            click.echo(e.stderr, err=True)
            continue
        except OSError as e:
            click.echo(
                f"Error during file operations for {original_path}: {e}", err=True
            )
            continue
