#!/usr/bin/env python3
"""
bootstrap-method-and-fixes.py

Apply the following changes to the sep-coin-tori document:

  1. Add a Methodology section (one paragraph) between Theory and Results.
  2. Rewrite the four Results paragraphs with N instead of T, corrected
     to 209 parameter sets, and with the full_revivals_references citation.
  3. Rewrite tab-period-count.tex and tab-max-period.tex with N.
  4. Append the full_revivals_references bib entry if not present.
  5. Apply T -> N substitutions to the conclusion and intro components.
  6. Add the Methodology section to the manifest, before the Results
     section entry.

Prints a per-file summary as it goes.

Run:  python bootstrap-method-and-fixes.py
"""

from pathlib import Path
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")


ROOT     = Path(__file__).parent.resolve()
DOC      = ROOT / "docs" / "sep-coin-tori"
COMP     = DOC / "components"
PARAS    = COMP / "paragraphs"
TABLES   = COMP / "tables"
BIB      = DOC / "references.bib"
MANIFEST = DOC / "manifest.yaml"


# ---------------------------------------------------------------------------
# 1. Methodology paragraph
# ---------------------------------------------------------------------------

METHOD_1 = r"""The classification proceeds in two stages. The starting point is the 1D
revival set $\{2, 3, 4, 5, 6, 8, 10\}$ established in Theorem~1, together
with the corresponding 1D parameter tables of Dukes~\cite{Dukes2014},
which for each cycle length $k$ in the revival set list the reflection
and phase values $(\rho, \delta)$ that produce a full-state revival and
the associated step count $N$. Taking these as given, we assemble the 1D
walk operator $U_k = S_k(I_k \otimes C_k)$ in the computational basis
using the coin of Eq.~(\ref{eq:1d_coin}) and verify each tabulated
revival by direct matrix exponentiation, checking that $U_k^N$ equals
the identity up to a global phase to within a numerical tolerance of
$10^{-8}$. The 2D classification then follows from the tensor-product
factorisation $U_{k \times m} = U_k \otimes U_m$ of
Eq.~(\ref{eq:factorised_unitary}). For each pair $(k, m)$ with
$k, m \in \{2, 3, 4, 5, 6, 8, 10\}$, we enumerate the periods $N$ shared
by the two 1D revival sets $\mathcal{N}_k$ and $\mathcal{N}_m$ and, for
each such $N$, record every combination of 1D parameters
$(\rho_x, \delta_x) \in \mathcal{R}_k(N)$ and
$(\rho_y, \delta_y) \in \mathcal{R}_m(N)$ that produces the revival,
verifying each candidate numerically by the same matrix-exponentiation
check. Because the 1D input is complete and the 2D pairing is
exhaustive over the finite revival set, the resulting classification of
$209$ inequivalent parameter sets is complete. The verification script
and the full classification are available at
\cite{full_revivals_references}.
"""


# ---------------------------------------------------------------------------
# 2. Results paragraphs (N, 209, citation)
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
# 3. Tables
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
# 4. Bib entry
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
# 5. T -> N substitutions
# ---------------------------------------------------------------------------

T_SUBSTITUTIONS = [
    (re.compile(r"\$T = 60\$"),   r"$N = 60$"),
    (re.compile(r"\$T=60\$"),     r"$N=60$"),
    (re.compile(r"period \$T\$"), r"period $N$"),
    (re.compile(r"\$T\$"),        r"$N$"),
    (re.compile(r"\bT = 60\b"),   r"N = 60"),
    (re.compile(r"period, T ="),  r"period, N ="),
]

TARGET_FILES = [
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
    if not path.exists():
        return False
    original = path.read_text()
    text = original
    for pat, repl in patterns:
        text = pat.sub(repl, text)
    if text != original:
        path.write_text(text)
        n_changed = sum(1 for a, b in zip(original.splitlines(),
                                         text.splitlines()) if a != b)
        # account for line-count differences
        n_changed = max(n_changed,
                        abs(len(original.splitlines()) - len(text.splitlines())))
        print(f"  patched {path.relative_to(ROOT)}  ({n_changed} line(s) affected)")
        return True
    return False


def ensure_bib_entry(path, entry, key):
    if not path.exists():
        path.write_text(entry.strip() + "\n")
        print(f"  created {path.relative_to(ROOT)} with {key}")
        return
    text = path.read_text()
    if key in text:
        print(f"  {path.relative_to(ROOT)} already contains {key}, skipped")
        return
    sep = "" if text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
    path.write_text(text + sep + entry.strip() + "\n")
    print(f"  appended {key} to {path.relative_to(ROOT)}")


def insert_method_section(manifest):
    """Insert a Methodology section immediately before the Results section."""
    sections = manifest.get("sections", [])

    # Already present?
    for sec in sections:
        if sec.get("label") == "method":
            print("  Methodology section already present, skipping insert")
            return False

    method_section = {
        "label": "method",
        "title": "Methodology",
        "components": [
            "docs/sep-coin-tori/components/paragraphs/method-1",
        ],
    }

    # Find the Results section index
    results_idx = None
    for i, sec in enumerate(sections):
        if sec.get("label") == "results" or \
           sec.get("title", "").strip().lower() == "experimental results":
            results_idx = i
            break

    if results_idx is None:
        print("  WARNING: Results section not found; appending Method at end")
        sections.append(method_section)
    else:
        sections.insert(results_idx, method_section)
    manifest["sections"] = sections
    print("  inserted Methodology section before Results")
    return True


def update_roadmap(path):
    """Best-effort: replace the road-map sentence in intro-4.tex."""
    if not path.exists():
        return False
    text = path.read_text()
    old = r"""Section II of this paper establishes the underlying theory deriving the
parameterised unitary operation (Coin and Shift operators) for the
separable walk on the $k \times m$ tori.  It also gives an example of a
step of the separable walk and a proof that full-state
revivals only occur when $k,m \in \{2, 3, 4, 5, 6, 8, 10\}$ for a
$k \times m$ toroidal lattice. 
Section III contains the experimental results. 
Section IV contains the discussion
of results and Section V, concluding remarks."""
    new = r"""Section~\ref{sec:theory} establishes the underlying theory deriving the
parameterised unitary operation (Coin and Shift operators) for the
separable walk on the $k \times m$ tori. It also gives an example of a
step of the separable walk and a proof that full-state revivals only
occur when $k, m \in \{2, 3, 4, 5, 6, 8, 10\}$ for a $k \times m$
toroidal lattice. Section~\ref{sec:method} describes the two-stage
enumeration used to generate the classification. Section~\ref{sec:results}
presents the results, Section~\ref{sec:discussion} discusses them, and
Section~\ref{sec:conclusion} closes."""
    if old in text:
        path.write_text(text.replace(old, new))
        print(f"  updated road-map in {path.relative_to(ROOT)}")
        return True
    # Try a looser match on the key sentence
    loose_old = "Section III contains the experimental results"
    loose_new = "Section~\\ref{sec:method} describes the two-stage enumeration used to generate the classification. Section~\\ref{sec:results} presents the experimental results"
    if loose_old in text:
        path.write_text(text.replace(loose_old, loose_new))
        print(f"  updated road-map (loose match) in {path.relative_to(ROOT)}")
        return True
    print(f"  road-map in {path.relative_to(ROOT)} not matched; edit manually")
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("bootstrap-method-and-fixes.py")
    print("=" * 70)

    # ---- 1. Methodology paragraph --------------------------------------
    print("\n[1] Writing Methodology paragraph")
    write(PARAS / "method-1.tex", METHOD_1)

    # ---- 2. Results paragraphs -----------------------------------------
    print("\n[2] Rewriting Results paragraphs (N, 209, citation)")
    write(PARAS / "results-1.tex", RESULTS_1)
    write(PARAS / "results-2.tex", RESULTS_2)
    write(PARAS / "results-3.tex", RESULTS_3)
    write(PARAS / "results-4.tex", RESULTS_4)

    # ---- 3. Tables -----------------------------------------------------
    print("\n[3] Rewriting tables that used T")
    write(TABLES / "tab-period-count" / "tab-period-count.tex", TAB_PERIOD_COUNT)
    write(TABLES / "tab-max-period"   / "tab-max-period.tex",   TAB_MAX_PERIOD)
    for flat in (TABLES / "tab-period-count.tex", TABLES / "tab-max-period.tex"):
        if flat.exists():
            flat.unlink()
            print(f"  removed stale flat copy {flat.relative_to(ROOT)}")

    # ---- 4. Bib entry --------------------------------------------------
    print("\n[4] Ensuring bibliography entry")
    ensure_bib_entry(BIB, BIB_ENTRY, "full_revivals_references")

    # ---- 5. T -> N substitutions --------------------------------------
    print("\n[5] Substituting T -> N in prose components")
    changed_any = False
    for target in TARGET_FILES:
        if patch_file(target, T_SUBSTITUTIONS):
            changed_any = True
    if not changed_any:
        print("  no T references found in the target files")

    # ---- 6. Road-map update in intro-4 ---------------------------------
    print("\n[6] Updating road-map in intro-4.tex")
    update_roadmap(PARAS / "intro-4.tex")

    # ---- 7. Manifest: insert Methodology section ----------------------
    print("\n[7] Inserting Methodology section into manifest")
    if not MANIFEST.exists():
        sys.exit(f"manifest not found: {MANIFEST}")
    manifest = yaml.safe_load(MANIFEST.read_text())
    insert_method_section(manifest)
    MANIFEST.write_text(
        yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True,
                       default_flow_style=False, width=1000)
    )
    print(f"  rewrote {MANIFEST.relative_to(ROOT)}")

    # ---- 8. Summary ----------------------------------------------------
    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)
    print("""
Next steps:

  # 1. fix the abstract in the template manually (if it still uses T)
  grep -n '\\$T\\$' templates/revtex-pra/template.tex.j2

  # 2. rebuild
  python build.py docs/sep-coin-tori/manifest.yaml -o output --no-compile

  # 3. verify no T remains in the assembled paper
  grep -n '\\$T\\$' output/sep-coin-tori/main.tex

  # 4. verify the new section and citation resolve
  grep -n 'sec:method\\|full_revivals_references' output/sep-coin-tori/main.tex

  # 5. commit
  git add -A
  git commit -m "Add Methodology section; fix T->N in Results; cite full_revivals_references"
  git push
""")


if __name__ == "__main__":
    main()
