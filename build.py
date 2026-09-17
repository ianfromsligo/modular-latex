#!/usr/bin/env python3
"""Assemble modular LaTeX components into a single document and compile it."""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent.resolve()


def emit_component(output_dir: Path, comp: str) -> str:
    """Return LaTeX code that includes the given component.

    Figures and tables live in a directory named after the component and
    contain a matching .tex wrapper plus their asset. Everything else is a
    plain .tex file.
    """
    comp_path = ROOT / comp
    if comp_path.is_dir():
        tex_name = comp_path.name + ".tex"
        tex_file = comp_path / tex_name
        if not tex_file.exists():
            raise FileNotFoundError(f"No {tex_name} inside {comp_path}")
        rel = os.path.relpath(comp_path, output_dir)
        return (
            f"\\def\\figpath{{{rel}}}\n"
            f"\\input{{{rel}/{tex_name}}}\n"
        )
    else:
        tex_file = comp_path.with_suffix(".tex")
        if not tex_file.exists():
            raise FileNotFoundError(f"Missing component: {tex_file}")
        rel = os.path.relpath(tex_file.with_suffix(""), output_dir)
        return f"\\input{{{rel}}}\n"


def render(manifest: dict, output_dir: Path) -> str:
    env = Environment(
        loader=FileSystemLoader(ROOT / "templates" / manifest["template"]),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    tmpl = env.get_template("template.tex.j2")
    return tmpl.render(
        manifest=manifest,
        emit=lambda comp: emit_component(output_dir, comp),
    )


def build(manifest_path: Path, output_dir: Path) -> None:
    manifest = yaml.safe_load(manifest_path.read_text())
    output_dir.mkdir(parents=True, exist_ok=True)

    tex = render(manifest, output_dir)
    (output_dir / "main.tex").write_text(tex)
    print(f"[build] wrote {output_dir / 'main.tex'}")

    bib = manifest["metadata"].get("bibliography")
    if bib:
        shutil.copy(ROOT / bib, output_dir / Path(bib).name)
        print(f"[build] copied {bib}")

    result = subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
        cwd=output_dir,
    )
    if result.returncode != 0:
        sys.exit("LaTeX compilation failed")
    print(f"[build] PDF at {output_dir / 'main.pdf'}")


def main() -> None:
    p = argparse.ArgumentParser(description="Build a modular LaTeX document.")
    p.add_argument("manifest", type=Path, help="Path to manifest YAML")
    p.add_argument("-o", "--output", type=Path, default=ROOT / "output")
    args = p.parse_args()
    build(args.manifest, args.output.resolve())


if __name__ == "__main__":
    main()
