#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_overview.py -- series overview: modern sites vs. the coins
=================================================================

One figure for the whole eleven-coin series, laid out exactly as asked
(PRIMER.md A4, 2026-09-23): a stylised map of the Palatinate on the
**left** (modern administrative district outlines, from
``data/raw/geo/rlp_palatinate_districts.geojson``, with a numbered pin
at each coin's real modern site from ``data/raw/manual/sites.yaml``),
and a numbered grid of all eleven coins' actual obverse images on the
**right** (``data/raw/coins/images/``, captioned from
``data/raw/manual/series_metadata.yaml``) -- coin *images*, not a table
of names and identifiers (the map-plus-table shape of the old ad-hoc
prototype, ``data/raw/reference/I--XI_map.png``, is explicitly not what
was asked for this time).

The same small numeral badge (I-XI) appears on a site's map pin and on
its coin's thumbnail, so a reader can match one side to the other
without a legend. It is deliberately outside the REAL/CLASS/TERM/
PROPERTY palette used for the terminology graph elsewhere in this
repo (``elwetritsche_visuals_utils.CATEGORY_LABELS``): the numeral is a
cross-reference index, not a fiction/reality assertion, and colouring
it from that palette would imply one. The fiction/reality distinction
this series otherwise insists on (PRIMER.md A2, property 2) is carried
instead by the two section headings themselves -- "Modern sites (real)"
/ "Elwetritsch staters I-XI (fictional)" -- which is exactly the
distinction the coin-level cards already draw between a "Site" card
and a "Find spot (fictional)" card.

The map's projection is a plain equirectangular one with a
cosine-latitude correction (no cartopy/geopandas/pyproj -- this repo's
one dependency exception for a figure is Pillow for font metrics, not a
geo stack): accurate enough at this scale (under a degree of latitude
end to end) and it keeps the repo's "pure Python, minimal dependencies"
house style.

Geo data is fetched once into ``data/raw/geo/`` and read here, never
fetched live (house rule, PRIMER.md A3) -- see that file's own
provenance/licence note in ``data/raw/README.md``.

House rules: no title/footer baked into the SVG, no diagonal lines in
what this script *draws* (the one visual exception is the district
outlines themselves, which are real administrative boundaries traced
from source data, not a decorative diagonal), deterministic output.

Writes: img/overview/series_overview.{svg,png}
Run standalone: ``python py/step_overview.py``
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import yaml

import elwetritsche_visuals_utils as vu

OUT = vu.OUT_DIRS["overview"]
GEO_PATH = vu.DATA_RAW / "geo" / "rlp_palatinate_districts.geojson"

# --------------------------------------------------------------------------- #
# Layout constants. A fresh canvas width for this figure rather than reusing
# step_semantics_detail's CANVAS_W/CANVAS_H: that figure's proportions (a
# near-square coin pair plus a narrow graph spine) have nothing to do with
# this one (a wide map plus a coin grid), so tying the two together would
# just make a future change to one script silently reshape the other.
# --------------------------------------------------------------------------- #
CANVAS_W = 2350
MARGIN = 50
GAP = 50
HEADING_SIZE = 22

MAP_W = 950
MAP_MARGIN_DEG = 0.05  # padding around the site bounding box before projecting

RIGHT_X = MARGIN + MAP_W + GAP
RIGHT_W = CANVAS_W - MARGIN - RIGHT_X

GRID_COLS = 4
CELL_GAP = 24
IMG_PAD = 12
LABEL_H = 62

BADGE_R_MAP = 17
BADGE_R_GRID = 20
BADGE_FILL = vu.TEXT_DARK
BADGE_STROKE = "#ffffff"
BADGE_TEXT = "#ffffff"

# The district fill/stroke deliberately reuse SUBJECT (the house palette's
# generic pastel-grey node colour) rather than a new colour: a district is a
# generic backdrop here, not a category the rest of the series' colour
# scheme needs to distinguish.
DISTRICT_FILL = vu.SUBJECT["fill"]
DISTRICT_STROKE = vu.SUBJECT["stroke"]


# --------------------------------------------------------------------------- #
# Data loading
# --------------------------------------------------------------------------- #
def load_sites() -> dict:
    return yaml.safe_load((vu.DATA_MANUAL / "sites.yaml").read_text(encoding="utf-8"))


def load_series() -> dict:
    return yaml.safe_load((vu.DATA_MANUAL / "series_metadata.yaml").read_text(encoding="utf-8"))


def load_geo() -> dict:
    return json.loads(GEO_PATH.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- #
# Projection: equirectangular with a cosine-latitude correction, fitted and
# centred inside a given pixel box. Not reused across calls -- each figure
# built from ``build()`` gets its own projector closed over that call's
# site table, so nothing here needs to be a class or carry mutable state.
# --------------------------------------------------------------------------- #
def _make_projector(sites: dict, map_x: float, map_y: float, map_w: float, map_h: float):
    lons = [s["lon"] for s in sites.values()]
    lats = [s["lat"] for s in sites.values()]
    lon0, lon1 = min(lons) - MAP_MARGIN_DEG, max(lons) + MAP_MARGIN_DEG
    lat0, lat1 = min(lats) - MAP_MARGIN_DEG, max(lats) + MAP_MARGIN_DEG
    cos_lat = math.cos(math.radians((lat0 + lat1) / 2))
    span_x = (lon1 - lon0) * cos_lat
    span_y = lat1 - lat0
    scale = min(map_w / span_x, map_h / span_y)
    off_x = map_x + (map_w - span_x * scale) / 2
    off_y = map_y + (map_h - span_y * scale) / 2

    def project(lon: float, lat: float) -> tuple[float, float]:
        x = (lon - lon0) * cos_lat * scale + off_x
        # SVG y grows downward, latitude grows northward -- flip against lat1.
        y = (lat1 - lat) * scale + off_y
        return x, y

    return project


def _polygon_path(geometry: dict, project) -> str:
    """SVG path data for a Polygon or MultiPolygon, one subpath per ring
    (outer boundary and any holes alike) so the caller can fill it with
    ``fill-rule="evenodd"`` and get holes for free."""
    polys = geometry["coordinates"] if geometry["type"] == "MultiPolygon" else [geometry["coordinates"]]
    subpaths = []
    for poly in polys:
        for ring in poly:
            pts = [project(lon, lat) for lon, lat in ring]
            subpaths.append("M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z")
    return " ".join(subpaths)


# --------------------------------------------------------------------------- #
# Left column: map
# --------------------------------------------------------------------------- #
def _index_badge(x: float, y: float, r: float, label: str, *, size: float) -> str:
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{BADGE_FILL}" '
            f'stroke="{BADGE_STROKE}" stroke-width="2.2"/>\n'
            + vu.svg_text(x, y + 1, label, size=size, weight=500, color=BADGE_TEXT,
                           anchor="middle", baseline="central"))


def _map(parts: list[str], sites: dict, series: dict, geo: dict,
          map_x: float, map_y: float, map_w: float, map_h: float) -> float:
    project = _make_projector(sites, map_x, map_y, map_w, map_h)

    clip_id = "map-clip"
    parts.append(f'<defs><clipPath id="{clip_id}"><rect x="{map_x:.1f}" y="{map_y:.1f}" '
                  f'width="{map_w:.1f}" height="{map_h:.1f}" rx="8"/></clipPath></defs>')
    parts.append(f'<g clip-path="url(#{clip_id})">')
    # A solid full-box fill under the district boundaries, rather than
    # relying on each district's own fill to tile the box: the source
    # GeoJSON is a "niedrig" (low-detail/simplified) cut, simplified per
    # district rather than as one shared network, so neighbouring
    # boundaries don't always meet exactly -- filling each polygon on its
    # own left thin white slivers of canvas showing through along several
    # of those seams. One base fill first, then boundaries drawn
    # stroke-only on top, gets a solid-looking area regardless.
    parts.append(f'<rect x="{map_x:.1f}" y="{map_y:.1f}" width="{map_w:.1f}" height="{map_h:.1f}" '
                  f'fill="{DISTRICT_FILL}"/>')
    for feature in geo["features"]:
        path_d = _polygon_path(feature["geometry"], project)
        parts.append(f'<path d="{path_d}" fill-rule="evenodd" fill="none" '
                      f'stroke="{DISTRICT_STROKE}" stroke-width="1.3"/>')
    parts.append("</g>")
    parts.append(f'<rect x="{map_x:.1f}" y="{map_y:.1f}" width="{map_w:.1f}" height="{map_h:.1f}" '
                  f'rx="8" fill="none" stroke="{vu.BORDER}" stroke-width="1.6"/>')

    # Pins, and a short site-name label beside each one. Label direction
    # alternates per site rather than a single fixed offset -- several
    # sites sit only a few kilometres apart (Elmstein/Annweiler/Dahn,
    # Deidesheim/Kallstadt) and a single-direction label would collide
    # with its neighbour's pin.
    label_offsets = {
        "edenkoben": (1, 1), "dahn": (1, -1), "annweiler_am_trifels": (-1, 1),
        "deidesheim": (1, -1), "speyer": (1, 1), "elmstein": (-1, -1),
        "busenberg": (1, 1), "kallstadt": (1, 1), "germersheim": (1, 1),
        "neustadt_an_der_weinstrasse": (-1, -1), "limburgerhof": (1, -1),
    }
    for coin_id, coin in series["coins"].items():
        site_key = coin["site_key"]
        site = sites[site_key]
        x, y = project(site["lon"], site["lat"])
        dx, dy = label_offsets.get(site_key, (1, 1))
        parts.append(_index_badge(x, y, BADGE_R_MAP, coin_id, size=14))
        label_x = x + dx * (BADGE_R_MAP + 8)
        label_y = y + dy * 4
        parts.append(vu.svg_text(label_x, label_y, site["label"], size=13, weight=500,
                                  color=vu.TEXT_DARK, anchor="start" if dx > 0 else "end",
                                  baseline="central"))

    return map_y + map_h


# --------------------------------------------------------------------------- #
# Right column: coin grid
# --------------------------------------------------------------------------- #
def _coin_grid(parts: list[str], series: dict, grid_x: float, grid_y: float, grid_w: float) -> float:
    coins = list(series["coins"].items())
    n = len(coins)
    rows = math.ceil(n / GRID_COLS)
    cell_w = (grid_w - (GRID_COLS - 1) * CELL_GAP) / GRID_COLS
    img_side = cell_w - 2 * IMG_PAD
    cell_h = IMG_PAD + img_side + 10 + LABEL_H

    img_dir = vu.DATA_COINS / "images"

    for i, (coin_id, coin) in enumerate(coins):
        col, row = i % GRID_COLS, i // GRID_COLS
        cx = grid_x + col * (cell_w + CELL_GAP)
        cy = grid_y + row * (cell_h + CELL_GAP)

        parts.append(f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{cell_w:.1f}" height="{cell_h:.1f}" '
                      f'rx="10" fill="{vu.CARD_BG}" stroke="{vu.BORDER}" stroke-width="1.4"/>')
        img_x, img_y = cx + IMG_PAD, cy + IMG_PAD
        parts.append(vu.svg_image_crop(img_x, img_y, img_side, img_side,
                                        img_dir / coin["obverse_image"]))
        parts.append(_index_badge(img_x + BADGE_R_GRID + 6, img_y + BADGE_R_GRID + 6,
                                   BADGE_R_GRID, coin_id, size=16))

        text_y = img_y + img_side + 24
        title_line = f'{coin["elw_id"]} — {coin["title"]}'
        block, text_y = vu.svg_text_block(cx + 14, text_y, title_line, cell_w - 28, size=15,
                                           weight=500, line_h=19, color=vu.TEXT_DARK)
        parts.append(block)
        block, _ = vu.svg_text_block(cx + 14, text_y + 2, coin["modern_site"], cell_w - 28,
                                      size=13, line_h=17, color=vu.TEXT_MUTED)
        parts.append(block)

    total_h = rows * cell_h + (rows - 1) * CELL_GAP
    return grid_y + total_h


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #
def build(sites: dict, series: dict, geo: dict) -> list[str]:
    body: list[str] = []

    body.append(vu.svg_text(MARGIN, MARGIN + 6, "Modern sites (real)", size=HEADING_SIZE,
                             weight=500, color=vu.TEXT_DARK))
    map_y = MARGIN + 42
    map_bottom = _map(body, sites, series, geo, MARGIN, map_y, MAP_W, MAP_W * 0.94)
    caption_y = map_bottom + 26
    body.append(vu.svg_text(MARGIN, caption_y, "Pin numbers match the coin numbers on the right.",
                             size=14, italic=True, color=vu.TEXT_MUTED))
    left_bottom = caption_y + 6

    body.append(vu.svg_text(RIGHT_X, MARGIN + 6, "Elwetritsch staters I–XI (fictional)",
                             size=HEADING_SIZE, weight=500, color=vu.TEXT_DARK))
    grid_y = MARGIN + 42
    right_bottom = _coin_grid(body, series, RIGHT_X, grid_y, RIGHT_W)

    canvas_h = int(round(max(left_bottom, right_bottom) + MARGIN))
    parts = [vu.svg_open("Elwetritsch stater series overview: findspots and modern sites",
                          w=CANVAS_W, h=canvas_h)]
    parts.extend(body)
    parts.append(vu.svg_close())

    return vu.write_figure(OUT, "series_overview", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    vu.ensure_dirs()
    sites = load_sites()
    series = load_series()
    geo = load_geo()
    written = build(sites, series, geo)
    for p in written:
        print(f"  wrote {p}")
    return written


if __name__ == "__main__":
    main()
