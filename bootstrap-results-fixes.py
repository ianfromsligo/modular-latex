#!/usr/bin/env python3
"""
bootstrap-results-fixes.py

Apply a set of corrections to the sep-coin-tori document:

  1. Rewrite the four Results paragraphs (results-1 .. results-4)
     with N instead of T and with the corrected 209 / 373 counts.
  2. Rewrite tab-period-count.tex and tab-max-period.tex with N.
  3. Append the full_revivals_references bib entry if not present.
  4. Replace the remaining $T$ references in Abstract and Conclusion
     components with $N$, where they refer to the revival period.

Prints a per-file diff summary so you can inspect what changed.

Run:  python bootstrap-results-fixes.py
"""

from pathlib import Path
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")


ROOT      = Path(__file__).parent.resolve()
DOC       = ROOT / "docs" / "sep-coin-tori"
COMP      = DOC / "components"
PARAS     = COMP / "paragraphs"
TABLES    = COMP / "tables"
BIB       = DOC / "references.bib"
MANIFEST  = DOC / "manifest.yaml"


# ---------------------------------------------------------------------------
# 1. Results paragraphs
# ---------------------------------------------------------------------------

RESULTS_1 = r"""We present the results of the exhaustive search for complete quantum
revivals of separable-coin walks on $L_x \times L_y$ tori. Revivals are
found at periods
\begin{equation}
N \in \{\,2,\ 6,\ 8,\ 10,\ 12,\ 16,\ 20,\ 24,\ 30,\ 60\,\},
\end{equation}
across the torus sizes $L_x, L_y \in \{2, 3, 4, 5, 6, 8, 10\}$. The
reduced classification contains $209$ parameter sets, one for each
inequivalent $(L_x, L_y, \rho_x, \delta_x, \rho_y, \delta_y)$ under the
interchange $L_x \leftrightarrow L_y$; the full set of values, including
both orientations of every non-square torus, is available at
\cite{full_revivals_references}. The periods $N = 12$ and $N = 24$
dominate the classification, together accounting for $163$ of the $209$
parameter sets.
"""

RESULTS_2 = r"""Not every period is available on every torus. Table~\ref{tab:torus-period}
records which torus sizes support which periods, and
Table~\ref{tab:period-count} records the number of parameter sets at each
period. The period spectrum is concentrated on the highly composite
values $12$ and $24$; the extreme values $N = 2$ and $N = 60$ are
confined to the smallest and largest tori respectively. Notably, the
smallest prime torus $5 \times 5$ admits the longest period $N = 60$,
inverting the classical intuition that larger state spaces recur more
slowly. Table~\ref{tab:max-period} summarises the maximum period observed
on each torus.
"""

RESULTS_3 = r"""The reflection parameters $\rho_x, \rho_y$ in the reduced classification
take $20$ distinct algebraic values, tabulated by period in
Table~\ref{tab:rho-by-period}. The values are heavily concentrated: the
half-split $\rho = 1/2$ occurs in $110$ of the $418$ parameter slots
(counting both $\rho_x$ and $\rho_y$ for each row), the third-split
$\rho = 1/3$ in $84$, and the pentagonal pair $(5 \pm \sqrt{5})/10$ in
$104$ collectively. Every value is either a low-order rational, a
quadratic surd, or a simple trigonometric combination thereof, and the
duality $\rho \leftrightarrow 1 - \rho$ is manifest throughout.
Table~\ref{tab:rho-frequency} gives the full frequency distribution.
"""

RESULTS_4 = r"""The phase parameters $\delta_x, \delta_y$ take only rational multiples of
$\pi$, tabulated by period in Table~\ref{tab:delta-by-period}. The
zero-phase case $\delta = 0$ is by far the most common, appearing in
$226$ of the $418$ parameter slots. The non-zero phases cluster at
rational multiples of $\pi$ with denominators matching the torus
dimensions: $2\pi/5$ and $4\pi/5$ on the $5 \times 5$, $5 \times 10$, and
$10 \times 10$ tori, and $2\pi/3$ and $4\pi/3$ on the $3 \times 3$ and
$3 \times 6$ tori. This concentration reflects the underlying root-of-unity
structure of the revival condition. Three structural facts follow from
the tables. First, the longest period $N = 60$ occurs on the smallest
prime torus $5 \times 5$. Second, the torus sizes $3 \times 4$, $3 \times
8$, and $4 \times 6$ admit revivals only in the asymmetric configuration
$\rho_x \neq \rho_y$, whereas the remaining tori admit both symmetric and
asymmetric parameter sets. Third, all phase parameters are rational
multiples of $\pi$, with denominators dividing twice the torus dimension.
These three facts together characterise the separable-coin revival
landscape and motivate the algebraic analysis in
Section~\ref{sec:discussion}.
"""


# ---------------------------------------------------------------------------
# 2. Tables that still use T
# ---------------------------------------------------------------------------

TAB_PERIOD_COUNT = r"""\begin{table}[htbp]
\centering
\caption{Revival periods and the number of reduced parameter sets producing
each. The peak at $N = 12$ and the secondary peak at $N = 24$ together
account for over three-quarters of the classification.}
\label{tab:period-count}
\begin{tabular}{lcccccccccc}
\toprule
$N$ & $2$ & $6$ & $8$ & $10$ & $12$ & $16$ & $20$ & $24$ & $30$ & $60$ \\
\midrule
Sets & $4$ & $1$ & $11$ & $3$ & $82$ & $18$ & $13$ & $81$ & $4$ & $52$ \\
\bottomrule
\end{tabular}
\end{table}
"""

TAB_MAX_PERIOD = r"""\begin{table}[htbp]
\centering
\caption{Maximum revival period observed on each torus, sorted by torus
size. The longest period $N = 60$ occurs on the smallest prime torus
$5 \times 5$ and its multiples.}
\label{tab:max-period}
\begin{tabular}{cc}
\toprule
Torus & Maximum $N$ \\
\midrule
$2\times2$   & $2$ \\
$3\times3$   & $30$ \\
$3\times4$   & $24$ \\
$3\times6$   & $16$ \\
$3\times8$   & $24$ \\
$4\times4$   & $24$ \\
$4\times6$   & $16$ \\
$4\times8$   & $24$ \\
$5\times5$   & $60$ \\
$5\times10$  & $60$ \\
$6\times6$   & $16$ \\
$8\times8$   & $24$ \\
$10\times10$ & $60$ \\
\bottomrule
\end{tabular}
\end{table}
"""


# ---------------------------------------------------------------------------
# 3. Bib entry
# ---------------------------------------------------------------------------

BIB_ENTRY = r"""
@misc{full_revivals_references,
  title        = {Full Set of Revival Values for Separable Quantum Walks on Tori},
  author       = {{focussed}},
  year         = {2026},
  howpublished = {\url{https://github.com/focussed/separable_walk_references}},
  note         = {Repository of reference data accompanying this paper. Accessed: 2026-09-22}
}
"""


# ---------------------------------------------------------------------------
# 4. T -> N substitutions in Abstract and Conclusion
#
# Each pattern is (compiled regex, replacement). Applied to files whose
# names match the list in TARGETS below.
# ---------------------------------------------------------------------------

T_SUBSTITUTIONS = [
    # "$T = 60$"  ->  "$N = 60$"
    (re.compile(r"\$T = 60\$"), r"$N = 60$"),
    # "$T=60$"  ->  "$N=60$"
    (re.compile(r"\$T=60\$"), r"$N=60$"),
    # "period $T$"  ->  "period $N$"
    (re.compile(r"period \$T\$"), r"period $N$"),
    # "period $T = 60$" (covered above but let's be safe)
    (re.compile(r"\$T\$"), r"$N$"),
    # "T = 60" in prose without math delimiters
    (re.compile(r"\bT = 60\b"), r"N = 60"),
    # standalone capital T in the phrase "longest revival period, T = 60"
    (re.compile(r"period, T ="), r"period, N ="),
]

# Only apply the substitutions to these files. Keeps the regex from
# accidentally hitting table labels like tab:torus-period or
# references in the bibliography.
TARGET_FILES = [
    # Abstract lives inline in main.tex, not in a component file, so
    # it's not touched by this script. If you later move the abstract
    # into a component, add it here.
    PARAS / "conclusion.tex",
    PARAS / "intro-1.tex",
    PARAS / "intro-2.tex",
    PARAS / "intro-3.tex",
    PARAS / "intro-4.tex",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"  wrote {path.relative_to(ROOT)}")


def patch_file(path, patterns):
    """Apply each pattern to path. Return True if the file changed."""
    if not path.exists():
        return False
    original = path.read_text()
    text = original
    for pat, repl in patterns:
        text = pat.sub(repl, text)
    if text != original:
        path.write_text(text)
        # Show a small diff summary
        changed = sum(1 for line in original.splitlines()
                      if line not in text.splitlines())
        print(f"  patched {path.relative_to(ROOT)}  ({changed} line(s) changed)")
        return True
    return False


def ensure_bib_entry(path, entry, key):
    """Append entry to bib file if key not already present."""
    if not path.exists():
        path.write_text(entry.strip() + "\n")
        print(f"  created {path.relative_to(ROOT)} with {key}")
        return
    text = path.read_text()
    if key in text:
        print(f"  {path.relative_to(ROOT)} already contains {key}, skipped")
        return
    # Append with a blank line separator
    sep = "" if text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
    path.write_text(text + sep + entry.strip() + "\n")
    print(f"  appended {key} to {path.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("bootstrap-results-fixes.py")
    print("=" * 70)

    # ---- 1. Rewrite Results paragraphs ---------------------------------
    print("\n[1] Rewriting Results paragraphs")
    write(PARAS / "results-1.tex", RESULTS_1)
    write(PARAS / "results-2.tex", RESULTS_2)
    write(PARAS / "results-3.tex", RESULTS_3)
    write(PARAS / "results-4.tex", RESULTS_4)

    # ---- 2. Rewrite the two tables with T ------------------------------
    print("\n[2] Rewriting tables that used T")
    write(TABLES / "tab-period-count" / "tab-period-count.tex", TAB_PERIOD_COUNT)
    write(TABLES / "tab-max-period"   / "tab-max-period.tex",   TAB_MAX_PERIOD)
    # Clean up flat copies if present
    for flat in (TABLES / "tab-period-count.tex", TABLES / "tab-max-period.tex"):
        if flat.exists():
            flat.unlink()
            print(f"  removed stale flat copy {flat.relative_to(ROOT)}")

    # ---- 3. Bib entry --------------------------------------------------
    print("\n[3] Ensuring bibliography entry")
    ensure_bib_entry(BIB, BIB_ENTRY, "full_revivals_references")

    # ---- 4. T -> N substitutions --------------------------------------
    print("\n[4] Substituting T -> N in prose components")
    changed_any = False
    for target in TARGET_FILES:
        if patch_file(target, T_SUBSTITUTIONS):
            changed_any = True
    if not changed_any:
        print("  no T references found in the target files")

    # ---- 5. Check the abstract -----------------------------------------
    # The abstract lives inline in main.tex and won't be reached by the
    # component-file substitutions above. Report if it still contains T.
    main_tex = ROOT / "output" / "sep-coin-tori" / "main.tex"
    source_main = None
    # Look for the source-of-truth main.tex — the one the build reads.
    # In this project the assembled main.tex is written to output/; the
    # source-of-truth is the template plus manifest, so the abstract
    # lives in the template. Warn the user to check it manually.
    print("\n[5] Abstract check")
    print("  The abstract is defined in the template, not in a component.")
    print("  Please grep for '$T$' manually:")
    print("      grep -n '\\$T\\$' templates/revtex-pra/template.tex.j2")
    print("  and replace any matches with '$N$'.")

    # ---- 6. Summary ----------------------------------------------------
    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)
    print("""
Next steps:

  # 1. fix the abstract in the template manually (see [5] above)
  grep -n '\\$T\\$' templates/revtex-pra/template.tex.j2

  # 2. rebuild
  python build.py docs/sep-coin-tori/manifest.yaml -o output --no-compile

  # 3. verify the Results section now uses N throughout
  grep -n '\\$T\\$' output/sep-coin-tori/main.tex
  # expect: no matches in the Results section

  # 4. verify the citation resolves
  grep -n 'full_revivals_references' output/sep-coin-tori/main.tex

  # 5. commit and push
  git add -A
  git commit -m "Results: fix T->N, correct to 209 sets, cite full_revivals_references"
  git push
""")


if __name__ == "__main__":
    main()
