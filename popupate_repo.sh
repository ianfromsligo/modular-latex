#!/usr/bin/env bash
#
# update_repo.sh — refresh the paper, notebooks, data, and figures in the
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
NOTEBOOK_033="${SRC_LATEX}/docs/sep-coin-tori/data/EXP033.ipynb"
NOTEBOOK_032B="${SRC_LATEX}/docs/sep-coin-tori/data/EXP032b.ipynb"
DATA_OUT_033="${SRC_LATEX}/docs/sep-coin-tori/data/EXP033_outputs"
DATA_OUT_032B="${SRC_LATEX}/docs/sep-coin-tori/data/EXP032b_outputs"

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
# Notebooks
# ---------------------------------------------------------------------------

echo "Updating notebooks..."

if [[ -f "${NOTEBOOK_033}" ]]; then
  cp "${NOTEBOOK_033}" "${DST_NOTEBOOK}/EXP033.ipynb"
  echo "  notebook/EXP033.ipynb"
fi

if [[ -f "${NOTEBOOK_032B}" ]]; then
  cp "${NOTEBOOK_032B}" "${DST_NOTEBOOK}/EXP032b.ipynb"
  echo "  notebook/EXP032b.ipynb"
fi

# ---------------------------------------------------------------------------
# Data — CSVs gzipped (accept already-gzipped sources), the rest plain
# ---------------------------------------------------------------------------

echo "Updating data..."

for base in 2d_classification 2d_classification_full; do
  if [[ -f "${DATA_OUT_033}/${base}.csv.gz" ]]; then
    cp "${DATA_OUT_033}/${base}.csv.gz" "${DST_DATA}/${base}.csv.gz"
    size=$(du -h "${DST_DATA}/${base}.csv.gz" | cut -f1)
    echo "  data/${base}.csv.gz (${size})"
  elif [[ -f "${DATA_OUT_033}/${base}.csv" ]]; then
    gzip -c "${DATA_OUT_033}/${base}.csv" > "${DST_DATA}/${base}.csv.gz"
    size=$(du -h "${DST_DATA}/${base}.csv.gz" | cut -f1)
    echo "  data/${base}.csv.gz (${size})"
  fi
done

for f in EXP033_1d_verification.txt 2d_classification.hash; do
  if [[ -f "${DATA_OUT_033}/${f}" ]]; then
    cp "${DATA_OUT_033}/${f}" "${DST_DATA}/${f}"
    echo "  data/${f}"
  fi
done

# EXP032b outputs: all exhaustive-report variants plus the quick summary
shopt -s nullglob
for f in "${DATA_OUT_032B}"/exhaustive_report_*.txt "${DATA_OUT_032B}"/exhaustive_quick.txt; do
  cp "${f}" "${DST_DATA}/"
  echo "  data/$(basename "${f}")"
done
shopt -u nullglob

# Remove stale plain CSVs if a previous run left them
for f in 2d_classification.csv 2d_classification_full.csv; do
  [[ -f "${DST_DATA}/${f}" ]] && rm "${DST_DATA}/${f}" && echo "  removed stale data/${f}"
done

# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------

echo "Updating figures..."

for f in demo_k2_new.png demo_k4_new.png demo_k4_dukes.png demo_k3_dukes.png; do
  if [[ -f "${DATA_OUT_033}/${f}" ]]; then
    cp "${DATA_OUT_033}/${f}" "${DST_FIGURES}/${f}"
    echo "  figures/${f}"
  fi
done

# ---------------------------------------------------------------------------
# Commit
# ---------------------------------------------------------------------------

echo
echo "Changes in ${DST}:"
echo

cd "${DST}"
git status --short

if [[ -n "$(git status --porcelain)" ]]; then
  git add -A
  git commit -m "Update paper/data from latex build"
  git push
  echo
  echo "Committed and pushed."
else
  echo
  echo "No changes to commit."
fi
