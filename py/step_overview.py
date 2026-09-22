#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_overview.py -- series overview: modern sites vs. the coins
=================================================================

One figure for the whole eleven-coin series, laid out as asked
(PRIMER.md A4, 2026-09-23): a stylised map of the Palatinate on the
**left** (Rheinland-Pfalz highlighted within Germany, the Rhine, a
handful of larger towns for orientation, and a numbered pin at each
coin's real modern site from ``data/raw/manual/sites.yaml``), and a
numbered grid of all eleven
coins' actual obverse images on the **right**
(``data/raw/coins/images/``, captioned from
``data/raw/manual/series_metadata.yaml``) -- coin *images*, not a table
of names and identifiers (the map-plus-table shape of the old ad-hoc
prototype, ``data/raw/reference/I--XI_map.png``, is explicitly not what
was asked for).

Second round of feedback (2026-09-23), folded in here:

- The map is now sized to end flush with the bottom of the coin grid
  rather than stopping short of it (``_cover_bounds`` below expands
  whichever of the map's longitude/latitude span is short so a uniform,
  aspect-correct scale fills exactly the height available, instead of
  centring inside a taller box and leaving a gap).
- The map is zoomed out further and gained three new layers a plain
  district-outline map didn't have -- Rhineland-Palatinate highlighted
  within Germany (main map fill *and* a small Germany inset, both from
  ``data/raw/geo/germany_states.geojson``), the Rhine
  (``data/raw/geo/rhine.geojson``), and a handful of larger nearby towns
  (``data/raw/manual/reference_cities.yaml``).

Third round of feedback (2026-09-23): the Kreis-level district outlines
from ``data/raw/geo/rlp_palatinate_districts.geojson`` (the first pass's
main content, kept as a "subtle" line layer in the second pass) are
dropped from the map entirely. Even as a subtle line, they were
independently simplified per district rather than as one shared
network, so two neighbouring districts' versions of their common border
rarely land on exactly the same pixels -- at this zoomed-out extent that
read as doubled, crossing lines rather than a clean boundary. The
Rheinland-Pfalz/neighbour state fill plus the Rhine and reference towns
now carry the map's context on their own; the raw file itself is kept
in ``data/raw/geo/`` for provenance and a possible future re-attempt at
a coarser detail level, but this step no longer reads it.

The same small numeral badge (I-XI) appears on a site's map pin and on
its coin's thumbnail, so a reader can match one side to the other
without a legend. It is deliberately outside the REAL/CLASS/TERM/
PROPERTY palette used for the terminology graph elsewhere in this repo
(``elwetritsche_visuals_utils.CATEGORY_LABELS``): the numeral is a
cross-reference index, not a fiction/reality assertion, and colouring it
from that palette would imply one. The fiction/reality distinction this
series otherwise insists on (PRIMER.md A2, property 2) is carried
instead by the two section headings themselves -- "Modern sites (real)"
/ "Elwetritsch staters I-XI (fictional)" -- which is exactly the
distinction the coin-level cards already draw between a "Site" card and
a "Find spot (fictional)" card. The map's land/water colours (a warm
tan for Rhineland-Palatinate, blue for the Rhine) are a small
cartographic palette of their own, separate from that node palette --
a landmass or a river is not a semantic graph node, so there is nothing
in the house Mermaid scheme for it to reuse.

The map's projection is a plain equirectangular one with a
cosine-latitude correction (no cartopy/geopandas/pyproj -- this repo's
one dependency exception for a figure is Pillow for font metrics, not a
geo stack): accurate enough at this scale (a couple of degrees of
latitude end to end) and it keeps the repo's "pure Python, minimal
dependencies" house style.

Geo data is fetched once into ``data/raw/geo/`` and read here, never
fetched live (house rule, PRIMER.md A3) -- see that directory's own
provenance/licence notes in ``data/raw/README.md``.

House rules: no title/footer baked into the SVG, deterministic output.

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
GEO_DIR = vu.DATA_RAW / "geo"
STATES_PATH = GEO_DIR / "germany_states.geojson"
RHINE_PATH = GEO_DIR / "rhine.geojson"

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
# Padding (in degrees) added around the sites+towns bounding box before
# zooming out further to fill the available map height -- see
# _cover_bounds. Larger than the first pass's 0.05 deg (user feedback
# 2026-09-23: "etwas raus-zoomen").
PAD_LON = 0.16
PAD_LAT = 0.10
KM_PER_DEG_LAT = 111.32  # good enough at this latitude/scale; see module docstring

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

# A small cartographic palette, separate from the house Mermaid node
# palette (see module docstring): warm tan for the highlighted state
# (Rheinland-Pfalz), a paler neutral for its neighbours, blue for the
# Rhine, and a muted dot for reference towns that are not coin sites.
LAND_FILL, LAND_STROKE = "#efe6d1", "#b9a877"
NEIGHBOUR_FILL, NEIGHBOUR_STROKE = "#f6f5f0", "#cdc8b8"
RHINE_STROKE = "#7fb2d6"
CITY_DOT = "#57534a"

INSET_W, INSET_H = 190, 150


# --------------------------------------------------------------------------- #
# Data loading
# --------------------------------------------------------------------------- #
def load_sites() -> dict:
    return yaml.safe_load((vu.DATA_MANUAL / "sites.yaml").read_text(encoding="utf-8"))


def load_series() -> dict:
    return yaml.safe_load((vu.DATA_MANUAL / "series_metadata.yaml").read_text(encoding="utf-8"))


def load_cities() -> dict:
    return yaml.safe_load((vu.DATA_MANUAL / "reference_cities.yaml").read_text(encoding="utf-8"))


def load_states() -> dict:
    return json.loads(STATES_PATH.read_text(encoding="utf-8"))


def load_rhine() -> dict:
    return json.loads(RHINE_PATH.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- #
# Projection: equirectangular with a cosine-latitude correction.
# --------------------------------------------------------------------------- #
def _fit_projector(lon0: float, lat0: float, lon1: float, lat1: float,
                    box_x: float, box_y: float, box_w: float, box_h: float):
    """Project lon/lat onto a pixel box, centred, at a uniform scale (the
    smaller of the two axis scales -- so the content is fully visible,
    possibly with letterboxing on one axis). Returns (project, px_per_km),
    the latter via KM_PER_DEG_LAT: the cosine-latitude correction applied
    to longitude cancels back out when converting a projected-unit scale
    to a physical one, so one px-per-km figure holds in both directions."""
    cos_lat = math.cos(math.radians((lat0 + lat1) / 2))
    span_x = (lon1 - lon0) * cos_lat
    span_y = lat1 - lat0
    scale = min(box_w / span_x, box_h / span_y)
    off_x = box_x + (box_w - span_x * scale) / 2
    off_y = box_y + (box_h - span_y * scale) / 2

    def project(lon: float, lat: float) -> tuple[float, float]:
        x = (lon - lon0) * cos_lat * scale + off_x
        # SVG y grows downward, latitude grows northward -- flip against lat1.
        y = (lat1 - lat) * scale + off_y
        return x, y

    return project, scale / KM_PER_DEG_LAT


def _cover_bounds(lon0: float, lat0: float, lon1: float, lat1: float,
                   box_w: float, box_h: float) -> tuple[float, float, float, float]:
    """Expand whichever of the lon/lat span is short, symmetrically, so a
    box of this aspect ratio is filled edge to edge at one uniform,
    aspect-correct scale -- like CSS ``background-size: cover`` -- rather
    than centred with letterboxing. Used for the main map, which must end
    flush with the bottom of the coin grid next to it, not stop short of
    or run past it (user feedback 2026-09-23), so its own aspect ratio
    can't be chosen freely; whatever height that leaves it, this fills
    exactly by widening the visible area rather than distorting it."""
    cos_lat = math.cos(math.radians((lat0 + lat1) / 2))
    span_x = (lon1 - lon0) * cos_lat
    span_y = lat1 - lat0
    box_aspect = box_w / box_h
    if span_x / span_y > box_aspect:
        extra = (span_x / box_aspect - span_y) / 2
        lat0, lat1 = lat0 - extra, lat1 + extra
    else:
        extra = ((span_y * box_aspect) / cos_lat - (lon1 - lon0)) / 2
        lon0, lon1 = lon0 - extra, lon1 + extra
    return lon0, lat0, lon1, lat1


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


def _line_path(geometry: dict, project) -> str:
    """SVG path data for a LineString or MultiLineString (the Rhine)."""
    lines = geometry["coordinates"] if geometry["type"] == "MultiLineString" else [geometry["coordinates"]]
    subpaths = []
    for line in lines:
        pts = [project(lon, lat) for lon, lat in line]
        subpaths.append("M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts))
    return " ".join(subpaths)


def _bounds(geo: dict) -> tuple[float, float, float, float]:
    lons, lats = [], []
    for feature in geo["features"]:
        g = feature["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            for ring in poly:
                for lon, lat in ring:
                    lons.append(lon)
                    lats.append(lat)
    return min(lons), min(lats), max(lons), max(lats)


# --------------------------------------------------------------------------- #
# Left column: map
# --------------------------------------------------------------------------- #
def _index_badge(x: float, y: float, r: float, label: str, *, size: float) -> str:
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{BADGE_FILL}" '
            f'stroke="{BADGE_STROKE}" stroke-width="2.2"/>\n'
            + vu.svg_text(x, y + 1, label, size=size, weight=500, color=BADGE_TEXT,
                           anchor="middle", baseline="central"))


def _states_layer(parts: list[str], states: dict, project, *, highlight: str) -> None:
    # Draw the highlighted state (Rheinland-Pfalz) last so its border sits
    # cleanly on top of any neighbour it touches, rather than the other
    # way around.
    feats = sorted(states["features"], key=lambda f: f["properties"]["name"] == highlight)
    for feature in feats:
        is_home = feature["properties"]["name"] == highlight
        fill, stroke, sw = (LAND_FILL, LAND_STROKE, 1.8) if is_home else (NEIGHBOUR_FILL, NEIGHBOUR_STROKE, 1.1)
        path_d = _polygon_path(feature["geometry"], project)
        parts.append(f'<path d="{path_d}" fill-rule="evenodd" fill="{fill}" '
                      f'stroke="{stroke}" stroke-width="{sw}"/>')


def _rhine_layer(parts: list[str], rhine: dict, project) -> None:
    for feature in rhine["features"]:
        path_d = _line_path(feature["geometry"], project)
        parts.append(f'<path d="{path_d}" fill="none" stroke="{RHINE_STROKE}" stroke-width="5" '
                      f'stroke-linecap="round" stroke-linejoin="round"/>')


def _cities_layer(parts: list[str], cities: dict, project) -> None:
    for city in cities.values():
        x, y = project(city["lon"], city["lat"])
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{CITY_DOT}" '
                      f'stroke="#ffffff" stroke-width="1.3"/>')
        parts.append(vu.svg_text(x + 9, y + 4, city["label"], size=12, color=vu.TEXT_MUTED))


def _sites_layer(parts: list[str], sites: dict, series: dict, project) -> None:
    # Label direction alternates per site rather than a single fixed
    # offset -- several sites sit only a few kilometres apart (Elmstein/
    # Annweiler/Dahn, Deidesheim/Kallstadt) and a single-direction label
    # would collide with its neighbour's pin.
    label_offsets = {
        "edenkoben": (1, 1), "dahn": (1, -1), "annweiler_am_trifels": (-1, 1),
        "deidesheim": (1, -1), "speyer": (1, 1), "elmstein": (-1, -1),
        "busenberg": (1, 1), "kallstadt": (1, 1), "germersheim": (1, 1),
        "neustadt_an_der_weinstrasse": (1, -1), "limburgerhof": (1, -1),
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


def _inset(parts: list[str], states: dict, inset_x: float, inset_y: float) -> None:
    """A small Germany-outline inset with Rheinland-Pfalz picked out, so
    the main map's regional extent is placed in context (user feedback
    2026-09-23: "ggf noch ... Bundesländer; ein bisschen wie zuvor")."""
    parts.append(f'<rect x="{inset_x:.1f}" y="{inset_y:.1f}" width="{INSET_W}" height="{INSET_H}" '
                  f'rx="6" fill="#ffffff" stroke="{vu.BORDER}" stroke-width="1.4"/>')
    pad = 8
    lon0, lat0, lon1, lat1 = _bounds(states)
    project, _ = _fit_projector(lon0, lat0, lon1, lat1, inset_x + pad, inset_y + pad,
                                 INSET_W - 2 * pad, INSET_H - 2 * pad - 14)
    _states_layer(parts, states, project, highlight="Rheinland-Pfalz")
    parts.append(vu.svg_text(inset_x + INSET_W / 2, inset_y + INSET_H - 10, "Germany",
                              size=11, color=vu.TEXT_MUTED, anchor="middle"))


def _scale_bar(parts: list[str], x: float, y: float, px_per_km: float) -> None:
    km = next((c for c in (5, 10, 20, 25, 50, 100) if 90 <= c * px_per_km <= 220), 20)
    px = km * px_per_km
    bar_h = 5
    parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{px:.1f}" height="{bar_h}" '
                  f'fill="none" stroke="{vu.TEXT_DARK}" stroke-width="1.2"/>')
    parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{px / 2:.1f}" height="{bar_h}" fill="{vu.TEXT_DARK}"/>')
    parts.append(vu.svg_text(x, y + bar_h + 15, "0", size=11, color=vu.TEXT_MUTED, anchor="middle"))
    parts.append(vu.svg_text(x + px, y + bar_h + 15, f"{km} km", size=11, color=vu.TEXT_MUTED, anchor="middle"))


def _north_arrow(parts: list[str], cx: float, cy: float, size: float = 24) -> None:
    tip_y, base_y = cy - size / 2, cy + size / 2
    parts.append(f'<line x1="{cx:.1f}" y1="{base_y:.1f}" x2="{cx:.1f}" y2="{tip_y + 7:.1f}" '
                  f'stroke="{vu.TEXT_DARK}" stroke-width="2"/>')
    parts.append(f'<path d="M {cx - 6:.1f} {tip_y + 8:.1f} L {cx:.1f} {tip_y:.1f} '
                  f'L {cx + 6:.1f} {tip_y + 8:.1f} Z" fill="{vu.TEXT_DARK}"/>')
    parts.append(vu.svg_text(cx, base_y + 15, "N", size=12, weight=500, color=vu.TEXT_DARK, anchor="middle"))


def _map(parts: list[str], sites: dict, series: dict, cities: dict,
          states: dict, rhine: dict, map_x: float, map_y: float, map_w: float, map_h: float) -> float:
    lons = [s["lon"] for s in sites.values()] + [c["lon"] for c in cities.values()]
    lats = [s["lat"] for s in sites.values()] + [c["lat"] for c in cities.values()]
    lon0, lon1 = min(lons) - PAD_LON, max(lons) + PAD_LON
    lat0, lat1 = min(lats) - PAD_LAT, max(lats) + PAD_LAT
    lon0, lat0, lon1, lat1 = _cover_bounds(lon0, lat0, lon1, lat1, map_w, map_h)
    project, px_per_km = _fit_projector(lon0, lat0, lon1, lat1, map_x, map_y, map_w, map_h)

    clip_id = "map-clip"
    parts.append(f'<defs><clipPath id="{clip_id}"><rect x="{map_x:.1f}" y="{map_y:.1f}" '
                  f'width="{map_w:.1f}" height="{map_h:.1f}" rx="8"/></clipPath></defs>')
    parts.append(f'<g clip-path="url(#{clip_id})">')
    _states_layer(parts, states, project, highlight="Rheinland-Pfalz")
    _rhine_layer(parts, rhine, project)
    _cities_layer(parts, cities, project)
    _sites_layer(parts, sites, series, project)
    parts.append("</g>")
    parts.append(f'<rect x="{map_x:.1f}" y="{map_y:.1f}" width="{map_w:.1f}" height="{map_h:.1f}" '
                  f'rx="8" fill="none" stroke="{vu.BORDER}" stroke-width="1.6"/>')

    _inset(parts, states, map_x + 14, map_y + 14)
    _north_arrow(parts, map_x + map_w - 32, map_y + 34)
    _scale_bar(parts, map_x + 20, map_y + map_h - 34, px_per_km)

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
def build(sites: dict, series: dict, cities: dict, states: dict, rhine: dict) -> list[str]:
    # The right column's height is computed first: the map (left) must end
    # flush with the bottom of the coin panel (right), not the other way
    # round (user feedback 2026-09-23).
    right_body: list[str] = [
        vu.svg_text(RIGHT_X, MARGIN + 6, "Elwetritsch staters I–XI (fictional)",
                    size=HEADING_SIZE, weight=500, color=vu.TEXT_DARK)
    ]
    grid_y = MARGIN + 42
    right_bottom = _coin_grid(right_body, series, RIGHT_X, grid_y, RIGHT_W)

    body: list[str] = [
        vu.svg_text(MARGIN, MARGIN + 6, "Modern sites (real)", size=HEADING_SIZE,
                    weight=500, color=vu.TEXT_DARK)
    ]
    map_y = MARGIN + 42
    caption_reserve = 32  # 26px gap to the caption baseline + 6px below it
    map_h = right_bottom - map_y - caption_reserve
    map_bottom = _map(body, sites, series, cities, states, rhine,
                       MARGIN, map_y, MAP_W, map_h)
    caption_y = map_bottom + 26
    body.append(vu.svg_text(MARGIN, caption_y,
                             "Pin numbers match the coin numbers on the right; the Rhine and "
                             "nearby towns are shown for orientation.",
                             size=14, italic=True, color=vu.TEXT_MUTED))
    left_bottom = caption_y + 6

    body.extend(right_body)

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
    cities = load_cities()
    states = load_states()
    rhine = load_rhine()
    written = build(sites, series, cities, states, rhine)
    for p in written:
        print(f"  wrote {p}")
    return written


if __name__ == "__main__":
    main()
