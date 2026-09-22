# data/raw/

All inputs to the figures in this repository. Unchanged as obtained;
`main.py` never writes here. No step accesses the network.

| Path | Contents | Source |
|---|---|---|
| `coins/elwetritsch_coin_series_metadata_v3.md` | The eleven-coin series metadata: identifier, composition, obverse/reverse motifs, modern site, fictional findspot and find context, per coin | Drafted in an earlier chat as the series' own documentation; delivered as part of `Elwetrisch_Coin.zip` |
| `coins/images/<ID>_obverse.png`, `<ID>_reverse.png` | The eleven coins' obverse and reverse images (1254×1254, white background) | AI-generated illustrations commissioned by the repository author for this fictional demonstration series; **licence for these images not yet confirmed** (see PRIMER.md Teil D) |
| `manual/sites.yaml` | Wikidata QID, GeoNames ID and coordinates for each of the eleven real modern Palatinate municipalities the series' coins are nominally "found near" | Resolved by hand via web search against wikidata.org / geonames.org (no direct API access from the sandbox this was compiled in — see PRIMER.md A1 Befunde) |
| `manual/series_metadata.yaml` | Structured transcription of every field in `coins/elwetritsch_coin_series_metadata_v3.md`, for all eleven coins: identifier, composition, obverse/reverse description, modern site (+ `site_key` into `sites.yaml`), fictional findspot, find context, interpretative label, prompt — plus the shared classification and the "suggested graph properties" | Transcribed by hand from `coins/elwetritsch_coin_series_metadata_v3.md`, values unchanged (see PRIMER.md A1 Befunde, S-metadata) |
| `manual/coin_<ID>.yaml` | Semantics-detail page content per coin: card text and the CIDOC-CRM terminology-graph relations (property, target label, target identifier, category) | Transcribed from the hand-iterated pilot graphic (`reference/I_semantics_detail.png`), cross-checked against `coins/elwetritsch_coin_series_metadata_v3.md` |
| `reference/I_semantics_detail.png` | The approved pilot graphic this repository's first figure reproduces programmatically | Delivered as part of `Elwetrisch_Coin.zip`; not read by any step — provenance / visual-comparison reference only |
| `reference/I--XI_map.png` | A hand-illustrated fantasy-style overview map of all eleven findspots (not reused: this repository's own overview map, once built, follows the plain modern-border documentation style of the semantics-detail figures instead — PRIMER.md A4) | Delivered as part of `Elwetrisch_Coin.zip`; not read by any step — provenance reference only |
| `geo/rlp_palatinate_districts.geojson` | Modern Rhineland-Palatinate district (Kreis) boundaries, low-detail cut, filtered to the 16 districts overlapping the eleven sites' bounding box — the base map for `step_overview.py` | Fetched once from `isellsoap/deutschlandGeoJSON` (`4_kreise/4_niedrig.geo.json` on GitHub, `raw.githubusercontent.com`; the GitHub API itself is not reachable from this sandbox), released under the Unlicense (public domain); underlying geometry credited by that repository to [DIVA-GIS](http://www.diva-gis.org/gdata). Not fetched live — see PRIMER.md A3 |

## Fiction vs. reality

Repeated from `coins/elwetritsch_coin_series_metadata_v3.md`, because every
figure in this repository depends on keeping the two apart: the coins
themselves, their findspots, hoards and metallurgical analyses are entirely
invented for Linked-Open-Data demonstration purposes. The modern site names
and their Wikidata/GeoNames identifiers in `manual/sites.yaml` are real.
