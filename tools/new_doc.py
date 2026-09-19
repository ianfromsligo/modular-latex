#!/usr/bin/env python3
"""Scaffold a new document under docs/ from an existing template.

Usage:
    python tools/new_doc.py exp031-new-thing --template article-labnote
    python tools/new_doc.py my-paper --template revtex-pra --title "My Paper"
"""
import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()

TEMPLATE_DEFAULTS = {
    "article-sample": {
        "title": "A New Paper",
        "authors_yaml": (
            '    - name: Author One\n'
            '      email: author.one@example.com\n'
            '      affiliation: University One\n'
            '    - name: Author Two\n'
            '      affiliation: University Two'
        ),
        "date": '"today"',
        "extra": 'acknowledgements: >\n  Add acknowledgements here.',
    },
    "article-labnote": {
        "title": "EXP###: A New Experiment Log",
        "subtitle": "One-line subtitle",
        "author_name": "Ian Craig",
        "author_email": "ian.craig@atu.ie",
        "date": '"today"',
        "extra": "",
    },
    "revtex-pra": {
        "title": "A New APS Paper",
        "authors_yaml": (
            '    - name: Ian Craig\n'
            '      email: ian.craig@atu.ie\n'
            '      affiliation: Atlantic Technological University, Sligo, Ireland'
        ),
        "date": '"today"',
        "biblio_style": "apsrev4-2",
        "extra": "",
    },
}


def write(rel, content):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    print(f"  wrote {rel}")


def make_manifest(doc, template, title):
    defaults = TEMPLATE_DEFAULTS[template]

    if template == "article-sample":
        return f"""template: article-sample

metadata:
  title: "{title}"
  authors:
{defaults['authors_yaml']}
  date: {defaults['date']}
  abstract: >
    Add abstract here.
  bibliography: docs/{doc}/references.bib

{defaults['extra']}

sections:
  - title: Introduction
    components:
      - docs/{doc}/components/paragraphs/intro
"""
    if template == "article-labnote":
        return f"""template: article-labnote

metadata:
  title: "{title}"
  subtitle: "{defaults['subtitle']}"
  author:
    name: {defaults['author_name']}
    email: {defaults['author_email']}
  date: {defaults['date']}
  abstract: >
    Add abstract here.
  bibliography: docs/{doc}/references.bib

prelude:
  - title: Revision History
    components:
      - docs/{doc}/components/tables/revision-history

sections:
  - title: Introduction
    components:
      - docs/{doc}/components/paragraphs/intro

postlude:
  - title: Code Availability
    components:
      - docs/{doc}/components/paragraphs/code-availability
"""
    if template == "revtex-pra":
        return f"""template: revtex-pra

metadata:
  title: "{title}"
  authors:
{defaults['authors_yaml']}
  date: {defaults['date']}
  abstract: >
    Add abstract here.
  bibliographystyle: {defaults['biblio_style']}
  bibliography: docs/{doc}/references.bib

sections:
  - title: Introduction
    label: intro
    components:
      - docs/{doc}/components/paragraphs/intro

  - title: Conclusion
    label: conclusion
    components:
      - docs/{doc}/components/paragraphs/conclusion
"""
    raise ValueError(f"Unknown template: {template}")


def main():
    p = argparse.ArgumentParser(description="Scaffold a new modular-LaTeX doc.")
    p.add_argument("doc", help="Directory name under docs/, e.g. exp031-new-thing")
    p.add_argument("--template", required=True,
                   choices=list(TEMPLATE_DEFAULTS.keys()),
                   help="Template to base the manifest on")
    p.add_argument("--title", default=None,
                   help="Document title (defaults to the doc name)")
    args = p.parse_args()

    doc = args.doc
    if "/" in doc or doc.startswith("_"):
        raise SystemExit("Doc name should be a simple directory name, "
                         "not starting with '_' and not containing '/'")

    target = ROOT / "docs" / doc
    if target.exists():
        raise SystemExit(f"docs/{doc} already exists")

    title = args.title or doc.replace("-", " ").title()

    print(f"==> Creating docs/{doc} (template: {args.template})")

    # manifest
    write(f"docs/{doc}/manifest.yaml", make_manifest(doc, args.template, title))

    # empty bib
    write(f"docs/{doc}/references.bib", "% Add your bib entries here.\n")

    # starter components
    write(f"docs/{doc}/components/paragraphs/intro.tex",
          "Add the introduction paragraph text here.\n")
    write(f"docs/{doc}/components/paragraphs/conclusion.tex",
          "Add the conclusion paragraph text here.\n")

    if args.template == "article-labnote":
        write(f"docs/{doc}/components/tables/revision-history/revision-history.tex",
              r"""\begin{table}[H]
\centering
\begin{tabular}{cll}
\toprule
\textbf{Revision} & \textbf{Date} & \textbf{Description} \\
\midrule
01 & \today & Initial draft \\
\bottomrule
\end{tabular}
\end{table}
""")
        write(f"docs/{doc}/components/paragraphs/code-availability.tex",
              "Code available at: \\url{https://github.com/ianfromsligo/}\n")

    print()
    print("Next:")
    print(f"  python build.py docs/{doc}/manifest.yaml -o output --overleaf overleaf --no-compile")
    print(f"  git add docs/{doc} && git commit -m 'Add {doc}' && git push")


if __name__ == "__main__":
    main()
