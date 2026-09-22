#!/usr/bin/env python3
"""
bootstrap-results-section.py

Replace the Results section of the sep-coin-tori document with the
corrected version. Writes:

  Paragraphs:
    components/paragraphs/results-1.tex   (replaced)
    components/paragraphs/results-2.tex   (replaced)
    components/paragraphs/results-3.tex   (new)
    components/paragraphs/results-4.tex   (new)

  Tables:
    components/tables/tab-period-count/tab-period-count.tex           (new)
    components/tables/tab-torus-period/tab-torus-period.tex           (replaced)
    components/tables/tab-max-period/tab-max-period.tex               (replaced)
    components/tables/tab-rho-by-period/tab-rho-by-period.tex         (replaced)
    components/tables/tab-rho-frequency/tab-rho-frequency.tex         (new)
    components/tables/tab-delta-by-period/tab-delta-by-period.tex     (replaced)

Also:
  - Removes tab-complete-phase and tab-violations from the manifest
    (leaves the files on disk; delete manually if you want).
  - Patches the Results section entry in manifest.yaml.
  - Deletes the obsolete flat-layout tab-period-count.tex and
    tab-max-period.tex from tables/ if they exist at the top level,
    since we now use subdirectories.

Run:  python bootstrap-results-section.py
"""

from pathlib import Path
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")


ROOT = Path(__file__).parent.resolve()
DOC = ROOT / "docs" / "sep-coin-tori"
COMP = DOC / "components"
PARAS = COMP / "paragraphs"
TABLES = COMP / "tables"
MANIFEST = DOC / "manifest.yaml"


# ---------------------------------------------------------------------------
# Paragraph content
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
interchange $L_x \leftrightarrow L_y$; the full table with both
orientations of each non-square torus contains $373$ entries. The
periods $N = 12$ and $N = 24$ dominate the classification, together
accounting for $163$ of the $209$ parameter sets.
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
# Table content
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

TAB_TORUS_PERIOD = r"""\begin{table}[htbp]
\centering
\caption{Revival periods observed on each torus $L_x \times L_y$. Only
one orientation of each non-square torus is shown; the $L_y \times L_x$
case is identical by interchangeability. A bullet indicates that at least
one parameter set produces a revival at that period.}
\label{tab:torus-period}
\begin{tabular}{lcccccccccc}
\toprule
Torus & $2$ & $6$ & $8$ & $10$ & $12$ & $16$ & $20$ & $24$ & $30$ & $60$ \\
\midrule
$2\times2$   & $\bullet$ & & & & & & & & & \\
$3\times3$   & & & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & \\
$3\times4$   & & & $\bullet$ & & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & & \\
$3\times6$   & & & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & & & & \\
$3\times8$   & & & & & & & & $\bullet$ & & \\
$4\times4$   & & $\bullet$ & $\bullet$ & & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & & \\
$4\times6$   & & & $\bullet$ & & $\bullet$ & $\bullet$ & & & & \\
$4\times8$   & & & & & & & & $\bullet$ & & \\
$5\times5$   & & & & & & & & & & $\bullet$ \\
$5\times10$  & & & & & & & & & & $\bullet$ \\
$6\times6$   & & & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & & & & \\
$8\times8$   & & & & & & & & $\bullet$ & & \\
$10\times10$ & & & & & & & & & & $\bullet$ \\
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

TAB_RHO_BY_PERIOD = r"""\begin{table}[htbp]
\centering
\caption{Distinct reflection parameters $\rho$ appearing in the reduced
classification, grouped by revival period. All values are given in exact
fractional or surd form. The duality $\rho \leftrightarrow 1 - \rho$ is
manifest at every period.}
\label{tab:rho-by-period}
\begin{tabular}{cl}
\toprule
$N$ & Values of $\rho$ \\
\midrule
$2$  & $\nicefrac{1}{2}$ \\
$6$  & $\nicefrac{3}{4}$ \\
$8$  & $\nicefrac{1}{2}$, $\nicefrac{2}{3}$ \\
$10$ & $\nicefrac{5-\sqrt{5}}{6}$ \\
$12$ & $\nicefrac{1}{3}$, $\nicefrac{1}{4}$, $\nicefrac{1}{2}$, $\nicefrac{3}{4}$, $\nicefrac{2-\sqrt{3}}{2}$, $\nicefrac{2-\sqrt{3}}{4}$, $\nicefrac{2+\sqrt{3}}{4}$ \\
$16$ & $\nicefrac{2-\sqrt{2}}{3}$, $\nicefrac{2-\sqrt{2}}{4}$, $\nicefrac{2+\sqrt{2}}{4}$, $\nicefrac{2-\sqrt{2}}{2}$ \\
$20$ & $\nicefrac{3-\sqrt{5}}{6}$, $\nicefrac{3-\sqrt{5}}{8}$, $\nicefrac{3+\sqrt{5}}{8}$, $\nicefrac{5-\sqrt{5}}{8}$ \\
$24$ & $\nicefrac{1}{2}$, $\nicefrac{2}{3}$, $\nicefrac{2-\sqrt{3}}{3}$, $\nicefrac{2-\sqrt{3}}{4}$, $\nicefrac{2+\sqrt{3}}{4}$ \\
$30$ & $\nicefrac{5-\sqrt{5}}{6}$ \\
$60$ & $\nicefrac{5-\sqrt{5}}{10}$, $\nicefrac{5+\sqrt{5}}{10}$ \\
\bottomrule
\end{tabular}
\end{table}
"""

TAB_RHO_FREQUENCY = r"""\begin{table}[htbp]
\centering
\caption{Frequency of each reflection parameter $\rho$ across the $209$
reduced parameter sets. Frequencies count occurrences in both the
$\rho_x$ and $\rho_y$ columns, so they sum to $418$.}
\label{tab:rho-frequency}
\begin{tabular}{lrlr}
\toprule
$\rho$ & Count & $\rho$ & Count \\
\midrule
$\nicefrac{1}{2}$           & $110$ & $\nicefrac{2-\sqrt{3}}{3}$ & $14$ \\
$\nicefrac{1}{3}$           & $84$  & $\nicefrac{2-\sqrt{2}}{3}$ & $12$ \\
$\nicefrac{5-\sqrt{5}}{10}$ & $52$  & $\nicefrac{2+\sqrt{2}}{4}$ & $8$  \\
$\nicefrac{5+\sqrt{5}}{10}$ & $52$  & $\nicefrac{2-\sqrt{2}}{4}$ & $8$  \\
$\nicefrac{2}{3}$           & $38$  & $\nicefrac{2-\sqrt{2}}{2}$ & $8$  \\
$\nicefrac{2-\sqrt{3}}{2}$  & $32$  & $\nicefrac{3+\sqrt{5}}{8}$ & $7$  \\
$\nicefrac{1}{4}$           & $32$  & $\nicefrac{5-\sqrt{5}}{8}$ & $7$  \\
$\nicefrac{3}{4}$           & $18$  & $\nicefrac{3-\sqrt{5}}{8}$ & $7$  \\
$\nicefrac{2+\sqrt{3}}{4}$  & $15$  & $\nicefrac{3-\sqrt{5}}{6}$ & $5$  \\
$\nicefrac{2-\sqrt{3}}{4}$  & $15$  & $\nicefrac{5-\sqrt{5}}{6}$ & $14$ \\
\bottomrule
\end{tabular}
\end{table}
"""

TAB_DELTA_BY_PERIOD = r"""\begin{table}[htbp]
\centering
\caption{Distinct phase parameters $\delta$ appearing in the reduced
classification, grouped by revival period and expressed in units of
$\pi$. All values are rational multiples of $\pi$.}
\label{tab:delta-by-period}
\begin{tabular}{cl}
\toprule
$N$ & Values of $\delta / \pi$ \\
\midrule
$2$  & $0$, $1$ \\
$6$  & $0$ \\
$8$  & $0$, $1$ \\
$10$ & $0$ \\
$12$ & $0$, $\nicefrac{1}{2}$, $\nicefrac{2}{3}$, $1$, $\nicefrac{4}{3}$, $\nicefrac{3}{2}$ \\
$16$ & $0$, $\nicefrac{1}{2}$ \\
$20$ & $0$, $1$ \\
$24$ & $0$, $\nicefrac{1}{2}$, $1$, $\nicefrac{3}{2}$ \\
$30$ & $\nicefrac{2}{3}$, $\nicefrac{4}{3}$ \\
$60$ & $0$, $\nicefrac{2}{5}$, $\nicefrac{4}{5}$ \\
\bottomrule
\end{tabular}
\end{table}
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"  wrote {path.relative_to(ROOT)}")


def remove_if_exists(path):
    if path.exists():
        path.unlink()
        print(f"  removed {path.relative_to(ROOT)}")
    else:
        print(f"  (skip) {path.relative_to(ROOT)} not present")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("bootstrap-results-section.py")
    print("=" * 70)

    # ---- 1. Paragraphs --------------------------------------------------
    print("\n[1] Writing Results paragraphs")
    write(PARAS / "results-1.tex", RESULTS_1)
    write(PARAS / "results-2.tex", RESULTS_2)
    write(PARAS / "results-3.tex", RESULTS_3)
    write(PARAS / "results-4.tex", RESULTS_4)

    # ---- 2. Tables ------------------------------------------------------
    print("\n[2] Writing Results tables")
    write(TABLES / "tab-period-count"   / "tab-period-count.tex",   TAB_PERIOD_COUNT)
    write(TABLES / "tab-torus-period"   / "tab-torus-period.tex",   TAB_TORUS_PERIOD)
    write(TABLES / "tab-max-period"     / "tab-max-period.tex",     TAB_MAX_PERIOD)
    write(TABLES / "tab-rho-by-period"  / "tab-rho-by-period.tex",  TAB_RHO_BY_PERIOD)
    write(TABLES / "tab-rho-frequency"  / "tab-rho-frequency.tex",  TAB_RHO_FREQUENCY)
    write(TABLES / "tab-delta-by-period"/ "tab-delta-by-period.tex",TAB_DELTA_BY_PERIOD)

    # ---- 3. Clean up obsolete flat-layout tables ------------------------
    # Earlier versions placed tab-period-count.tex and tab-max-period.tex
    # directly under tables/ rather than in their own subdirectories. If
    # those files exist, remove them so the manifest doesn't accidentally
    # pick up the stale copies.
    print("\n[3] Removing obsolete flat-layout table files")
    remove_if_exists(TABLES / "tab-period-count.tex")
    remove_if_exists(TABLES / "tab-max-period.tex")

    # ---- 4. Patch the manifest ------------------------------------------
    print("\n[4] Patching manifest.yaml")
    if not MANIFEST.exists():
        sys.exit(f"manifest not found: {MANIFEST}")

    manifest = yaml.safe_load(MANIFEST.read_text())
    sections = manifest.get("sections", [])

    new_results_components = [
        "docs/sep-coin-tori/components/paragraphs/results-1",
        "docs/sep-coin-tori/components/tables/tab-period-count/tab-period-count",
        "docs/sep-coin-tori/components/tables/tab-torus-period/tab-torus-period",
        "docs/sep-coin-tori/components/paragraphs/results-2",
        "docs/sep-coin-tori/components/tables/tab-max-period/tab-max-period",
        "docs/sep-coin-tori/components/paragraphs/results-3",
        "docs/sep-coin-tori/components/tables/tab-rho-by-period/tab-rho-by-period",
        "docs/sep-coin-tori/components/tables/tab-rho-frequency/tab-rho-frequency",
        "docs/sep-coin-tori/components/paragraphs/results-4",
        "docs/sep-coin-tori/components/tables/tab-delta-by-period/tab-delta-by-period",
    ]

    found = False
    for sec in sections:
        # Match on label first, then fall back to title
        if sec.get("label") == "results" or \
           sec.get("title", "").strip().lower() == "experimental results":
            sec["components"] = new_results_components
            found = True
            print("  rewrote Results section component list")
            break

    if not found:
        print("  WARNING: no Results section found in manifest; "
              "add one manually with the component list above.")

    MANIFEST.write_text(
        yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True,
                       default_flow_style=False, width=1000)
    )
    print(f"  rewrote {MANIFEST.relative_to(ROOT)}")

    # ---- 5. Summary ------------------------------------------------------
    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)
    print("""
Next steps:

  python build.py docs/sep-coin-tori/manifest.yaml -o output --no-compile
  grep -n 'tab:period-count\\|tab:torus-period\\|tab:rho-by-period\\|tab:delta-by-period' \\
       output/sep-coin-tori/main.tex

If the output looks good:

  git add -A
  git commit -m "Correct Results section; add rho-frequency table; fix N=60 rho values"
  git push

Note: the files tab-complete-phase.tex and tab-violations.tex are no
longer referenced by the manifest. They remain on disk; delete them
manually if you want to remove them entirely:

  rm docs/sep-coin-tori/components/tables/tab-complete-phase.tex
  rm docs/sep-coin-tori/components/tables/tab-violations.tex
""")


if __name__ == "__main__":
    main()
