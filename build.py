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
FIGPATH_DEF_RE = re.compile(r'\\def\\figpath\{([^}]*)\}')


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


def inline_inputs(tex: str, base: Path, seen: set | None = None) -> str:
    """Recursively replace \\input{path} with the contents of path.tex.

    Paths are resolved relative to `base`, which should be the directory
    containing the .tex file being scanned. When a component is inlined,
    its own nested \\input calls are resolved relative to that component's
    directory.
    """
    seen = seen or set()

    def repl(match):
        target = match.group(1)
        candidate = (base / target).with_suffix(".tex").resolve()
        if not candidate.exists():
            return match.group(0)
        if candidate in seen:
            return match.group(0)
        seen.add(candidate)
        body = candidate.read_text()
        return inline_inputs(body, candidate.parent, seen)

    return INPUT_RE.sub(repl, tex)


def expand_figpath(tex: str) -> str:
    """Replace \\def\\figpath{X} ... \\figpath refs with X, and drop the def.

    The assembler emits \\def\\figpath{<rel>} immediately before each
    figure component. After inlining, the def precedes the inlined figure
    body. This function walks the text and, for each def, rewrites the
    \\figpath references in the block that follows it — matching what
    LaTeX would do — then removes the def line itself.
    """
    out = []
    pos = 0
    for m in FIGPATH_DEF_RE.finditer(tex):
        out.append(tex[pos:m.start()])
        value = m.group(1)
        # Find the next def, or end of string
        next_def = tex.find(r'\def\figpath', m.end())
        block_end = next_def if next_def != -1 else len(tex)
        block = tex[m.end():block_end]
        block = block.replace(r'\figpath/', value + '/')
        block = block.replace(r'\figpath', value)
        out.append(block)
        pos = block_end
    out.append(tex[pos:])
    return "".join(out)


def flatten_graphics(tex: str, out_dir: Path, base: Path) -> str:
    """Copy referenced images into out_dir and rewrite paths to bare filenames."""
    def repl(match):
        original = match.group(1)
        candidates = [
            (base / original).resolve(),
            (ROOT / original).resolve(),
            (base / ".." / original).resolve(),
            (base / "../.." / original).resolve(),
        ]
        for cand in candidates:
            if cand.exists() and cand.is_file():
                dst = out_dir / cand.name
                shutil.copy(cand, dst)
                return match.group(0).replace(original, cand.name)
        return match.group(0)

    return INCLUDE_RE.sub(repl, tex)


def write_overleaf_bundle(assembled_tex: str, out_dir: Path,
                          manifest: dict, assembled_tex_dir: Path) -> None:
    """Produce a single self-contained main.tex plus assets.

    `assembled_tex_dir` is the directory containing the assembled main.tex,
    used as the base for resolving all \\input and \\includegraphics paths.
    """
    out_dir.mkdir(parents=True, exist_ok=True)

    flat = inline_inputs(assembled_tex, base=assembled_tex_dir)
    flat = expand_figpath(flat)
    flat = flatten_graphics(flat, out_dir, base=assembled_tex_dir)

    (out_dir / "main.tex").write_text(flat)

    bib = manifest["metadata"].get("bibliography")
    if bib:
        src = ROOT / bib
        if src.exists():
            shutil.copy(src, out_dir / src.name)


def build(manifest_path: Path, output_dir: Path,
          compile_pdf: bool, overleaf_dir: Path | None) -> None:
    manifest = yaml.safe_load(manifest_path.read_text())
    manifest["_doc_name"] = doc_name(manifest_path)
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

    if overleaf_dir is not None:
        write_overleaf_bundle(tex, overleaf_dir / doc, manifest,
                              assembled_tex_dir=doc_out)
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
