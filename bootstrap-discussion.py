#!/usr/bin/env python3
"""
bootstrap-discussion.py

Replace the Discussion section of the sep-coin-tori document with the
two-part version:

  Part A: four general-observation paragraphs (disc-1-1 .. disc-1-4)
  Part B: eleven per-period paragraphs   (disc-2-1 .. disc-2-11)

Also removes obsolete Discussion components from the manifest and
leaves the old files on disk (they are not deleted).

Prints a per-file summary as it goes.

Run:  python bootstrap-discussion.py
"""

from pathlib import Path
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")


ROOT     = Path(__file__).parent.resolve()
DOC      = ROOT / "docs" / "sep-coin-tori"
PARAS    = DOC / "components" / "paragraphs"
MANIFEST = DOC / "manifest.yaml"


# ---------------------------------------------------------------------------
# Part A - General findings
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Part B - Specific findings, by period
# ---------------------------------------------------------------------------

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


# New paragraph files in order
NEW_DISC_FILES = [
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

# New manifest component list for Discussion
NEW_DISC_COMPONENTS = [
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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"  wrote {path.relative_to(ROOT)}")


def patch_manifest(path):
    if not path.exists():
        sys.exit(f"manifest not found: {path}")
    manifest = yaml.safe_load(path.read_text())
    sections = manifest.get("sections", [])

    found = False
    for sec in sections:
        if sec.get("label") == "discussion" or \
           sec.get("title", "").strip().lower() == "discussion":
            sec["components"] = NEW_DISC_COMPONENTS
            found = True
            print("  rewrote Discussion component list")
            break

    if not found:
        print("  WARNING: no Discussion section found; add manually")

    path.write_text(
        yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True,
                       default_flow_style=False, width=1000)
    )
    print(f"  rewrote {path.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("bootstrap-discussion.py")
    print("=" * 70)

    # ---- 1. Write the new Discussion paragraphs -------------------------
    print("\n[1] Writing Discussion paragraphs")
    for fname, content in NEW_DISC_FILES:
        write(PARAS / fname, content)

    # ---- 2. Patch the manifest ------------------------------------------
    print("\n[2] Patching manifest.yaml")
    patch_manifest(MANIFEST)

    # ---- 3. Summary ------------------------------------------------------
    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)
    print("""
Next steps:

  # 1. rebuild
  python build.py docs/sep-coin-tori/manifest.yaml -o output --no-compile

  # 2. check the Discussion section renders
  sed -n '/sec:discussion/,/sec:conclusion/p' output/sep-coin-tori/main.tex | head -80

  # 3. commit
  git add -A
  git commit -m "Replace Discussion section with two-part structure"
  git push

Note: the following old files are no longer referenced by the manifest
but remain on disk. Delete them manually if you want a clean tree:

  rm docs/sep-coin-tori/components/paragraphs/disc-3-1.tex
  rm docs/sep-coin-tori/components/paragraphs/disc-3-2.tex
  rm docs/sep-coin-tori/components/paragraphs/disc-4-1.tex
  rm docs/sep-coin-tori/components/paragraphs/disc-5-1.tex
  rm docs/sep-coin-tori/components/paragraphs/disc-6-1.tex
  rm docs/sep-coin-tori/components/paragraphs/disc-7-1.tex
  rm docs/sep-coin-tori/components/paragraphs/disc-8-1.tex
  rm docs/sep-coin-tori/components/paragraphs/disc-9-1.tex
  rm docs/sep-coin-tori/components/paragraphs/disc-10-1.tex
  rm docs/sep-coin-tori/components/paragraphs/disc-11-1.tex
  rm docs/sep-coin-tori/components/paragraphs/disc-12-1.tex

  rm docs/sep-coin-tori/components/tables/tab-period8.tex
  rm docs/sep-coin-tori/components/tables/tab-period60.tex
  rm docs/sep-coin-tori/components/tables/tab-complete-phase-disc.tex
  rm docs/sep-coin-tori/components/tables/tab-violations.tex
""")


if __name__ == "__main__":
    main()
