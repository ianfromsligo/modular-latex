#!/usr/bin/env python3
"""
fix_disc_files.py — repair LaTeX escaping bugs in auto-generated
disc-*.tex files.

Bugs fixed:
  1. Nested math in lists:  $\{$a$, $b$, $c$\}$  -->  $\{a, b, c\}$
  2. Double-backslash times:  2\\times2  -->  2\times2
  3. Double-backslash commands:  \\pi  -->  \pi  (and other common ones)
  4. Trailing whitespace and stray blank lines

Run from the repo root:
    python3 tools/fix_disc_files.py

Backs up each modified file to <name>.tex.prefix.bak
"""

import re
from pathlib import Path

PARA_DIR = Path("docs/sep-coin-tori/components/paragraphs")

# ---------------------------------------------------------------------------
# Fix 1: nested math inside $\{ ... \}$
# ---------------------------------------------------------------------------

# Match a full $\{...\}$ block, possibly containing inner $...$ pairs.
# Non-greedy inner match, but anchored by the closing \}$.
NESTED = re.compile(r"\$\\\{(.+?)\\\}\$", re.DOTALL)

def _collapse_inner_math(inner: str) -> str:
    """inner looks like: $0.5000$, $0.5359$, $0.6667$"""
    # Remove every $ pair.
    inner = inner.replace("$", "")
    # Normalise separators: collapse multiple spaces around commas.
    inner = re.sub(r"\s*,\s*", ", ", inner.strip())
    # Collapse remaining whitespace runs.
    inner = re.sub(r"\s+", " ", inner)
    return inner

def fix_nested_math(text: str) -> str:
    def repl(match):
        inner = match.group(1)
        # Only collapse if there are *inner* math delimiters.
        if "$" in inner:
            inner = _collapse_inner_math(inner)
        return "$\\{" + inner + "\\}$"
    return NESTED.sub(repl, text)

# ---------------------------------------------------------------------------
# Fix 2 & 3: double-backslash commands
# ---------------------------------------------------------------------------

# Order matters: longest first so \\times isn't half-eaten by \\tim.
DOUBLE_BACKSLASH_COMMANDS = [
    r"\\times", r"\\cdot", r"\\pi", r"\\rho", r"\\delta", r"\\sqrt",
    r"\\frac", r"\\left", r"\\right", r"\\big", r"\\Big",
    r"\\mathcal", r"\\mathrm", r"\\text",
]

def fix_double_backslash(text: str) -> str:
    for cmd in DOUBLE_BACKSLASH_COMMANDS:
        single = cmd[1:]   # strip one backslash
        text = text.replace(cmd, single)
    return text

# ---------------------------------------------------------------------------
# Fix 4: whitespace hygiene
# ---------------------------------------------------------------------------

def fix_whitespace(text: str) -> str:
    # Strip trailing whitespace on each line
    lines = [ln.rstrip() for ln in text.splitlines()]
    # Collapse 3+ blank lines to 2
    out = []
    blanks = 0
    for ln in lines:
        if ln.strip() == "":
            blanks += 1
            if blanks <= 1:
                out.append(ln)
        else:
            blanks = 0
            out.append(ln)
    # Ensure single trailing newline
    return "\n".join(out).rstrip() + "\n"

# ---------------------------------------------------------------------------
# Apply
# ---------------------------------------------------------------------------

def fix_all(text: str) -> str:
    text = fix_nested_math(text)
    text = fix_double_backslash(text)
    text = fix_whitespace(text)
    return text

# ---------------------------------------------------------------------------
# Diagnostic
# ---------------------------------------------------------------------------

def report(text: str, name: str) -> None:
    """Print warnings for suspicious patterns still present after fix."""
    issues = []
    if r"\\" in text:
        issues.append("still contains \\\\")
    if re.search(r"\$\{[^}]*\$[^$]*\$[^}]*\}", text):
        issues.append("suspicious nested math")
    if re.search(r"\$\s*\$", text):
        issues.append("empty math $...$")
    if issues:
        print(f"  WARN: {name}: " + "; ".join(issues))

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    files = sorted(PARA_DIR.glob("disc-*.tex"))
    if not files:
        print(f"No files found in {PARA_DIR}")
        return

    print(f"Found {len(files)} files in {PARA_DIR}")
    n_fixed = 0
    for f in files:
        original = f.read_text()
        fixed = fix_all(original)
        if fixed != original:
            bak = f.with_suffix(".tex.prefix.bak")
            if not bak.exists():
                bak.write_text(original)
            f.write_text(fixed)
            n_fixed += 1
            print(f"  patched: {f.name}")
            report(fixed, f.name)
        else:
            report(original, f.name)

    print(f"\nPatched {n_fixed} / {len(files)} files.")
    print(f"Backups: {PARA_DIR}/*.prefix.bak")

    # Sanity checks on a few files
    print("\n--- sample output ---")
    for sample in ("disc-1-3.tex", "disc-auto-n4.tex", "disc-1-0.tex"):
        p = PARA_DIR / sample
        if p.exists():
            print(f"\n{sample}:")
            for ln in p.read_text().splitlines()[:5]:
                print(f"  {ln}")


if __name__ == "__main__":
    main()
