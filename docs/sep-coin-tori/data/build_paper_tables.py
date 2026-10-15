#!/usr/bin/env python3
"""
build_paper_tables.py

Clears the tables directory and regenerates the five LaTeX
tables from the deduped canonical CSV produced by EXP033.ipynb.

Run from the repo root:
    python docs/sep-coin-tori/data/build_paper_tables.py
"""

import csv
import math
import shutil
from pathlib import Path
from collections import Counter

DATA   = Path("docs/sep-coin-tori/data/EXP033_outputs")
CANON  = DATA / "2d_classification.csv"
VERIF  = DATA / "EXP033_1d_verification.txt"
TABLES = Path("docs/sep-coin-tori/components/tables")

# ---- clear the tables directory ----

if TABLES.exists():
    for entry in TABLES.iterdir():
        if entry.is_dir():
            shutil.rmtree(entry)
        elif entry.is_file() and (entry.suffix == ".tex"
                                  or entry.name.endswith(".tex.bak")):
            entry.unlink()
else:
    TABLES.mkdir(parents=True)
print(f"cleared {TABLES}")

# ---- exact rho forms ----

RHO_EXACT = [
    (0.5,                    r"\nicefrac{1}{2}"),
    (0.25,                   r"\nicefrac{1}{4}"),
    (0.75,                   r"\nicefrac{3}{4}"),
    (1/3,                    r"\nicefrac{1}{3}"),
    (2/3,                    r"\nicefrac{2}{3}"),
    ((5 - math.sqrt(5))/6,   r"\frac{5 - \sqrt{5}}{6}"),
    ((5 - math.sqrt(5))/8,   r"\frac{5 - \sqrt{5}}{8}"),
    ((5 + math.sqrt(5))/8,   r"\frac{5 + \sqrt{5}}{8}"),
    ((2 - math.sqrt(3))/2,   r"\frac{2 - \sqrt{3}}{2}"),
    ((5 - math.sqrt(5))/10,  r"\frac{5 - \sqrt{5}}{10}"),
    ((5 + math.sqrt(5))/10,  r"\frac{5 + \sqrt{5}}{10}"),
]

def exact_rho(rho):
    for (val, tex) in RHO_EXACT:
        if abs(rho - val) < 1e-4:
            return tex
    return f"{rho:.6f}"

# ---- parse the 1D verification log ----

def parse_1d_log(path):
    sigs = []
    with open(path) as f:
        for line in f:
            if not line.startswith("k="):
                continue
            parts = line.strip().split()
            k = int(parts[0].split("=")[1])
            rho = float(parts[1].split("=")[1])
            delta = float(parts[2].split("=")[1])
            N = int(parts[3].split("=")[1])
            prov = line[line.index("[")+1 : line.index("]")]
            sigs.append((k, rho, delta, N, prov))
    return sigs

one_d = parse_1d_log(VERIF)
print(f"parsed {len(one_d)} 1D signatures")

def delta_tex(d):
    if abs(d) < 1e-6:
        return "0"
    ratio = d / math.pi
    for (num, den) in [(1,2), (1,3), (2,3), (1,4), (3,4), (1,1),
                       (3,2), (4,3), (5,3), (5,4),
                       (1,5), (2,5), (3,5), (4,5),
                       (6,5), (7,5), (8,5), (9,5)]:
        if abs(ratio - num/den) < 1e-3:
            if den == 1:
                return r"\pi"
            if num == 1:
                return f"\\pi/{den}"
            return f"{num}\\pi/{den}"
    return f"{ratio:.3f}\\pi"

# ---- load the canonical 2D CSV ----

records = []
with open(CANON) as f:
    for r in csv.DictReader(f):
        records.append(dict(
            k=int(r["k"]), m=int(r["m"]), N=int(r["N"]),
            rho_x=float(r["rho_x"]), delta_x=float(r["delta_x"]),
            rho_y=float(r["rho_y"]), delta_y=float(r["delta_y"]),
            provenance=r["provenance"]))

print(f"loaded {len(records)} canonical 2D records")

tori    = sorted({(r["k"], r["m"]) for r in records})
periods = sorted({r["N"] for r in records})

def write_table(name, content):
    d = TABLES / name
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{name}.tex").write_text(content)
    print(f"  {name}/{name}.tex")

# ---- Table 1: 1D catalogue ----

# ---- Table 1: 1D catalogue ----

L = [r"\begin{longtable}{rrrrc}",
     r"\caption{Canonical 1D full-state revivals, with reflection "
     r"parameters in exact form.}"
     r"\label{tab:1d-catalogue-exact} \\",
     r"\toprule",
     r"$k$ & $\rho$ & $\delta$ & $N_{\min}$ & source \\",
     r"\midrule",
     r"\endfirsthead",
     r"\toprule",
     r"$k$ & $\rho$ & $\delta$ & $N_{\min}$ & source \\",
     r"\midrule",
     r"\endhead",
     r"\bottomrule",
     r"\endfoot"]
for (k, rho, delta, N, prov) in one_d:
    L.append(f"{k} & ${exact_rho(rho)}$ & ${delta_tex(delta)}$ & "
             f"{N} & {prov} \\\\")
L.append(r"\end{longtable}")
write_table("tab-1d-catalogue-exact", "\n".join(L))

# ---- Table 2: per-torus summary ----

L = [r"\begin{table*}[htbp]", r"\centering",
     r"\caption{Per-torus summary: canonical 2D revivals and "
     r"range of revival periods.}",
     r"\label{tab:tori-summary}",
     r"\begin{tabular}{lrcr}", r"\toprule",
     r"Torus & Records & $N$ range & max $N$ \\", r"\midrule"]
for (k, m) in tori:
    sub = [r for r in records if r["k"] == k and r["m"] == m]
    Ns = [r["N"] for r in sub]
    L.append(f"${k}\\times{m}$ & {len(sub)} & "
             f"${min(Ns)}$--${max(Ns)}$ & ${max(Ns)}$ \\\\")
L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
write_table("tab-tori-summary", "\n".join(L))

# ---- Table 3: grid for N <= 60 ----

short = [N for N in periods if N <= 60]
L = [r"\begin{table*}[htbp]", r"\centering",
     r"\caption{Revival periods observed on each torus for "
     r"$N \le 60$. A bullet indicates at least one canonical "
     r"revival at that period.}",
     r"\label{tab:torus-period-n60}",
     r"\begin{tabular}{l" + "c" * len(short) + "}", r"\toprule",
     "Torus & " + " & ".join(f"${N}$" for N in short) + r" \\",
     r"\midrule"]
for (k, m) in tori:
    row = [f"${k}\\times{m}$"]
    for N in short:
        hit = any(r["k"] == k and r["m"] == m and r["N"] == N
                  for r in records)
        row.append(r"$\bullet$" if hit else "")
    L.append(" & ".join(row) + r" \\")
L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
write_table("tab-torus-period-n60", "\n".join(L))

# ---- Table 4: per-period summary ----

L = [r"\begin{table}[htbp]", r"\centering",
     r"\caption{Per-period summary: canonical records at each "
     r"revival period.}",
     r"\label{tab:period-summary}",
     r"\begin{tabular}{rr}", r"\toprule",
     r"$N$ & Records \\", r"\midrule"]
for N in periods:
    n = sum(1 for r in records if r["N"] == N)
    L.append(f"${N}$ & {n} \\\\")
L += [r"\midrule", f"Total & {len(records)} \\\\",
      r"\bottomrule", r"\end{tabular}", r"\end{table}"]
write_table("tab-period-summary", "\n".join(L))

# ---- Table 5: delta summary ----

def is_zero(x):
    return abs(x) < 1e-6 or abs(abs(x) - 2*math.pi) < 1e-6

cat = Counter()
for r in records:
    dx0 = is_zero(r["delta_x"]); dy0 = is_zero(r["delta_y"])
    if dx0 and dy0: cat["both_zero"] += 1
    elif dx0 or dy0: cat["one_zero"] += 1
    elif abs(r["delta_x"] - r["delta_y"]) < 1e-6: cat["equal_nonzero"] += 1
    else: cat["unequal_nonzero"] += 1

total = sum(cat.values())
L = [r"\begin{table}[htbp]", r"\centering",
     r"\caption{Distribution of phase parameters across the "
     r"canonical 2D revivals.}",
     r"\label{tab:delta-summary}",
     r"\begin{tabular}{lrr}", r"\toprule",
     r"Category & Count & Percentage \\", r"\midrule"]
for key, label in [
    ("both_zero",       r"$\delta_x = \delta_y = 0$"),
    ("one_zero",        r"exactly one of $\delta_x,\delta_y$ zero"),
    ("equal_nonzero",   r"$\delta_x = \delta_y \neq 0$"),
    ("unequal_nonzero", r"$\delta_x \neq \delta_y$, both non-zero"),
]:
    n = cat[key]; pct = 100.0 * n / total
    L.append(f"{label} & {n} & {pct:.1f}\\% \\\\")
L += [r"\midrule", f"Total & {total} & 100\\% \\\\",
      r"\bottomrule", r"\end{tabular}", r"\end{table}"]
write_table("tab-delta-summary", "\n".join(L))

# ---- summary ----

print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"1D signatures:      {len(one_d)}")
print(f"canonical records:  {len(records)}")
print(f"tori:               {len(tori)}")
print(f"periods:            {len(periods)}")
print(f"grid columns:       {len(short)} (N <= 60)")
print()
print("phase categories:")
for key in ["both_zero", "one_zero", "equal_nonzero", "unequal_nonzero"]:
    print(f"  {key:<18}  {cat[key]:>6}  ({100*cat[key]/total:.1f}%)")
