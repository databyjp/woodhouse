# This script will strip sections of cells between
# '# BEGIN_SOLUTION' & '# END_SOLUTION' and
# replace it with '# ADD YOUR CODE HERE'
# to produce student-friendly versions of Jupyter notebooks
import nbformat
import re
import argparse
from pathlib import Path


def strip_solutions_from_notebook(input_path, output_path):
    """
    Removes solution blocks from a Jupyter notebook and writes the result to output_path.
    Solution blocks are marked by '# BEGIN_SOLUTION' and '# END_SOLUTION'.
    """
    with open(input_path, "r") as f:
        nb = nbformat.read(f, as_version=4)

    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.source = re.sub(
                r"# BEGIN_SOLUTION.*?# END_SOLUTION",
                "# ADD YOUR CODE HERE",
                cell.source,
                flags=re.DOTALL,
            )
            cell.outputs = []
            cell.execution_count = None

    with open(output_path, "w") as f:
        nbformat.write(nb, f)
