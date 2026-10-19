#!/usr/bin/env bash
#
# update_repo.sh — refresh the paper, notebook, data, and figures in the
# separable_quantum_walk_tori repo from the modular LaTeX working tree.
#
# Run from ~/src/latex after rebuilding the paper:
#
#     cd ~/src/latex
#     python build.py docs/sep-coin-tori/manifest.yaml -o output --overleaf overleaf --no-compile
#     ./update_repo.sh
#
# Idempotent. Does NOT touch README.md, LICENSE, LICENSE-DATA, CITATION.cff,
# .gitignore, data/README.md, or figures/README.md — those are hand-maintained
# in the repo and should not be overwritten.

set -euo pipefail

SRC_LATEX="${HOME}/src/latex"
DST="${HOME}/src/separable_quantum_walk_tori"

OVERLEAF_DIR="${SRC_LATEX}/overleaf/sep-coin-tori"
OVERLEAF_MAIN="${OVERLEAF_DIR}/main.tex"
BIB="${SRC_LATEX}/docs/sep-coin-tori/references.bib"
NOTEBOOK="${SRC_LATEX}/docs/sep-coin-tori/data/EXP033.ipynb"
DATA_OUT="${SRC_LATEX}/docs/sep-coin-tori/data/EXP033_outputs"

DST_PAPER="${DST}/paper"
DST_NOTEBOOK="${DST}/notebook"
DST_DATA="${DST}/data"
DST_FIGURES="${DST}/figures"

# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

if [[ ! -d "${DST}" ]]; then
  echo "ERROR: target tree not found: ${DST}" >&2
  exit 1
fi

if [[ ! -f "${OVERLEAF_MAIN}" ]]; then
  echo "ERROR: assembled main.tex not found: ${OVERLEAF_MAIN}" >&2
  echo "Run: python build.py docs/sep-coin-tori/manifest.yaml -o output --overleaf overleaf --no-compile" >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# Paper
# ---------------------------------------------------------------------------

echo "Updating paper..."

cp "${OVERLEAF_MAIN}" "${DST_PAPER}/main.tex"
echo "  paper/main.tex"

if [[ -f "${BIB}" ]]; then
  cp "${BIB}" "${DST_PAPER}/references.bib"
  echo "  paper/references.bib"
fi

shopt -s nullglob
for png in "${OVERLEAF_DIR}"/*.png; do
  cp "${png}" "${DST_PAPER}/"
  echo "  paper/$(basename "${png}")"
done
shopt -u nullglob

# ---------------------------------------------------------------------------
# Notebook
# ---------------------------------------------------------------------------

echo "Updating notebook..."

if [[ -f "${NOTEBOOK}" ]]; then
  cp "${NOTEBOOK}" "${DST_NOTEBOOK}/EXP033.ipynb"
  echo "  notebook/EXP033.ipynb"
fi

# ---------------------------------------------------------------------------
# Data — CSVs gzipped, the rest plain
# ---------------------------------------------------------------------------

echo "Updating data..."

for f in 2d_classification.csv 2d_classification_full.csv; do
  if [[ -f "${DATA_OUT}/${f}" ]]; then
    gzip -c "${DATA_OUT}/${f}" > "${DST_DATA}/${f}.gz"
    size=$(du -h "${DST_DATA}/${f}.gz" | cut -f1)
    echo "  data/${f}.gz (${size})"
  fi
done

for f in EXP033_1d_verification.txt 2d_classification.hash; do
  if [[ -f "${DATA_OUT}/${f}" ]]; then
    cp "${DATA_OUT}/${f}" "${DST_DATA}/${f}"
    echo "  data/${f}"
  fi
done

# Remove stale plain CSVs if a previous run left them
for f in 2d_classification.csv 2d_classification_full.csv; do
  [[ -f "${DST_DATA}/${f}" ]] && rm "${DST_DATA}/${f}" && echo "  removed stale data/${f}"
done

# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------

echo "Updating figures..."

for f in demo_k2_new.png demo_k4_new.png demo_k4_dukes.png demo_k3_dukes.png; do
  if [[ -f "${DATA_OUT}/${f}" ]]; then
    cp "${DATA_OUT}/${f}" "${DST_FIGURES}/${f}"
    echo "  figures/${f}"
  fi
done

# ---------------------------------------------------------------------------
# Show what changed
# ---------------------------------------------------------------------------

echo
echo "Changes in ${DST}:"
echo

cd "${DST}"
git status --short

echo
echo "To review and commit:"
echo "  cd ${DST}"
echo "  git diff           # inspect the changes"
echo "  git add -A"
echo "  git commit -m 'Update paper/data from latex build'"
echo "  git push"
