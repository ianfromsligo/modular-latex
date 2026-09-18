#!/usr/bin/env python3
"""Add exp030-entangled-coins as a real doc, split from sample2.tex."""
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.resolve()

def write(rel, content):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    print(f"  wrote {rel}")

def rm(rel):
    p = ROOT / rel
    if p.exists():
        shutil.rmtree(p) if p.is_dir() else p.unlink()
        print(f"  removed {rel}")

print("==> docs/exp030-entangled-coins")
rm("archive/exp030-stub")
rm("docs/exp030-entangled-coins")
DOC = "docs/exp030-entangled-coins"

write(f"{DOC}/manifest.yaml", """template: article-labnote

metadata:
  title: "EXP030: Entangled Coin Quantum Walks on Tori"
  subtitle: "Using Bell-State Entanglement Between x and y Directions"
  author:
    name: Ian Craig
    email: ian.craig@atu.ie
  date: "1st June 2026"
  abstract: >
    This experiment investigates quantum state revivals on n x m tori
    using entangled coins based on Bell states. Unlike separable coins
    (where x and y motions are independent) or Grover-like coins (which
    mix all four directions equally), Bell-state coins create maximal
    entanglement between the x and y directions. Key discovery: the
    Phi-minus Bell state on the 2x2 torus produces revivals at all
    multiples of 8. The Phi-plus, Psi-plus, and Psi-minus states produce
    revivals at multiples of 24 - three times slower. The only difference
    between Phi-minus and Phi-plus is a relative minus sign, yet this
    changes the revival period by a factor of 3.
  bibliography: docs/exp030-entangled-coins/references.bib

prelude:
  - title: Revision History
    components:
      - docs/exp030-entangled-coins/components/tables/revision-history

sections:
  - title: Introduction
    components:
      - docs/exp030-entangled-coins/components/paragraphs/intro

  - title: Theory
    subsections:
      - title: Mapping Two Qubits to Four Directions
        components:
          - docs/exp030-entangled-coins/components/paragraphs/theory-1-mapping
          - docs/exp030-entangled-coins/components/tables/tab-mapping
      - title: The Four Bell States
        components:
          - docs/exp030-entangled-coins/components/equations/eq-bell-states
      - title: The Critical Sign Difference
        components:
          - docs/exp030-entangled-coins/components/paragraphs/theory-3-sign
          - docs/exp030-entangled-coins/components/equations/eq-sign-difference
      - title: Physical Interpretation
        components:
          - docs/exp030-entangled-coins/components/tables/tab-correlation
      - title: Entangled Coin Operator
        components:
          - docs/exp030-entangled-coins/components/paragraphs/theory-5-operator
          - docs/exp030-entangled-coins/components/equations/eq-bell-operator

  - title: Results
    subsections:
      - title: Complete Classification of Entangled Coin Revivals
        components:
          - docs/exp030-entangled-coins/components/paragraphs/results-1-1
          - docs/exp030-entangled-coins/components/tables/tab-revivals
          - docs/exp030-entangled-coins/components/paragraphs/results-1-2
      - title: Comparison of Bell-State Revivals
        components:
          - docs/exp030-entangled-coins/components/tables/tab-bell-comparison
      - title: Comparison of All Coin Types
        components:
          - docs/exp030-entangled-coins/components/tables/tab-all-coins
          - docs/exp030-entangled-coins/components/paragraphs/results-3-1

  - title: Discussion
    subsections:
      - title: The Role of the Sign
        components:
          - docs/exp030-entangled-coins/components/paragraphs/disc-1-1
      - title: Limitations
        components:
          - docs/exp030-entangled-coins/components/paragraphs/disc-2-1

  - title: Conclusion
    components:
      - docs/exp030-entangled-coins/components/paragraphs/conclusion

postlude:
  - title: Code Availability
    components:
      - docs/exp030-entangled-coins/components/paragraphs/code-availability
""")

write(f"{DOC}/references.bib", r"""@book{Washington1997,
  title={Introduction to Cyclotomic Fields},
  author={Washington, Lawrence C.},
  volume={83},
  year={1997},
  publisher={Springer Science \& Business Media},
  series={Graduate Texts in Mathematics},
  address={New York}
}

@book{Niven1956,
  title={Irrational Numbers},
  author={Niven, Ivan},
  year={1956},
  publisher={Mathematical Association of America},
  series={Carus Mathematical Monographs},
  volume={11}
}

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
""")

write(f"{DOC}/components/tables/revision-history/revision-history.tex", r"""\begin{table}[H]
\centering
\begin{tabular}{cll}
\toprule
\textbf{Revision} & \textbf{Date} & \textbf{Description} \\
\midrule
01 & 1st June 2026       & Initial entangled coin classification \\
02 & 18th September 2026 & Migrated to modular-LaTeX pipeline \\
\bottomrule
\end{tabular}
\end{table}
""")

# --- Introduction ---
write(f"{DOC}/components/paragraphs/intro.tex", r"""Previous experiments have explored:

\begin{itemize}
    \item \textbf{EXP024}: Complete classification of 1D cycle revivals
          ($k \in \{2,3,4,5,6,8,10\}$)
    \item \textbf{EXP025}: Separable coins on tori
          ($C = C_x \otimes C_y$)
    \item \textbf{EXP027}: Fixed non-separable coins (Grover, DFT,
          Hadamard 4D)
    \item \textbf{EXP028}: Parameterized non-separable coins with phases
\end{itemize}

This experiment introduces a new class of coins: \textbf{entangled
coins} based on Bell states. These coins create maximal entanglement
between the $x$ and $y$ directions, correlating the walker's motion in
both dimensions.
""")

# --- Theory: mapping ---
write(f"{DOC}/components/paragraphs/theory-1-mapping.tex", r"""We map two qubits to the four spatial directions, one qubit per axis.
""")

write(f"{DOC}/components/tables/tab-mapping/tab-mapping.tex", r"""\begin{table}[H]
\centering
\caption{Mapping between the two qubits and the four spatial directions.}
\label{tab:mapping}
\begin{tabular}{ccc}
\toprule
\textbf{Qubit 1 ($x$)} & \textbf{Qubit 2 ($y$)} & \textbf{Direction} \\
\midrule
0 & 0 & Right (R) \\
0 & 1 & Left (L) \\
1 & 0 & Up (U) \\
1 & 1 & Down (D) \\
\bottomrule
\end{tabular}
\end{table}
""")

# --- Theory: Bell states ---
write(f"{DOC}/components/equations/eq-bell-states.tex", r"""The Bell states are maximally entangled two-qubit states. In terms of
the four spatial directions:
\begin{align}
  |\Phi^+\rangle &= \frac{1}{\sqrt{2}}(|R\rangle + |D\rangle), \\
  |\Phi^-\rangle &= \frac{1}{\sqrt{2}}(|R\rangle - |D\rangle), \\
  |\Psi^+\rangle &= \frac{1}{\sqrt{2}}(|L\rangle + |U\rangle), \\
  |\Psi^-\rangle &= \frac{1}{\sqrt{2}}(|L\rangle - |U\rangle).
\end{align}
""")

# --- Theory: sign ---
write(f"{DOC}/components/paragraphs/theory-3-sign.tex", r"""The only difference between $\Phi^+$ and $\Phi^-$ is a relative sign
between the two components:
""")

write(f"{DOC}/components/equations/eq-sign-difference.tex", r"""\begin{align*}
  |\Phi^+\rangle &= \frac{1}{\sqrt{2}}(|R\rangle + |D\rangle)
                  \qquad \text{(plus sign)}, \\
  |\Phi^-\rangle &= \frac{1}{\sqrt{2}}(|R\rangle - |D\rangle)
                  \qquad \text{(minus sign)}.
\end{align*}

Similarly, $\Psi^+$ and $\Psi^-$ differ by a sign:
\begin{align*}
  |\Psi^+\rangle &= \frac{1}{\sqrt{2}}(|L\rangle + |U\rangle)
                  \qquad \text{(plus sign)}, \\
  |\Psi^-\rangle &= \frac{1}{\sqrt{2}}(|L\rangle - |U\rangle)
                  \qquad \text{(minus sign)}.
\end{align*}

This relative sign determines whether the two components interfere
constructively or destructively when the walker's paths recombine.
""")

# --- Theory: correlation table ---
write(f"{DOC}/components/tables/tab-correlation/tab-correlation.tex", r"""\begin{table}[H]
\centering
\caption{Correlation between $x$ and $y$ motions by Bell state.}
\label{tab:correlation}
\begin{tabular}{cl}
\toprule
\textbf{Bell State} & \textbf{Correlation} \\
\midrule
$\Phi^+$ & Right correlated with Down (same phase) \\
$\Phi^-$ & Right anti-correlated with Down (opposite phase) \\
$\Psi^+$ & Left correlated with Up (same phase) \\
$\Psi^-$ & Left anti-correlated with Up (opposite phase) \\
\bottomrule
\end{tabular}
\end{table}
""")

# --- Theory: operator ---
write(f"{DOC}/components/paragraphs/theory-5-operator.tex", r"""The entangled coin is a unitary transformation that maps the
computational basis to the Bell basis. The four Bell states are
obtained by applying phase patterns to a common base matrix:
""")

write(f"{DOC}/components/equations/eq-bell-operator.tex", r"""\begin{equation}
C_{\text{Bell}} = \frac{1}{\sqrt{2}}\begin{pmatrix}
1 & 0 & 0 & 1 \\
1 & 0 & 0 & -1 \\
0 & 1 & 1 & 0 \\
0 & 1 & -1 & 0
\end{pmatrix}.
\end{equation}
""")

# --- Results ---
write(f"{DOC}/components/paragraphs/results-1-1.tex", r"""Table~\ref{tab:revivals} summarises all revivals found for entangled
coins on tori up to $4 \times 4$.
""")

write(f"{DOC}/components/tables/tab-revivals/tab-revivals.tex", r"""\begin{table}[H]
\centering
\caption{Full state revivals for entangled coins (fundamental
periods).}
\label{tab:revivals}
\begin{tabular}{lcccc}
\toprule
\textbf{Torus} & $\Phi^+$ & $\Phi^-$ & $\Psi^+$ & $\Psi^-$ \\
\midrule
$2 \times 2$ & $24$ & \textbf{8} & $24$ & $24$ \\
$3 \times 3$ & --- & --- & --- & --- \\
$3 \times 4$ & --- & --- & --- & --- \\
$4 \times 4$ & $24$ & --- & $24$ & --- \\
\bottomrule
\end{tabular}
\end{table}
""")

write(f"{DOC}/components/paragraphs/results-1-2.tex", r"""\textbf{Note:} Revival at $N$ implies revivals at all multiples of
$N$ because $U^N = I$.
""")

write(f"{DOC}/components/tables/tab-bell-comparison/tab-bell-comparison.tex", r"""\begin{table}[H]
\centering
\caption{Comparison of Bell-state revivals on the $2 \times 2$ torus.}
\label{tab:bell-comparison}
\begin{tabular}{lcc}
\toprule
\textbf{Bell State} & \textbf{Fundamental Period $N$} & \textbf{Significance} \\
\midrule
$\Phi^-$ & \textbf{8} & Star discovery (fastest Bell revival) \\
$\Phi^+$ & $24$ & 3$\times$ slower than $\Phi^-$ \\
$\Psi^+$ & $24$ & 3$\times$ slower than $\Phi^-$ \\
$\Psi^-$ & $24$ & 3$\times$ slower than $\Phi^-$ \\
\bottomrule
\end{tabular}
\end{table}
""")

write(f"{DOC}/components/tables/tab-all-coins/tab-all-coins.tex", r"""\begin{table}[H]
\centering
\caption{Comparison of coin types on the $2 \times 2$ torus.}
\label{tab:all-coins}
\begin{tabular}{lcc}
\toprule
\textbf{Coin Type} & \textbf{Fundamental Period $N$} & \textbf{Revivals per 100 steps} \\
\midrule
Grover & $4$ & 25 \\
Bell $\Phi^-$ & $8$ & 12 \\
Hadamard 4D & $8$ & 12 \\
Bell $\Phi^+$ & $24$ & 4 \\
Bell $\Psi^+$ & $24$ & 4 \\
Bell $\Psi^-$ & $24$ & 4 \\
DFT & $16$ & 6 \\
\bottomrule
\end{tabular}
\end{table}
""")

write(f"{DOC}/components/paragraphs/results-3-1.tex", r"""\textbf{Key insight:} The only difference between $\Phi^-$ and
$\Phi^+$ is the sign in the superposition. This minus sign creates
destructive interference that enhances periodicity on the
$2 \times 2$ torus, reducing the revival period from 24 to 8 --- a
3$\times$ speedup.
""")

# --- Discussion ---
write(f"{DOC}/components/paragraphs/disc-1-1.tex", r"""The comparison between $\Phi^-$ and $\Phi^+$ reveals a fundamental
principle: the relative phase between entangled components dramatically
affects the walk's periodicity. A minus sign (destructive interference)
leads to faster revivals (period 8), while a plus sign (constructive
interference) leads to slower revivals (period 24).

This is a subtle but important result: the sign pattern in the Bell
state determines whether the walker's paths interfere constructively or
destructively, directly controlling the revival period.
""")

write(f"{DOC}/components/paragraphs/disc-2-1.tex", r"""Limitations of this experiment include:

\begin{itemize}
    \item No revivals found on $3 \times 3$ or $3 \times 4$ tori with
          any Bell coin
    \item The $4 \times 4$ torus revives only with $\Phi^+$ and
          $\Psi^+$ (period 24)
    \item The $\Psi^-$ coin shows no revivals on $4 \times 4$
\end{itemize}
""")

# --- Conclusion ---
write(f"{DOC}/components/paragraphs/conclusion.tex", r"""This experiment introduces entangled coins as a new class of
non-separable quantum walk coins. Key findings:

\begin{enumerate}
    \item \textbf{Major discovery:} The $\Phi^-$ Bell state on the
          $2 \times 2$ torus produces revivals at \textbf{all multiples
          of 8} --- the fastest Bell revival (period 8).
    \item \textbf{Comparison:} $\Phi^+$, $\Psi^+$, $\Psi^-$ on
          $2 \times 2$ revive at multiples of 24 --- 3$\times$ slower
          than $\Phi^-$.
    \item \textbf{The sign matters:} The only difference between
          $\Phi^-$ and $\Phi^+$ is a minus sign, yet this changes the
          revival period from 24 to 8.
    \item $4 \times 4$ revivals: $\Phi^+$ and $\Psi^+$ revive at
          multiples of 24.
    \item No revivals on $3 \times 3$ or $3 \times 4$ tori with any
          Bell coin.
\end{enumerate}

This opens a new direction for quantum walk coin design: using the
sign pattern in entangled states to engineer periodic behavior.
""")

# --- Code availability ---
write(f"{DOC}/components/paragraphs/code-availability.tex", r"""The complete Python simulation code is available at:
\url{https://github.com/ianfromsligo/EXP030_entangled_coin_tori}
""")

print()
print("Done. Next:")
print("  python build.py docs/exp030-entangled-coins/manifest.yaml -o output --overleaf overleaf --no-compile")
print("  git add -A && git commit -m 'Add exp030-entangled-coins as real doc'")
print("  git push")
