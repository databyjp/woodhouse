# jphtools

A collection of random personal tools.

## CLI Usage

You can use the `jphtools` command-line interface to access various tools. For example, to strip solution blocks from a Jupyter notebook:

```sh
jphtools notebook strip-answers input.ipynb output.ipynb
```

This will remove code between `# BEGIN_SOLUTION` and `# END_SOLUTION` in code cells, replacing it with `# ADD YOUR CODE HERE` in the output notebook.

To compress PNG files, use the `crunch` command:

```sh
jphtools crunch "**/cat*.png"
```

This command will find all PNG files matching the pattern, run `crunch` on them, rename the originals to `*-precrunch.png`, and rename the compressed files to their original names.

It requires [Crunch](https://github.com/chrissimpkins/Crunch) to be installed and in your PATH.

## Recommended Tools

### PNG Compression

For PNG compression, we recommend using [Crunch](https://github.com/chrissimpkins/Crunch) - an excellent tool that can achieve 30-70% size reduction while maintaining visual quality.

Installation - [see this page](https://github.com/chrissimpkins/Crunch/blob/master/docs/EXECUTABLE.md)
(This is now automated with the `crunch` command).

## TODOs

- PDF to JPGs
- Automation for Weaviate scripts
    - Pull in Weaviate template code
    - Generate starter Weaviate code for local/Cloud w/ Claude
