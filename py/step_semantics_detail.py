#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_semantics_detail.py -- per-coin "semantics detail" page
==============================================================

One figure per fictional Elwetritsch stater: the coin's obverse and
reverse images, five attribute cards (material, obverse motif, reverse
motif, fictional find spot, metallurgical analysis), and a terminology
graph on the right showing how the coin, as a CIDOC-CRM E22 Human-Made
Object instance, links to CIDOC-CRM classes, controlled-vocabulary terms
and real-world entities (Wikidata, GeoNames, Getty AAT) with persistent
identifiers.

Every coin that has a ``data/raw/manual/coin_<ID>.yaml`` file is built;
this is what lets later chats add Coins II-XI without touching this
script -- see PRIMER.md Teil D. Site identifiers (Wikidata/GeoNames for
the real modern municipality each coin is "found near") come from the
shared ``data/raw/manual/sites.yaml``.

Fiction/reality distinction (repeated on every card and node, per the
series' own metadata, elwetritsch_coin_series_metadata_v3.md): the coin,
its findspot, hoard and metallurgical analysis are entirely invented for
Linked-Open-Data demonstration purposes; the modern site names and their
Wikidata/GeoNames identifiers are real.

House rules: no title/footer baked into the SVG (a caller supplies those,
e.g. a project README), no diagonal lines, deterministic output.

Writes: img/semantics-detail/<ID>_semantics_detail.{svg,png}
Run standalone: ``python py/step_semantics_detail.py``
"""

from __future__ import annotations

from pathlib import Path

import yaml

import elwetritsche_visuals_utils as vu

OUT = vu.OUT_DIRS["semantics-detail"]

CATEGORY = {"REAL": vu.REAL, "CLASS": vu.CLASS, "TERM": vu.TERM, "OWL": vu.OWL,
            "PROPERTY": vu.PROPERTY, "SUBJECT": vu.SUBJECT, "FICTIONAL": vu.FICTIONAL}

MARGIN = 40
LEFT_W = 1310
GAP = 34
RIGHT_X = MARGIN + LEFT_W + GAP
RIGHT_W = vu.CANVAS_W - MARGIN - RIGHT_X


# --------------------------------------------------------------------------- #
# Data loading
# --------------------------------------------------------------------------- #
def load_sites() -> dict:
    return yaml.safe_load((vu.DATA_MANUAL / "sites.yaml").read_text(encoding="utf-8"))


def load_coin(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- #
# Left column: coin image pair + attribute cards
# --------------------------------------------------------------------------- #
def _coin_images(parts: list[str], d: dict) -> float:
    """Obverse + reverse side by side, top of the left column. Returns the
    y coordinate of the row below them."""
    img_dir = vu.DATA_COINS / "images"
    side = 500
    gap = 40
    total_w = side * 2 + gap
    x0 = MARGIN + (LEFT_W - total_w) / 2
    y0 = MARGIN
    for i, key in enumerate(("obverse_image", "reverse_image")):
        x = x0 + i * (side + gap)
        parts.append(vu.svg_image_crop(x, y0, side, side, img_dir / d[key]))
        parts.append(f'<rect x="{x:.1f}" y="{y0:.1f}" width="{side}" height="{side}" '
                      f'fill="none" stroke="{vu.BORDER}" stroke-width="1"/>')
    label_y = y0 + side + 22
    parts.append(vu.svg_text(x0 + side / 2, label_y, "Obverse", size=13, color=vu.TEXT_MUTED,
                              anchor="middle"))
    parts.append(vu.svg_text(x0 + side + gap + side / 2, label_y, "Reverse", size=13,
                              color=vu.TEXT_MUTED, anchor="middle"))
    return label_y + 24


def _cards(parts: list[str], d: dict, y0: float) -> None:
    cards = d["cards"]
    n = len(cards)
    card_gap = 18
    card_w = (LEFT_W - (n - 1) * card_gap) / n

    # Pre-wrap every card's text so all cards can share one height.
    label_w = card_w - 28
    wrapped = []
    for c in cards:
        value_lines = vu.wrap_lines(c["value"], label_w, 17)
        notes = c.get("notes", [])
        chips = c.get("chips", [])
        wrapped.append((value_lines, notes, chips, c.get("caption", "")))

    max_value_lines = max(len(w[0]) for w in wrapped)
    max_notes_lines = max(len(w[1]) for w in wrapped)
    max_chip_rows = max(len(w[2]) for w in wrapped) or 1

    content_h = 18 + 16 + 6 + max_value_lines * 23 + 6 + max_notes_lines * 18
    link_area_h = 14 + max_chip_rows * 19 + 8
    card_h = content_h + link_area_h

    for i, c in enumerate(cards):
        value_lines, notes, chips, caption = wrapped[i]
        x = MARGIN + i * (card_w + card_gap)
        parts.append(f'<rect x="{x:.1f}" y="{y0:.1f}" width="{card_w:.1f}" height="{card_h:.1f}" '
                      f'rx="10" fill="{vu.CARD_BG}" stroke="{vu.BORDER}" stroke-width="1.4"/>')
        ty = y0 + 22
        parts.append(vu.svg_text(x + 14, ty, c["label"].upper(), size=12, weight=500,
                                  color=vu.TEXT_MUTED))
        ty += 22
        for line in value_lines:
            parts.append(vu.svg_text(x + 14, ty, line, size=17, weight=500, color=vu.TEXT_DARK))
            ty += 23
        ty += 4
        for line in notes:
            parts.append(vu.svg_text(x + 14, ty, line, size=12.5, color=vu.TEXT_MUTED))
            ty += 18

        link_y = y0 + content_h + 12
        parts.append(f'<line x1="{x + 14:.1f}" y1="{link_y - 6:.1f}" x2="{x + card_w - 14:.1f}" '
                      f'y2="{link_y - 6:.1f}" stroke="{vu.BORDER}" stroke-width="1"/>')
        if chips:
            cy = link_y
            for chip_label in chips:
                parts.append(vu.svg_text(x + 14, cy, chip_label, size=12.5, weight=500,
                                          color=vu.REAL["fill"]))
                cy += 19
        elif caption:
            block, _ = vu.svg_text_block(x + 14, link_y + 10, caption, card_w - 28, size=12,
                                          line_h=17, color=vu.TEXT_MUTED, italic=True)
            parts.append(block)


# --------------------------------------------------------------------------- #
# Right column: terminology graph (a vertical spine with branch nodes)
# --------------------------------------------------------------------------- #
def _terminology_graph(parts: list[str], d: dict) -> None:
    x, w = RIGHT_X, RIGHT_W
    y = MARGIN

    parts.append(vu.svg_text(x, y + 6, "Terminology graph (Linked Open Data)", size=20,
                              weight=500, color=vu.TEXT_DARK))
    y += 40

    root = d["terminology_graph"]["root"]
    root_h = 62
    parts.append(vu.svg_box(x, y, w, root_h, root["label"], root.get("subtitle", ""),
                             colors=CATEGORY[root["category"]]))
    spine_x = x + 26
    spine_top = y + root_h

    relations = d["terminology_graph"]["relations"]
    rel_ys = []
    cursor = spine_top
    pill_h = 30
    node_h = 62
    gap_pill_node = 8
    gap_after_node = 24
    for rel in relations:
        pill_y = cursor + 16
        rel_ys.append(pill_y)
        node_y = pill_y + pill_h + gap_pill_node
        cursor = node_y + node_h + gap_after_node
    spine_bottom = cursor - gap_after_node

    parts.append(f'<line x1="{spine_x:.1f}" y1="{spine_top:.1f}" x2="{spine_x:.1f}" '
                  f'y2="{spine_bottom:.1f}" stroke="{vu.LINE_NEUTRAL}" stroke-width="1.6"/>')

    cursor = spine_top
    for rel in relations:
        pill_y = cursor + 16
        pill_x = spine_x + 18
        parts.append(f'<line x1="{spine_x:.1f}" y1="{pill_y + pill_h/2:.1f}" '
                      f'x2="{pill_x:.1f}" y2="{pill_y + pill_h/2:.1f}" '
                      f'stroke="{vu.LINE_NEUTRAL}" stroke-width="1.6" marker-end="url(#arrow)"/>')
        chip, chip_w = vu.svg_chip(pill_x, pill_y, rel["property"], vu.PROPERTY, size=13,
                                    h=pill_h, align="start", pad=14)
        parts.append(chip)

        node_y = pill_y + pill_h + gap_pill_node
        parts.append(vu.svg_box(x, node_y, w, node_h, rel["target_label"],
                                 rel.get("target_subtitle", ""),
                                 colors=CATEGORY[rel["category"]]))
        cursor = node_y + node_h + gap_after_node

    legend_y = spine_bottom + 26
    parts.append(vu.svg_legend(x, legend_y, vu.CATEGORY_LABELS, col_w=w / len(vu.CATEGORY_LABELS)))


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #
def build(coin_yaml: Path, sites: dict) -> list[str]:
    d = load_coin(coin_yaml)
    site = sites[d["site_key"]]
    d["_site"] = site

    parts = [vu.svg_open(f"Elwetritsch stater {d['coin_id']} — {d['title']}: "
                          "semantics detail")]
    y_after_images = _coin_images(parts, d)
    _cards(parts, d, y_after_images)
    _terminology_graph(parts, d)
    parts.append(vu.svg_close())

    name = f"{d['coin_id']}_semantics_detail"
    return vu.write_figure(OUT, name, "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    vu.ensure_dirs()
    sites = load_sites()
    coin_files = sorted(vu.DATA_MANUAL.glob("coin_*.yaml"))
    if not coin_files:
        print("  no data/raw/manual/coin_*.yaml files found -- nothing to do")
        return []
    written: list[str] = []
    for coin_yaml in coin_files:
        written += build(coin_yaml, sites)
    for p in written:
        print(f"  wrote {p}")
    return written


if __name__ == "__main__":
    main()
