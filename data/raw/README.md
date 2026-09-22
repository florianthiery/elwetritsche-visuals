# data/raw/

All inputs to the figures in this repository. Unchanged as obtained;
`main.py` never writes here. No step accesses the network.

| Path | Contents | Source |
|---|---|---|
| `coins/elwetritsch_coin_series_metadata_v3.md` | The eleven-coin series metadata: identifier, composition, obverse/reverse motifs, modern site, fictional findspot and find context, per coin | Drafted in an earlier chat as the series' own documentation; delivered as part of `Elwetrisch_Coin.zip` |
| `coins/images/<ID>_obverse.png`, `<ID>_reverse.png` | The eleven coins' obverse and reverse images (1254×1254, white background) | AI-generated illustrations commissioned by the repository author for this fictional demonstration series; **licence for these images not yet confirmed** (see PRIMER.md Teil D) |
| `manual/sites.yaml` | Wikidata QID, GeoNames ID and coordinates for each of the eleven real modern Palatinate municipalities the series' coins are nominally "found near" | Resolved by hand via web search against wikidata.org / geonames.org (no direct API access from the sandbox this was compiled in — see PRIMER.md A1 Befunde) |
| `manual/coin_<ID>.yaml` | Semantics-detail page content per coin: card text and the CIDOC-CRM terminology-graph relations (property, target label, target identifier, category) | Transcribed from the hand-iterated pilot graphic (`reference/I_semantics_detail.png`), cross-checked against `coins/elwetritsch_coin_series_metadata_v3.md` |
| `reference/I_semantics_detail.png` | The approved pilot graphic this repository's first figure reproduces programmatically | Delivered as part of `Elwetrisch_Coin.zip`; not read by any step — provenance / visual-comparison reference only |
| `reference/I--XI_map.png` | A hand-illustrated fantasy-style overview map of all eleven findspots (not reused: this repository's own overview map, once built, follows the plain modern-border documentation style of the semantics-detail figures instead — PRIMER.md A4) | Delivered as part of `Elwetrisch_Coin.zip`; not read by any step — provenance reference only |

## Fiction vs. reality

Repeated from `coins/elwetritsch_coin_series_metadata_v3.md`, because every
figure in this repository depends on keeping the two apart: the coins
themselves, their findspots, hoards and metallurgical analyses are entirely
invented for Linked-Open-Data demonstration purposes. The modern site names
and their Wikidata/GeoNames identifiers in `manual/sites.yaml` are real.
