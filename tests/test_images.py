import os
import shutil
import subprocess
from pathlib import Path
from click.testing import CliRunner

import pytest
from jphtools.__main__ import crunch

# Skip all tests in this file if crunch is not installed
crunch_installed = shutil.which("crunch") is not None

pytestmark = pytest.mark.skipif(
    not crunch_installed,
    reason="crunch command not found, skipping image compression tests",
)


CWD = Path(__file__).parent
EXAMPLE_PNG = CWD / "catexample.png"


@pytest.fixture
def temp_image():
    """Copy the example image to a temporary file to avoid modifying the original."""
    temp_path = CWD / "temp_catexample.png"
    shutil.copy(EXAMPLE_PNG, temp_path)
    yield temp_path
    # Teardown: remove the temporary file and any generated files
    precrunch_path = temp_path.with_stem(f"{temp_path.stem}-precrunch")
    crunched_path = temp_path.with_stem(f"{temp_path.stem}-crunch")

    if temp_path.exists():
        temp_path.unlink()
    if precrunch_path.exists():
        precrunch_path.unlink()
    if crunched_path.exists():
        crunched_path.unlink()


def test_crunch_single_image(temp_image):
    """Test crunching a single image."""
    original_size = temp_image.stat().st_size

    runner = CliRunner()
    result = runner.invoke(crunch, [str(temp_image)])

    assert result.exit_code == 0, f"CLI runner failed with output: {result.output}"

    # The original file should now be the crunched one
    assert temp_image.exists()
    crunched_size = temp_image.stat().st_size

    precrunch_path = temp_image.with_stem(f"{temp_image.stem}-precrunch")
    assert precrunch_path.exists()

    assert crunched_size < original_size

    # Cleanup is handled by the fixture, but let's double check it's clean for next test
    precrunch_path.unlink()
