import re
from collections import defaultdict, Counter

rows = []
with open("table-reduced-surd.tex") as f:
    for line in f:
        m = re.match(r"\$(\d+) \\times (\d+)\$ & (\d+) & (.+?) & (.+?) & (.+?) & (.+?) \\\\", line.strip())
        if m:
            rows.append((int(m[1]), int(m[2]), int(m[3]), m[4], m[5], m[6], m[7]))

# Table 1: period -> (tori, rows)
by_N = defaultdict(lambda: {"tori": set(), "rows": 0})
for lx, ly, N, *_ in rows:
    by_N[N]["tori"].add((lx, ly))
    by_N[N]["rows"] += 1

print("Table 1: N | tori | rows")
for N in sorted(by_N):
    print(f"  {N} | {len(by_N[N]['tori'])} | {by_N[N]['rows']}")

# Table 2: torus -> (periods, rows, symmetric?)
by_torus = defaultdict(lambda: {"N": set(), "rows": 0, "sym": 0})
for lx, ly, N, rx, dx, ry, dy in rows:
    by_torus[(lx, ly)]["N"].add(N)
    by_torus[(lx, ly)]["rows"] += 1
    if rx == ry:
        by_torus[(lx, ly)]["sym"] += 1

print("\nTable 2: torus | periods | rows | rows with rx=ry")
for t in sorted(by_torus):
    info = by_torus[t]
    print(f"  {t[0]}x{t[1]} | {sorted(info['N'])} | {info['rows']} | {info['sym']}")

# Table 3: rho distribution
rho_counts = Counter()
for *_, rx, dx, ry, dy in rows:
    rho_counts[rx] += 1
    rho_counts[ry] += 1

print("\nTable 3: rho | occurrences across all rows")
for rho, cnt in sorted(rho_counts.items(), key=lambda x: -x[1]):
    print(f"  {rho} | {cnt}")

# Table 4: delta distribution
delta_counts = Counter()
for *_, rx, dx, ry, dy in rows:
    delta_counts[dx] += 1
    delta_counts[dy] += 1

print("\nTable 4: delta | occurrences")
for d, cnt in sorted(delta_counts.items(), key=lambda x: -x[1]):
    print(f"  {d} | {cnt}")
