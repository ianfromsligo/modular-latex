#!/usr/bin/env python3
"""
bootstrap-discussion-10x10-figures.py

 1. Rewrite methodology as a simple step-by-step paragraph.
 2. Add a new Discussion paragraph on the 10x10 revival, placed
    immediately AFTER the existing N=60 paragraph (disc-2-11), so
    the N=30 discussion at disc-2-10 is preserved untouched.
 3. Write three figure component files for the images.
 4. Patch the manifest to insert the new paragraph and its three
    figures directly after disc-2-11.

Prerequisite: the three PNG files must already be in
docs/sep-coin-tori/components/figures/ with these names:

    fig-10x10-fidelity.png
    fig-10x10-probability.png
    fig-10x10-spin.png

Run:  python bootstrap-discussion-10x10-figures.py
"""

from pathlib import Path
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")


ROOT     = Path(__file__).parent.resolve()
DOC      = ROOT / "docs" / "sep-coin-tori"
COMP     = DOC / "components"
PARAS    = COMP / "paragraphs"
FIGS     = COMP / "figures"
MANIFEST = DOC / "manifest.yaml"


# ---------------------------------------------------------------------------
# 1. Simplified methodology paragraph
# ---------------------------------------------------------------------------

METHOD_1 = r"""The classification proceeds in three steps.

\emph{Step 1 (1D input).} We take as given the 1D revival set
$\{2, 3, 4, 5, 6, 8, 10\}$ from Theorem~1 and the corresponding 1D
parameter tables of Dukes~\cite{Dukes2014}. For each cycle length $k$ in
the revival set, these tables list the reflection and phase values
$(\rho, \delta)$ that produce a full-state revival, together with the
associated step count $N$.

\emph{Step 2 (1D verification).} For each tabulated 1D revival, we
assemble the walk operator $U_k = S_k(I_k \otimes C_k)$ in the
computational basis using the coin of Eq.~(\ref{eq:1d_coin}), raise it
to the tabulated step count $N$, and verify that $U_k^N$ equals the
identity up to a global phase to within a numerical tolerance of
$10^{-8}$.

\emph{Step 3 (2D pairing).} The 2D classification follows from the
tensor-product factorisation $U_{k \times m} = U_k \otimes U_m$ of
Eq.~(\ref{eq:factorised_unitary}). For each pair $(k, m)$ with
$k, m \in \{2, 3, 4, 5, 6, 8, 10\}$, we take the periods $N$ shared by
the two 1D revival sets $\mathcal{N}_k$ and $\mathcal{N}_m$ and, for each
such $N$, record every combination of 1D parameters
$(\rho_x, \delta_x) \in \mathcal{R}_k(N)$ and
$(\rho_y, \delta_y) \in \mathcal{R}_m(N)$ that produces the revival,
verifying each candidate by the same matrix-exponentiation check.

Because the 1D input is complete and the 2D pairing is exhaustive over
the finite revival set, the resulting classification of $209$
inequivalent parameter sets is complete. The verification script and the
full classification are available at \cite{full_revivals_references}.
"""


# ---------------------------------------------------------------------------
# 2. New Discussion paragraph on the 10x10 revival
#    (to be placed AFTER disc-2-11, the N=60 paragraph)
# ---------------------------------------------------------------------------

DISC_10X10 = r"""\subsubsection{The $10 \times 10$ revival: a case study}

The $10 \times 10$ torus is the largest torus in the classification that
admits the longest period $N = 60$, and it provides a clean illustration
of the revival mechanism. We take the reflection parameters
$\rho_x = \rho_y = (5-\sqrt{5})/10 \approx 0.2764$ and set
$\delta_x = \delta_y = 0$.

Figure~\ref{fig:10x10-fidelity} tracks the fidelity of the walker's
state against the initial state over eighty steps. The fidelity reaches
its maximum at $N = 60$ with a value numerically indistinguishable from
$1$; no other step in the range shown produces a full-state revival.
Figure~\ref{fig:10x10-probability} shows the position probability
distribution at ten snapshots between step~1 and step~70. The walker
starts localised at the origin, spreads outward over the first thirty
steps, and refocuses to the origin at $N = 60$, by which point the
distribution matches the initial condition almost exactly.

Figure~\ref{fig:10x10-spin} shows the four components of the spin (coin)
distribution over the same range. The coin state returns to its initial
values at both $N = 30$ and $N = 60$. The return at $N = 30$ is a
\emph{partial} revival only: the coin reconstructs itself while the
position distribution has not yet refocused, and no full-state revival
occurs at that step. It is only at $N = 60$ that the coin and position
distributions both coincide with their initial values, producing the
exact full-state revival recorded in Table~\ref{tab:period-count}. This
distinction between partial coin revival and full-state revival is
visible directly in the two panels of Figs.~\ref{fig:10x10-fidelity}
and~\ref{fig:10x10-spin}: the spin distribution shows structure at both
$N = 30$ and $N = 60$, while the fidelity remains below the revival
threshold at the former.
"""


# ---------------------------------------------------------------------------
# 3. Figure component .tex files
# ---------------------------------------------------------------------------

FIG_10X10_FIDELITY = r"""\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{fig-10x10-fidelity.png}
  \caption{Fidelity of the joint position$\otimes$coin state against the
           initial state, for the $10 \times 10$ torus with
           $\rho_x = \rho_y = (5-\sqrt{5})/10 \approx 0.2764$ and
           $\delta_x = \delta_y = 0$. The fidelity reaches
           $1$ at $N = 60$, confirming the exact full-state revival. A
           partial peak appears at $N = 30$, but the state does not
           fully refocus at that step.}
  \label{fig:10x10-fidelity}
\end{figure}
"""

FIG_10X10_PROBABILITY = r"""\begin{figure*}[htbp]
  \centering
  \includegraphics[width=\textwidth]{fig-10x10-probability.png}
  \caption{Position probability distribution at ten snapshots between
           step~1 and step~70, for the same parameters as
           Fig.~\ref{fig:10x10-fidelity}. The walker starts localised at
           the origin, spreads outward over the first thirty steps, and
           refocuses to the origin at $N = 60$. The distribution at
           step~60 matches the initial condition; the distributions at
           intermediate steps do not.}
  \label{fig:10x10-probability}
\end{figure*}
"""

FIG_10X10_SPIN = r"""\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{fig-10x10-spin.png}
  \caption{Spin (coin) distribution over eighty steps for the
           $10 \times 10$ torus at $\rho = (5-\sqrt{5})/10$,
           $\delta = 0$. The four coin components return to their
           initial values at both $N = 30$ and $N = 60$. The return at
           $N = 30$ is a partial revival of the coin alone; only at
           $N = 60$ does the position distribution also coincide with
           the initial condition, producing the full-state revival.}
  \label{fig:10x10-spin}
\end{figure}
"""


# ---------------------------------------------------------------------------
# Expected image filenames
# ---------------------------------------------------------------------------

EXPECTED_IMAGES = [
    "fig-10x10-fidelity.png",
    "fig-10x10-probability.png",
    "fig-10x10-spin.png",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"  wrote {path.relative_to(ROOT)}")


def check_images():
    missing = [n for n in EXPECTED_IMAGES if not (FIGS / n).exists()]
    if missing:
        print("  WARNING: the following image files are missing:")
        for n in missing:
            print(f"    {FIGS / n}")
        print("  Copy the three PNG files into that directory before building.")
    else:
        print("  all three image files present")


def patch_manifest(path):
    if not path.exists():
        sys.exit(f"manifest not found: {path}")

    manifest = yaml.safe_load(path.read_text())
    sections = manifest.get("sections", [])

    disc = None
    for sec in sections:
        if sec.get("label") == "discussion" or \
           sec.get("title", "").strip().lower() == "discussion":
            disc = sec
            break

    if disc is None:
        sys.exit("No Discussion section found in manifest")

    components = disc.get("components", [])

    # The new content goes immediately AFTER the N=60 paragraph
    # (disc-2-11). The N=30 paragraph (disc-2-10) is preserved.
    new_entries = [
        "docs/sep-coin-tori/components/paragraphs/disc-2-12",
        "docs/sep-coin-tori/components/figures/fig-10x10-fidelity",
        "docs/sep-coin-tori/components/figures/fig-10x10-probability",
        "docs/sep-coin-tori/components/figures/fig-10x10-spin",
    ]

    # Remove any prior insertion of these to keep the operation idempotent
    components = [c for c in components if c not in new_entries]

    # Find the index of disc-2-11 (N=60 paragraph)
    try:
        idx = components.index(
            "docs/sep-coin-tori/components/paragraphs/disc-2-11"
        )
    except ValueError:
        # Fallback: append at end
        idx = len(components) - 1

    # Insert AFTER disc-2-11
    insert_at = idx + 1
    for offset, entry in enumerate(new_entries):
        components.insert(insert_at + offset, entry)

    disc["components"] = components

    path.write_text(
        yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True,
                       default_flow_style=False, width=1000)
    )
    print(f"  rewrote {path.relative_to(ROOT)}")
    print(f"  inserted {len(new_entries)} entries after disc-2-11 "
          f"(N=60 paragraph)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("bootstrap-discussion-10x10-figures.py")
    print("=" * 70)

    # ---- 1. Rewrite methodology -----------------------------------------
    print("\n[1] Rewriting methodology as step-by-step")
    write(PARAS / "method-1.tex", METHOD_1)

    # ---- 2. Write the new 10x10 discussion paragraph as disc-2-12 -------
    print("\n[2] Writing 10x10 case study paragraph (disc-2-12)")
    write(PARAS / "disc-2-12.tex", DISC_10X10)

    # ---- 3. Write the three figure components ---------------------------
    print("\n[3] Writing figure component files")
    write(FIGS / "fig-10x10-fidelity"    / "fig-10x10-fidelity.tex",    FIG_10X10_FIDELITY)
    write(FIGS / "fig-10x10-probability" / "fig-10x10-probability.tex", FIG_10X10_PROBABILITY)
    write(FIGS / "fig-10x10-spin"        / "fig-10x10-spin.tex",        FIG_10X10_SPIN)

    # ---- 4. Check for the PNG files -------------------------------------
    print("\n[4] Checking for the three image files")
    check_images()

    # ---- 5. Patch the manifest ------------------------------------------
    print("\n[5] Patching manifest.yaml")
    patch_manifest(MANIFEST)

    # ---- 6. Summary ------------------------------------------------------
    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)
    print("""
What was done:

  - method-1.tex rewritten as three explicit steps.
  - disc-2-12.tex added: 10x10 case study, placed after the N=60
    paragraph. Includes the sentence about the partial coin revival
    at N=30.
  - Three figure components written and inserted into the Discussion.
  - The N=30 paragraph (disc-2-10) is untouched.

Next steps:

  # 1. Rebuild and compile
  python build.py docs/sep-coin-tori/manifest.yaml -o output
  cd output/sep-coin-tori
  latexmk -pdf main.tex
  cd ../..

  # 2. Verify the new content landed
  grep -n 'disc-2-12\\|fig-10x10' output/sep-coin-tori/main.tex

  # 3. Commit
  git add -A
  git commit -m "Simplify methodology; add 10x10 case study with three figures"
  git push
""")


if __name__ == "__main__":
    main()
