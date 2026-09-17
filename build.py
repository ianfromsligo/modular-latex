#!/usr/bin/env python3
"""Assemble modular LaTeX components into a single document.

Usage:
    python build.py docs/<doc>/manifest.yaml
    python build.py docs/<doc>/manifest.yaml -o output
    python build.py docs/<doc>/manifest.yaml --no-compile
    python build.py docs/<doc>/manifest.yaml --overleaf overleaf

Outputs:
    <output>/<doc>/main.tex      assembled (repo-path) document
    <output>/<doc>/main.pdf      compiled PDF (unless --no-compile)
    <overleaf>/<doc>/main.tex    flattened self-contained document
    <overleaf>/<doc>/...         copied assets + references.bib
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent.resolve()

INPUT_RE = re.compile(r'\\input\{([^}]+)\}')
INCLUDE_RE = re.compile(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}')


def doc_name(manifest_path: Path) -> str:
    return manifest_path.parent.name


def emit_component(output_dir: Path, comp: str) -> str:
    """LaTeX code that includes the given component.

    Figure/table components are directories named after themselves,
    containing <name>.tex plus assets. Everything else is a .tex file.
    Paths emitted are relative to output_dir.
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
        block_start_string="<%",
        block_end_string="%>",
        variable_start_string="<<",
        variable_end_string=">>",
        comment_start_string="<#",
        comment_end_string="#>",
    )
    env.filters["basename"] = lambda p: os.path.basename(p)
    tmpl = env.get_template("template.tex.j2")
    return tmpl.render(
        manifest=manifest,
        emit=lambda comp: emit_component(output_dir, comp),
    )


def inline_inputs(tex: str, seen: set | None = None) -> str:
    """Recursively replace \\input{path} with the contents of path.tex."""
    seen = seen or set()

    def repl(match):
        target = match.group(1)
        candidate = (ROOT / target).with_suffix(".tex")
        if not candidate.exists():
            return match.group(0)
        if candidate in seen:
            return match.group(0)
        seen.add(candidate)
        body = candidate.read_text()
        return inline_inputs(body, seen)

    return INPUT_RE.sub(repl, tex)


def flatten_graphics(tex: str, out_dir: Path, base: Path) -> str:
    """Copy referenced images into out_dir and rewrite paths to bare filenames."""
    search_prefixes = (
        "",
        "../",
        "../components/",
        "../components/figures/",
        "components/",
        "components/figures/",
    )

    def repl(match):
        original = match.group(1)
        for prefix in search_prefixes:
            cand = (base / prefix / original).resolve()
            if cand.exists() and cand.is_file():
                dst = out_dir / cand.name
                shutil.copy(cand, dst)
                return match.group(0).replace(original, cand.name)
        return match.group(0)

    return INCLUDE_RE.sub(repl, tex)


def write_overleaf_bundle(assembled_tex: str, out_dir: Path,
                          manifest: dict, doc_dir: Path) -> None:
    """Produce a single self-contained main.tex plus assets."""
    out_dir.mkdir(parents=True, exist_ok=True)

    flat = inline_inputs(assembled_tex)
    flat = flatten_graphics(flat, out_dir, base=ROOT)

    (out_dir / "main.tex").write_text(flat)

    # copy bib
    bib = manifest["metadata"].get("bibliography")
    if bib:
        src = ROOT / bib
        if src.exists():
            shutil.copy(src, out_dir / src.name)


def build(manifest_path: Path, output_dir: Path,
          compile_pdf: bool, overleaf_dir: Path | None) -> None:
    manifest = yaml.safe_load(manifest_path.read_text())
    doc = doc_name(manifest_path)
    doc_out = output_dir / doc
    doc_out.mkdir(parents=True, exist_ok=True)

    tex = render(manifest, doc_out)
    (doc_out / "main.tex").write_text(tex)
    print(f"[build] wrote {doc_out / 'main.tex'}")

    bib = manifest["metadata"].get("bibliography")
    if bib:
        shutil.copy(ROOT / bib, doc_out / Path(bib).name)
        print(f"[build] copied {bib}")

    # Overleaf bundle (before compilation, so it's produced even if compile fails)
    if overleaf_dir is not None:
        write_overleaf_bundle(tex, overleaf_dir / doc, manifest, manifest_path.parent)
        print(f"[build] wrote overleaf bundle {overleaf_dir / doc}")

    if not compile_pdf:
        return

    compiler = os.environ.get("LATEXMK", "latexmk")
    cmd = [compiler, "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
    try:
        result = subprocess.run(cmd, cwd=doc_out)
    except FileNotFoundError:
        sys.exit(
            f"Compiler '{compiler}' not found on PATH. Install a TeX distribution "
            "or set LATEXMK to a compiler you have."
        )
    if result.returncode != 0:
        sys.exit("LaTeX compilation failed")
    print(f"[build] PDF at {doc_out / 'main.pdf'}")


def main() -> None:
    p = argparse.ArgumentParser(description="Build a modular LaTeX document.")
    p.add_argument("manifest", type=Path, help="Path to manifest YAML")
    p.add_argument("-o", "--output", type=Path, default=ROOT / "output")
    p.add_argument("--overleaf", type=Path, default=None,
                   help="Directory in which to write the flattened Overleaf bundle")
    p.add_argument("--no-compile", action="store_true",
                   help="Only assemble main.tex; do not run LaTeX.")
    args = p.parse_args()
    build(args.manifest, args.output.resolve(),
          compile_pdf=not args.no_compile,
          overleaf_dir=args.overleaf.resolve() if args.overleaf else None)


if __name__ == "__main__":
    main()
