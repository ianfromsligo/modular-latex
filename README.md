# Modular LaTeX

Build LaTeX documents from versioned components using a DevOps-style pipeline.

## Layout

- `components/` — paragraphs, equations, subsections, figures, tables
- `templates/` — Jinja2 LaTeX templates per output format
- `manifests/` — YAML manifests declaring which components go where
- `build.py` — assembler + compiler
- `.github/workflows/build.yml` — CI that produces a PDF artifact on every push

## Local build

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python build.py manifests/paper-v1.yaml -o output
```

The PDF is written to `output/main.pdf`.

## Adding a component

- **Paragraph/equation/subsection**: create a `.tex` file under the matching
  subdirectory of `components/`, then reference it in a manifest.
- **Figure/table**: create a directory `components/figures/<name>/` containing
  `<name>.tex` and the asset (`.png`, `.jpg`, `.pdf`). Reference the directory
  (not the `.tex` file) in the manifest.

## Adding a variant

Copy a manifest, adjust the `sections` list, and add a step to the CI workflow
(or a new matrix entry). Same components, different output.
