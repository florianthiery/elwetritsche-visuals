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

# Column widths, pixel-measured against the reference figure (data/raw/
# reference/I_semantics_detail.png): the root/relation-node boxes there
# span x=1602..2278 (width 676) of a 2350-wide canvas, i.e. a far narrower
# right column -- and correspondingly wider left column, with visibly
# bigger coin images -- than this script first assumed (PRIMER.md A1
# Befund, 2026-09-22: user-reported "coin too small / placement off").
MARGIN = 40
LEFT_W = 1480
GAP = 40
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
    side = 734
    gap = 15
    total_w = side * 2 + gap
    x0 = MARGIN + (LEFT_W - total_w) / 2
    y0 = MARGIN
    for i, key in enumerate(("obverse_image", "reverse_image")):
        x = x0 + i * (side + gap)
        parts.append(vu.svg_image_crop(x, y0, side, side, img_dir / d[key]))
    label_y = y0 + side + 26
    parts.append(vu.svg_text(x0 + side / 2, label_y, "Obverse", size=15, color=vu.TEXT_MUTED,
                              anchor="middle"))
    parts.append(vu.svg_text(x0 + side + gap + side / 2, label_y, "Reverse", size=15,
                              color=vu.TEXT_MUTED, anchor="middle"))
    return label_y + 24


def _cards(parts: list[str], d: dict, y0: float) -> float:
    cards = d["cards"]
    n = len(cards)
    card_gap = 22
    card_w = (LEFT_W - (n - 1) * card_gap) / n

    # Font sizes and line spacing pixel-measured against the reference
    # figure (data/raw/reference/I_semantics_detail.png): the first
    # rebuild used sizes closer to hdoku26-visuals' own house scale, which
    # reads visibly smaller than the reference's own text (PRIMER.md A1
    # Befund, 2026-09-22: user-reported font size/position mismatch).
    label_size, value_size, notes_size, chip_size = 16, 18, 14, 17

    # Pre-wrap every card's text so all cards can share one height. Notes
    # are re-flowed through wrap_lines rather than trusted as already-fitting
    # lines: they used to be rendered exactly as split in the YAML, which
    # assumed whoever wrote the line breaks had judged the pixel width
    # correctly -- Coin III's "real castle above the findspot (Trifels)" and
    # Coin II's "Südwestpfalz sandstone country" hadn't, and ran past their
    # card's edge (PRIMER.md A1 Befund, 2026-09-22: user-reported "text
    # overflow in boxes").
    label_w = card_w - 28
    wrapped = []
    for c in cards:
        value_lines = vu.wrap_lines(c["value"], label_w, value_size)
        notes_text = " ".join(c.get("notes", []))
        notes = vu.wrap_lines(notes_text, label_w, notes_size) if notes_text else []
        chips = c.get("chips", [])
        wrapped.append((value_lines, notes, chips, c.get("caption", "")))

    max_value_lines = max(len(w[0]) for w in wrapped)
    max_notes_lines = max(len(w[1]) for w in wrapped)
    max_chip_rows = max(len(w[2]) for w in wrapped) or 1

    # link_y (first chip's own baseline) sits 44px below content_h rather
    # than 14: with only 14px, the divider line -- drawn 8px above it --
    # landed just 8px above that first chip's baseline, well inside a 17px
    # font's cap-height, so the divider visually crossed through the chip
    # text itself (PRIMER.md A1 Befund, 2026-09-22: user-reported "the
    # links overlap with the line"). The extra 30px also brings the
    # chips' own gap from the divider in line with the caption's (the
    # "cf. real published range" text in the Metallurgical analysis card,
    # which already sat 30px below the divider -- user-reported the two
    # should match). link_area_h grows to keep the bottom padding below
    # the last chip row unchanged.
    content_h = 22 + 20 + 6 + max_value_lines * 25 + 6 + max_notes_lines * 20
    link_area_h = 56 + max_chip_rows * 25
    card_h = content_h + link_area_h

    for i, c in enumerate(cards):
        value_lines, notes, chips, caption = wrapped[i]
        x = MARGIN + i * (card_w + card_gap)
        parts.append(f'<rect x="{x:.1f}" y="{y0:.1f}" width="{card_w:.1f}" height="{card_h:.1f}" '
                      f'rx="10" fill="{vu.CARD_BG}" stroke="{vu.BORDER}" stroke-width="1.4"/>')
        ty = y0 + 26
        parts.append(vu.svg_text(x + 14, ty, c["label"].upper(), size=label_size, weight=500,
                                  color=vu.TEXT_MUTED))
        ty += 26
        for line in value_lines:
            parts.append(vu.svg_text(x + 14, ty, line, size=value_size, weight=500,
                                      color=vu.TEXT_DARK))
            ty += 25
        ty += 4
        for line in notes:
            parts.append(vu.svg_text(x + 14, ty, line, size=notes_size, color=vu.TEXT_MUTED))
            ty += 20

        divider_y = y0 + content_h + 14
        link_y = y0 + content_h + 44
        parts.append(f'<line x1="{x + 14:.1f}" y1="{divider_y:.1f}" x2="{x + card_w - 14:.1f}" '
                      f'y2="{divider_y:.1f}" stroke="{vu.BORDER}" stroke-width="1"/>')
        if chips:
            cy = link_y
            for chip_label in chips:
                parts.append(vu.svg_text(x + 14, cy, chip_label, size=chip_size, weight=500,
                                          color=vu.TERM["fill"]))
                cy += 25
        elif caption:
            block, _ = vu.svg_text_block(x + 14, link_y, caption, card_w - 28,
                                          size=notes_size, line_h=19, color=vu.TEXT_MUTED,
                                          italic=True)
            parts.append(block)

    return y0 + card_h


# --------------------------------------------------------------------------- #
# Right column: terminology graph (a vertical spine with branch nodes)
# --------------------------------------------------------------------------- #
def _terminology_graph(parts: list[str], d: dict) -> float:
    x, w = RIGHT_X, RIGHT_W
    y = MARGIN

    parts.append(vu.svg_text(x, y + 6, f"Coin {d['coin_id']} Graph", size=22,
                              weight=500, color=vu.TEXT_DARK))
    y += 42

    root = d["terminology_graph"]["root"]
    root_h = 80
    parts.append(vu.svg_box(x, y, w, root_h, root["label"], root.get("subtitle", ""),
                             colors=CATEGORY[root["category"]], title_size=18, subtitle_size=16,
                             align="start"))
    # Spine, pills and the external identifier caption are pixel-measured
    # against the reference figure (data/raw/reference/I_semantics_detail.
    # png): its pills AND identifier captions both start flush at
    # x+80-ish, well clear of the spine at x+33-ish -- this script first
    # put both flush with the box's own left edge (x+0/x+18), so the
    # spine line ran straight through the "wd:Q..." caption text in the
    # gap between boxes (PRIMER.md A1 Befund, 2026-09-22: user-reported
    # "line goes through the identifier").
    spine_x = x + 30
    content_x = x + 80
    spine_top = y + root_h

    # Node boxes carry only the title; a persistent identifier (when the
    # relation has one) is printed as a small caption *below* the box, in
    # muted grey -- matching the reference figure (data/raw/reference/
    # I_semantics_detail.png) rather than the root box's own convention of
    # a subtitle baked into the box (root has no external identifier of its
    # own, so that distinction doubles as "this box IS the object" vs.
    # "this box names a concept that HAS an identifier").
    relations = d["terminology_graph"]["relations"]
    cursor = spine_top
    pill_h = 32
    node_h = 46
    # Equal gap above and below every pill (was 16 above / 8 below, plus
    # an extra 18 trailing gap folded into the "above" side -- 34 vs 8
    # overall -- so each pill hugged the box below it far more than the
    # content above; PRIMER.md A1 Befund, 2026-09-22: user-reported the
    # gaps above/below a pill should match, i.e. the pill vertically
    # centred in the space it sits in).
    gap_v = 16
    id_h = 26
    for rel in relations:
        pill_y = cursor + gap_v
        node_y = pill_y + pill_h + gap_v
        cursor = node_y + node_h + (id_h if rel.get("target_subtitle") else 0)
    spine_bottom = cursor

    parts.append(f'<line x1="{spine_x:.1f}" y1="{spine_top:.1f}" x2="{spine_x:.1f}" '
                  f'y2="{spine_bottom:.1f}" stroke="{vu.LINE_NEUTRAL}" stroke-width="1.6"/>')

    cursor = spine_top
    for rel in relations:
        pill_y = cursor + gap_v
        branch_y = pill_y + pill_h / 2
        parts.append(f'<line x1="{spine_x:.1f}" y1="{branch_y:.1f}" '
                      f'x2="{content_x:.1f}" y2="{branch_y:.1f}" '
                      f'stroke="{vu.LINE_NEUTRAL}" stroke-width="1.6" marker-end="url(#arrow)"/>')
        parts.append(f'<circle cx="{spine_x:.1f}" cy="{branch_y:.1f}" r="3.5" '
                      f'fill="{vu.LINE_NEUTRAL}"/>')
        chip, chip_w = vu.svg_chip(content_x, pill_y, rel["property"], vu.PROPERTY, size=16,
                                    h=pill_h, align="start", pad=11)
        parts.append(chip)

        node_y = pill_y + pill_h + gap_v
        parts.append(vu.svg_box(x, node_y, w, node_h, rel["target_label"], "",
                                 colors=CATEGORY[rel["category"]], title_size=18, align="start"))
        subtitle = rel.get("target_subtitle", "")
        if subtitle:
            parts.append(vu.svg_text(content_x, node_y + node_h + 20, subtitle, size=16,
                                      color=vu.TEXT_MUTED))
        cursor = node_y + node_h + (id_h if subtitle else 0)

    legend_y = spine_bottom + 26
    parts.append(vu.svg_legend(x, legend_y, vu.CATEGORY_LABELS, col_w=w / len(vu.CATEGORY_LABELS),
                                size=16))
    return legend_y + 24


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #
def build(coin_yaml: Path, sites: dict) -> list[str]:
    d = load_coin(coin_yaml)
    site = sites[d["site_key"]]
    d["_site"] = site

    # Canvas height is fitted to this coin's own content rather than a
    # fixed constant, so the figure doesn't carry a large blank margin
    # when a coin's card/graph content is shorter than the tallest coin
    # in the series (PRIMER.md A1 Befund, 2026-09-22: user-reported
    # excess white space at the bottom).
    body: list[str] = []
    y_after_images = _coin_images(body, d)
    left_bottom = _cards(body, d, y_after_images)
    right_bottom = _terminology_graph(body, d)
    canvas_h = int(round(max(left_bottom, right_bottom) + MARGIN))

    parts = [vu.svg_open(f"Elwetritsch stater {d['coin_id']} — {d['title']}: "
                          "semantics detail", h=canvas_h)]
    parts.extend(body)
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
