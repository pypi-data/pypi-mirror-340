# pdfbaker

Create PDF documents from YAML-configured SVG templates.

## Quickstart

### Installation

pdfbaker is available on [PyPI](https://pypi.org/project/pdfbaker/) and can be installed
using [pipx](https://github.com/pypa/pipx):

```bash
pipx install pdfbaker
```

If you don't have pipx yet,
[install it first](https://pipx.pypa.io/latest/installation/):

```bash
sudo apt install pipx
pipx ensurepath
```

### Optional Dependencies

- For SVG to PDF conversion, [CairoSVG](https://cairosvg.org/) is used by default. If
  you need [Inkscape](https://inkscape.org/) instead, install it:

  ```bash
  sudo apt install inkscape
  ```

- For PDF compression, install [Ghostscript](https://www.ghostscript.com/):
  ```bash
  sudo apt install ghostscript
  ```

### Basic Usage

1. Create your document design in an SVG editor
2. Replace text with variables using Jinja2 (e.g., `{{ title }}`)
3. Configure your content in YAML
4. Generate PDFs with:

```bash
pdfbaker bake <config_file>
```

This will produce your PDF files in a `dist/` directory where your configuration file
lives. It will also create a `build/` directory with intermediate files, which is only
kept if you specify `--debug`.

## Documentation

- [Overview](docs/overview.md)
- [Configuration](docs/configuration.md)
- [Variants](docs/variants.md)
- [Custom Processing](docs/custom_processing.md)

( [on GitHub](https://github.com/pythonnz/pdfbaker/tree/main/docs) )
