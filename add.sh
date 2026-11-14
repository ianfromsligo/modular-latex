#!/usr/bin/env bash
# Add List of Figures / List of Tables as components.
# Run from the repo root (the dir containing docs/ and templates/).
set -euo pipefail

DOC="docs/thesis-coin-tori"
PAR="$DOC/components/paragraphs"
MAN="$DOC/manifest.yaml"

# ---- sanity checks ---------------------------------------------------------
[[ -f "$MAN" ]] || { echo "ERROR: $MAN not found. Run from repo root."; exit 1; }
[[ -d "$PAR" ]] || { echo "ERROR: $PAR not found."; exit 1; }

# ---- 1. component .tex files ----------------------------------------------
cat > "$PAR/list_of_figures.tex" <<'EOF'
\listoffigures
EOF
echo "wrote $PAR/list_of_figures.tex"

cat > "$PAR/list_of_tables.tex" <<'EOF'
\listoftables
EOF
echo "wrote $PAR/list_of_tables.tex"

# ---- 2. patch manifest.yaml -----------------------------------------------
# Insert the two entries after the "Glossary" entry in prelude, unless
# they're already present. Pure-bash + awk, no external YAML tool needed.
if grep -q 'components/paragraphs/list_of_figures' "$MAN"; then
  echo "manifest.yaml already has list_of_figures; skipping patch"
else
  cp "$MAN" "$MAN.bak"

  awk '
    BEGIN { in_prelude = 0; done = 0 }
    /^prelude:[[:space:]]*$/ { in_prelude = 1 }
    in_prelude && /^- title: Glossary[[:space:]]*$/ {
      print
      # consume the following two lines (components: + list_of_figures path)
      # — they exist only if we see them; if not, insert fresh
      getline c1
      getline c2
      if (c1 ~ /components:/ && c2 ~ /glossary/) {
        print c1
        print c2
        print "- title: List of Figures"
        print "  components:"
        print "  - docs/thesis-coin-tori/components/paragraphs/list_of_figures"
        print "- title: List of Tables"
        print "  components:"
        print "  - docs/thesis-coin-tori/components/paragraphs/list_of_tables"
        done = 1
        next
      }
      # glossary entry had a different shape — fall back to simple insert
      print c1
      print c2
      next
    }
    { print }
  ' "$MAN.bak" > "$MAN"

  echo "patched $MAN"
fi

# ---- 3. show the result ---------------------------------------------------
echo
echo "--- prelude section of manifest.yaml ---"
awk '/^prelude:/{f=1} f&&/^sections:/{exit} f{print}' "$MAN"
