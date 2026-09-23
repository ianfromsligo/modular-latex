#!/usr/bin/env python3
"""
bootstrap-fix-manifest-discussion.py

Repairs the Discussion section of the manifest by:
  1. Removing the stale subsections: block that referenced the old
     discussion files (disc-1-2-n2, disc-1-3-n8, ..., tab-period8,
     tab-period60, tab-complete-phase-disc, tab-violations).
  2. Replacing the Discussion components with the new list of 15 files
     plus two subsection wrapper files (disc-1-0, disc-2-0).
  3. Writing the two wrapper files if not present.
  4. Adding \\usepackage{nicefrac} to the RevTeX template if it is
     missing.

Run:  python bootstrap-fix-manifest-discussion.py
"""

from pathlib import Path
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")


ROOT      = Path(__file__).parent.resolve()
DOC       = ROOT / "docs" / "sep-coin-tori"
PARAS     = DOC / "components" / "paragraphs"
MANIFEST  = DOC / "manifest.yaml"

TEMPLATES = [
    ROOT / "templates" / "revtex-pra" / "template.tex.j2",
]


NEW_DISCUSSION_COMPONENTS = [
    "docs/sep-coin-tori/components/paragraphs/disc-1-0",
    "docs/sep-coin-tori/components/paragraphs/disc-1-1",
    "docs/sep-coin-tori/components/paragraphs/disc-1-2",
    "docs/sep-coin-tori/components/paragraphs/disc-1-3",
    "docs/sep-coin-tori/components/paragraphs/disc-1-4",
    "docs/sep-coin-tori/components/paragraphs/disc-2-0",
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
            # Replace the entire section: new components, remove subsections
            sec.pop("subsections", None)
            sec["components"] = NEW_DISCUSSION_COMPONENTS
            found = True
            print("  rewrote Discussion: components replaced, subsections removed")
            break

    if not found:
        print("  WARNING: no Discussion section found in manifest")

    path.write_text(
        yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True,
                       default_flow_style=False, width=1000)
    )
    print(f"  rewrote {path.relative_to(ROOT)}")


def ensure_nicefrac(template_path):
    if not template_path.exists():
        print(f"  template not found: {template_path.relative_to(ROOT)}, skipped")
        return False
    text = template_path.read_text()
    if "\\usepackage{nicefrac}" in text:
        print(f"  {template_path.relative_to(ROOT)} already loads nicefrac")
        return False
    # Insert after \usepackage{enumitem} or after the last \usepackage line
    marker = "\\usepackage{enumitem}"
    if marker in text:
        text = text.replace(marker, marker + "\n\\usepackage{nicefrac}")
    else:
        # Fallback: insert after last \usepackage{...}
        import re
        last = None
        for m in re.finditer(r"\\usepackage\{[^}]+\}", text):
            last = m
        if last is None:
            print(f"  no \\usepackage lines found in {template_path.relative_to(ROOT)}")
            return False
        text = text[:last.end()] + "\n\\usepackage{nicefrac}" + text[last.end():]
    template_path.write_text(text)
    print(f"  added \\usepackage{{nicefrac}} to {template_path.relative_to(ROOT)}")
    return True


def main():
    print("=" * 70)
    print("bootstrap-fix-manifest-discussion.py")
    print("=" * 70)

    # ---- 1. Write subsection wrapper files ------------------------------
    print("\n[1] Writing subsection wrapper files")
    write(PARAS / "disc-1-0.tex", "\\subsection{General Observations}\n")
    write(PARAS / "disc-2-0.tex", "\\subsection{Period-by-Period Observations}\n")

    # ---- 2. Patch the manifest ------------------------------------------
    print("\n[2] Patching manifest.yaml")
    patch_manifest(MANIFEST)

    # ---- 3. Ensure nicefrac is loaded ----------------------------------
    print("\n[3] Checking for nicefrac in the template")
    for tpl in TEMPLATES:
        if tpl.exists():
            ensure_nicefrac(tpl)
            break
    else:
        print("  no template found among candidates")

    # ---- 4. Summary -----------------------------------------------------
    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)
    print("""
Next steps:

  # 1. Rebuild and compile
  python build.py docs/sep-coin-tori/manifest.yaml -o output
  cd output/sep-coin-tori
  latexmk -pdf main.tex
  cd ../..

  # 2. Verify the old discussion files are no longer referenced
  grep -n 'disc-1-2-n2\\|disc-1-3-n8\\|disc-3-1\\|tab-period8\\|tab-violations' \\
       output/sep-coin-tori/main.tex
  # expected: no matches

  # 3. Verify the new discussion renders
  grep -n 'General Observations\\|Period-by-Period' output/sep-coin-tori/main.tex

  # 4. Commit
  git add -A
  git commit -m "Fix Discussion manifest: remove stale subsections; add nicefrac"
  git push

Optional cleanup (removes old files no longer referenced):

  rm docs/sep-coin-tori/components/paragraphs/disc-1-2-n2.tex
  rm docs/sep-coin-tori/components/paragraphs/disc-1-3-n8.tex
  rm docs/sep-coin-tori/components/paragraphs/disc-1-4-n12.tex
  rm docs/sep-coin-tori/components/paragraphs/disc-1-5-n16.tex
  rm docs/sep-coin-tori/components/paragraphs/disc-1-6-n20.tex
  rm docs/sep-coin-tori/components/paragraphs/disc-1-7-n24.tex
  rm docs/sep-coin-tori/components/paragraphs/disc-1-8-n30.tex
  rm docs/sep-coin-tori/components/paragraphs/disc-3-1.tex
  rm docs/sep-coin-tori/components/paragraphs/disc-3-2.tex
  rm docs/sep-coin-tori/components/paragraphs/disc-4-1.tex
  rm docs/sep-coin-tori/components/paragraphs/disc-5-1.tex
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
