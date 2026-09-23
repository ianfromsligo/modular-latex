#!/usr/bin/env python3
"""
fix-10x10-figpaths.py

Rewrite the three figure .tex files to use compile-root-relative paths
(the same convention as fig-one-step.tex), so LaTeX finds the PNGs from
the output/sep-coin-tori/ compile directory.

Run:  python fix-10x10-figpaths.py
"""

from pathlib import Path

ROOT = Path(__file__).parent.resolve()
FIGS = ROOT / "docs" / "sep-coin-tori" / "components" / "figures"

PREFIX = "../../docs/sep-coin-tori/components/figures"


FIG_FIDELITY = r"""\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{%(prefix)s/fig-10x10-fidelity.png}
  \caption{Fidelity of the joint position$\otimes$coin state against the
           initial state, for the $10 \times 10$ torus with
           $\rho_x = \rho_y = (5-\sqrt{5})/10 \approx 0.2764$ and
           $\delta_x = \delta_y = 0$. The fidelity reaches
           $1$ at $N = 60$, confirming the exact full-state revival. A
           partial peak appears at $N = 30$, but the state does not
           fully refocus at that step.}
  \label{fig:10x10-fidelity}
\end{figure}
""" % {"prefix": PREFIX}


FIG_PROBABILITY = r"""\begin{figure*}[htbp]
  \centering
  \includegraphics[width=\textwidth]{%(prefix)s/fig-10x10-probability.png}
  \caption{Position probability distribution at ten snapshots between
           step~1 and step~70, for the same parameters as
           Fig.~\ref{fig:10x10-fidelity}. The walker starts localised at
           the origin, spreads outward over the first thirty steps, and
           refocuses to the origin at $N = 60$. The distribution at
           step~60 matches the initial condition; the distributions at
           intermediate steps do not.}
  \label{fig:10x10-probability}
\end{figure*}
""" % {"prefix": PREFIX}


FIG_SPIN = r"""\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{%(prefix)s/fig-10x10-spin.png}
  \caption{Spin (coin) distribution over eighty steps for the
           $10 \times 10$ torus at $\rho = (5-\sqrt{5})/10$,
           $\delta = 0$. The four coin components return to their
           initial values at both $N = 30$ and $N = 60$. The return at
           $N = 30$ is a partial revival of the coin alone; only at
           $N = 60$ does the position distribution also coincide with
           the initial condition, producing the full-state revival.}
  \label{fig:10x10-spin}
\end{figure}
""" % {"prefix": PREFIX}


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"  wrote {path.relative_to(ROOT)}")


def main():
    print("Rewriting figure files with compile-root-relative paths")
    write(FIGS / "fig-10x10-fidelity"    / "fig-10x10-fidelity.tex",    FIG_FIDELITY)
    write(FIGS / "fig-10x10-probability" / "fig-10x10-probability.tex", FIG_PROBABILITY)
    write(FIGS / "fig-10x10-spin"        / "fig-10x10-spin.tex",        FIG_SPIN)

    print("\nVerify:")
    for name in ("fig-10x10-fidelity", "fig-10x10-probability", "fig-10x10-spin"):
        f = FIGS / name / f"{name}.tex"
        if f.exists():
            for line in f.read_text().splitlines():
                if "includegraphics" in line:
                    print(f"  {name}: {line.strip()}")

    print("\nNext:")
    print("  python build.py docs/sep-coin-tori/manifest.yaml -o output")
    print("  cd output/sep-coin-tori && latexmk -pdf main.tex")


if __name__ == "__main__":
    main()
