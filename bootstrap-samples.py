#!/usr/bin/env python3
"""Rebuild both sample docs to final spec. Applies from v0.2 state."""
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
        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()
        print(f"  removed {rel}")

# =====================================================================
# 1. article-sample template (formal paper, two authors, email in footer)
# =====================================================================
print("==> templates/article-sample")
write("templates/article-sample/template.tex.j2", r"""\documentclass[11pt]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{fancyhdr}
\usepackage[margin=1in]{geometry}

% Footer: primary author's email on every page
\pagestyle{fancy}
\fancyhf{}
<%- if manifest.metadata.authors[0].email %>
\fancyfoot[L]{\texttt{<<- manifest.metadata.authors[0].email ->>}}
<%- endif %>
\fancyfoot[R]{\thepage}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Search paths so components can use repo-root-relative \input paths
\makeatletter
\def\input@path{{../}{../docs/<<- manifest._doc_name ->>/components/}{../docs/<<- manifest._doc_name ->>/components/paragraphs/}{../docs/<<- manifest._doc_name ->>/components/equations/}{../docs/<<- manifest._doc_name ->>/components/tables/}{../docs/<<- manifest._doc_name ->>/components/figures/}}
\makeatother
\graphicspath{{../}{../docs/<<- manifest._doc_name ->>/components/figures/}}

\title{ <<- manifest.metadata.title ->> }
\author{
<%- for a in manifest.metadata.authors %>
  << a.name >>
  <%- if a.email %>
  \\ \texttt{<< a.email >>}
  <%- endif %>
  <%- if a.affiliation %>
  \\ \small << a.affiliation >>
  <%- endif %>
  <%- if not loop.last %> \\[0.8em] \and <%- endif %>
<%- endfor %>
}
\date{ <<- manifest.metadata.date ->> }

\begin{document}

\maketitle

\begin{abstract}
<<- manifest.metadata.abstract >>
\end{abstract}

<%- for section in manifest.sections %>
\section{ <<- section.title ->> }
<%- if section.subsections %>
<%- for sub in section.subsections %>
\subsection{ <<- sub.title ->> }
<%- for comp in sub.components %>
<< emit(comp) >>
<%- endfor %>
<%- endfor %>
<%- endif %>
<%- if section.components %>
<%- for comp in section.components %>
<< emit(comp) >>
<%- endfor %>
<%- endif %>
<%- endfor %>

<%- if manifest.acknowledgements %>
\section*{Acknowledgements}
<<- manifest.acknowledgements >>
<%- endif %>

\bibliographystyle{plain}
\bibliography{ <<- manifest.metadata.bibliography | replace('.bib','') | basename ->> }

\end{document}
""")

# =====================================================================
# 2. article-labnote template (informal record, one author, subsections)
# =====================================================================
print("==> templates/article-labnote")
write("templates/article-labnote/template.tex.j2", r"""\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage[margin=1in]{geometry}
\usepackage{xcolor}
\usepackage{float}
\usepackage{array}
\usepackage{multirow}

\definecolor{revival}{RGB}{34,139,34}
\definecolor{entangled}{RGB}{70,130,180}
\definecolor{star}{RGB}{255,165,0}

% Search paths so components can use repo-root-relative \input paths
\makeatletter
\def\input@path{{../}{../docs/<<- manifest._doc_name ->>/components/}{../docs/<<- manifest._doc_name ->>/components/paragraphs/}{../docs/<<- manifest._doc_name ->>/components/equations/}{../docs/<<- manifest._doc_name ->>/components/tables/}{../docs/<<- manifest._doc_name ->>/components/figures/}}
\makeatother
\graphicspath{{../}{../docs/<<- manifest._doc_name ->>/components/figures/}}

<%- if manifest.metadata.subtitle %>
\title{ <<- manifest.metadata.title ->> \\
       \large <<- manifest.metadata.subtitle ->> }
<%- else %>
\title{ <<- manifest.metadata.title ->> }
<%- endif %>
\author{ <<- manifest.metadata.author.name ->> }
<%- if manifest.metadata.author.email %>
\date{ <<- manifest.metadata.date ->> \\ \texttt{<<- manifest.metadata.author.email ->>} }
<%- else %>
\date{ <<- manifest.metadata.date ->> }
<%- endif %>

\begin{document}

\maketitle

\begin{abstract}
<<- manifest.metadata.abstract >>
\end{abstract}

<%- if manifest.prelude %>
<%- for section in manifest.prelude %>
\section*{ <<- section.title ->> }
<%- for comp in section.components %>
<< emit(comp) >>
<%- endfor %>
<%- endfor %>
<%- endif %>

<%- for section in manifest.sections %>
\section{ <<- section.title ->> }
<%- if section.subsections %>
<%- for sub in section.subsections %>
\subsection{ <<- sub.title ->> }
<%- for comp in sub.components %>
<< emit(comp) >>
<%- endfor %>
<%- endfor %>
<%- endif %>
<%- if section.components %>
<%- for comp in section.components %>
<< emit(comp) >>
<%- endfor %>
<%- endif %>
<%- endfor %>

<%- if manifest.postlude %>
<%- for section in manifest.postlude %>
\section*{ <<- section.title ->> }
<%- for comp in section.components %>
<< emit(comp) >>
<%- endfor %>
<%- endfor %>
<%- endif %>

<%- if manifest.metadata.bibliography %>
\bibliographystyle{plain}
\bibliography{ <<- manifest.metadata.bibliography | replace('.bib','') | basename ->> }
<%- endif %>

\end{document}
""")

# =====================================================================
# 3. DOC: sample-paper
# =====================================================================
print("==> docs/sample-paper")
rm("docs/sample-paper")
DOC = "docs/sample-paper"

write(f"{DOC}/manifest.yaml", """template: article-sample

metadata:
  title: "A Sample Paper: Demonstration of the Modular LaTeX Pipeline"
  authors:
    - name: Aoife Ní Bhriain
      email: aoife.nibhriain@atu.ie
      affiliation: Atlantic Technological University, Sligo
    - name: Declan O'Sullivan
      affiliation: University of Galway, Galway
  date: "18th September 2026"
  abstract: >
    This is a sample paper demonstrating the modular-LaTeX pipeline.
    It contains three paragraphs of introduction, a theoretical framework
    with two subsections and a figure, a results section with two tables
    and a figure, a discussion with a table, a conclusion, and
    acknowledgements. The document is assembled from components held under
    docs/sample-paper/components/ by build.py, and compiled by continuous
    integration on every push.
  bibliography: docs/sample-paper/references.bib

acknowledgements: >
  The authors thank their colleagues for helpful discussions, and
  acknowledge the support of their respective institutions.

sections:
  - title: Introduction
    components:
      - docs/sample-paper/components/paragraphs/intro-1
      - docs/sample-paper/components/paragraphs/intro-2
      - docs/sample-paper/components/paragraphs/intro-3

  - title: Theoretical Framework
    subsections:
      - title: First Subsection
        components:
          - docs/sample-paper/components/paragraphs/theory-1a
          - docs/sample-paper/components/figures/fig-overview
          - docs/sample-paper/components/paragraphs/theory-1b
      - title: Second Subsection
        components:
          - docs/sample-paper/components/paragraphs/theory-2a
          - docs/sample-paper/components/paragraphs/theory-2b

  - title: Results
    components:
      - docs/sample-paper/components/paragraphs/results-1
      - docs/sample-paper/components/tables/tab-results-1
      - docs/sample-paper/components/tables/tab-results-2
      - docs/sample-paper/components/figures/fig-results
      - docs/sample-paper/components/paragraphs/results-2

  - title: Discussion of Results
    components:
      - docs/sample-paper/components/paragraphs/discussion-1
      - docs/sample-paper/components/paragraphs/discussion-2
      - docs/sample-paper/components/tables/tab-discussion

  - title: Conclusion
    components:
      - docs/sample-paper/components/paragraphs/conclusion-1
      - docs/sample-paper/components/paragraphs/conclusion-2
""")

write(f"{DOC}/references.bib", r"""@article{Dukes2014,
  title={Quantum state revivals in quantum walks on cycles},
  author={Dukes, Peter R.},
  journal={Results in Physics},
  volume={4},
  pages={189--197},
  year={2014},
  publisher={Elsevier},
  doi={10.1016/j.rinp.2014.08.011}
}

@article{Jayakody2018,
  title={Full state revivals in higher dimensional quantum walks},
  author={Jayakody, Mahesh N. and Nanayakkara, Asiri},
  journal={Results in Physics},
  volume={11},
  pages={1008--1012},
  year={2018},
  doi={10.1016/j.rinp.2018.10.054}
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
""")

write(f"{DOC}/components/paragraphs/intro-1.tex", r"""Discrete-time quantum walks on finite graphs exhibit a striking
phenomenon: under certain coin and topology conditions, the walker's
state returns exactly to its initial configuration after a fixed number
of steps. These \emph{full-state revivals} were classified on 1D cycles
by Dukes~\cite{Dukes2014}, and the algebraic structure that governs
them has since been connected to cyclotomic fields~\cite{Washington1997}.
""")

write(f"{DOC}/components/paragraphs/intro-2.tex", r"""Extending the classification to higher-dimensional lattices raises
immediate questions. Does the tensor-product structure of a separable
coin preserve the 1D revival set, or does it introduce new periods?
The recent work of Jayakody and Nanayakkara~\cite{Jayakody2018}
suggests that higher-dimensional walks admit revivals beyond the
1D classification, but a complete treatment is still missing.
""")

write(f"{DOC}/components/paragraphs/intro-3.tex", r"""In this sample paper we exercise the modular-LaTeX pipeline end to
end: components are stored as individual files, selected by a manifest,
assembled into a templated document, and compiled by continuous
integration. The scientific content is illustrative only; the point is
to demonstrate that each paragraph, equation, table, and figure can be
edited in isolation and that the assembled output tracks those changes.
""")

write(f"{DOC}/components/paragraphs/theory-1a.tex", r"""The single-step evolution of the walker on a $k \times m$ toroidal
lattice is governed by the canonical unitary operation
\begin{equation}
  U = S \, (I_p \otimes C),
  \label{eq:general-evolution}
\end{equation}
where $I_p$ denotes the identity on the position space, $C$ is the coin
operator, and $S$ is the conditional shift operator.
""")

write(f"{DOC}/components/paragraphs/theory-1b.tex", r"""Because the spatial directions are orthogonal and the coin acts
separably, the conditional shift operator decomposes into commuting
directional components $S = S_x S_y$. This tensor-product factorisation
isolates the spectral constraints along each axis, so the root-of-unity
conditions that govern full-state revivals can be evaluated
dimension-by-dimension. Figure~\ref{fig:overview} illustrates the
decomposition.
""")

write(f"{DOC}/components/figures/fig-overview/fig-overview.tex", r"""\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.75\linewidth]{\figpath/overview.png}
  \caption{The tensor-product decomposition of a separable-coin walk on
           a toroidal lattice. Each spatial direction contributes an
           independent 1D evolution operator.}
  \label{fig:overview}
\end{figure}
""")

write(f"{DOC}/components/figures/fig-overview/meta.yaml", """type: figure
title: Tensor-product decomposition
asset: overview.png
status: sample
""")

write(f"{DOC}/components/paragraphs/theory-2a.tex", r"""A full-state revival occurs if and only if every eigenphase of $U$ is a
rational multiple of $2\pi$. On a $k$-cycle, this condition constrains
$k$ to the set $\{2, 3, 4, 5, 6, 8, 10\}$. The proof proceeds by
examining the ratio of consecutive spatial harmonics, which is forced
to be a purely geometric quantity independent of the coin parameter.
""")

write(f"{DOC}/components/paragraphs/theory-2b.tex", r"""For a $k \times m$ torus, the same argument applied independently to
each dimension yields the corollary: a revival exists if and only if
both $k$ and $m$ lie in the 1D revival set \emph{and} their achievable
revival period sets share a common element. This is the main
theoretical result of the framework.
""")

write(f"{DOC}/components/paragraphs/results-1.tex", r"""We present the results of an exhaustive search for complete quantum
revivals on $k \times m$ tori with $k, m \in \{2, 3, 4, 5, 6, 8, 10\}$.
Revivals are found at periods
\begin{equation}
  T \in \{\,2,\ 6,\ 8,\ 10,\ 12,\ 16,\ 20,\ 24,\ 30,\ 60\,\},
\end{equation}
across the torus sizes considered. Table~\ref{tab:results-1} summarises
the number of parameter sets producing each period.
""")

write(f"{DOC}/components/tables/tab-results-1/tab-results-1.tex", r"""\begin{table}[htbp]
  \centering
  \caption{Revival periods and the number of parameter sets producing
           each.}
  \label{tab:results-1}
  \begin{tabular}{lcccccccccc}
    \toprule
    $T$ & 2 & 6 & 8 & 10 & 12 & 16 & 20 & 24 & 30 & 60 \\
    \midrule
    Sets & 4 & 1 & 20 & 4 & 133 & 25 & 16 & 115 & 4 & 36 \\
    \bottomrule
  \end{tabular}
\end{table}
""")

write(f"{DOC}/components/tables/tab-results-2/tab-results-2.tex", r"""\begin{table}[htbp]
  \centering
  \caption{Maximum observed revival period by torus size.}
  \label{tab:results-2}
  \begin{tabular}{cc}
    \toprule
    Torus & Maximum $T$ \\
    \midrule
    $2 \times 2$   & 2  \\
    $3 \times 3$   & 30 \\
    $4 \times 4$   & 24 \\
    $5 \times 5$   & 60 \\
    $8 \times 8$   & 24 \\
    $10 \times 10$ & 60 \\
    \bottomrule
  \end{tabular}
\end{table}
""")

write(f"{DOC}/components/figures/fig-results/fig-results.tex", r"""\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.7\linewidth]{\figpath/results.png}
  \caption{Revival period as a function of torus dimension for the
           three largest periods observed.}
  \label{fig:results}
\end{figure}
""")

write(f"{DOC}/components/figures/fig-results/meta.yaml", """type: figure
title: Revival period versus torus size
asset: results.png
status: sample
""")

write(f"{DOC}/components/paragraphs/results-2.tex", r"""Two structural facts stand out. First, the longest period $T=60$ occurs
on the smallest prime torus $5 \times 5$, inverting the classical
intuition that larger state spaces recur more slowly. Second, all
reflection parameters fall into a small set of rational or low-degree
surd values, with the duality $\rho \leftrightarrow 1-\rho$ manifest
throughout. Figure~\ref{fig:results} plots the period against torus
dimension for the three largest periods.
""")

write(f"{DOC}/components/paragraphs/discussion-1.tex", r"""The comparison between symmetric and asymmetric torus sizes reveals a
fundamental principle: the arithmetic structure of the dimensions
determines the achievable revival periods more than their magnitude
does. A $5 \times 5$ torus supports a longer period than an
$8 \times 8$ torus despite having fewer states.
""")

write(f"{DOC}/components/paragraphs/discussion-2.tex", r"""This inversion of the classical intuition has practical consequences
for state-routing and quantum memory architectures: the smallest
torus on which a desired period occurs is often the most efficient
choice. Table~\ref{tab:discussion} collects the observations that
support this conclusion.
""")

write(f"{DOC}/components/tables/tab-discussion/tab-discussion.tex", r"""\begin{table}[htbp]
  \centering
  \caption{Summary of the inverse relationship between torus size and
           maximum revival period.}
  \label{tab:discussion}
  \begin{tabular}{lcc}
    \toprule
    Torus & Maximum $T$ & Notes \\
    \midrule
    $2 \times 2$   & 2  & only symmetric revivals \\
    $3 \times 3$   & 30 & isolated family \\
    $5 \times 5$   & 60 & longest period, smallest prime \\
    $8 \times 8$   & 24 & capped \\
    $10 \times 10$ & 60 & golden-ratio parameters \\
    \bottomrule
  \end{tabular}
\end{table}
""")

write(f"{DOC}/components/paragraphs/conclusion-1.tex", r"""We have presented a sample paper assembled from modular components,
demonstrating that individual paragraphs, equations, tables, and
figures can be edited in isolation and that the assembled output
tracks those changes automatically. The scientific content is
illustrative; the pipeline is the point.
""")

write(f"{DOC}/components/paragraphs/conclusion-2.tex", r"""Future work includes migrating the real scientific content into this
structure, adding further templates for different output styles, and
introducing automated checks for cross-reference integrity. The
infrastructure is in place; the remaining work is content.
""")

# =====================================================================
# 4. DOC: sample-experiment (lab note, record-style)
# =====================================================================
print("==> docs/sample-experiment")
rm("docs/sample-experiment")
DOC = "docs/sample-experiment"

write(f"{DOC}/manifest.yaml", """template: article-labnote

metadata:
  title: "EXP099: A Sample Experiment Log"
  subtitle: "Demonstrating the informal record-document template"
  author:
    name: Ian Craig
  date: "18th September 2026"
  abstract: >
    This is a sample experiment log, demonstrating the article-labnote
    template. Unlike a formal paper, this is a record document: it
    records what was done, what was found, and what remains to be
    investigated. It contains a revision history, an introduction, a
    theory section with subsections, a method section, results with
    tables and a figure, a discussion, a conclusion, and a code
    availability section.
  bibliography: docs/sample-experiment/references.bib

prelude:
  - title: Revision History
    components:
      - docs/sample-experiment/components/tables/revision-history

sections:
  - title: Introduction
    components:
      - docs/sample-experiment/components/paragraphs/intro-1
      - docs/sample-experiment/components/paragraphs/intro-2

  - title: Theory
    subsections:
      - title: Entangled Coins
        components:
          - docs/sample-experiment/components/paragraphs/theory-1a
          - docs/sample-experiment/components/equations/eq-bell-states
          - docs/sample-experiment/components/paragraphs/theory-1b
      - title: Sign Structure
        components:
          - docs/sample-experiment/components/paragraphs/theory-2a
          - docs/sample-experiment/components/tables/tab-correlation

  - title: Method
    components:
      - docs/sample-experiment/components/paragraphs/method-1
      - docs/sample-experiment/components/paragraphs/method-2

  - title: Results
    components:
      - docs/sample-experiment/components/paragraphs/results-1
      - docs/sample-experiment/components/tables/tab-revivals
      - docs/sample-experiment/components/figures/fig-revival-plot
      - docs/sample-experiment/components/paragraphs/results-2
      - docs/sample-experiment/components/tables/tab-all-coins

  - title: Discussion
    components:
      - docs/sample-experiment/components/paragraphs/discussion-1
      - docs/sample-experiment/components/paragraphs/discussion-2

  - title: Conclusion
    components:
      - docs/sample-experiment/components/paragraphs/conclusion

postlude:
  - title: Code Availability
    components:
      - docs/sample-experiment/components/paragraphs/code-availability
""")

write(f"{DOC}/references.bib", r"""@article{Dukes2014,
  title={Quantum state revivals in quantum walks on cycles},
  author={Dukes, Peter R.},
  journal={Results in Physics},
  volume={4},
  pages={189--197},
  year={2014},
  publisher={Elsevier},
  doi={10.1016/j.rinp.2014.08.011}
}

@article{Jayakody2018,
  title={Full state revivals in higher dimensional quantum walks},
  author={Jayakody, Mahesh N. and Nanayakkara, Asiri},
  journal={Results in Physics},
  volume={11},
  pages={1008--1012},
  year={2018},
  doi={10.1016/j.rinp.2018.10.054}
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

write(f"{DOC}/components/paragraphs/intro-1.tex", r"""This log records an exploration of entangled coins on $n \times m$
tori. Previous experiments in this series classified separable coins
and fixed non-separable coins; the present experiment introduces
entangled coins based on Bell states as a new class. The aim is to
determine the revival periods each Bell state produces on small tori.
""")

write(f"{DOC}/components/paragraphs/intro-2.tex", r"""The log is written in the informal record style: sections record what
was attempted, what was found, and what remains to be investigated.
No formal claims are made; the document serves as a durable record of
the experiment and a starting point for future work.
""")

write(f"{DOC}/components/paragraphs/theory-1a.tex", r"""Two qubits are mapped to the four spatial directions (R, L, U, D). The
Bell states are the maximally entangled two-qubit states, and each
induces a specific correlation between the $x$ and $y$ motions of the
walker.
""")

write(f"{DOC}/components/equations/eq-bell-states.tex", r"""\begin{align}
  |\Phi^+\rangle &= \frac{1}{\sqrt{2}}(|R\rangle + |D\rangle), \\
  |\Phi^-\rangle &= \frac{1}{\sqrt{2}}(|R\rangle - |D\rangle), \\
  |\Psi^+\rangle &= \frac{1}{\sqrt{2}}(|L\rangle + |U\rangle), \\
  |\Psi^-\rangle &= \frac{1}{\sqrt{2}}(|L\rangle - |U\rangle).
\end{align}
""")

write(f"{DOC}/components/paragraphs/theory-1b.tex", r"""The entangled coin is a unitary transformation that maps the
computational basis to the Bell basis. The four Bell states are
obtained by applying phase patterns to a common base matrix.
""")

write(f"{DOC}/components/paragraphs/theory-2a.tex", r"""The only difference between $\Phi^+$ and $\Phi^-$ is a relative minus
sign. This sign determines whether the two components interfere
constructively or destructively when the walker's paths recombine, and
it controls the revival period.
""")

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

write(f"{DOC}/components/paragraphs/method-1.tex", r"""The simulation followed the same procedure as previous experiments in
this series. For each $n \times m$ torus with
$n, m \in \{2, 3, 4\}$, we constructed the unitary step operator for
each Bell-state coin and propagated an initial localised state forward
in discrete steps.
""")

write(f"{DOC}/components/paragraphs/method-2.tex", r"""A revival was recorded when the propagated state matched the initial
state to within numerical tolerance. Because the operator is unitary,
a revival at step $N$ implies revivals at all multiples of $N$; we
record the fundamental period, the smallest such $N$.
""")

write(f"{DOC}/components/paragraphs/results-1.tex", r"""Table~\ref{tab:revivals} summarises the fundamental revival periods
found for each Bell state on the tori considered. The $\Phi^-$ state on
the $2 \times 2$ torus is the fastest at period 8; the other Bell states
are three times slower on the same torus. Figure~\ref{fig:revival-plot}
visualises the comparison.
""")

write(f"{DOC}/components/tables/tab-revivals/tab-revivals.tex", r"""\begin{table}[H]
\centering
\caption{Full state revivals for entangled coins (fundamental periods).}
\label{tab:revivals}
\begin{tabular}{lcccc}
\toprule
\textbf{Torus} & $\Phi^+$ & $\Phi^-$ & $\Psi^+$ & $\Psi^-$ \\
\midrule
$2 \times 2$ & 24 & \textbf{8} & 24 & 24 \\
$3 \times 3$ & --- & --- & --- & --- \\
$3 \times 4$ & --- & --- & --- & --- \\
$4 \times 4$ & 24 & --- & 24 & --- \\
\bottomrule
\end{tabular}
\end{table}
""")

write(f"{DOC}/components/figures/fig-revival-plot/fig-revival-plot.tex", r"""\begin{figure}[H]
  \centering
  \includegraphics[width=0.7\linewidth]{\figpath/revival-plot.png}
  \caption{Revival period by Bell state on the $2 \times 2$ torus. The
           $\Phi^-$ state stands out as the fastest.}
  \label{fig:revival-plot}
\end{figure}
""")

write(f"{DOC}/components/figures/fig-revival-plot/meta.yaml", """type: figure
title: Revival period by Bell state
asset: revival-plot.png
status: sample
""")

write(f"{DOC}/components/paragraphs/results-2.tex", r"""Table~\ref{tab:all-coins} compares the Bell-state coins to the other
coin types tested in earlier experiments on the same torus. The
$\Phi^-$ Bell coin matches the Hadamard 4D coin at period 8, and both
are slower than the Grover coin at period 4.
""")

write(f"{DOC}/components/tables/tab-all-coins/tab-all-coins.tex", r"""\begin{table}[H]
\centering
\caption{Comparison of coin types on $2 \times 2$ torus.}
\label{tab:all-coins}
\begin{tabular}{lcc}
\toprule
\textbf{Coin Type} & \textbf{Fundamental Period $N$} & \textbf{Revivals per 100 steps} \\
\midrule
Grover & 4 & 25 \\
Bell $\Phi^-$ & 8 & 12 \\
Hadamard 4D & 8 & 12 \\
Bell $\Phi^+$ & 24 & 4 \\
Bell $\Psi^+$ & 24 & 4 \\
Bell $\Psi^-$ & 24 & 4 \\
DFT & 16 & 6 \\
\bottomrule
\end{tabular}
\end{table}
""")

write(f"{DOC}/components/paragraphs/discussion-1.tex", r"""The relative sign in the Bell state has an outsized effect on the
revival period. Comparing $\Phi^-$ (minus sign, period 8) to $\Phi^+$
(plus sign, period 24) shows that a single sign change triples the
period. This is the most surprising result of the experiment.
""")

write(f"{DOC}/components/paragraphs/discussion-2.tex", r"""Several questions remain open. No revivals were found on the
$3 \times 3$ or $3 \times 4$ tori with any Bell coin, and the
$4 \times 4$ torus revived only with $\Phi^+$ and $\Psi^+$. Whether
these gaps reflect a fundamental constraint or simply the small range
of torus sizes tested is unclear and should be addressed in a follow-up.
""")

write(f"{DOC}/components/paragraphs/conclusion.tex", r"""Entangled coins form a new class of non-separable quantum walk coins.
The key finding is that the sign pattern in the Bell state controls the
revival period: the $\Phi^-$ state on the $2 \times 2$ torus revives at
period 8, while the other three Bell states revive at period 24. This
opens a design direction in which the sign structure of an entangled
coin is used to engineer the walker's periodicity.
""")

write(f"{DOC}/components/paragraphs/code-availability.tex", r"""The complete Python simulation code is available at:
\url{https://github.com/ianfromsligo/EXP099_sample_log}
""")

# =====================================================================
# 5. Figure generator
# =====================================================================
print("==> tools/make_sample_figures.py")
rm("tools/make_sample_figure.py")

write("tools/make_sample_figures.py", r'''"""Generate all sample figures for the sample docs."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path


def _save(fig, out):
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out}")


def paper_overview():
    fig, ax = plt.subplots(figsize=(5.5, 3))
    ax.text(0.5, 0.85, "U  =  U_k  x  U_m", ha="center", va="center",
            fontsize=15, family="monospace")
    ax.text(0.25, 0.42, "U_k", ha="center", va="center", fontsize=17,
            bbox=dict(boxstyle="round,pad=0.35", fc="#cfe8ff", ec="#333"))
    ax.text(0.75, 0.42, "U_m", ha="center", va="center", fontsize=17,
            bbox=dict(boxstyle="round,pad=0.35", fc="#d5f5d5", ec="#333"))
    ax.annotate("", xy=(0.32, 0.5), xytext=(0.44, 0.78),
                arrowprops=dict(arrowstyle="->", color="#333"))
    ax.annotate("", xy=(0.68, 0.5), xytext=(0.56, 0.78),
                arrowprops=dict(arrowstyle="->", color="#333"))
    ax.text(0.25, 0.15, "x-direction", ha="center", fontsize=9)
    ax.text(0.75, 0.15, "y-direction", ha="center", fontsize=9)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    _save(fig, "docs/sample-paper/components/figures/fig-overview/overview.png")


def paper_results():
    fig, ax = plt.subplots(figsize=(5.5, 3))
    sizes = ["2", "3", "4", "5", "8", "10"]
    periods = [2, 30, 24, 60, 24, 60]
    ax.bar(sizes, periods, color="#cfe8ff", edgecolor="#333")
    ax.set_xlabel("Torus dimension L (L x L)")
    ax.set_ylabel("Maximum period T")
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    _save(fig, "docs/sample-paper/components/figures/fig-results/results.png")


def experiment_revival_plot():
    fig, ax = plt.subplots(figsize=(5, 3))
    states = ["Phi+", "Phi-", "Psi+", "Psi-"]
    periods = [24, 8, 24, 24]
    colors = ["#cfe8ff", "#ffd7b3", "#cfe8ff", "#cfe8ff"]
    ax.bar(states, periods, color=colors, edgecolor="#333")
    ax.set_ylabel("Fundamental period N")
    ax.set_xlabel("Bell state")
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    _save(fig, "docs/sample-experiment/components/figures/fig-revival-plot/revival-plot.png")


if __name__ == "__main__":
    paper_overview()
    paper_results()
    experiment_revival_plot()
''')

# =====================================================================
# 6. .gitignore update
# =====================================================================
print("==> .gitignore")
gi = ROOT / ".gitignore"
keep = []
for line in gi.read_text().splitlines() if gi.exists() else []:
    if "pipeline.png" in line:
        continue
    keep.append(line)
new_lines = [
    "docs/sample-paper/components/figures/fig-overview/overview.png",
    "docs/sample-paper/components/figures/fig-results/results.png",
    "docs/sample-experiment/components/figures/fig-revival-plot/revival-plot.png",
]
for line in new_lines:
    if line not in keep:
        keep.append(line)
gi.write_text("\n".join(keep) + "\n")
print("  updated .gitignore")

# =====================================================================
# 7. workflow generator call
# =====================================================================
print("==> workflow")
wf = ROOT / ".github/workflows/build.yml"
src = wf.read_text()
if "make_sample_figure.py" in src:
    src = src.replace("python tools/make_sample_figure.py",
                      "python tools/make_sample_figures.py")
    wf.write_text(src)
    print("  updated generator call")
else:
    print("  workflow already uses make_sample_figures.py (or step was renamed)")

print()
print("Done. Next:")
print("  python tools/make_sample_figures.py")
print("  python build.py docs/sample-paper/manifest.yaml -o output --overleaf overleaf --no-compile")
print("  python build.py docs/sample-experiment/manifest.yaml -o output --overleaf overleaf --no-compile")
print("  head -40 output/sample-paper/main.tex")
print("  git add -A && git commit -m 'Rebuild sample docs to spec; add article-sample template'")
print("  git push")
