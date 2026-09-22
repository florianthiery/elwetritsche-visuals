# elwetritsche-visuals

Figures for the **Elwetritsch stater series** — a fictional set of eleven
archaic-style electrum coins, invented for Linked Open Data / terminology-graph
demonstration purposes. Each coin combines Palatinate folklore (the
*Elwetritsch*, a humorous hybrid creature from Palatinate legend) with archaic
Greek coin aesthetics, and is nominally "found" near a real Palatinate
municipality — while the coin itself, its findspot, hoard and metallurgical
analysis are entirely invented.

Same house pattern as
[hdoku26-visuals](https://github.com/florianthiery/hdoku26-visuals): pure-Python
SVG authoring, PNG rasterised in-process with resvg-py and the vendored Fira
Sans, no title or citation baked into the figure itself, deterministic output.
Unlike that repository this one is single-language (English) — see
`PRIMER.md` A3.

## Figures

| Coin | Figure | Files |
|---|---|---|
| I — The Reveller (ELW-01) | Semantics detail: obverse/reverse images, five attribute cards (material, motifs, fictional find spot, metallurgical analysis) and a CIDOC-CRM terminology graph (the coin as an E22 Human-Made Object instance, linked to real Wikidata/GeoNames/Getty AAT identifiers) | `img/semantics-detail/I_semantics_detail.{svg,png}` |
| II — The Wanderer (ELW-02) | Same page; reverse motif's real depicts target is the Palatinate Forest (Pfälzerwald) | `img/semantics-detail/II_semantics_detail.{svg,png}` |
| III — The Guardian (ELW-03) | Same page; reverse motif's real depicts target is Trifels Castle, the real castle at the coin's site (Annweiler am Trifels) | `img/semantics-detail/III_semantics_detail.{svg,png}` |

Coins IV–XI follow the same page once their `data/raw/manual/coin_<ID>.yaml`
is drafted — no code change needed, `step_semantics_detail.py` builds
whichever coin files exist (see PRIMER.md Teil B/D). An overview figure
across all eleven coins (findspot vs. modern site, with a stylised
modern-border map) is planned as a second figure family; see PRIMER.md A4.

## Build

    pip install -r requirements.txt
    python main.py

`python main.py --list` shows the steps; `--only semantics`, `--from
semantics`, `--skip semantics`, `--dry-run` and `--strict` work as in the
sibling repositories.

**Fonts:** `fonts/FiraSans-Regular.ttf` and `fonts/FiraSans-Medium.ttf` (SIL
Open Font License), the same files as in hdoku26-visuals.

## Data

All inputs are under `data/raw/` and are described in
[`data/raw/README.md`](data/raw/README.md). No step accesses the network.

## Licence

Code: MIT. Figures (SVG/PNG output of this repository): CC BY 4.0. Wikidata
content: CC0. GeoNames content: CC BY 4.0. The coin illustrations under
`data/raw/coins/images/` are AI-generated for this fictional series; their
licence is not yet confirmed (PRIMER.md Teil D).
