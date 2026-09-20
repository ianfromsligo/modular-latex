#!/usr/bin/env python3
"""Rewrite section 2 prose and tighten the theorem/proof.

Applies:
  - New prose for theory-1-1 through theory-1-7 (pre-example part of §2)
  - Cleaner wording in thm-revival-set.tex
  - Notation glossary and simplified Galois argument in proof-revival-set.tex

Leaves all eq-*.tex and cor-*/proof-corollary unchanged.
"""
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
DOC = ROOT / "docs" / "sep-coin-tori"
PARAS = DOC / "components" / "paragraphs"
THEOREMS = DOC / "components" / "theorems"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    try:
        rel = path.relative_to(ROOT)
    except ValueError:
        rel = path
    print(f"  wrote {rel}")


# =====================================================================
# Pre-example section 2 — prose files only (equations untouched)
# =====================================================================

write(PARAS / "theory-1-1.tex", r"""The single-step evolution of the walker is governed by the canonical
unitary operation
""")

write(PARAS / "theory-1-2.tex", r"""In the 1D cycle framework, Dukes \cite{Dukes2014} introduced the
parametrised coin operator
""")

write(PARAS / "theory-1-3.tex", r"""The construction extends to a two-dimensional \(k \times m\) toroidal
lattice by assembling the total state space as a tensor product of
position and coin Hilbert spaces,
\(\mathcal{H} = \mathcal{H}_p \otimes \mathcal{H}_c\). The spatial
component \(\mathcal{H}_p = \mathcal{H}_{p_x} \otimes
\mathcal{H}_{p_y}\) is spanned by the basis
\(\{|x, y\rangle : x \in \mathbb{Z}_k, y \in \mathbb{Z}_m\}\),
subject to the periodic boundary conditions \(x + k \equiv x\) and
\(y + m \equiv y\). The coin space
\(\mathcal{H}_c = \mathcal{H}_{c_x} \otimes \mathcal{H}_{c_y} \cong
\mathbb{C}^4\) carries the directional basis
\(\{|L\rangle, |R\rangle\} \otimes \{|D\rangle, |U\rangle\}\),
corresponding to negative and positive displacements along the
horizontal and vertical axes respectively. The Kronecker product in
lexicographical order yields the ordered basis
""")

write(PARAS / "theory-1-4.tex", r"""A separable coin factorises as \(C_{k \times m} = C_x(\rho_x,
\delta_x) \otimes C_y(\rho_y, \delta_y)\), with independent 1D
parameters on each axis. In the ordered basis above, the \(4 \times 4\)
matrix representation is
""")

write(PARAS / "theory-1-5.tex", r"""Because the spatial axes are orthogonal and the coin acts separably,
the conditional shift decomposes into commuting directional components
\(S = S_x S_y\). With subsystem identities \(I_x \equiv I_{p_x}
\otimes I_{c_x}\) and \(I_y \equiv I_{p_y} \otimes I_{c_y}\), the two
components are
""")

write(PARAS / "theory-1-6.tex", r"""The separability of the coin and the orthogonality of the axes yield
a tensor-product factorisation of the full unitary itself. Reordering
the total Hilbert space as \(\mathcal{H} \cong (\mathcal{H}_{p_x}
\otimes \mathcal{H}_{c_x}) \otimes (\mathcal{H}_{p_y} \otimes
\mathcal{H}_{c_y})\), the single-step operator reduces to
""")

write(PARAS / "theory-1-7.tex", r"""where \(U_k = S_{1D,x} (I_k \otimes C_x)\) and
\(U_m = S_{1D,y} (I_m \otimes C_y)\) are independent 1D evolution
operators on the \(x\)- and \(y\)-cycles. The factorisation isolates
the spectral constraints along each axis, so the root-of-unity
conditions that govern full-state revivals can be evaluated
dimension-by-dimension.
""")

# =====================================================================
# Theorem — cleaner wording
# =====================================================================

write(THEOREMS / "thm-revival-set.tex", r"""\begin{theorem}
A discrete-time quantum walk on a 1D cycle graph \(\mathbb{Z}_k\)
driven by Dukes' coin \(C(\rho, \delta) \in \mathrm{U}(2)\) admits a
non-trivial full-state revival with coin parameter \(\rho \in (0,1)\)
if and only if \(k \in \{2, 3, 4, 5, 6, 8, 10\}\).
\end{theorem}
""")

# =====================================================================
# Proof — notation glossary, simplified Galois argument
# =====================================================================

write(THEOREMS / "proof-revival-set.tex", r"""\begin{proof}
We first fix notation. Let \(k \in \mathbb{N}\) denote the number of
vertices on the cycle, \(N \in \mathbb{N}\) the candidate revival step
count, and \(j \in \{1, 2, \dots, \lfloor k/2 \rfloor\}\) the index of
a non-trivial spatial harmonic (Fourier mode) of the walk on the ring.
The single-step eigenphases are denoted \(\theta_j\), and \(\rho\) is
the reflection parameter of Dukes' coin, defined in
Eq.~(\ref{eq:1d_coin}).

A full-state revival, \(U_k^N = e^{i\phi} I_{2k}\), occurs if and only
if every eigenphase is a rational multiple of \(\pi\), i.e.\
\(\theta_j = r_j \pi / N\) for integers \(r_j\). This is the
root-of-unity condition, and it is the criterion we test.

For a cycle of size \(k\), the eigenphases obey the dispersion relation
\begin{equation} \label{eq:disp_rel}
\sin(\theta_j) = \sqrt{\rho} \sin\left(\frac{2\pi j}{k}\right).
\end{equation}
The strategy of the proof is to eliminate the coin parameter \(\rho\)
entirely and reduce the revival condition to a purely algebraic
constraint on \(k\). Consider the ratio of the second harmonic to the
fundamental:
\begin{equation}
\frac{\sin(\theta_2)}{\sin(\theta_1)}
= \frac{\sqrt{\rho}\sin\left(4\pi/k\right)}
       {\sqrt{\rho}\sin\left(2\pi/k\right)}
= 2\cos\left(\frac{2\pi}{k}\right).
\label{eq:mode_ratio}
\end{equation}
The factor \(\sqrt{\rho}\) cancels. On the left-hand side we have a
ratio of sines of rational multiples of \(\pi\), which is an algebraic
number in the cyclotomic subfield generated by such sines; on the
right-hand side we have a purely geometric constant determined by
\(k\). For a revival to exist, therefore, \(2\cos(2\pi/k)\) must lie in
the same cyclotomic subfield. This is a strong constraint.

Two cases are exceptional. For \(k = 2\) and \(k = 3\), the system has
only a single non-trivial spatial harmonic (\(j = 1\)), so
Eq.~(\ref{eq:mode_ratio}) does not apply; the revival condition reduces
to a solvable equation in \(\rho\), and both cycles admit non-trivial
revivals. We consider \(k \ge 4\) from here.

For \(k \ge 4\), the constant \(2\cos(2\pi/k)\) generates the real
cyclotomic subfield \(\mathbb{K}_k = \mathbb{Q}(\cos(2\pi/k))\). The
degree of this extension over \(\mathbb{Q}\), written
\(d(k) = [\mathbb{K}_k : \mathbb{Q}]\), is given by Euler's totient
function: \(d(k) = \phi(k)/2\) for all \(k \ge 3\)
\cite{Washington1997}. The revival condition therefore restricts \(k\)
by the size of \(\phi(k)\):

\begin{enumerate}
\item \textbf{Solvable regime (\(\phi(k)/2 \le 2\)).}
The candidate set is \(k \in \{2, 3, 4, 5, 6, 8, 10\}\) together with
the exceptional case \(k = 12\). For these sizes, \(2\cos(2\pi/k)\) is
either rational (\(d = 1\)) or quadratic (\(d = 2\)). A single real
parameter \(\rho\) then has sufficient freedom to synchronise the
spatial harmonics across the subfield, and non-trivial revivals with
\(\rho \in (0,1)\) exist for every candidate size except \(k = 12\).

\item \textbf{Degenerate case (\(k = 12\)).}
Although \(\phi(12)/2 = 2\) places \(k = 12\) in the quadratic regime,
this cycle has three non-trivial spatial harmonics (\(j = 1, 2, 3\)).
Evaluating the third harmonic gives
\begin{equation}
\sin(\theta_3) = \sqrt{\rho}\sin(\pi/2) = \sqrt{\rho}.
\end{equation}
For \(\theta_3\) to be a rational multiple of \(\pi\), \(\sqrt{\rho}\)
must be the sine of a rational angle, and simultaneous alignment with
the first two harmonics forces \(\theta_3 = \pi/2\) uniquely, hence
\(\rho = 1\). The coin then reduces to a deterministic reflector, and
no non-trivial revival exists in the open interval \(\rho \in (0,1)\).

\item \textbf{Overconstrained regime (\(\phi(k)/2 \ge 3\)).}
For \(k \in \{7, 9\}\) and all \(k \ge 11\) with the sole exception of
\(k = 12\), Euler's totient gives \(\phi(k) \ge 6\), hence
\(d(k) \ge 3\). The minimal polynomial of \(2\cos(2\pi/k)\) over
\(\mathbb{Q}\) has degree at least three.

A standard argument from algebraic number theory resolves this case.
If a revival existed, the automorphisms of the Galois group
\(\mathrm{Gal}(\mathbb{Q}(\zeta_{2N})/\mathbb{Q})\), where
\(\zeta_{2N} = e^{i\pi/N}\) is the \(2N\)-th root of unity
\cite{Niven1956}, would generate at least three independent algebraic
constraints from the dispersion relations---one for each conjugate of
\(2\cos(2\pi/k)\). A single real parameter \(\rho\) cannot satisfy
three independent constraints simultaneously. The system is
overconstrained, and only the boundary solutions \(\rho \in \{0, 1\}\)
survive.
\end{enumerate}

We therefore conclude that non-trivial full-state revivals
(\(\rho \in (0,1)\)) occur on 1D cycles if and only if
\(k \in \{2, 3, 4, 5, 6, 8, 10\}\).
\end{proof}
""")

print()
print("Done. Next:")
print("  python build.py docs/sep-coin-tori/manifest.yaml -o output --no-compile")
print("  sed -n '/sec:theory/,/sec:results/p' output/sep-coin-tori/main.tex | head -80")
print("  git add docs/sep-coin-tori/components/")
print("  git commit -m 'Rewrite section 2 prose; notation glossary in proof'")
print("  git push")
