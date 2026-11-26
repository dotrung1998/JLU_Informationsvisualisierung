# Changelog

Änderungen am Lernserver und an diesem Repository. Neueste zuerst; pro Datum ein
Thema, damit die Liste nicht zerfasert. Die kurze Fassung steht im Lernserver im
Kanal `#changelog`, die Entscheidungen und Gründe in
`Wissen_Informationsvisualisierung/00 Start/Entscheidungen.md`.

## 2026-11-26 — Unterseiten, Bildtafeln und Wischen mit dem Trackpad

**Thema:** Navigation und Anschauung.

- `Wissen_Informationsvisualisierung/00 Start/lernserver.html`
  - sechs Unterseiten an den Kapiteln: `03-gestalt-farben`, `04-diagrammtypen`,
    `05-filterzustaende`, `06-graph-layouts`, `07-baum-layouts`, `08-zeit-diagramme`;
    jede mit einer schematischen Bildtafel (Gestaltgesetze und Farbskalen, sechs
    Diagrammtypen, Filterzustände, vier Graph-Layouts, drei Baum-Layouts, drei
    Zeitbilder) und einer Merkpunkt-Nachricht;
  - `buildSubChannels()` erzeugt die eingerückten Einträge aus `data-parent`; ein Kapitel
    kann mehrere Unterseiten tragen (`04-multivariate-daten`: `04-clutter-beispiele` und
    `04-diagrammtypen`);
  - der Pager reagiert auf horizontales `wheel` (Trackpad, Magic Mouse): ein Wisch
    blättert, ohne die Maustaste zu halten; vertikales Scrollen bleibt unberührt;
  - Legende, Kanalzähler (25) und Suchfuß beschreiben den neuen Stand, der Suchfuß zählt
    die Sektionen selbst.
- `Status.md`, `Entscheidungen.md`, `Start.md`: Stand, Entscheidung und Sitzungsnotiz
  fortgeschrieben.

## 2026-11-26 — 04-clutter-beispiele: Unterkanal, zwei Seiten, Rückweg

**Thema:** Ergänzungskanal zu Kapitel 4, Einordnung und Lesbarkeit.

- `Wissen_Informationsvisualisierung/00 Start/lernserver.html`
  - `#04-clutter-beispiele` steht im Kanalbaum eingerückt unter
    `#04-multivariate-daten` (Klasse `chan sub`), nicht mehr auf derselben Ebene wie die
    Kapitel;
  - jede Nachricht des Kanals hat **zwei** Seiten statt einer — Deutsch und
    Tiếng Việt; die Vorher/Nachher-Grafik bleibt auf Seite 1, deshalb entfällt die
    erzeugte Seite 2 (Attribut `data-de-vi` statt `data-nopager`, `buildPagers()` baut
    dafür zwei Registerkarten);
  - die vietnamesischen Fassungen — sieben, auch für die Nachricht am Kanalende — stehen
    im JSON-Block `#viData` unter `k04beispiele`; die Fazit-Nachricht hat dafür Seite 1
    auf Deutsch (Einordnung und Verweise) und Seite 3 auf Vietnamesisch;
  - die Legende in `#willkommen-&-regeln` nennt die Ausnahme: zwei statt drei Seiten im
    Galeriekanal, weil die Vorher/Nachher-Grafik dort schon auf Seite 1 steht;
  - `buildPagers()` prüft nur noch `data-pager`; die Ausnahme `data-nopager` ist entfallen,
    weil keine Nachricht sie mehr nutzt;
  - Rückweg über dem Kanal und am Ende: `← zurück zu #04-multivariate-daten`;
  - Eintrag im Kanal `#changelog`, Zähler unverändert bei 19 Kanälen.
- `Wissen_Informationsvisualisierung/00 Start/Entscheidungen.md`: Entscheidung vom 25.11.
  zur Einseitigkeit fortgeschrieben (zwei Seiten statt drei, Einordnung als Unterkanal).

## 2026-11-25 — Clutter-Reduktion: Beispielgalerie und Verweise

**Thema:** Kapitel 4, sechs Techniken der Clutter-Reduktion.

- `Wissen_Informationsvisualisierung/00 Start/lernserver.html`
  - neuer Ergänzungskanal `#04-clutter-beispiele` mit sechs schematischen
    Vorher/Nachher-Abbildungen (SVG): Dimension Re-Ordering, Sampling, Magic Lens,
    konstante Informationsdichte, Punktverschiebung sowie Aggregation/Clustering
    und Filtering;
  - die sechs Punkte im Kanal `#04-multivariate-daten` verlinken auf das jeweilige
    Beispiel und, wo der Stoff ausführlicher steht, auf die Stelle im Kapitel
    (parallele Koordinaten, Daten-Transformation, Rank-by-Feature, Filter in
    `#05-interaktion`);
  - Eintrag im bestehenden Kanal `#changelog` mit Sprung zum ersten Beispiel;
  - Kanalzähler und Suchfuß auf 19 Kanäle aktualisiert.
- `CHANGELOG.md` angelegt: Langfassung mit Dateipfaden.
