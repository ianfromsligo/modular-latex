#!/usr/bin/env bash
# Add Glossary / List of Figures / List of Tables to the thesis.
# Ensures Introduction is first in sections.
# Run from repo root with the venv active.
set -euo pipefail

DOC="docs/thesis-coin-tori"
PAR="$DOC/components/paragraphs"
MAN="$DOC/manifest.yaml"

[[ -f "$MAN" ]] || { echo "ERROR: $MAN not found. Run from repo root."; exit 1; }

# ---------------------------------------------------------------------------
# 1. Component .tex files
# ---------------------------------------------------------------------------
cat > "$PAR/glossary.tex" <<'EOF'
\begin{description}
  \item[Quantum walk] A discrete-time unitary evolution on a graph, driven
    by a coin operator and a shift operator.
  \item[Coin operator] The unitary $C$ acting on the internal (coin) degree
    of freedom at each vertex.
  \item[Shift operator] The unitary $S$ that moves the walker along edges
    conditional on the coin state.
  \item[Revival] A return of the walker's state to its initial configuration
    after some number of steps $t > 0$.
  \item[Torus] The Cartesian product $C_N \times C_M$ of two cycles, with
    periodic boundary conditions in both directions.
\end{description}
EOF
echo "wrote $PAR/glossary.tex"

cat > "$PAR/list_of_figures.tex" <<'EOF'
\begingroup
\renewcommand{\listfigurename}{}
\listoffigures
\endgroup
EOF
echo "wrote $PAR/list_of_figures.tex"

cat > "$PAR/list_of_tables.tex" <<'EOF'
\begingroup
\renewcommand{\listtablename}{}
\listoftables
\endgroup
EOF
echo "wrote $PAR/list_of_tables.tex"

# ---------------------------------------------------------------------------
# 2. Rewrite manifest.yaml: prelude first, then sections with Intro first.
#    The rest of the sections are preserved in their current order.
# ---------------------------------------------------------------------------
cp "$MAN" "$MAN.bak"
echo "backed up to $MAN.bak"

python3 - <<'PY'
import re
from pathlib import Path

man_path = Path("docs/thesis-coin-tori/manifest.yaml")
text = man_path.read_text()

# --- split manifest into (header, sections-block, postlude-block) ----------
# Locate the "sections:" line and the "postlude:" line (if any).
sec_match = re.search(r'^sections:[ \t]*\n', text, re.M)
if not sec_match:
    raise SystemExit("No 'sections:' key in manifest.yaml")
post_match = re.search(r'^postlude:[ \t]*\n', text, re.M)

header = text[:sec_match.start()]
if post_match:
    sections_block = text[sec_match.end():post_match.start()]
    postlude_block = text[post_match.start():]
else:
    sections_block = text[sec_match.end():]
    postlude_block = ""

# --- parse sections into a list of blocks (each starting with "- title:") ---
# Split on lines that start with "- " at column 0.
raw = sections_block
# Use a simple state machine: each new top-level "- " starts a new entry.
entries = []
current = []
for line in raw.splitlines(keepends=True):
    if line.startswith("- "):
        if current:
            entries.append("".join(current))
        current = [line]
    else:
        current.append(line)
if current:
    entries.append("".join(current))

# --- identify Introduction entry and move it to the front ------------------
intro_idx = None
for i, e in enumerate(entries):
    if re.search(r'^-\s+title:\s*["\']?Introduction["\']?\s*$', e, re.M):
        intro_idx = i
        break
if intro_idx is None:
    raise SystemExit("No 'Introduction' entry found in sections")

if intro_idx != 0:
    entries.insert(0, entries.pop(intro_idx))
    print("moved Introduction to the top of sections")
else:
    print("Introduction already first")

# --- rebuild sections_block with a leading newline after "sections:" -------
sections_out = "".join(entries)

# --- build the prelude block (inserted before sections) -------------------
prelude_out = """prelude:
- title: Glossary
  components:
  - docs/thesis-coin-tori/components/paragraphs/glossary

- title: List of Figures
  components:
  - docs/thesis-coin-tori/components/paragraphs/list_of_figures

- title: List of Tables
  components:
  - docs/thesis-coin-tori/components/paragraphs/list_of_tables

"""

# --- assemble -------------------------------------------------------------
# Strip any existing prelude block from the header so we don't duplicate it.
header = re.sub(r'^prelude:.*?(?=^\S)', '', header, flags=re.M | re.S)

new_text = header.rstrip() + "\n\n" + prelude_out + "sections:\n" + sections_out
if postlude_block:
    new_text = new_text.rstrip() + "\n\n" + postlude_block

man_path.write_text(new_text)
print("rewrote", man_path)
PY

# ---------------------------------------------------------------------------
# 3. Show result
# ---------------------------------------------------------------------------
echo
echo "--- resulting component files ---"
find "$PAR" -type f -name '*.tex' | sort

echo
echo "--- manifest preview (first 60 lines) ---"
sed -n '1,60p' "$MAN"
