# PRIMER — elwetritsche-visuals

Arbeitsplan für die Grafiken der fiktiven Elwetritsch-Elektronstater-Serie
(elf Münzen, Palatinate-Folklore auf archaischer Münzästhetik) — als
Beispielmaterial für Terminologie-Wissensgraphen / Linked-Open-Data-Lehre.
Entstanden aus einem Chat, in dem ein einzelnes Detailbild (Münze I) und eine
Ad-hoc-Übersichtsgrafik per PIL/matplotlib gebaut wurden; dieses Repo baut
beides sauber und reproduzierbar in Python (SVG + resvg-py) nach.

Zu Beginn jedes Chats hochladen, am Ende zurückschreiben.

---

## Teil A — Immer gültig

### A1 Ausgangslage

| Was | Rolle |
|---|---|
| hdoku26-visuals | Stilvorlage: Utils, Canvas, Hausregeln — hierher kopiert, nicht referenziert |
| `Elwetrisch_Coin.zip` / `Elwetrisch_Coin_1.zip` | Rohdaten: `elwetritsch_coin_series_metadata_v3.md` (Serienmetadaten), 11×2 Münzbilder, zwei Referenzgrafiken (`I_semantics_detail.png`, `I--XI_map.png`) |
| `elwetritsch_coin_series_metadata_v3.md` | Autoritative Quelle für Material, Motive, Fundkontext und Site pro Münze — Koordinaten bewusst weggelassen, da alle Fundorte fiktiv sind |

**Befunde (geprüft 2026-09-22):**

- Der erste Upload (`Elwetrisch_Coin.zip`) hatte **keine Bilder für Münze X**
  (`X_obverse.png`/`X_reverse.png` fehlten) und benannte Münze V als `5_*`.
  Der zweite Upload (`Elwetrisch_Coin_1.zip`, strukturiert in
  `coins/`/`detail/`/`map/`) hat alle elf Bildpaare korrekt benannt
  (`I_*`…`XI_*`); `elwetritsch_coin_series_metadata_v3.md` ist zwischen
  beiden Uploads byte-identisch (MD5 `3b8a6d2c2407188fd9d2a03c87c49172`).
- `detail/I_semantics_detail.png` im zweiten Upload ist exakt die Datei, die
  im vorherigen Chat als PIL-Grafik geliefert wurde (gleiche Byte-Größe,
  1881964 Bytes) — der Nutzer hat sie als Zielvorgabe für dieses Repo in den
  Rohdaten abgelegt, nicht als neue Version.
- Terminologie-Graph-Knoten „P45 consists of“ zeigte in der Referenzgrafik
  den Titel **„Electron“** statt „Electrum“ (Tippfehler aus einer früheren
  Iteration; die Material-Karte und der Zielbezeichner wd:Q239481 sagen
  korrekt „Electrum“). In `data/raw/manual/coin_I.yaml` auf „Electrum“
  korrigiert.
- Wikidata-QIDs und GeoNames-IDs für alle elf modernen Pfalz-Gemeinden
  wurden per Websuche aufgelöst (kein direkter API-Zugriff im Sandbox) und
  in `data/raw/manual/sites.yaml` abgelegt — u. a. Disambiguierung
  Gemeinde vs. Verbandsgemeinde bei Annweiler am Trifels (Q22953 vs.
  Q519620), Deidesheim (Q22951 vs. Q562644) und Germersheim (Q22629 vs.
  Q8543, letzteres der Landkreis).
- Ausgabe-Palette folgt dem Mermaid-Hausfarbschema
  (RealObject grün/Class orange/Term violett/Property amber), aber mit
  dezenter statt schwarzer Kontur — so wie in der genehmigten Referenzgrafik
  `I_semantics_detail.png`, nicht wie im generischen Mermaid-Default.
- **Nachgebessert per Pixel-Sampling (geprüft 2026-09-22, nach dem ersten
  Commit):** der erste Nachbau von `I_semantics_detail.png` wich sichtbar
  von der Referenz ab. Systematisches Pixel-Sampling der Referenzdatei (PIL)
  ergab drei konkrete Abweichungen, alle in `py/step_semantics_detail.py`
  bzw. `py/elwetritsche_visuals_utils.py` korrigiert:
  1. Kennungen in den Attributkarten sind **violett** (`#4C1D95`, Term-Farbe),
     nicht grün — Zeile 100 unten war falsch und ist korrigiert.
  2. Legendenbeschriftungen lauten exakt „RealObject / Class / Term /
     Property" (je ein Wort), nicht die längeren Umschreibungen der ersten
     Iteration.
  3. Im Terminologiegraphen steht die Kennung eines Relations-Zielknotens
     (z. B. „wd:Q239481") **außerhalb/unterhalb** der farbigen Box, in
     gedecktem Grau — nur der Wurzelknoten trägt seinen Untertitel
     („(fictional coin)") weiterhin weiß **innerhalb** der Box. Zusätzlich
     bekam jeder Verzweigungspunkt auf der senkrechten Linie einen kleinen
     gefüllten Punkt (in der Referenz vorhanden, in der ersten Iteration
     gefehlt).

### A2 Zielbild

```
data/raw/coins/ (Serienmetadaten, 11×2 Münzbilder)
data/raw/manual/ (sites.yaml, coin_<ID>.yaml)
      │
      ▼  python main.py   (offline, deterministisch)
py/step_semantics_detail.py  ──►  img/semantics-detail/<ID>_semantics_detail.{svg,png}
```

Eigenschaften:
1. Jede Karte und jeder Graphknoten stammt aus `data/raw/manual/coin_<ID>.yaml`;
   kein Text ist im Skript fest verdrahtet.
2. Fiktion und Realität bleiben unterscheidbar: nur echte, extern auflösbare
   Bezeichner (wd:/geonames:/aat:/cidoc-crm.org) erscheinen als Identifier-Zeile.
3. Zwei Läufe hintereinander → `git status` sauber (geprüft: `cmp` auf SVG
   und PNG byte-identisch).
4. Neue Münzen (II–XI) kommen allein durch eine neue
   `data/raw/manual/coin_<ID>.yaml` hinzu — `step_semantics_detail.py`
   entdeckt sie automatisch, kein Codeeingriff nötig.

### A3 Querschnittsregeln

- Rohdaten unter `data/raw/`, unverändert, read-only; Produkte nach `img/`.
- Wiederverwendung heißt kopieren (Utils aus hdoku26-visuals), nicht
  referenzieren.
- Keine Uhr in der Ausgabe: `RELEASE`-Konstante, kein `datetime.now()`.
- Kein Netzzugriff in den Schritten (Wikidata/GeoNames-IDs sind bereits in
  `manual/sites.yaml` fixiert).
- Hausregeln aus hdoku26-visuals: Fira Sans, kein Titel/Footer eingebrannt
  (die Grafik ist ein Dokumentationsbaustein, kein Foliendeck), **keine
  Diagonalen**.
- **Abweichend von hdoku26-visuals: nur Englisch, kein DE/EN-Paar.** Diese
  Serie war von Anfang an englisch angelegt (britisches Englisch), sie ist
  kein Vortragsfolien-Material.
- Sprache: PRIMER deutsch, alles andere britisches Englisch.
- Windows ist Referenzplattform; Befehle einzeilig für `cmd`.

### A4 Beschlusslage

| Frage | Beschluss | seit |
|---|---|---|
| Repo-Name | `elwetritsche-visuals` (github.com/florianthiery/elwetritsche-visuals) | 2026-09-22 |
| Stil-/Technikbasis | wie hdoku26-visuals: SVG + resvg-py statt der PIL/matplotlib-Ad-hoc-Skripte aus dem Vorgängerchat | 2026-09-22 |
| Sprache | nur Englisch (kein DE/EN-Paar) | 2026-09-22 |
| Reihenfolge | zuerst Semantics-Detail-Seite für Münze I reproduzierbar (dieser Chat), danach die Übersichtsgrafik über alle 11 Münzen | 2026-09-22 |
| Übersichtsgrafik-Stil (Vorschlag) | wie `I_semantics_detail.png`: keine Titel-/Footer-Zeile im SVG, klare Formen, gleiches Farbschema; **kein** Fantasy-Kartenstil wie `reference/I--XI_map.png` | Vorschlag 2026-09-22 |
| Palette | Mermaid-Hausfarbschema (RealObject grün/Class orange/Term violett/Property amber), Kontur dezent statt schwarz — folgt der genehmigten Referenzgrafik | 2026-09-22 |
| Kennungs-Darstellung in den Attributkarten | Klartext in Term-Violett (`#4C1D95`) untereinander (wie im Original-PIL-Bild, per Pixel-Sampling verifiziert — **nicht** Real-Grün, das war die erste, falsche Annahme), **keine** gefüllten Chips — Chips bleiben den CIDOC-Property-Pills im Terminologiegraphen vorbehalten | korrigiert 2026-09-22 |
| Kennung am Relations-Zielknoten (Terminologiegraph) | kleine Grau-Beschriftung außerhalb/unterhalb der Box, nicht als weißer Untertitel innerhalb — nur der Wurzelknoten (Münze selbst) behält den Untertitel innerhalb der Box | 2026-09-22 |
| Lizenz der Münzbilder (Vorschlag) | noch nicht bestätigt — AI-generiert vom Repo-Autor, vermutlich CC BY 4.0 wie die übrigen Grafiken; zu bestätigen | Vorschlag 2026-09-22 |

### A5 Was in welchem Chat hochgeladen wird

Das ganze Repo ohne `.git/`, `.venv/`:

    robocopy elwetritsche-visuals %TEMP%\elwetritsche-bundle /E /XD .git .venv __pycache__ & powershell Compress-Archive -Path %TEMP%\elwetritsche-bundle\* -DestinationPath elwetritsche-bundle.zip -Force

`img/` bewusst NICHT ausgeschlossen (anders als bei hdoku26-visuals empfohlen)
— das Repo ist klein genug, und die Ausgabedateien sind das versionierte,
zitierfähige Produkt.

---

## Teil B — Schrittübersicht

| ID | Schritt | hängt ab von | Status |
|---|---|---|---|
| S0 | Festlegungen (Technikbasis, Sprache, Reihenfolge, Palette) | — | erledigt 2026-09-22 |
| S1 | Skelett: main.py, Utils, Rohdaten, Lizenz | S0 | erledigt 2026-09-22 |
| S-I | Semantics-Detail-Seite Münze I (Pilot) | S1 | erledigt 2026-09-22 |
| S-metadata | Serienmetadaten aller 11 Münzen als `data/raw/manual/series_metadata.yaml` | S1 | erledigt 2026-09-22 |
| S-II…S-XI | Semantics-Detail-Seiten Münzen II–XI | S-I, S-metadata | offen |
| S-overview | Übersichtsgrafik über alle 11 Münzen (Fundort vs. moderne Site, stilisierte Karte) | S1, S-metadata | offen |

S-metadata, S-II…S-XI und S-overview hängen nur vom Skelett (S1) ab, nicht
voneinander, und können in beliebiger Reihenfolge angegangen werden; laut A4
zuerst aber S-I abschließend prüfen, dann S-overview. S-metadata ist reine
Datenaufbereitung (keine Grafikausgabe) und war schnell erledigt, sobald S-I
lief — S-II…S-XI liest sie künftig statt erneut die Markdown-Quelle zu
parsen.

---

## Teil C — Die Schritte

### S1 — Skelett

**Ziel:** `main.py`, `py/elwetritsche_visuals_utils.py`, `requirements.txt`,
`LICENSE`, `CITATION.cff`, `.gitignore`, Rohdaten unter `data/raw/`.

**Abnahme:** `python main.py --list` zeigt die Schritte; `python main.py`
läuft durch und erzeugt `img/semantics-detail/I_semantics_detail.{svg,png}`;
zweiter Lauf byte-identisch (`cmp`).

#### Erledigt 2026-09-22

- Utils aus `hdoku26-visuals/py/hdoku26_visuals_utils.py` kopiert und
  angepasst: Palette ersetzt (Mermaid-Schema statt GND/Community/Aggregator),
  Canvas auf 2350×1160, `t()` auf Englisch-only reduziert (API-Kompatibilität
  beibehalten, damit ein späteres DE/EN-Bedürfnis nicht die Signatur bricht).
  `resvg-py` (0.5.0) und `PyYAML` per `pip install --break-system-packages`
  installiert und getestet.
- Fonts (`FiraSans-Regular.ttf`, `FiraSans-Medium.ttf`,
  `LICENSE-FiraSans.txt`) unverändert aus hdoku26-visuals kopiert.
- `LICENSE` (MIT) aus hdoku26-visuals kopiert; `CITATION.cff` neu für dieses
  Repo (Titel, Keywords, Repo-URL).

### S-I — Semantics-Detail-Seite Münze I (Pilot)

**Ziel:** `I_semantics_detail.png` — bisher eine Hand-iterierte PIL-Grafik —
als reproduzierbares SVG+PNG aus `data/raw/manual/coin_I.yaml` und
`data/raw/manual/sites.yaml` nachbauen: Münzbild (Avers/Revers), fünf
Attributkarten (Material, Motiv Avers, Motiv Revers, Fundort (fiktiv),
Metallurgische Analyse), Terminologiegraph rechts (CIDOC-CRM-Klassen,
Vokabularbegriffe, reale Bezeichner).

**Abnahme:** `python py/step_semantics_detail.py` läuft standalone; jede
Zahl/Kennung in der Grafik stammt aus `coin_I.yaml`/`sites.yaml`; visueller
Abgleich mit `data/raw/reference/I_semantics_detail.png` — Layout, Farben und
Inhalt entsprechen der Referenz (mit der Electron→Electrum-Korrektur aus A1);
zweiter Lauf byte-identisch.

#### Erledigt 2026-09-22

- `py/step_semantics_detail.py` entdeckt `data/raw/manual/coin_*.yaml`
  automatisch (`glob`) — für Münzen II–XI genügt eine neue YAML-Datei, kein
  Codeeingriff.
- Kennungen in den Attributkarten als Klartext statt gefüllter Chips
  gerendert — entspricht dem Original-PIL-Bild genauer als die erste
  Iteration mit `svg_chip`.
- `svg_image_crop` (aus hdoku26-visuals übernommen) bettet die beiden
  1254×1254-PNGs direkt ein; kein Zwischenschritt nötig.
- Determinismus geprüft: zwei Läufe, `cmp` auf `.svg` und `.png` ohne
  Ausgabe (byte-identisch).

#### Nachgebessert 2026-09-22 (nach erstem Commit, per Pixel-Sampling-Abgleich)

Der Nutzer meldete, der erste committete Nachbau sehe nicht wie die
Referenz aus. Ursache und Fix siehe A1 Befunde/A4 (Kennungsfarbe
Term-Violett statt Real-Grün, Legendentext „RealObject/Class/Term/
Property", Relations-Kennung außerhalb der Box, Verzweigungspunkt auf der
Linie ergänzt). Nach dem Fix erneut visuell gegen
`data/raw/reference/I_semantics_detail.png` abgeglichen (Karten- und
Graphenbereich Ausschnitt für Ausschnitt) — deckt sich jetzt bis auf die
bewusste Electron→Electrum-Korrektur (siehe `coin_I.yaml`-Kopfkommentar).
Determinismus erneut geprüft: zwei Läufe, `cmp` byte-identisch.

### S-metadata — Serienmetadaten als YAML

**Ziel:** alle Prosafelder aus `elwetritsch_coin_series_metadata_v3.md` (pro
Münze: Identifier, Komposition, Avers/Revers-Beschreibung, moderne Site,
Fundort, Fundkontext, interpretativer Titel, Prompt) sowie die gemeinsame
Klassifikation und die „Suggested graph properties" strukturiert in
`data/raw/manual/series_metadata.yaml` ablegen — damit spätere Schritte
(S-II…S-XI, S-overview) das nicht erneut aus der Markdown-Datei
herausparsen müssen.

**Abnahme:** Datei lädt mit `yaml.safe_load`; jeder `site_key` löst gegen
`sites.yaml` auf, jedes `obverse_image`/`reverse_image` existiert unter
`data/raw/coins/images/` — beides per Python-Einzeiler geprüft.

#### Erledigt 2026-09-22

- Per Hand transkribiert (wie `sites.yaml`) statt geparst — die Quelle ist
  Markdown-Prosa mit uneinheitlicher Interpunktion, ein Parser wäre selbst
  fehleranfälliger als sorgfältiges Abtippen bei nur 11 Einträgen.
- `composition_text` (Originalstring) **und** `composition_pct`
  (`{au, ag, cu}`, geparst) parallel abgelegt — spätere Grafiken (z. B. ein
  Materialdiagramm) brauchen die Zahlen, die Attributkarten weiterhin den
  Originalstring.
- `prompt` am Quelltrenner „|" in `prompt_obverse`/`prompt_reverse`
  gesplittet.
- Ergänzt `data/raw/README.md` um den Eintrag für diese Datei.
- Bewusst **kein** Ersatz für `coin_<ID>.yaml`: Letztere bleiben die
  kuratierte, layoutnahe Quelle für `step_semantics_detail.py` (Kartentexte
  sind dort kompakter formuliert als die Markdown-Prosa, und die
  Terminologiegraph-Relationen sind dort Handarbeit, kein 1:1-Abbild der
  Markdown-Quelle). `series_metadata.yaml` ist die vollständige,
  quellennahe Ablage daneben.

### S-II…S-XI — Semantics-Detail-Seiten der übrigen zehn Münzen

**Ziel:** wie S-I, für Münzen II–XI. Je eine `data/raw/manual/coin_<ID>.yaml`
nach dem Schema von `coin_I.yaml`, inhaltlich gestützt auf
`data/raw/manual/series_metadata.yaml` (S-metadata); Terminologiegraph-
Relationen pro Münze neu überlegen (nicht alle Münzen haben zwingend
dieselben sechs Relationen wie Münze I — z. B. hat Münze V zwei
Herrschaftsattribute, Münze X einen Routen-/Pilgerbezug ohne
Dubbeglas-Motiv).

**Abnahme:** wie S-I.

### S-overview — Übersichtsgrafik über alle 11 Münzen

**Ziel:** eine Grafik im Stil von `I_semantics_detail.png` (keine
Titel-/Footer-Zeile im SVG, klare Formen, Mermaid-Farbschema), die pro Münze
Fundort (fiktiv) und übergeordnete moderne Site zeigt, mit einer stilisierten
Karte (moderne Verwaltungsgrenzen, nicht der Fantasy-Kartenstil aus
`reference/I--XI_map.png`) — Fortführung der Ad-hoc-Vorversion aus dem
Vorgängerchat (`elwetritsch-series-overview-map.png`, PIL/matplotlib), jetzt
im SVG+resvg-py-Hausstil dieses Repos.

**Abnahme:** wie S-I; zusätzlich alle Koordinaten/Kennungen aus
`data/raw/manual/sites.yaml`, keine im Skript fest verdrahteten Werte.

#### Offen

- Kartenbasis (Verwaltungsgrenzen Rheinland-Pfalz) muss als Rohdatei nach
  `data/raw/` — die Ad-hoc-Vorversion hat sie live von
  `raw.githubusercontent.com/isellsoap/deutschlandGeoJSON` geladen, was der
  Kein-Netzzugriff-Regel (A3) widerspricht; für dieses Repo einmalig laden
  und unter `data/raw/geo/` ablegen.
- Layout (Karte links/rechts, Tabelle vs. Kartenraster) noch offen.

---

## Teil D — Offene Punkte

- Lizenz der Münzbilder unter `data/raw/coins/images/` noch nicht bestätigt
  (A4, als Vorschlag markiert).
- Terminologiegraph-Relationen für Münzen II–XI: gemeinsames Schema
  (P45/P2/P2/P62/P53/P62 wie Münze I) oder pro Münze individuell? Betrifft
  v. a. Münzen mit zusätzlichen Motiven (z. B. Münze V: Krone, Zepter, Orb —
  eventuell ein zusätzliches P62-depicts-Paar).
- `reference/I--XI_map.png` und `reference/I_semantics_detail.png` sind
  reine Provenienz-Referenzen (von keinem Schritt gelesen) — falls das Repo
  wächst, prüfen ob sie weiterhin nötig sind oder in die PR-Beschreibung des
  ersten Commits verschoben werden können.
