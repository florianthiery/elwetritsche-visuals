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
- **Zweite Nachbesserung per Pixel-Sampling (geprüft 2026-09-22, nach dem
  zweiten Commit):** Nutzerhinweis „Münzbild zu klein, Platzierung falsch".
  Direktes Vermessen der Referenzdatei ergab, dass die rechte Spalte
  (Terminologiegraph) dort nur 676px breit ist (Wurzelbox `x=1602..2278`
  auf 2350px Canvas-Breite) — deutlich schmaler, als dieses Skript zuerst
  annahm (`RIGHT_W=926`), und entsprechend war die linke Spalte
  (Münzbild + Karten) mit `LEFT_W=1310` zu schmal statt der tatsächlichen
  ≈1480px (Kartenreihe misst `x=60..1540`). Korrigiert: `LEFT_W=1310→1530`,
  `GAP=34→40`, Münzbild-Seitenlänge `500px→734px` (Referenz: Avers
  701px, Revers 717px, Lücke 15px — beides nahe an den neuen Werten),
  Wurzelbox-Höhe `62px→80px` (Referenz: `y=84..164`, Höhe 80, an vier
  x-Stichproben identisch reproduziert).

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
| Site vs. Fundort (Attributkarten + Terminologiegraph) | zwei getrennte Karten statt einer kombinierten: "Site" (reale moderne Gemeinde, mit wd:/geonames:-Kennung) und "Find spot (fictional)" (erfundener Fundkontext, ohne externe Kennung) — entsprechend ein siebtes Relations-Objekt im Terminologiegraphen (`property: "findspot"`, `property_uri: ""`, da `elwetritsch_coin_series_metadata_v3.md` diese Relation selbst als bespoke/nicht-formal ausweist), Farbe TERM/Violett wie alle anderen Nicht-Wurzel-Knoten. Gilt für alle Münzen (Schema-Entscheidung, nicht nur Münze I). | 2026-09-22 |
| Textausrichtung im Terminologiegraphen | alle Boxen linksbündig, auch die Wurzelbox ("Elwetritsch stater") — bewusste Abweichung von der alten Referenzgrafik (die die Wurzelbox zentriert zeigt), expliziter Nutzerwunsch | 2026-09-23 |
| Schriftbreiten-Messung | echte Glyphenbreite aus der vendorten Fira-Sans-.ttf via Pillow statt einer geschätzten Zeichen-Durchschnittsbreite — eine flache Schätzung passt nie gleichzeitig zu kurzen Property-Namen und langen Sätzen (`Pillow` als neue Abhängigkeit in `requirements.txt`) | 2026-09-23 |

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
| S-II…S-XI | Semantics-Detail-Seiten Münzen II–XI | S-I, S-metadata | teilweise erledigt 2026-09-22 (II, III) |
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

#### Nachgebessert 2026-09-22, zweiter Durchgang (Spaltenbreiten/Münzgröße)

Nutzerhinweis: Münzbild zu klein, Platzierung falsch — insbesondere die
Breite. Direktes Vermessen der Referenzdatei (siehe A1 Befunde) zeigte:
die rechte Spalte war in der ersten Fassung ~250px zu breit und die linke
Spalte entsprechend zu schmal, was das Münzbild kleiner wirken ließ, als
es in der Referenz ist. `MARGIN`/`LEFT_W`/`GAP`/Münzbild-Seitenlänge/
Wurzelbox-Höhe in `py/step_semantics_detail.py` an die vermessenen Werte
angepasst (siehe A1). Erneut visuell gegen die Referenz abgeglichen
(Wurzelbox jetzt `x≈1611..2309` gegen Referenz `x=1602..2278` — praktisch
deckungsgleich). Determinismus erneut geprüft: zwei Läufe, `cmp`
byte-identisch.

#### Nachgebessert 2026-09-22, dritter Durchgang (Rahmen, Schriftgrößen)

Nutzerhinweis: Rahmen um die Münzbilder soll weg, und Schriftposition/
-größe passen noch nicht ganz. Umgesetzt:

- Die dünne graue Rahmenlinie um Avers-/Revers-Bild (`<rect ... stroke=
  BORDER/>` in `_coin_images`) entfernt — reine Stilentscheidung auf
  Nutzerwunsch, unabhängig davon, ob die Referenz selbst einen (kaum
  sichtbaren) Rahmen hat.
- Alle Textgrößen in den Attributkarten und im Terminologiegraphen per
  Zeilen-Höhen-Messung (Bandprofil: helle/dunkle Pixelreihen pro Textzeile
  zählen) gegen die Referenz kalibriert, statt der zuerst aus
  hdoku26-visuals übernommenen Werte: Kartenlabel 12→16, Kartenwert
  17→18, Notizen 12.5→14, Kennungs-Chip 12.5→17, Wurzelbox-Titel 15.5→18,
  Wurzelbox-Untertitel 11.5→16, Knotentitel 15.5→16, Property-Pill 13→14,
  externe Knotenkennung 12.5→14, Legende 12.5→15, Überschrift 20→22,
  Avers/Revers-Beschriftung 13→15. `svg_box()` bekam dafür neue
  Parameter `title_size`/`subtitle_size` (Default weiterhin 16), da
  Wurzelbox und Relationsknoten unterschiedliche Zielgrößen brauchen.
  Kartenreihe: `card_gap` 18→22 (ebenfalls pixel-gemessen, `LEFT_W`
  zugleich 1530→1480 zur Deckung mit der gemessenen Kartenreihenbreite
  `x=60..1540`).
- Determinismus erneut geprüft: zwei Läufe, `cmp` byte-identisch.

#### Nachgebessert 2026-09-22, vierter Durchgang (Einzug, Überschrift, Canvas-Höhe, Site/Fundort-Trennung)

Nutzerfeedback (nach Commit des dritten Durchgangs, anhand aller drei
Münzen): Schrift rechts in den Boxen zu klein; Überschrift soll nur
„Coin X Graph" lauten; die graue Bezeichner-Beschriftung („wd:Q…") unter
jeder Box wird von der senkrechten Verbindungslinie durchkreuzt; Site und
Fundort sollen getrennte Karten/Boxen sein; zu viel weißer Rand unten.

- **Linie durch Bezeichnertext:** Pixel-Vermessung der Referenz zeigt die
  Spine-Linie bei `x≈1635`, Property-Pill und Bezeichnertext dagegen erst
  bei `x≈1681` — ein Einzug von rund 80px ab der Box-Kante (`x=1602`), den
  dieser Nachbau bisher nicht hatte (Bezeichnertext stand bündig mit der
  Box-Kante, dadurch schien die durchgehend gezeichnete Spine-Linie durch
  den Text zu laufen). Fix: gemeinsame `content_x = x + 80` für Pill und
  Bezeichnertext in `_terminology_graph()`; `spine_x` bleibt bei einem
  kleineren `x+30`-Versatz, sodass beide sich nie horizontal überlappen.
  Die separat gemeldete Farbabweichung („leicht grau passt nicht zur
  Referenz") erwies sich beim Nachmessen als exakter Treffer
  (`#64635e` = `vu.TEXT_MUTED`) — dasselbe Kreuzungsartefakt macht den
  Text nur optisch "kaputt" wirkend, keine echte Farbabweichung.
- **Überschrift:** von „Terminology graph (Linked Open Data)" auf
  `f"Coin {coin_id} Graph"` geändert — wörtliche Nutzervorgabe.
- **Schriftgrößen rechts:** Knotentitel 16→18, Property-Pill/Chip 14→16,
  Bezeichnertext 14→16, Legende per neuem `size=16`-Argument (vorher
  Default 15); `pill_h` 30→32, `id_h` 24→26 entsprechend mitgewachsen.
- **Canvas-Höhe dynamisch statt fest:** `_cards()` und
  `_terminology_graph()` geben jetzt ihre jeweilige Bottom-Y zurück;
  `build()` baut den SVG-Body zunächst in eine Liste, berechnet
  `canvas_h = max(left_bottom, right_bottom) + MARGIN` und übergibt das
  erst dann an `vu.svg_open(..., h=canvas_h)` statt der festen
  `CANVAS_H=1160`. Damit passt sich die Bildhöhe an den tatsächlichen
  Inhalt jeder Münze an (durch die siebte Relation und die größeren
  Schriften jetzt `1256` statt der alten festen `1160` — höher, aber ohne
  Rest-Weißraum darunter, was der eigentliche Nutzerwunsch war).
- **Site/Fundort-Trennung** (siehe A4): die bisher kombinierte „Find spot
  (fictional)"-Karte in zwei Karten aufgeteilt — „Site" (reale Gemeinde,
  behält die wd:/geonames:-Kennungen) und „Find spot (fictional)" (nur
  noch der erfundene Fundkontext, keine externe Kennung). Im
  Terminologiegraphen entsprechend eine siebte Relation ergänzt
  (`property: "findspot"`, `property_uri: ""`, Farbe TERM) zwischen der
  bestehenden „P53 has former or current location"-Relation und der
  abschließenden „P62 depicts → Elwetritsch"-Relation. Angewendet auf
  `coin_I.yaml`, `coin_II.yaml`, `coin_III.yaml` — sechs Karten und sieben
  Relationen jetzt bei allen drei Münzen identisch strukturiert (nur die
  Inhalte unterscheiden sich).
- Alle drei Münzen neu gebaut und visuell geprüft (Übersicht und
  Graph-Detailausschnitt je Münze) — Einzug behoben, Überschrift korrekt,
  sechste Karte + siebte (violette) Box vorhanden, kein Rest-Weißraum mehr
  unterhalb der Legende. Determinismus geprüft: zwei Läufe, `cmp` auf alle
  sechs Dateien (3× SVG + 3× PNG) ohne Ausgabe.

#### Nachgebessert 2026-09-22, fünfter Durchgang (Linie/Kennung-Abstand in den Karten, Ausrichtung + Breite im Graphen, Text-Überlauf)

Nutzerfeedback (nach Commit des vierten Durchgangs): unten in den
Attributkarten überschneidet sich die Trennlinie mit der Kennung
("die Links"); im Terminologiegraphen soll die Schrift linksbündig statt
zentriert stehen, die gelben Property-Pills seien zu lang, und Text läuft
teilweise über den Kartenrand hinaus.

- **Trennlinie kreuzt Kennungstext (Karten):** dieselbe Ursache wie beim
  Graphen im vierten Durchgang, nur diesmal in den Attributkarten: die
  Trennlinie stand nur 8px über der ersten Kennungszeile — bei 17px
  Schrift liegt das mitten in der Zeichenhöhe. `_cards()` reserviert jetzt
  20px mehr zwischen Trennlinie und erster Kennungszeile (Trennlinie
  bleibt an ihrer Position, die Kennungszeilen rutschen 20px tiefer;
  `link_area_h` entsprechend um 20px gewachsen, damit der Kartenrand
  darunter gleich bleibt).
- **Text-Überlauf in den Karten:** Ursache war nicht in erster Linie die
  Schriftbreiten-Schätzung, sondern dass die `notes`-Zeilen aus dem YAML
  *ungeprüft* übernommen wurden — wer die Zeilenumbrüche im YAML gesetzt
  hatte, musste die Pixelbreite selbst richtig einschätzen, und das ging
  bei Münze III ("real castle above the findspot (Trifels)", 41 Zeichen)
  und Münze II ("Südwestpfalz sandstone country" / "Südliche Weinstraße
  vineyard margin") schief — die Zeile lief über den Kartenrand hinaus.
  Fix: `notes` wird jetzt zu einem String zusammengefügt und wie `value`
  durch `wrap_lines()` neu umgebrochen, nicht mehr 1:1 aus dem YAML
  übernommen.
- **Schriftbreiten-Schätzung nachgeschärft:** `text_width()` war mit
  `0.56*size` pro Zeichen kalibriert; ein Pixel-Nachmessen der Referenz
  ("P53 has former or current location" in `wd:Q537985`s Zeile) ergibt
  eher `0.50*size` — auf `0.52` gesetzt (Mittelweg, keine Überanpassung
  an einen einzelnen String). `wrap_lines()` bekommt zusätzlich 6%
  Sicherheitsspanne (bricht etwas früher um), damit eine Unterschätzung
  nie wieder zu echtem Überlauf führt, statt nur die Rundung zu
  verbessern.
- **Zentriert statt linksbündig (Terminologiegraph):** die Referenz zeigt
  die Relations-Knoten ("near Edenkoben (Palatinate)", "Dubbeglas (wine
  glass)", …) links­bündig, nur die Wurzelbox ("Elwetritsch stater") ist
  zentriert (Pixel-Nachmessen: Kennungstext-Einzug ~14px vom Box-Rand).
  `svg_box()` in `elwetritsche_visuals_utils.py` bekommt einen neuen
  `align`-Parameter (`"middle"` Default, `"start"` linksbündig mit `pad`);
  `_terminology_graph()` übergibt `align="start"` für alle Relations-
  Knoten, die Wurzelbox bleibt beim Default.
- **Gelbe Property-Pills zu lang:** direkte Folge derselben zu großzügigen
  `text_width`-Schätzung plus `pad=14` (Referenz misst ~9–10px) — mit der
  nachgeschärften Schätzung und `pad=11` in `_terminology_graph()`s
  `svg_chip`-Aufruf liegen die Pills jetzt nah an der gemessenen
  Referenzbreite (`"P53 has former or current location"`: Referenz
  ≈290px, jetzt ≈300px statt vorher ≈333px).
- Alle drei Münzen neu gebaut; Kartenzeile und Graph-Ausschnitt je Münze
  visuell geprüft — keine Linie kreuzt mehr Text, keine Karte läuft mehr
  über, Relations-Knoten linksbündig, Pills spürbar schmaler.
  Determinismus geprüft: zwei Läufe, `cmp` auf alle sechs Dateien (3× SVG
  + 3× PNG) ohne Ausgabe.

#### Nachgebessert 2026-09-22/23, sechster Durchgang (Kennung-Abstand = Caption-Abstand, Wurzelbox linksbündig, Pill-Vertikalzentrierung, echte Schriftbreiten-Messung)

Nutzerfeedback (nach Commit des fünften Durchgangs): die `wd:...`-Kennung
in den Karten soll denselben Abstand zur Trennlinie haben wie die
"cf. real ..."-Caption; die grüne Wurzelbox oben im Graphen soll auch
linksbündig sein; die Abstände der gelben Pills nach oben/unten passen
nicht — sollen vertikal zentriert sein; und (Pixel-Nachmessen auf meiner
Seite, nicht explizit gemeldet, aber derselbe Befund) die Pills selbst
hatten bei kurzen Property-Namen wie "P2 has type" bis zu 4× mehr
Weißraum rechts als links.

- **Kennung-Abstand ≠ Caption-Abstand:** beide starteten an
  unterschiedlichen Offsets von der Trennlinie (Kennung bei +20, Caption
  bei +30). `_cards()`s `link_y` auf `content_h+44` angehoben (Trennlinie
  bleibt bei `content_h+14`, beide also jetzt +30) und die Caption
  benutzt `link_y` direkt statt `link_y+10` — beide Fälle jetzt am
  selben Abstand. `link_area_h` entsprechend gewachsen, damit der
  Kartenrand darunter gleich bleibt.
- **Wurzelbox linksbündig:** `_terminology_graph()` übergibt jetzt auch
  für die Wurzelbox `align="start"` (bewusste Abweichung von der alten
  Referenzgrafik, die die Wurzelbox zentriert zeigt — expliziter
  Nutzerwunsch, in A4 als eigene Zeile festgehalten, siehe unten).
- **Pills nicht vertikal zentriert:** die beiden Abstände um jeden Pill
  waren `16` oberhalb (plus zusätzlich `18` aus der vorherigen Relation,
  also faktisch `34`) gegen nur `8` unterhalb — der Pill hing praktisch
  am unteren Knoten. Beide Konstanten (`gap_pill_node`, `gap_after_node`)
  durch eine einzige `gap_v = 16` ersetzt, oben *und* unten am Pill
  verwendet; die Spline-/Cursor-Fortschreibung in `_terminology_graph()`
  entsprechend vereinfacht.
- **Schriftbreiten-Schätzung durch echte Messung ersetzt:** die
  Nachkalibrierung im fünften Durchgang (0.56→0.52 pro Zeichen) behob
  einen einzelnen pixel-gemessenen String, verschlimmerte aber andere —
  "P2 has type" (viele kurze, schmale Zeichen) rendert real bei etwa der
  Hälfte dessen, was jeder flache Faktor vorhersagt, wodurch dessen Pill
  im letzten Durchgang links 18px, rechts aber 71px Weißraum hatte. Eine
  flache Zeichen-Durchschnittsbreite kann Kurztexte und lange Sätze nicht
  gleichzeitig richtig treffen. `text_width()` misst jetzt die
  tatsächliche Glyphenbreite aus der vendorten Fira-Sans-.ttf via Pillow
  (`Pillow>=10.0` zu `requirements.txt` hinzugefügt) statt zu schätzen;
  `wrap_lines()`s Sicherheitsspanne entsprechend von 6% auf 2% reduziert
  (jetzt nur noch ein Puffer gegen resvg-py-vs-Pillow-Rendering-Differenzen,
  keine Korrektur eines systematischen Schätzfehlers mehr).
- Alle drei Münzen neu gebaut; Pill-Innenabstände beidseitig nachgemessen
  (z. B. "P2 has type": vorher 18px/71px links/rechts, jetzt 18px/16px) —
  Kartenzeile und Graph-Ausschnitt je Münze zusätzlich visuell geprüft.
  Determinismus geprüft: zwei Läufe, `cmp` auf alle sechs Dateien (3× SVG
  + 3× PNG) ohne Ausgabe.

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

#### Erledigt 2026-09-22 (Münzen II und III, als Paket-Test)

Nutzerwunsch: vor dem weiteren Rollout erst prüfen, ob Coin I's Layout auch
für andere Münzen "im Paket" funktioniert. `coin_II.yaml` (Dahn/
Pfälzerwald, "The Wanderer") und `coin_III.yaml` (Annweiler am Trifels,
"The Guardian") angelegt, nach demselben Sechs-Relationen-Schema wie
Münze I (Material → Klassenhierarchie → Revers-Motiv (real) → Site →
Kreatur), aber mit münzspezifischem, real existierendem Depicts-Ziel statt
eines Kopiervorgangs:

- Münze II: Revers zeigt Pfälzerwald-Landschaft mit Sandstein-Formation →
  `P62 depicts` → **Palatinate Forest** (wd:Q707004) statt eines
  generischen Ziels; Karte zusätzlich mit **sandstone** (wd:Q13085) als
  zweitem Chip.
- Münze III: Revers zeigt eine Burg auf einem Hügel → `P62 depicts` →
  **Trifels Castle** (wd:Q559202) — die tatsächliche Burg oberhalb von
  Annweiler am Trifels, dem Site der Münze; damit bekommt das fiktive
  Revers-Motiv ein reales, thematisch passendes Ziel statt eines
  Platzhalters.

Beide QIDs per Websuche gegen wikidata.org aufgelöst (gleiche Methode wie
bei `sites.yaml`, kein direkter API-Zugriff im Sandbox). `grapevine`
(wd:Q1422342) aus Münze I wiederverwendet (dort bereits als Karten-Chip
geführt, nicht neu verifiziert).

`python main.py` baut jetzt alle drei Münzen automatisch (`glob` über
`coin_*.yaml`, kein Codeeingriff nötig, wie schon in S-I vorgesehen).
Determinismus geprüft: zwei Läufe, `cmp` auf alle sechs Dateien (3× SVG +
3× PNG) ohne Ausgabe.

Im vierten Nachbesserungs-Durchgang zu S-I (siehe dort) auf die
Site/Fundort-Kartentrennung + siebte Relation nachgezogen, damit alle drei
Münzen weiterhin identisch strukturiert sind: `coin_II.yaml`'s vorherige
kombinierte Karte ("near Dahn, Palatinate", real) wurde zu "Site" (Dahn,
Palatinate) + neuer "Find spot (fictional)"-Karte ("Rock-shelter deposit
2"); `coin_III.yaml` entsprechend zu "Site" (Annweiler am Trifels) +
"Find spot (fictional)" (Hoard 7, "Am Sonnenberg").

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
