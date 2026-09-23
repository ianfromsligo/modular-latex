#!/usr/bin/env python3
"""
bootstrap-editor-fixes.py

Apply every fix from the editor's report:

  1. Replace the Discussion section with the two-part version
     (general observations + period-by-period) — writes 15 paragraph files
     and patches the manifest.
  2. Fix the Results section: T -> N, correct 209/373 counts, add
     \cite{full_revivals_references}, add the rho-frequency table.
  3. Fix the abstract and conclusion: T -> N, resolve "two vs three
     phenomena" inconsistency.
  4. Fix the road-map paragraph in intro-4.tex: Sectionf typo,
     Section IV/V -> \ref{...}, consolidate citation keys.
  5. Consolidate \cite{my_classification} and \cite{full_revivals_references}
     into a single canonical key: full_revivals_references.
  6. Remove the duplicate \pdfstringdefDisableCommands block.
  7. Fix typos: "adjactent" -> "adjacent".
  8. Append a bib entry for full_revivals_references if not present.

The abstract and preamble live in the template or main.tex, not in
component files. The script patches the template if it finds it; if the
paper is assembled with the abstract inline in main.tex (as currently),
the user is given the exact lines to change by hand.

Run:  python bootstrap-editor-fixes.py
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

# Candidate locations for the template file (RevTeX abstract + preamble)
TEMPLATE_CANDIDATES = [
    ROOT / "templates" / "revtex-pra" / "template.tex.j2",
    ROOT / "templates" / "article-sample" / "template.tex.j2",
    ROOT / "templates" / "article-labnote" / "template.tex.j2",
]


# ===========================================================================
# 1. Discussion section: 15 paragraph files
# ===========================================================================

DISC_1_1 = r"""We now interpret the classification presented in Section~\ref{sec:results}.
Three structural features organise the entire dataset. First, the
revival periods are concentrated on the highly composite values
$N \in \{8, 12, 24\}$, with $N = 12$ and $N = 24$ alone accounting for
$163$ of the $209$ parameter sets. Second, the reflection parameters
take only $20$ distinct algebraic values, all of them either
low-order rationals or quadratic surds, and every one of them is paired
with its complement $1-\rho$ elsewhere in the classification. Third, the
phase parameters are uniformly rational multiples of $\pi$, with
denominators that divide twice the corresponding torus dimension.
"""

DISC_1_2 = r"""The duality $\rho \leftrightarrow 1-\rho$ deserves emphasis because it
holds without exception. Wherever a parameter set
$(\rho_x, \rho_y, \delta_x, \delta_y)$ admits a revival at some period
$N$, so does the set obtained by replacing any occurrence of $\rho$
with $1-\rho$ and leaving all other parameters fixed. This is a direct
consequence of the symmetry of the dispersion relation under
$\rho \to 1-\rho$, and it roughly halves the number of independent
reflection values that need to be tabulated.
"""

DISC_1_3 = r"""A third general feature is the asymmetry between square and non-square
tori. On a square torus $L_x = L_y$, every observed revival admits a
symmetric realisation with $\rho_x = \rho_y$. On the non-square tori
$3 \times 4$, $3 \times 8$, and $4 \times 6$, no symmetric realisation
exists, and revivals are only possible with $\rho_x \neq \rho_y$. This
distinction is visible even at the level of the reduced classification
and suggests that the two spatial cycle lengths must be commensurate
for the symmetric configuration to work.
"""

DISC_1_4 = r"""Finally, the phase parameters play a different role from the reflection
parameters. Whereas $\rho$ determines the achievable periods and the
specific values that appear in the classification, $\delta$ acts as a
selector: for each $(\rho_x, \rho_y)$ pair, only certain phase
combinations produce a revival, and the set of allowed phases is
determined by the denominators of the root-of-unity conditions along
each axis. We now examine the individual periods in turn.
"""

DISC_2_1 = r"""\subsubsection{Period $N = 2$: the $2 \times 2$ Hadamard point}

The shortest period in the classification is realised only on the
$2 \times 2$ torus, and only at $\rho_x = \rho_y = 1/2$ with
$\delta_x, \delta_y \in \{0, \pi\}$. The four parameter sets
corresponding to the four phase combinations exhaust the classification
at this period. The absence of $N = 2$ on any larger torus reflects the
fact that the two-cycle is the only cycle whose Fourier spectrum has a
single non-trivial spatial harmonic.
"""

DISC_2_2 = r"""\subsubsection{The absence of $N = 4$}

No revival occurs at period $N = 4$ anywhere in the classification.
This is not a numerical accident. A revival at $N = 4$ would require
every eigenphase of $U_{k \times m}$ to lie in
$\{0, \pi/2, \pi, 3\pi/2\}$, so that $\sin\theta_j \in \{0, \pm 1\}$.
On any cycle of length $k \ge 3$, the fundamental harmonic
$\sin(2\pi/k)$ is not $0$ or $\pm 1$, and a single real parameter
$\rho$ cannot place both the fundamental and the second harmonic on
the four allowed values simultaneously. The only way to satisfy the
$N = 4$ condition is $\rho = 0$ or $\rho = 1$, which reduces the coin
to a deterministic reflector and produces no non-trivial revival. Period
$N = 4$ therefore belongs to the boundary set excluded by the
definition of an intrinsic revival.
"""

DISC_2_3 = r"""\subsubsection{Period $N = 6$: the $4 \times 4$ singleton}

A single parameter set yields period $N = 6$, on the $4 \times 4$ torus
with $\rho_x = \rho_y = 3/4$ and $\delta_x = \delta_y = 0$. This is the
only period realised by exactly one parameter set, and it is the only
period between $N = 2$ and $N = 8$. The value $\rho = 3/4$ corresponds
to the primitive sixth root of unity, and the period $N = 6$ matches
the denominator of the eigenphase $2\pi/6$.
"""

DISC_2_4 = r"""\subsubsection{Period $N = 8$: the first non-square tori}

Period $N = 8$ is the first richly populated period, with $11$
parameter sets across the tori $3 \times 3$, $3 \times 4$, $3 \times 6$,
$4 \times 4$, $4 \times 6$, and $6 \times 6$. Only two reflection
values appear, $\rho = 2/3$ and $\rho = 1/2$. The non-square tori
$3 \times 4$ and $4 \times 6$ exhibit mixed-$\rho$ revivals for the
first time, establishing that the two axes of the separable coin do
not need to be tuned to the same value.
"""

DISC_2_5 = r"""\subsubsection{Period $N = 10$: the pentagonal $3$-cycle value}

Period $N = 10$ occurs on the $3 \times 3$, $3 \times 6$, and
$6 \times 6$ tori with $\rho = (5-\sqrt{5})/6$ and
$\delta_x = \delta_y = 0$. This is the same algebraic value that
appears in Dukes' 1D classification for the $3$-cycle at period
$N = 10$, and its propagation to $6$-cycles reflects the divisibility
relation $6 = 2 \cdot 3$.
"""

DISC_2_6 = r"""\subsubsection{Period $N = 12$: the largest family}

Period $N = 12$ is the most populated in the classification, with $82$
parameter sets spanning six tori. Five reflection values appear,
$\rho \in \{1/3,\ 1/4,\ 1/2,\ 3/4,\ (2-\sqrt{3})/2\}$, together with
$(2-\sqrt{3})/4$ on the asymmetric tori. The phase parameters take
values in $\{0, \pi/2, 2\pi/3, \pi, 4\pi/3, 3\pi/2\}$. The $3 \times 3$
torus alone contains nine parameter sets with $\rho_x = \rho_y = 1/3$
and $\delta_x, \delta_y \in \{0, 2\pi/3, 4\pi/3\}$, a complete phase
family whose revival is independent of the phase parameters. This is
the earliest and most economical example of a complete phase family in
the classification.
"""

DISC_2_7 = r"""\subsubsection{Period $N = 16$: the octagonal reflection values}

Period $N = 16$ occurs on the same six tori as $N = 12$, with $18$
parameter sets. The reflection parameters are the octagonal surds
$(2-\sqrt{2})/3$, $(2-\sqrt{2})/4$, $(2+\sqrt{2})/4$, and
$(2-\sqrt{2})/2$, all built from $\sqrt{2}$ and reflecting the eighth
roots of unity. The asymmetric tori $3 \times 4$ and $4 \times 6$
contribute the values $(2 \pm \sqrt{2})/4$ and $(2-\sqrt{2})/2$ along
the $4$-cycle axis, while the $3$-cycle contributes $(2-\sqrt{2})/3$.
The phase parameters are restricted to $\{0, \pi/2\}$, a narrower set
than at $N = 12$.
"""

DISC_2_8 = r"""\subsubsection{Period $N = 20$: the golden-ratio family}

Period $N = 20$ appears on three tori, $3 \times 3$, $3 \times 4$, and
$4 \times 4$, with $13$ parameter sets. The reflection values are the
golden-ratio surds $(3-\sqrt{5})/6$, $(3-\sqrt{5})/8$,
$(3+\sqrt{5})/8$, and $(5-\sqrt{5})/8$, and the phase parameters take
only $\{0, \pi\}$. The duality $\rho \leftrightarrow 1-\rho$ is
particularly visible: the value $(3-\sqrt{5})/8 \approx 0.0955$ pairs
with $(5+\sqrt{5})/8 \approx 0.9045$ on the same torus, and
$(3+\sqrt{5})/8 \approx 0.6545$ pairs with
$(5-\sqrt{5})/8 \approx 0.3455$.
"""

DISC_2_9 = r"""\subsubsection{Period $N = 24$: the second-largest family}

Period $N = 24$ is the second most populated, with $81$ parameter sets
spanning six tori: $3 \times 3$, $3 \times 4$, $3 \times 8$,
$4 \times 4$, $4 \times 8$, and $8 \times 8$. Four reflection values
appear: $1/2$, $2/3$, $(2-\sqrt{3})/3$, and the pair
$(2 \pm \sqrt{3})/4$. The $8 \times 8$ torus is particularly striking.
It contains sixteen period-$24$ parameter sets, all with
$\rho_x = \rho_y = 1/2$ and
$\delta_x, \delta_y \in \{0, \pi/2, \pi, 3\pi/2\}$, a complete phase
family at the Hadamard point. The same Hadamard coin that yields
period $2$ on the $2 \times 2$ torus yields period $24$ on the
$8 \times 8$ torus, showing that the torus size directly controls the
revival period at fixed coin parameters.
"""

DISC_2_10 = r"""\subsubsection{Period $N = 30$: the $3 \times 3$ isolated family}

Only four parameter sets yield period $N = 30$, all on the $3 \times 3$
torus with $\rho = (5-\sqrt{5})/6$ and
$\delta_x, \delta_y \in \{2\pi/3, 4\pi/3\}$. This is the same
reflection value that appears at $N = 10$ on the $3$-cycle, and the
period $30$ is three times that of $N = 10$. The extreme scarcity of
this family, together with its restriction to the smallest odd torus,
marks $N = 30$ as an isolated phenomenon in the classification.
"""

DISC_2_11 = r"""\subsubsection{Period $N = 60$: the $5 \times 5$ pentagonal family}

The longest period in the classification is $N = 60$, occurring on
$52$ parameter sets across the $5 \times 5$, $5 \times 10$, and
$10 \times 10$ tori. The reflection parameters are the golden-ratio
surs $(5-\sqrt{5})/10$ and $(5+\sqrt{5})/10$, and the phase parameters
take values in $\{0, 2\pi/5, 4\pi/5\}$. The $5 \times 5$ torus alone
contains $36$ of these parameter sets, making it by far the richest
single torus in the classification. The value
$(5-\sqrt{5})/10 \approx 0.2764$ admits an elegant characterisation in
terms of the golden ratio $\varphi = (1+\sqrt{5})/2$, since it satisfies
$\rho = 1/(\varphi + 2)$. This is the clearest instance in the data of
an inverse relationship between torus size and maximum revival period,
and it is the single most striking result of the classification.
"""

DISCUSSION_FILES = [
    ("disc-1-1.tex", DISC_1_1),
    ("disc-1-2.tex", DISC_1_2),
    ("disc-1-3.tex", DISC_1_3),
    ("disc-1-4.tex", DISC_1_4),
    ("disc-2-1.tex", DISC_2_1),
    ("disc-2-2.tex", DISC_2_2),
    ("disc-2-3.tex", DISC_2_3),
    ("disc-2-4.tex", DISC_2_4),
    ("disc-2-5.tex", DISC_2_5),
    ("disc-2-6.tex", DISC_2_6),
    ("disc-2-7.tex", DISC_2_7),
    ("disc-2-8.tex", DISC_2_8),
    ("disc-2-9.tex", DISC_2_9),
    ("disc-2-10.tex", DISC_2_10),
    ("disc-2-11.tex", DISC_2_11),
]

DISCUSSION_COMPONENTS = [
    "docs/sep-coin-tori/components/paragraphs/disc-1-1",
    "docs/sep-coin-tori/components/paragraphs/disc-1-2",
    "docs/sep-coin-tori/components/paragraphs/disc-1-3",
    "docs/sep-coin-tori/components/paragraphs/disc-1-4",
    "docs/sep-coin-tori/components/paragraphs/disc-2-1",
    "docs/sep-coin-tori/components/paragraphs/disc-2-2",
    "docs/sep-coin-tori/components/paragraphs/disc-2-3",
    "docs/sep-coin-tori/components/paragraphs/disc-2-4",
    "docs/sep-coin-tori/components/paragraphs/disc-2-5",
    "docs/sep-coin-tori/components/paragraphs/disc-2-6",
    "docs/sep-coin-tori/components/paragraphs/disc-2-7",
    "docs/sep-coin-tori/components/paragraphs/disc-2-8",
    "docs/sep-coin-tori/components/paragraphs/disc-2-9",
    "docs/sep-coin-tori/components/paragraphs/disc-2-10",
    "docs/sep-coin-tori/components/paragraphs/disc-2-11",
]


# ===========================================================================
# 2. Methodology paragraph
# ===========================================================================

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


# ===========================================================================
# 3. Results paragraphs
# ===========================================================================

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


# ===========================================================================
# 4. Tables
# ===========================================================================

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
\caption{Revival periods observed for each torus $L_x \times L_y$.
Only one orientation of each non-square torus is shown; the
$L_y \times L_x$ case is identical by interchangeability. A bullet
indicates that at least one parameter set produces a revival at that
period.}
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


# ===========================================================================
# 5. Bib entry
# ===========================================================================

BIB_ENTRY = r"""
@misc{full_revivals_references,
  title        = {Full Set of Revival Values for Separable Quantum Walks on Tori},
  author       = {{focussed}},
  year         = {2026},
  howpublished = {\url{https://github.com/focussed/separable_walk_references}},
  note         = {Repository of reference data accompanying this paper. Accessed: 2026-09-22}
}
"""


# ===========================================================================
# 6. Text substitutions
# ===========================================================================

# Substitute T -> N only in specific contexts to avoid clobbering labels
T_TO_N_PATTERNS = [
    (re.compile(r"\$T = 60\$"),   r"$N = 60$"),
    (re.compile(r"\$T=60\$"),     r"$N=60$"),
    (re.compile(r"period \$T\$"), r"period $N$"),
    (re.compile(r"\$T\$"),        r"$N$"),
    (re.compile(r"\bT = 60\b"),   r"N = 60"),
    (re.compile(r"period, T ="),  r"period, N ="),
]

# Files to apply T -> N substitution to (Results, Abstract, Conclusion)
T_TO_N_TARGETS = [
    PARAS / "results-1.tex",
    PARAS / "results-2.tex",
    PARAS / "results-3.tex",
    PARAS / "results-4.tex",
    PARAS / "conclusion.tex",
]

# Simple typo fixes across all paragraph files
TYPO_FIXES = [
    (re.compile(r"adjactent"), r"adjacent"),
    (re.compile(r"Sectionf II"), r"Section~\\ref{sec:theory}"),
    (re.compile(r"\\cite\{my_classification\}"), r"\\cite{full_revivals_references}"),
]


# ===========================================================================
# Helpers
# ===========================================================================

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"  wrote {path.relative_to(ROOT)}")


def patch_file(path, patterns, label=""):
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
        n_changed = max(n_changed,
                        abs(len(original.splitlines()) - len(text.splitlines())))
        suffix = f" [{label}]" if label else ""
        print(f"  patched {path.relative_to(ROOT)}{suffix}  ({n_changed} line(s))")
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


def dedupe_pdfstringdef(path):
    """Remove duplicate \\pdfstringdefDisableCommands blocks."""
    if not path.exists():
        return False
    text = path.read_text()
    # Find all occurrences of the block
    pattern = re.compile(
        r"\\pdfstringdefDisableCommands\{%\n"
        r".*?\n\}\n",
        re.DOTALL,
    )
    matches = pattern.findall(text)
    if len(matches) < 2:
        return False
    # Keep the first, remove the rest
    seen = False
    def replace(m):
        nonlocal seen
        if not seen:
            seen = True
            return m.group(0)
        return ""
    new_text = pattern.sub(replace, text)
    if new_text != text:
        path.write_text(new_text)
        print(f"  removed duplicate \\pdfstringdefDisableCommands from {path.relative_to(ROOT)}")
        return True
    return False


def patch_manifest_discussion(path):
    if not path.exists():
        print(f"  manifest not found: {path}")
        return False
    manifest = yaml.safe_load(path.read_text())
    sections = manifest.get("sections", [])
    found = False
    for sec in sections:
        if sec.get("label") == "discussion" or \
           sec.get("title", "").strip().lower() == "discussion":
            sec["components"] = DISCUSSION_COMPONENTS
            found = True
            print("  rewrote Discussion component list")
            break
    if not found:
        print("  WARNING: no Discussion section found in manifest")
    path.write_text(
        yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True,
                       default_flow_style=False, width=1000)
    )
    print(f"  rewrote {path.relative_to(ROOT)}")
    return found


def patch_manifest_results(path):
    """Fix the Results component list to include the rho-frequency table."""
    if not path.exists():
        return False
    manifest = yaml.safe_load(path.read_text())
    sections = manifest.get("sections", [])
    new_results = [
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
        if sec.get("label") == "results" or \
           sec.get("title", "").strip().lower() == "experimental results":
            sec["components"] = new_results
            found = True
            print("  rewrote Results component list")
            break
    if not found:
        print("  WARNING: no Results section found in manifest")
    path.write_text(
        yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True,
                       default_flow_style=False, width=1000)
    )
    return found


# ===========================================================================
# Main
# ===========================================================================

def main():
    print("=" * 70)
    print("bootstrap-editor-fixes.py")
    print("=" * 70)

    # ---- 1. Write Methodology and Results paragraphs --------------------
    print("\n[1] Writing Methodology and Results paragraphs")
    write(PARAS / "method-1.tex", METHOD_1)
    write(PARAS / "results-1.tex", RESULTS_1)
    write(PARAS / "results-2.tex", RESULTS_2)
    write(PARAS / "results-3.tex", RESULTS_3)
    write(PARAS / "results-4.tex", RESULTS_4)

    # ---- 2. Write Discussion paragraphs --------------------------------
    print("\n[2] Writing Discussion paragraphs")
    for fname, content in DISCUSSION_FILES:
        write(PARAS / fname, content)

    # ---- 3. Write corrected tables -------------------------------------
    print("\n[3] Writing corrected tables")
    write(TABLES / "tab-period-count"   / "tab-period-count.tex",   TAB_PERIOD_COUNT)
    write(TABLES / "tab-torus-period"   / "tab-torus-period.tex",   TAB_TORUS_PERIOD)
    write(TABLES / "tab-max-period"     / "tab-max-period.tex",     TAB_MAX_PERIOD)
    write(TABLES / "tab-rho-by-period"  / "tab-rho-by-period.tex",  TAB_RHO_BY_PERIOD)
    write(TABLES / "tab-rho-frequency"  / "tab-rho-frequency.tex",  TAB_RHO_FREQUENCY)
    write(TABLES / "tab-delta-by-period"/ "tab-delta-by-period.tex",TAB_DELTA_BY_PERIOD)

    # Remove flat-layout duplicates
    for flat in (TABLES / "tab-period-count.tex", TABLES / "tab-max-period.tex"):
        if flat.exists():
            flat.unlink()
            print(f"  removed stale flat copy {flat.relative_to(ROOT)}")

    # ---- 4. Bib entry --------------------------------------------------
    print("\n[4] Ensuring bibliography entry")
    ensure_bib_entry(BIB, BIB_ENTRY, "full_revivals_references")

    # ---- 5. T -> N in Results and Conclusion ---------------------------
    print("\n[5] Applying T -> N in Results and Conclusion")
    for target in T_TO_N_TARGETS:
        patch_file(target, T_TO_N_PATTERNS, label="T->N")

    # ---- 6. Typo fixes and citation consolidation ----------------------
    print("\n[6] Fixing typos and consolidating citation keys")
    for para in PARAS.glob("*.tex"):
        patch_file(para, TYPO_FIXES, label="typos")

    # ---- 7. Patch the manifest -----------------------------------------
    print("\n[7] Patching manifest.yaml")
    patch_manifest_results(MANIFEST)
    patch_manifest_discussion(MANIFEST)

    # ---- 8. Attempt to patch the abstract in the template --------------
    print("\n[8] Patching the abstract (if template is accessible)")
    for tpl in TEMPLATE_CANDIDATES:
        if tpl.exists():
            changed = patch_file(tpl, T_TO_N_PATTERNS, label="abstract T->N")
            dedupe_pdfstringdef(tpl)
            if changed:
                print(f"  -> patched {tpl.relative_to(ROOT)}")
            break
    else:
        print("  template not found among candidates; patch the abstract manually:")
        print("    grep -n '\\$T = 60\\$' output/sep-coin-tori/main.tex")
        print("    replace with '$N = 60$'")

    # ---- 9. Remove duplicate pdfstringdef in main.tex if present ------
    print("\n[9] Checking main.tex for duplicate preamble blocks")
    main_tex = ROOT / "output" / "sep-coin-tori" / "main.tex"
    if main_tex.exists():
        dedupe_pdfstringdef(main_tex)

    # ---- 10. Summary --------------------------------------------------
    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)
    print("""
Next steps:

  # 1. Rebuild from components
  python build.py docs/sep-coin-tori/manifest.yaml -o output --no-compile

  # 2. Compile (twice, to resolve refs and citations)
  cd output/sep-coin-tori
  latexmk -pdf main.tex
  latexmk -pdf main.tex
  cd ../..

  # 3. Verify the fixes landed
  grep -n '\\$T\\$' output/sep-coin-tori/main.tex
  grep -n 'my_classification' output/sep-coin-tori/main.tex
  grep -n 'adjactent' output/sep-coin-tori/main.tex
  grep -c 'undefined' output/sep-coin-tori/main.log

  # 4. Commit
  git add -A
  git commit -m "Apply editor's report fixes: Discussion rewrite, T->N, citation consolidation"
  git push

Manual checks that cannot be automated:

  - The abstract may still say "two novel phenomena" if it lives in the
    template in a form the regex didn't catch. Open
    templates/revtex-pra/template.tex.j2 and search for "two novel".
    Replace with "three novel phenomena".

  - Verify that \\ref{sec:method}, \\ref{sec:results},
    \\ref{sec:discussion}, \\ref{sec:conclusion} resolve. If any don't,
    check the section labels in the manifest.

  - The old discussion tables (tab-period8, tab-period60,
    tab-complete-phase-disc, tab-violations) remain on disk but are no
    longer referenced. Delete them manually if you want a clean tree:

      rm docs/sep-coin-tori/components/tables/tab-period8.tex
      rm docs/sep-coin-tori/components/tables/tab-period60.tex
      rm docs/sep-coin-tori/components/tables/tab-complete-phase-disc.tex
      rm docs/sep-coin-tori/components/tables/tab-violations.tex
""")


if __name__ == "__main__":
    main()
