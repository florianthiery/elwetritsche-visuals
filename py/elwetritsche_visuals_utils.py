#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
elwetritsche_visuals_utils.py -- shared constants, palette, paths and writers
==============================================================================

Every step module imports from here rather than repeating a hex code, a
path computation or a box/arrow primitive. Forked from the sibling repo
``hdoku26-visuals`` (same author, same house pattern: pure Python SVG
authoring + resvg-py rasterisation, no title header or citation footer
baked in, deterministic output). The drawing helpers below the palette are
carried over largely unchanged; the palette, the paths and the output
directories are specific to this repo.

This repo is single-language (English) -- unlike hdoku26-visuals it is not
slide material for a talk, but documentation of a fictional Linked-Open-Data
demonstration dataset, and the whole series has been drafted in English from
the start (see PRIMER.md A3).

Authors: Florian Thiery (LEIZA / Research Squirrel Engineers Network)
Licence: MIT (this script) / CC BY 4.0 (the figures it produces)
"""

from __future__ import annotations

import hashlib
from pathlib import Path

# --------------------------------------------------------------------------- #
# Release marker -- NOT datetime.now(). Bump by hand when the content set
# changes.
# --------------------------------------------------------------------------- #
RELEASE = "2026-09-22"

# --------------------------------------------------------------------------- #
# Paths, resolved relative to the repository root
# --------------------------------------------------------------------------- #
ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "img"
DATA_RAW = ROOT / "data" / "raw"
DATA_COINS = DATA_RAW / "coins"
DATA_IMAGES = DATA_COINS / "images"
DATA_MANUAL = DATA_RAW / "manual"
FONTS = ROOT / "fonts"

FONT_REGULAR = FONTS / "FiraSans-Regular.ttf"
FONT_MEDIUM = FONTS / "FiraSans-Medium.ttf"
FONT_SANS = "Fira Sans"

# --------------------------------------------------------------------------- #
# Canvas -- fixed landscape format, wide enough for a coin pair + cards on
# the left and a terminology-graph spine on the right (see step_semantics_detail).
# --------------------------------------------------------------------------- #
CANVAS_W = 2350
CANVAS_H = 1160

OUT_DIRS = {
    "semantics-detail": IMG / "semantics-detail",
}


def ensure_dirs() -> None:
    """Create every output directory this repo writes into. Idempotent."""
    for path in OUT_DIRS.values():
        path.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------------------------------- #
# Palette -- the house Mermaid/LOD colour scheme (see /preferences.md),
# applied consistently across every diagram in this repository family:
#
#   REAL      -- a real, externally verifiable entity (Wikidata / GeoNames /
#                CIDOC-CRM term with a persistent identifier) (dark green)
#   CLASS     -- a CIDOC-CRM class (dark orange)
#   TERM      -- a terminology / vocabulary concept (dark purple)
#   OWL       -- reserved for OWL-level nodes (white)
#   PROPERTY  -- a CIDOC-CRM property / predicate (amber/gold)
#   SUBJECT   -- a generic subject/object node (pastel grey)
#   FICTIONAL -- an invented research object with no real-world identifier
#                (neutral grey/cream, not part of the Mermaid scheme proper
#                but used consistently across this repo's own figures)
#
# Stroke follows the approved reference figure (data/raw/reference/
# I_semantics_detail.png) rather than the Mermaid default of pure black:
# a subtle, slightly darker-than-fill stroke reads cleaner at this size and
# was the figure the repo's first commit is reproducing (PRIMER A4,
# 2026-09-22).
# --------------------------------------------------------------------------- #
REAL = {"fill": "#166534", "stroke": "#0f4726", "text": "#ffffff"}
CLASS = {"fill": "#9a3412", "stroke": "#732709", "text": "#ffffff"}
TERM = {"fill": "#4c1d95", "stroke": "#38156f", "text": "#ffffff"}
OWL = {"fill": "#ffffff", "stroke": "#000000", "text": "#000000"}
PROPERTY = {"fill": "#fbbf24", "stroke": "#c8930a", "text": "#000000"}
SUBJECT = {"fill": "#e2e8f0", "stroke": "#94a3b8", "text": "#000000"}
FICTIONAL = {"fill": "#f7f6f1", "stroke": "#b4b2a7", "text": "#5f5e5a"}

CATEGORY_LABELS = [
    ("RealObject", REAL),
    ("Class", CLASS),
    ("Term", TERM),
    ("Property", PROPERTY),
]

TEXT_DARK = "#232321"
TEXT_MUTED = "#64635e"
BORDER = "#b4b2a7"
CARD_BG = "#f7f6f1"
LINE_NEUTRAL = "#8a8873"


def t(_lang: str, _de: str, en: str) -> str:
    """Kept for API parity with hdoku26-visuals; this repo is English-only,
    so it always returns the English string regardless of ``_lang``."""
    return en


# --------------------------------------------------------------------------- #
# Deterministic writers
# --------------------------------------------------------------------------- #
def content_fingerprint(data: bytes) -> str:
    """Short, stable fingerprint for logging / --strict checks."""
    return hashlib.sha256(data).hexdigest()[:12]


def write_svg(path: Path, svg_markup: str) -> str:
    """Write SVG source deterministically: UTF-8, exactly one trailing
    newline, no injected timestamps or random ids."""
    text = svg_markup.strip("\n") + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return content_fingerprint(text.encode("utf-8"))


def write_png_from_svg(svg_path: Path, png_path: Path, *, zoom: float = 1.5) -> str:
    """Rasterise an already-written SVG file to PNG via resvg-py, in-process,
    using the vendored Fira Sans weights. White background."""
    import resvg_py  # imported lazily so --list/--dry-run stay cheap

    png_bytes = resvg_py.svg_to_bytes(
        svg_path=str(svg_path),
        background="#ffffff",
        skip_system_fonts=True,
        font_files=[str(FONT_REGULAR), str(FONT_MEDIUM)],
        zoom=zoom,
    )
    png_path.parent.mkdir(parents=True, exist_ok=True)
    png_path.write_bytes(png_bytes)
    return content_fingerprint(png_bytes)


def write_figure(out_dir: Path, name: str, svg_markup: str, *, zoom: float = 1.5) -> list[str]:
    """Write both the .svg and the .png for one figure and return the two
    paths written, in the shape main.py expects from a step's return value."""
    svg_path = out_dir / f"{name}.svg"
    png_path = out_dir / f"{name}.png"
    write_svg(svg_path, svg_markup)
    write_png_from_svg(svg_path, png_path, zoom=zoom)
    return [str(svg_path), str(png_path)]


# --------------------------------------------------------------------------- #
# Small SVG-building helpers (ported from hdoku26_visuals_utils, trimmed to
# what this repo's figures actually use).
# --------------------------------------------------------------------------- #
ARROW_STROKE = "#73726c"

# NOTE (carried over from hdoku26-visuals / bb-5kbc-visuals, still true
# here): the CSS `context-stroke` keyword is NOT supported by resvg --
# arrowheads render invisible until pinned to a fixed colour.
ARROW_DEFS = (
    '<defs>'
    '<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" '
    'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
    f'<path d="M2 1L8 5L2 9" fill="none" stroke="{ARROW_STROKE}" stroke-width="1.5" '
    'stroke-linecap="round" stroke-linejoin="round"/></marker>'
    '</defs>'
)


def xml_escape(s: str) -> str:
    """Escape the five XML predefined entities. Every helper that places
    caller-supplied text into an SVG text node must run it through this."""
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def text_width(s: str, size: float = 14) -> float:
    """Rough width estimate (Fira Sans is close to 0.56*size per character)."""
    return len(s) * size * 0.56


def svg_text(x: float, y: float, s: str, *, size: float = 13, weight: int = 400,
             color: str = TEXT_DARK, anchor: str = "start", italic: bool = False,
             baseline: str = "auto", opacity: float = 1.0) -> str:
    """One line of text. ``weight`` 400 or 500 (the two vendored cuts)."""
    style = ' font-style="italic"' if italic else ""
    op = f' opacity="{opacity}"' if opacity != 1.0 else ""
    wt = ' font-weight="500"' if weight >= 500 else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" dominant-baseline="{baseline}" '
            f'font-family="Fira Sans" font-size="{size}"{wt}{style}{op} fill="{color}">'
            f'{xml_escape(s)}</text>')


def wrap_lines(s: str, max_width: float, size: float) -> list[str]:
    """Greedy word wrap against the rough Fira Sans width estimate."""
    lines: list[str] = []
    current = ""
    for word in s.split():
        trial = f"{current} {word}".strip()
        if current and text_width(trial, size) > max_width:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    return lines


def svg_text_block(x: float, y: float, s: str, max_width: float, *, size: float = 13,
                    line_h: float | None = None, **kw) -> tuple[str, float]:
    """Wrapped paragraph; returns (markup, y of the line after the block)."""
    line_h = line_h or size * 1.35
    parts = []
    for i, line in enumerate(wrap_lines(s, max_width, size)):
        parts.append(svg_text(x, y + i * line_h, line, size=size, **kw))
    return "\n".join(parts), y + len(parts) * line_h


def svg_chip(x: float, y: float, label: str, colors: dict, *, size: float = 11.5,
             h: float = 22, dashed: bool = False, pad: float = 10,
             width: float | None = None, align: str = "middle") -> tuple[str, float]:
    """A rounded identifier chip ("wd:Q239481"); returns (markup, width)."""
    w = width if width is not None else text_width(label, size) + 2 * pad
    dash = ' stroke-dasharray="4 3"' if dashed else ""
    tx = x + pad if align == "start" else x + w / 2
    markup = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h/2:.1f}" '
              f'fill="{colors["fill"]}" stroke="{colors["stroke"]}" stroke-width="1.2"{dash}/>\n'
              + svg_text(tx, y + h / 2 + 0.5, label, size=size, weight=500,
                         color=colors.get("text", TEXT_DARK), anchor=align, baseline="central"))
    return markup, w


def svg_box(x: float, y: float, w: float, h: float, title: str, subtitle: str = "",
            *, colors: dict, rx: float = 10, stroke_width: float = 1.4) -> str:
    """A category node: filled rounded box, bold title, optional grey
    subtitle line (used for a persistent identifier)."""
    fill, stroke, text_color = colors["fill"], colors["stroke"], colors.get("text", "#ffffff")
    parts = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
             f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>']
    cx = x + w / 2
    if subtitle:
        parts.append(svg_text(cx, y + h / 2 - 4, title, size=15.5, weight=500,
                               color=text_color, anchor="middle", baseline="central"))
        parts.append(svg_text(cx, y + h / 2 + 15, subtitle, size=11.5, color=text_color,
                               anchor="middle", baseline="central", opacity=0.82))
    else:
        parts.append(svg_text(cx, y + h / 2, title, size=15.5, weight=500, color=text_color,
                               anchor="middle", baseline="central"))
    return "\n".join(parts)


def svg_legend(x: float, y: float, entries: list[tuple[str, dict]], *, box: float = 16,
               gap: float = 10, row_h: float = 24, col_w: float = 240) -> str:
    """A small colour-key legend: one swatch + label per entry, laid out in
    one row."""
    parts = []
    for i, (label, colors) in enumerate(entries):
        ex = x + i * col_w
        ey = y
        parts.append(f'<rect x="{ex:.1f}" y="{ey:.1f}" width="{box}" height="{box}" rx="3" '
                      f'fill="{colors["fill"]}" stroke="{colors["stroke"]}" stroke-width="1.2"/>')
        parts.append(svg_text(ex + box + gap, ey + box / 2, label, size=12.5,
                               color=TEXT_DARK, baseline="central"))
    return "\n".join(parts)


def _image_size(data: bytes) -> tuple[int, int, str]:
    """Pixel size and MIME type of a PNG or baseline/progressive JPEG."""
    import struct
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", data[16:24])
        return w, h, "image/png"
    if data[:2] == b"\xff\xd8":
        i = 2
        while i < len(data):
            marker, length = data[i + 1], struct.unpack(">H", data[i + 2:i + 4])[0]
            if marker in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return w, h, "image/jpeg"
            i += 2 + length
    raise ValueError("unsupported image format")


def svg_image_crop(x: float, y: float, w: float, h: float, img_path: Path,
                    crop: tuple[int, int, int, int] | None = None) -> str:
    """Embed a PNG or JPEG (base64, so the SVG stays self-contained) showing
    only the ``crop`` region (x0, y0, x1, y1 in image pixels; whole image if
    None), scaled to fit the box and centred. Clipped with an explicit
    clipPath (resvg does not clip nested <svg> viewports); the clip id is
    derived from the file name, so output stays deterministic."""
    import base64
    data = img_path.read_bytes()
    iw, ih, mime = _image_size(data)
    x0, y0, x1, y1 = crop or (0, 0, iw, ih)
    cw, ch = x1 - x0, y1 - y0
    s = min(w / cw, h / ch)
    ox, oy = x + (w - cw * s) / 2, y + (h - ch * s) / 2
    cid = "clip-" + "".join(c if c.isalnum() else "-" for c in img_path.stem)
    b64 = base64.b64encode(data).decode("ascii")
    return (f'<defs><clipPath id="{cid}"><rect x="{ox:.2f}" y="{oy:.2f}" width="{cw * s:.2f}" '
            f'height="{ch * s:.2f}"/></clipPath></defs>'
            f'<g clip-path="url(#{cid})"><image x="{ox - x0 * s:.2f}" y="{oy - y0 * s:.2f}" '
            f'width="{iw * s:.2f}" height="{ih * s:.2f}" href="data:{mime};base64,{b64}"/></g>')


# --------------------------------------------------------------------------- #
# Canvas open/close. No title header, no source-citation footer (house rule,
# see PRIMER A3): these are general-purpose diagram assets, not
# self-captioned slides. ``title_for_a11y`` still goes into an invisible
# <title> element for accessibility/tooling.
# --------------------------------------------------------------------------- #
def svg_open(title_for_a11y: str, *, w: int = CANVAS_W, h: int = CANVAS_H) -> str:
    return (
        f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img">\n'
        f'<title>{xml_escape(title_for_a11y)}</title>\n'
        f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>\n'
        f'{ARROW_DEFS}\n'
    )


def svg_close() -> str:
    return "</svg>\n"
