# Modular LaTeX

Build LaTeX documents from versioned components using a DevOps-style
pipeline. Each document is a manifest plus a set of small `.tex`
component files. Continuous integration assembles and compiles them on
every push.

## Layout

```
.
├── build.py                     # assembler
├── requirements.txt
├── docs/
│   ├── <doc-name>/
│   │   ├── manifest.yaml        # what goes where
│   │   ├── references.bib       # per-doc bibliography
│   │   └── components/
│   │       ├── paragraphs/
│   │       ├── equations/
│   │       ├── tables/
│   │       └── figures/
│   └── ...
├── templates/
│   ├── article-sample/          # formal paper, two authors
│   ├── article-labnote/         # informal experiment log
│   └── revtex-pra/              # APS Physical Review A
├── tools/                       # figure generators, scaffolding
└── .github/workflows/build.yml
```

## Templates

| Template | Use for | Distinctive features |
|---|---|---|
| `article-sample` | Formal papers with two authors | Two authors, email in page footer, subsections |
| `article-labnote` | Experiment logs and record documents | Single author, subtitle, revision history, code availability |
| `revtex-pra` | APS / Physical Review A submissions | Two-column, theorems, wide equations, `apsrev4-2` bibliography |

## Build

All builds go through GitHub Actions. On every push to `main`, each
doc under `docs/` is assembled and compiled in parallel. Artifacts:

- `<doc>-pdf` — latest PDF
- `<doc>-pdf-<sha>` — same PDF, versioned by commit (90-day retention)
- `<doc>-tex` — assembled `main.tex` (uses `\input{../...}` paths, repo-tree only)
- `<doc>-overleaf` — flattened bundle for direct upload to Overleaf

## Local build

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt matplotlib

# Generate figures (if any component uses them)
python tools/make_sample_figures.py

# Assemble only (no TeX needed)
python build.py docs/<doc>/manifest.yaml -o output --overleaf overleaf --no-compile
```

If you have a TeX distribution locally, drop `--no-compile` and you'll
get a PDF too.

## Adding a new document

```bash
python tools/new_doc.py exp031-my-experiment --template article-labnote
```

That creates `docs/exp031-my-experiment/` with a starter manifest,
an empty bibliography, and one example component. Edit the manifest to
add sections, edit or add components, commit, push. CI discovers the
new doc automatically.

Alternatively, copy an existing doc of the same template:

```bash
cp -r docs/sample-experiment docs/my-new-doc
```

and edit the manifest.

## Writing a component

A component is a plain `.tex` fragment. It gets `\input{}`ed into the
assembled document. The convention:

- **Paragraphs** — prose only. May contain inline math, `\cite{}`,
  `\ref{}`, `\begin{itemize}`, `\begin{equation}`. One file per logical
  paragraph or paragraph group.
- **Equations** — a self-contained `equation`/`align` environment,
  usually with a `\label{}`.
- **Tables** — a `table` environment with `\caption{}` and `\label{}`.
  Files live in a directory `tab-<name>/` with `<name>.tex` inside.
- **Figures** — a `figure` environment with
  `\includegraphics{\figpath/<asset>}`. Files live in a directory
  `fig-<name>/` with `<name>.tex`, an image, and optional `meta.yaml`.

The manifest lists components by path (no `.tex` extension).

## Generated figures

Figures produced by a script under `tools/` are **not committed**. The
generator is committed; the PNG is regenerated in CI. Add the PNG path
to `.gitignore`.

Hand-authored images (screenshots, photos) are committed normally.

## Outputs

- `output/<doc>/` — assembled `.tex` and (optionally) compiled PDF
- `overleaf/<doc>/` — flattened, self-contained `main.tex` plus assets

The `overleaf/` directory is what you upload to Overleaf:
**New Project → Upload Project**, select the folder.

## Multi-doc

Docs are independent. No components are shared between them. Each has
its own bibliography. Adding a doc is a data operation — no changes to
`build.py` or the workflow.

## Contact

Ian Craig, ian.craig@atu.ie
