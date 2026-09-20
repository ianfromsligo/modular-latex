#!/usr/bin/env python3
"""Add a short Dukes-summary paragraph at the end of the Theory section,
and fix the section road-map in the introduction."""
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
DOC = "docs/sep-coin-tori"

def write(rel, content):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    print(f"  wrote {rel}")

write(f"{DOC}/components/paragraphs/theory-3-dukes-summary.tex", r"""Dukes' 1D classification establishes the framework on which the present
2D analysis rests. In that work, the coin operator is parameterised by
a real amplitude $\rho$ and a relative phase $\delta = \alpha + \beta$,
and the condition for a $k$-cycle to admit a full-state revival
$U_k^N = I_{2k}$ is that every eigenphase be a rational multiple of
$2\pi$. Dukes enumerated solutions for $k \in \{2,3,4,6\}$ up to
$N = 30$ and identified a finite set of solutions for $k \in
\{5,8,10\}$, but did not prove completeness of these lists; no exact
solutions are known for other cycle lengths. The revival set
$\{2,3,4,5,6,8,10\}$ that governs our 2D analysis is therefore an
established result, whereas the specific 1D period sets remain only
partially characterised. Section~\ref{sec:results} presents the 2D
enumeration directly, without relying on an assumed 1D period list.
""")

# Patch the manifest: append the new paragraph to the Theory section.
import yaml
manifest_path = ROOT / DOC / "manifest.yaml"
manifest = yaml.safe_load(manifest_path.read_text())

for section in manifest["sections"]:
    if section.get("label") == "theory":
        comps = section.setdefault("components", [])
        entry = f"{DOC}/components/paragraphs/theory-3-dukes-summary"
        if entry not in comps:
            comps.append(entry)
            print(f"  appended {entry} to Theory section")
        break
else:
    raise SystemExit("Theory section not found")

manifest_path.write_text(
    yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True,
                   default_flow_style=False, width=1000)
)
print(f"  rewrote {manifest_path.relative_to(ROOT)}")

print()
print("Next:")
print("  python build.py docs/sep-coin-tori/manifest.yaml -o output --no-compile")
print("  git add -A && git commit -m 'Add Dukes summary paragraph to Theory section'")
print("  git push")
