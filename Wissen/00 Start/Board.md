---
titel: Board
stand: 2026-11-22
kanban-plugin: board
---

# Board — Informationsvisualisierung

Karten tragen `#person`, `#team` oder `#auto`, optional `fällig:` und `beleg:`.
`beleg:` ist ein Pfadmuster relativ zum Projektordner; `board_sync.py` prüft es.
`#person` und `#team` werden **nie** automatisch abgehakt, nur mit Belegstand und
Überfälligkeit versehen. Nur `#auto` wandert bei vorhandenem Beleg nach `Done`.

Kette: AUFGABE → RECHNUNG → PRÄSENTATION → GRUPPENTEIL → PORTFOLIO → BLOCKSEMINAR.

## To Do
- [ ] **EINSTIEG-UPLOAD · Einstiegsseite in Stud.IP bestätigen** #person · fällig: 2026-10-25 — die `.tex` liegt lokal, ein Abgabenachweis fehlt; Seite 2 des Portfolios, 1:1 übernehmen · beleg: "Visual 3. Semester/Do_Trung_*Einstiegsseite.tex" · → [[Einstiegsseite]] · überfällig (29 Tage) · Beleg vorhanden
- [ ] **EINSTIEG-PDF · Einstiegsseite als PDF setzen** #person — bisher nur `.tex` und zwei Fotos; Wortzahl 119/120 im PDF prüfen · → [[Schreibregeln für .tex-Abgaben]]
- [ ] **VORLEISTUNG · Übungsaufgabe wählen und vorstellen** #person — eine Aufgabe U01–U14, eine Variante; 3–6 Min. laut Übungsblatt, 5–10 Min. laut Foliensatz; Termin nicht dokumentiert · → [[Prüfungsvorleistung]]
- [ ] **VORLEISTUNG-DATEIEN · Zustimmung/Ablehnung und Video abgeben** #person — zwei Dateien in Stud.IP, MP4 höchstens 25 MB, Neufassung mit `_VXX` vor der Endung · → [[Prüfungsvorleistung]]
- [ ] **FLEXNOW · Anmeldung und Gruppeneinteilung prüfen** #person — Einteilung „bis etwa Weihnachten 2026 bzw. nach Ende der Anmeldefrist“; Datum nicht dokumentiert · → [[Offene Entscheidungen]]
- [ ] **KAP05 · Kapitelnummerierung 5/6 klären** #person — Gesamtfolien: 5 = Interaktion, 6 = Graphen; Arbeitsfassung vom 19.11.: 5 = Graphen · → [[Vorlesungsplan]]
- [ ] **GRUPPE · Beispiele für den Gruppenteil auswählen** #team — ursprüngliche Darstellungen aller Gruppenmitglieder beurteilen, ein bis zwei begründet auswählen · → [[Gruppenarbeit]]
- [ ] **FOLIEN · höchstens fünf Folien für das Blockseminar** #team · fällig: 2027-04-09 — einschließlich Titelfolie; Inhalte ab Folie 6 gelten als nicht abgegeben · → [[Gruppenarbeit]]
- [ ] **FAZIT · persönliche Schlussseite höchstens 400 Wörter** #person · fällig: 2027-03-31 — Vorlesungsfazit und Gruppenfeedback, Wortzahl angeben · → [[Portfolio Trung]]
- [ ] **CODE · Programmcode den Ergebnissen zuordnen** #person · fällig: 2027-03-31 — zusätzlich einreichen, nachvollziehbar zugeordnet · → [[Anhang-Checkliste]]
- [ ] **PORTFOLIO · Gesamtportfolio zusammenstellen** #person · fällig: 2027-03-31 — 5–10 Seiten je Person, Deckblatt, Gruppenteil in allen Portfolios identisch · → [[Portfolio Trung]]


## Doing
- [ ] **SEITE2 · Einstiegsseite als Seite 2 übernehmen** #person — unverändert 1:1; Text, Skizzen und Fußnote stehen in der Datei · → [[Einstiegsseite]]


## Done
- [x] **VAULT · Gedächtnis und Automatik eingerichtet** #auto — Struktur und Werkzeuge wie im Schwesterprojekt; Beleg: `Wissen/_tools/ingest.py` · → [[Start]]
- [x] **MATERIAL · Kursmaterial eingelesen** #auto — fünf PDFs in `00_Materialien/`, automatische Notizen in `10 Kurs/` · → [[Ingest Log]]


%% kanban:settings
```
{"kanban-plugin":"board"}
```
%%
