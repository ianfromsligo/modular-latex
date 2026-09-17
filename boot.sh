#!/usr/bin/env bash
set -euo pipefail

# ---- sanity ----
[ -f build.py ] || { echo "ERROR: run this from the repo root (build.py not found)"; exit 1; }
if [ -n "$(git status --porcelain)" ]; then
  echo "ERROR: working tree is not clean. Commit or stash first."
  git status --short
  exit 1
fi

# ---- tag the known-good state ----
if ! git rev-parse v0.1-prototype >/dev/null 2>&1; then
  git tag -a v0.1-prototype -m "First green build (single-doc prototype)"
  echo "Tagged v0.1-prototype"
else
  echo "Tag v0.1-prototype already exists, skipping"
fi

# ---- move old content out of the way ----
mkdir -p archive
if [ -d docs/paper-1 ]; then
  git mv docs/paper-1 archive/paper-1-old 2>/dev/null \
    || { git mv docs archive/_tmp 2>/dev/null; mkdir -p docs; git mv archive/_tmp/paper-1 archive/paper-1-old; rmdir archive/_tmp; }
fi

# ---- remove old single-template + manifests ----
[ -d templates/article ] && git rm -r -q templates/article 2>/dev/null || true
[ -d templates/articles ] && git rm -r -q templates/articles 2>/dev/null || true
[ -d manifests ] && git rm -r -q manifests 2>/dev/null || true

# ---- dirs ----
mkdir -p templates/revtex-pra
mkdir -p docs/sample-paper/components/paragraphs
mkdir -p docs/sample-paper/components/equations
mkdir -p docs/sample-paper/components/tables
mkdir -p docs/sample-paper/components/figures/fig-pipeline
mkdir -p tools
mkdir -p .github/workflows

# ---- build.py ----
cat > build.py <<'PYEOF'
#!/usr/bin/env python3
"""Assemble modular LaTeX components into a single document.

Usage:
    python build.py docs/<doc>/manifest.yaml
    python build.py docs/<doc>/manifest.yaml -o output
    python build.py docs/<doc>/manifest.yaml --no-compile
    python build.py docs/<doc>/manifest.yaml --overleaf overleaf

Outputs:
    <output>/<doc>/main.tex      assembled (repo-path) document
    <output>/<doc>/main.pdf      compiled PDF (unless --no-compile)
    <overleaf>/<doc>/main.tex    flattened self-contained document
    <overleaf>/<doc>/...         copied assets + references.bib
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent.resolve()

INPUT_RE = re.compile(r'\\input\{([^}]+)\}')
INCLUDE_RE = re.compile(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}')


def doc_name(manifest_path: Path) -> str:
    return manifest_path.parent.name


def emit_component(output_dir: Path, comp: str) -> str:
    """LaTeX code that includes the given component.

    Figure/table components are directories named after themselves,
    containing <name>.tex plus assets. Everything else is a .tex file.
    Paths emitted are relative to output_dir.
    """
    comp_path = ROOT / comp
    if comp_path.is_dir():
        tex_name = comp_path.name + ".tex"
        tex_file = comp_path / tex_name
        if not tex_file.exists():
            raise FileNotFoundError(f"No {tex_name} inside {comp_path}")
        rel = os.path.relpath(comp_path, output_dir)
        return (
            f"\\def\\figpath{{{rel}}}\n"
            f"\\input{{{rel}/{tex_name}}}\n"
        )
    else:
        tex_file = comp_path.with_suffix(".tex")
        if not tex_file.exists():
            raise FileNotFoundError(f"Missing component: {tex_file}")
        rel = os.path.relpath(tex_file.with_suffix(""), output_dir)
        return f"\\input{{{rel}}}\n"


def render(manifest: dict, output_dir: Path) -> str:
    env = Environment(
        loader=FileSystemLoader(ROOT / "templates" / manifest["template"]),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        block_start_string="<%",
        block_end_string="%>",
        variable_start_string="<<",
        variable_end_string=">>",
        comment_start_string="<#",
        comment_end_string="#>",
    )
    tmpl = env.get_template("template.tex.j2")
    return tmpl.render(
        manifest=manifest,
        emit=lambda comp: emit_component(output_dir, comp),
    )


def inline_inputs(tex: str, seen: set | None = None) -> str:
    """Recursively replace \\input{path} with the contents of path.tex."""
    seen = seen or set()

    def repl(match):
        target = match.group(1)
        candidate = (ROOT / target).with_suffix(".tex")
        if not candidate.exists():
            return match.group(0)
        if candidate in seen:
            return match.group(0)
        seen.add(candidate)
        body = candidate.read_text()
        return inline_inputs(body, seen)

    return INPUT_RE.sub(repl, tex)


def flatten_graphics(tex: str, out_dir: Path, base: Path) -> str:
    """Copy referenced images into out_dir and rewrite paths to bare filenames."""
    search_prefixes = (
        "",
        "../",
        "../components/",
        "../components/figures/",
        "components/",
        "components/figures/",
    )

    def repl(match):
        original = match.group(1)
        for prefix in search_prefixes:
            cand = (base / prefix / original).resolve()
            if cand.exists() and cand.is_file():
                dst = out_dir / cand.name
                shutil.copy(cand, dst)
                return match.group(0).replace(original, cand.name)
        return match.group(0)

    return INCLUDE_RE.sub(repl, tex)


def write_overleaf_bundle(assembled_tex: str, out_dir: Path,
                          manifest: dict, doc_dir: Path) -> None:
    """Produce a single self-contained main.tex plus assets."""
    out_dir.mkdir(parents=True, exist_ok=True)

    flat = inline_inputs(assembled_tex)
    flat = flatten_graphics(flat, out_dir, base=ROOT)

    (out_dir / "main.tex").write_text(flat)

    # copy bib
    bib = manifest["metadata"].get("bibliography")
    if bib:
        src = ROOT / bib
        if src.exists():
            shutil.copy(src, out_dir / src.name)


def build(manifest_path: Path, output_dir: Path,
          compile_pdf: bool, overleaf_dir: Path | None) -> None:
    manifest = yaml.safe_load(manifest_path.read_text())
    doc = doc_name(manifest_path)
    doc_out = output_dir / doc
    doc_out.mkdir(parents=True, exist_ok=True)

    tex = render(manifest, doc_out)
    (doc_out / "main.tex").write_text(tex)
    print(f"[build] wrote {doc_out / 'main.tex'}")

    bib = manifest["metadata"].get("bibliography")
    if bib:
        shutil.copy(ROOT / bib, doc_out / Path(bib).name)
        print(f"[build] copied {bib}")

    # Overleaf bundle (before compilation, so it's produced even if compile fails)
    if overleaf_dir is not None:
        write_overleaf_bundle(tex, overleaf_dir / doc, manifest, manifest_path.parent)
        print(f"[build] wrote overleaf bundle {overleaf_dir / doc}")

    if not compile_pdf:
        return

    compiler = os.environ.get("LATEXMK", "latexmk")
    cmd = [compiler, "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
    try:
        result = subprocess.run(cmd, cwd=doc_out)
    except FileNotFoundError:
        sys.exit(
            f"Compiler '{compiler}' not found on PATH. Install a TeX distribution "
            "or set LATEXMK to a compiler you have."
        )
    if result.returncode != 0:
        sys.exit("LaTeX compilation failed")
    print(f"[build] PDF at {doc_out / 'main.pdf'}")


def main() -> None:
    p = argparse.ArgumentParser(description="Build a modular LaTeX document.")
    p.add_argument("manifest", type=Path, help="Path to manifest YAML")
    p.add_argument("-o", "--output", type=Path, default=ROOT / "output")
    p.add_argument("--overleaf", type=Path, default=None,
                   help="Directory in which to write the flattened Overleaf bundle")
    p.add_argument("--no-compile", action="store_true",
                   help="Only assemble main.tex; do not run LaTeX.")
    args = p.parse_args()
    build(args.manifest, args.output.resolve(),
          compile_pdf=not args.no_compile,
          overleaf_dir=args.overleaf.resolve() if args.overleaf else None)


if __name__ == "__main__":
    main()
PYEOF

# ---- requirements.txt ----
cat > requirements.txt <<'EOF'
PyYAML==6.0.1
Jinja2==3.1.4
EOF

# ---- .gitignore ----
cat > .gitignore <<'EOF'
output/
overleaf/
*.aux
*.log
*.out
*.bbl
*.blg
*.fdb_latexmk
*.fls
*.synctex.gz
__pycache__/
.venv/
.DS_Store
EOF

# ---- template: revtex-pra ----
cat > templates/revtex-pra/template.tex.j2 <<'TEXEOF'
\documentclass[aps,pra,reprint,amsmath,amssymb,superscriptaddress]{revtex4-2}
\usepackage{graphicx}
\usepackage{dcolumn}
\usepackage{bm}
\usepackage{hyperref}
\usepackage{amsthm}
\usepackage{booktabs}

\newtheorem{theorem}{Theorem}
\newtheorem{corollary}{Corollary}[theorem]
\newtheorem{remark}{Remark}

% Search paths so components can use repo-root-relative \input paths
\makeatletter
\def\input@path{{../}{../components/}{../components/paragraphs/}{../components/equations/}{../components/tables/}{../components/figures/}}
\makeatother
\graphicspath{{../}{../components/}{../components/figures/}{../components/figures/fig-pipeline/}}

\begin{document}

\title{ <<- manifest.metadata.title ->> }
<%- for a in manifest.metadata.authors %>
\author{ <<- a.name ->> }
<%- if a.email %>
\email{ <<- a.email ->> }
<%- endif %>
<%- if a.affiliation %>
\affiliation{ <<- a.affiliation ->> }
<%- endif %>
<%- endfor %>
<%- if manifest.metadata.date %>
\date{ <<- manifest.metadata.date ->> }
<%- else %>
\date{\today}
<%- endif %>

\begin{abstract}
<<- manifest.metadata.abstract ->> 
\end{abstract}

\maketitle

<%- if manifest.prelude %>
<%- for section in manifest.prelude %>
\section*{ <<- section.title ->> }
<%- for comp in section.components %>
<< emit(comp) >>
<%- endfor %>
<%- endfor %>
<%- endif %>

<%- for section in manifest.sections %>
\section{\label{sec:<<- section.label ->>}<<- section.title ->>}
<%- for comp in section.components %>
<< emit(comp) >>
<%- endfor %>
<%- endfor %>

<%- if manifest.postlude %>
<%- for section in manifest.postlude %>
\section*{ <<- section.title ->> }
<%- for comp in section.components %>
<< emit(comp) >>
<%- endfor %>
<%- endfor %>
<%- endif %>

\bibliographystyle{ <<- manifest.metadata.bibliographystyle ->> }
\bibliography{ <<- manifest.metadata.bibliography | replace('.bib','') | basename ->> }

\end{document}
TEXEOF

# ---- sample-paper manifest ----
cat > docs/sample-paper/manifest.yaml <<'EOF'
template: revtex-pra

metadata:
  title: "Revivals on Toroidal Lattices: A Sample Document"
  authors:
    - name: Aoife Ní Bhriain
      email: aoife.nibhriain@atu.ie
      affiliation: Atlantic Technological University, Sligo, Ireland
    - name: Declan O'Sullivan
      affiliation: University of Galway, Galway, Ireland
  abstract: >
    We present a sample document in the REVTeX-PRA style, demonstrating
    the modular-LaTeX build system. This file exists only to verify that
    the template renders correctly; content will be replaced once the
    infrastructure is confirmed. We include a theorem, a numbered
    equation, a table, a figure, and a citation to exercise each path.
  date: "1st June 2026"
  bibliographystyle: apsrev4-2
  bibliography: docs/sample-paper/references.bib

sections:
  - title: Introduction
    label: intro
    components:
      - docs/sample-paper/components/paragraphs/intro-1
      - docs/sample-paper/components/paragraphs/intro-2

  - title: Theoretical Framework
    label: theory
    components:
      - docs/sample-paper/components/equations/eq-general-evolution
      - docs/sample-paper/components/theorems/thm-revival-set
      - docs/sample-paper/components/paragraphs/theory-comment

  - title: Results
    label: results
    components:
      - docs/sample-paper/components/tables/tab-revival-periods
      - docs/sample-paper/components/figures/fig-pipeline

  - title: Conclusion
    label: conclusion
    components:
      - docs/sample-paper/components/paragraphs/conclusion
EOF

# ---- sample-paper references.bib ----
cat > docs/sample-paper/references.bib <<'EOF'
@article{Dukes2014,
  title={Quantum state revivals in quantum walks on cycles},
  author={Dukes, Peter R.},
  journal={Results in Physics},
  volume={4},
  pages={189--197},
  year={2014},
  publisher={Elsevier},
  doi={10.1016/j.rinp.2014.08.011}
}

@book{Washington1997,
  title={Introduction to Cyclotomic Fields},
  author={Washington, Lawrence C.},
  volume={83},
  year={1997},
  publisher={Springer Science \& Business Media},
  series={Graduate Texts in Mathematics},
  address={New York}
}
EOF

# ---- sample-paper components ----
mkdir -p docs/sample-paper/components/theorems

cat > docs/sample-paper/components/paragraphs/intro-1.tex <<'EOF'
Discrete-time quantum walks on finite graphs exhibit a striking
phenomenon: under certain coin and topology conditions, the walker's
state returns exactly to its initial configuration after a fixed number
of steps. These \emph{full-state revivals} were classified on 1D cycles
by Dukes~\cite{Dukes2014}, and the algebraic structure that governs
them has since been connected to cyclotomic fields~\cite{Washington1997}.
EOF

cat > docs/sample-paper/components/paragraphs/intro-2.tex <<'EOF'
In this sample document we exercise the modular-LaTeX pipeline: a
numbered equation, a theorem with proof, a table, a figure, and a
bibliography. Each is a separate component under
\texttt{docs/sample-paper/components/}, assembled by \texttt{build.py}
from the manifest. Replacing any one component changes only that part
of the output.
EOF

cat > docs/sample-paper/components/equations/eq-general-evolution.tex <<'EOF'
The single-step evolution of the walker is governed by the canonical
unitary operation
\begin{equation}
  U = S \, (I_p \otimes C),
  \label{eq:general-evolution}
\end{equation}
where $I_p$ denotes the identity on the position space, $C$ is the coin
operator acting on the internal degree of freedom, and $S$ is the
conditional shift operator.
EOF

cat > docs/sample-paper/components/theorems/thm-revival-set.tex <<'EOF'
\begin{theorem}
\textit{A discrete-time quantum walk on a 1D cycle $\mathbb{Z}_k$
driven by Dukes' coin admits a non-trivial full-state revival with
coin parameter $\rho \in (0,1)$ if and only if $k \in \{2, 3, 4, 5, 6,
8, 10\}$.}
\end{theorem}

\begin{proof}
The proof follows from the algebraic constraints imposed by the
dispersion relation and the cyclotomic structure of the resulting
field extensions. See Dukes~\cite{Dukes2014} for the full development.
\end{proof}
EOF

cat > docs/sample-paper/components/paragraphs/theory-comment.tex <<'EOF'
By Eq.~\eqref{eq:general-evolution}, the evolution factorises into
independent 1D operators when the coin is separable. This factorisation
is what allows the revival classification to be carried out
dimension-by-dimension.
EOF

cat > docs/sample-paper/components/tables/tab-revival-periods.tex <<'EOF'
\begin{table}[htbp]
  \centering
  \caption{Revival periods on small tori (sample data).}
  \label{tab:revival-periods}
  \begin{tabular}{lcc}
    \toprule
    Torus & Fundamental period $N$ & Multiplicity \\
    \midrule
    $2 \times 2$ & 8  & 4  \\
    $3 \times 3$ & 12 & 9  \\
    $4 \times 4$ & 24 & 16 \\
    $5 \times 5$ & 60 & 36 \\
    \bottomrule
  \end{tabular}
\end{table}
EOF

cat > docs/sample-paper/components/figures/fig-pipeline/fig-pipeline.tex <<'EOF'
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\linewidth]{\figpath/pipeline.png}
  \caption{The modular-LaTeX pipeline: components are assembled by the
           build script into a templated document.}
  \label{fig:pipeline}
\end{figure}
EOF

cat > docs/sample-paper/components/figures/fig-pipeline/meta.yaml <<'EOF'
type: figure
title: Modular LaTeX Pipeline
asset: pipeline.png
status: sample
EOF

cat > docs/sample-paper/components/paragraphs/conclusion.tex <<'EOF'
We have demonstrated the modular-LaTeX pipeline end to end: a manifest
selects components, the build script assembles them into a document
using a named template, and continuous integration produces both a
compiled PDF and a flattened \LaTeX{} bundle suitable for Overleaf.
EOF

# ---- tools/make_sample_figure.py ----
cat > tools/make_sample_figure.py <<'PYEOF'
"""Generate the sample pipeline figure used by docs/sample-paper."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

OUT = Path("docs/sample-paper/components/figures/fig-pipeline/pipeline.png")

fig, ax = plt.subplots(figsize=(6, 2.8))
boxes = [
    (0.03, 0.55, "components/", "#cfe8ff"),
    (0.30, 0.55, "manifest",    "#ffe7b3"),
    (0.57, 0.55, "template",    "#d5f5d5"),
    (0.30, 0.15, "build.py",    "#f5d5e5"),
    (0.57, 0.15, "main.pdf",    "#e0e0e0"),
]
for x, y, label, color in boxes:
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y), 0.20, 0.28,
        boxstyle="round,pad=0.02",
        linewidth=1, edgecolor="#333", facecolor=color))
    ax.text(x + 0.10, y + 0.14, label, ha="center", va="center",
            fontsize=10, family="monospace")

def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="#333"))

arrow(0.23, 0.69, 0.30, 0.69)
arrow(0.50, 0.69, 0.57, 0.69)
arrow(0.67, 0.55, 0.67, 0.43)
arrow(0.50, 0.29, 0.57, 0.29)
arrow(0.40, 0.55, 0.40, 0.43)

ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.axis("off")
plt.tight_layout()
OUT.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(OUT, dpi=200)
print(f"wrote {OUT}")
PYEOF

# ---- workflow ----
cat > .github/workflows/build.yml <<'YMLEOF'
name: Build Documents

"on":
  push:
    branches: [main]
  pull_request: {}
  workflow_dispatch: {}

jobs:
  discover:
    runs-on: ubuntu-latest
    outputs:
      docs: ${{ steps.list.outputs.docs }}
    steps:
      - uses: actions/checkout@v4
      - id: list
        run: |
          docs=$(ls -d docs/*/ | xargs -n1 basename | grep -v '^archive$' | jq -R -s -c 'split("\n")[:-1]')
          echo "docs=$docs" >> "$GITHUB_OUTPUT"
          echo "discovered docs: $docs"

  build:
    needs: discover
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        doc: ${{ fromJson(needs.discover.outputs.docs) }}
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install Python deps
        run: pip install -r requirements.txt matplotlib

      - name: Generate sample figure
        run: python tools/make_sample_figure.py

      - name: Assemble LaTeX + Overleaf bundle
        run: |
          python build.py docs/${{ matrix.doc }}/manifest.yaml \
            -o output \
            --overleaf overleaf \
            --no-compile

      - name: Compile PDF
        uses: xu-cheng/latex-action@v3
        with:
          working_directory: output/${{ matrix.doc }}
          root_file: main.tex
          args: -pdf -interaction=nonstopmode -halt-on-error -file-line-error

      - name: Show assembled main.tex (first 80 lines)
        run: head -80 output/${{ matrix.doc }}/main.tex

      - name: Upload PDF (latest)
        uses: actions/upload-artifact@v4
        with:
          name: ${{ matrix.doc }}-pdf
          path: output/${{ matrix.doc }}/main.pdf
          if-no-files-found: error

      - name: Upload PDF (versioned)
        uses: actions/upload-artifact@v4
        with:
          name: ${{ matrix.doc }}-pdf-${{ github.sha }}
          path: output/${{ matrix.doc }}/main.pdf
          retention-days: 90

      - name: Upload assembled tex
        uses: actions/upload-artifact@v4
        with:
          name: ${{ matrix.doc }}-tex
          path: output/${{ matrix.doc }}/main.tex

      - name: Upload Overleaf bundle
        uses: actions/upload-artifact@v4
        with:
          name: ${{ matrix.doc }}-overleaf
          path: overleaf/${{ matrix.doc }}/
YMLEOF

# ---- README ----
cat > README.md <<'MDEOF'
# Modular LaTeX

Build LaTeX documents from versioned components using a DevOps-style pipeline.

## Layout

- `docs/<doc>/` — one directory per document
  - `manifest.yaml` — declares template, metadata, sections, components
  - `references.bib` — bibliography (per-doc)
  - `components/` — paragraphs, equations, tables, figures
- `templates/<name>/template.tex.j2` — Jinja2 LaTeX templates per output style
- `tools/` — scripts that generate figures and other assets
- `build.py` — assembler (and optional local compile)
- `.github/workflows/build.yml` — CI matrix over `docs/*`

## Local build

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt matplotlib
python tools/make_sample_figure.py
python build.py docs/sample-paper/manifest.yaml -o output --overleaf overleaf
