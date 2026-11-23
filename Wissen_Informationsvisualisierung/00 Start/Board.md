---
titel: Board
stand: 2026-11-23
kanban-plugin: board
---

# Board — Informationsvisualisierung

Karten tragen `#person`, `#team` oder `#auto`, optional `fällig:` und `beleg:`.
`beleg:` ist ein Pfadmuster relativ zum Projektordner; `board_sync.py` prüft es.
`#person` und `#team` werden **nie** automatisch abgehakt, nur mit Belegstand und
Überfälligkeit versehen. Nur `#auto` wandert bei vorhandenem Beleg nach `Done`.

Kette: AUFGABE → RECHNUNG → PRÄSENTATION → GRUPPENTEIL → PORTFOLIO → BLOCKSEMINAR.

## To Do
- [ ] **VORLEISTUNG-DATEIEN · Zustimmung/Ablehnung und Video abgeben** #person — zwei Dateien in Stud.IP, MP4 höchstens 25 MB, Neufassung mit `_VXX` vor der Endung · → [[Prüfungsvorleistung]]
- [ ] **FLEXNOW · Anmeldung und Gruppeneinteilung prüfen** #person — Einteilung „bis etwa Weihnachten 2026 bzw. nach Ende der Anmeldefrist“; Datum nicht dokumentiert · → [[Offene Entscheidungen]]
- [ ] **KAP05 · Kapitelnummerierung 5/6 klären** #person — Gesamtfolien: 5 = Interaktion, 6 = Graphen; Arbeitsfassung vom 19.11.: 5 = Graphen · → [[Vorlesungsplan]]
- [ ] **GRUPPE · Beispiele für den Gruppenteil auswählen** #team — ursprüngliche Darstellungen aller Gruppenmitglieder beurteilen, ein bis zwei begründet auswählen · → [[Gruppenarbeit]]
- [ ] **FOLIEN · höchstens fünf Folien für das Blockseminar** #team · fällig: 2027-04-09 — einschließlich Titelfolie; Inhalte ab Folie 6 gelten als nicht abgegeben · → [[Gruppenarbeit]]
- [ ] **FAZIT · persönliche Schlussseite höchstens 400 Wörter** #person · fällig: 2027-03-31 — Vorlesungsfazit und Gruppenfeedback, Wortzahl angeben · → [[Portfolio Trung]]
- [ ] **CODE · Programmcode den Ergebnissen zuordnen** #person · fällig: 2027-03-31 — zusätzlich einreichen, nachvollziehbar zugeordnet · → [[Anhang-Checkliste]]
- [ ] **PORTFOLIO · Gesamtportfolio zusammenstellen** #person · fällig: 2027-03-31 — 5–10 Seiten je Person, Deckblatt, Gruppenteil in allen Portfolios identisch · → [[Portfolio Trung]]


## Doing
- [ ] **VORLEISTUNG · U02 Lie Factor vorbereiten und vorstellen** #person — Variante A bestätigt, Rechnung und Entwurf stehen (Lie Factor 5,00 für A, 2,20 für B), 3–6 Min.; Termin nicht dokumentiert, nichts abgegeben · → [[U02 Lie Factor]]
- [ ] **SEITE2 · Einstiegsseite als Seite 2 übernehmen** #person — unverändert 1:1; Text, Skizzen und Fußnote stehen in der Datei · → [[Einstiegsseite]]


## Done
- [x] **EINSTIEG-UPLOAD · Einstiegsseite in Stud.IP bestätigen** #person — laut Angabe der Person am 25.10.2026 eingereicht; eine Quittung liegt nicht im Projekt · → [[Einstiegsseite]]
- [x] **EINSTIEG-PDF · Einstiegsseite als PDF setzen** #person — 23.11.2026 mit `tectonic`: eine Seite A4, beide Fotos eingebettet, kein Platzhalter, „Wortzahl: 119/120“ · beleg: "Visual 3. Semester/Do_Trung_8229831_Einstiegsseite.pdf" · → [[Schreibregeln für .tex-Abgaben]] · Beleg vorhanden
- [x] **VAULT · Gedächtnis und Automatik eingerichtet** #auto — Struktur und Werkzeuge wie im Schwesterprojekt; Beleg: `Wissen_Informationsvisualisierung/_tools/ingest.py` · → [[Start]]
- [x] **MATERIAL · Kursmaterial eingelesen** #auto — fünf PDFs in `00_Materialien/`, automatische Notizen in `10 Kurs/` · → [[Ingest Log]]


%% kanban:settings
```
{"kanban-plugin":"board"}
```
%%
