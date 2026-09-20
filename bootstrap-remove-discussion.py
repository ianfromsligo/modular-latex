#!/usr/bin/env python3
"""Remove four redundant discussion subsections and their tables.

Removes from manifest (whole subsections):
  - Torus Size Inversely Controls Maximum Period   (disc-6-1, tab-max-period-disc)
  - Algebraic Structure                            (disc-7-1, tab-algebraic)
  - Phase Quantisation                             (disc-8-1, tab-phase-quant)
  - Comparison with Dukes (2014)                   (disc-9-1)

Deletes on disk (git rm --cached + unlink):
  - The four paragraph .tex files
  - The three table .tex files

Does NOT touch disc-10-1, disc-11-1, disc-12-1 or any other component.
Prints a plan and asks for confirmation before acting.
"""
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.resolve()
DOC = ROOT / "docs" / "sep-coin-tori"
MANIFEST = DOC / "manifest.yaml"

# Subsection titles to remove (must match manifest exactly).
SUBSECTIONS_TO_REMOVE = [
    "Torus Size Inversely Controls Maximum Period",
    "Algebraic Structure",
    "Phase Quantisation",
    "Comparison with Dukes (2014)",
]

# Component files to delete from disk (relative to repo root).
FILES_TO_DELETE = [
    "docs/sep-coin-tori/components/paragraphs/disc-6-1.tex",
    "docs/sep-coin-tori/components/paragraphs/disc-7-1.tex",
    "docs/sep-coin-tori/components/paragraphs/disc-8-1.tex",
    "docs/sep-coin-tori/components/paragraphs/disc-9-1.tex",
    "docs/sep-coin-tori/components/tables/tab-max-period-disc.tex",
    "docs/sep-coin-tori/components/tables/tab-algebraic.tex",
    "docs/sep-coin-tori/components/tables/tab-phase-quant.tex",
]


def main() -> None:
    manifest = yaml.safe_load(MANIFEST.read_text())

    # Locate the Discussion section.
    discussion = None
    for section in manifest.get("sections", []):
        if section.get("label") == "discussion":
            discussion = section
            break
    if discussion is None:
        sys.exit("No section with label 'discussion' found in manifest")

    subs = discussion.get("subsections") or []

    # Identify which subsections we'll remove, and confirm each exists.
    found = []
    for s in subs:
        if s.get("title") in SUBSECTIONS_TO_REMOVE:
            found.append(s)

    missing = [t for t in SUBSECTIONS_TO_REMOVE
               if t not in [s.get("title") for s in found]]
    if missing:
        print("WARNING: the following subsections were not found:")
        for t in missing:
            print(f"  - {t}")
        print("Check the manifest before proceeding.")
        sys.exit(1)

    # Show the plan.
    print("=" * 70)
    print("PLAN")
    print("=" * 70)
    print()
    print("Subsections to remove from the manifest:")
    for s in found:
        print(f"  - {s['title']}")
        for c in s.get("components", []):
            print(f"      {c}")
    print()
    print("Files to delete from disk:")
    for f in FILES_TO_DELETE:
        p = ROOT / f
        exists = "exists" if p.exists() else "MISSING"
        print(f"  [{exists}] {f}")
    print()
    print("Remaining subsections after removal:")
    for s in subs:
        if s.get("title") not in SUBSECTIONS_TO_REMOVE:
            print(f"  - {s['title']}")
    print()
    print("=" * 70)

    # Confirm.
    answer = input("Proceed? [y/N] ").strip().lower()
    if answer not in ("y", "yes"):
        print("Aborted.")
        sys.exit(0)

    # Edit manifest.
    discussion["subsections"] = [
        s for s in subs if s.get("title") not in SUBSECTIONS_TO_REMOVE
    ]
    MANIFEST.write_text(
        yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True,
                       default_flow_style=False, width=1000)
    )
    print(f"  rewrote {MANIFEST.relative_to(ROOT)}")

    # Delete files (git rm handles tracked files; fall back to unlink).
    for f in FILES_TO_DELETE:
        p = ROOT / f
        if not p.exists():
            print(f"  skipped (missing): {f}")
            continue
        try:
            subprocess.run(["git", "rm", "-q", f], cwd=ROOT, check=True)
            print(f"  git rm {f}")
        except subprocess.CalledProcessError:
            p.unlink()
            print(f"  unlinked (untracked): {f}")

    print()
    print("Done. Next:")
    print("  python build.py docs/sep-coin-tori/manifest.yaml -o output --no-compile")
    print("  grep -n 'subsection' output/sep-coin-tori/main.tex")
    print("  git add -A")
    print("  git commit -m 'Remove redundant discussion subsections and tables'")
    print("  git push")


if __name__ == "__main__":
    main()
