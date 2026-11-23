# AGENTS.md — Informationsvisualisierung (JLU Gießen)

Arbeits- **und** Gedächtnisort für die Vorlesung *Informationsvisualisierung*
(Prof. Sangam Chatterjee, Ph.D., WiSe 2026/27, JLU Gießen). Prüfungsleistung:
**e-Portfolio mit 5–10 Seiten und Programmcode**, Abgabe bis 31.03.2027 über Stud.IP;
Prüfungsvorleistung: Präsentation einer Übungsaufgabe U01–U14.

Dieses Projekt ist ein **eigenes Repository** (`dotrung1998/JLU_Informationsvisualisierung`)
und unabhängig vom Schwesterprojekt `../Projektplanung` (Seminar Projektplanung Data
Analytics). Nichts zwischen den beiden Projekten hin- und herkopieren, außer den Werkzeugen
in `Wissen_Informationsvisualisierung/_tools/`, die bewusst gleich gehalten sind.

## Zuerst lesen

0. `Wissen_Informationsvisualisierung/00 Start/Điểm vào (VI).md` — Kurzorientierung auf Vietnamesisch.
1. `Wissen_Informationsvisualisierung/00 Start/Start.md` — Einstieg, aktueller Stand, Landkarte.
2. `Wissen_Informationsvisualisierung/00 Start/Status.md` — Fristen, nächste Aktion je Person.
3. `Wissen_Informationsvisualisierung/00 Start/Offene Entscheidungen.md` — was nur die Lehrenden bzw. die Person
   entscheiden kann.

## Ordner

| Pfad | Rolle |
|---|---|
| `00_Materialien/` | **Quelle.** Kursmaterial: Foliensätze, Handout, Übungsblatt, Download-Liste. Unverändert lassen. |
| `Visual 3. Semester/` | **Quelle.** Abgabe der Einstiegsseite (`.tex`, zwei Fotos). Unverändert lassen. |
| `Prüfungsvorleistung/` | **Ablage.** Eigene Lösung der Übungsaufgabe, Video, Zustimmungs-PDF. |
| `e-Portfolio/Portfolio/` | **Ablage.** Gesamtportfolio (PDF). |
| `e-Portfolio/Programmcode/` | **Ablage.** Programmcode, den Ergebnissen zugeordnet. |
| `Wissen_Informationsvisualisierung/` | **Gedächtnis.** Obsidian-Vault mit Start, Kurs, Vorlesungen, Gruppe, Portfolio, Plan. |
| `Wissen_Informationsvisualisierung/_tools/` | `ingest.py`, `board_sync.py`, `daily.sh`, `daily_guard.sh`, `discord_notify.py`, `author_guard.py`. |

## Pflichtschritte am Anfang jeder Sitzung

```bash
python3 Wissen_Informationsvisualisierung/_tools/ingest.py        # neue/geänderte Quellen einlesen
python3 Wissen_Informationsvisualisierung/_tools/board_sync.py    # Board und Fristen fortschreiben
cat "Wissen_Informationsvisualisierung/00 Start/Neu seit letztem Lauf.md"
```

Danach `Start.md` und `Status.md` lesen und erst dann arbeiten.

## Pflichtschritte am Ende jeder Sitzung, in der etwas passiert ist

1. `Wissen_Informationsvisualisierung/00 Start/Status.md` — Fristen, nächste Aktion, Stand je Person.
2. `Wissen_Informationsvisualisierung/00 Start/Entscheidungen.md` — **jede** Entscheidung mit Datum, Grund und
   verworfener Alternative anhängen. Nie rückwirkend umschreiben, nur ergänzen.
3. Wenn neue Unterlagen dazukommen: Datei in `00_Materialien/` (Kursmaterial) oder in den
   passenden Abgabeordner legen, `ingest.py` laufen lassen, betroffene Notizen fortschreiben.
4. `Wissen_Informationsvisualisierung/00 Start/Start.md` — nur den Abschnitt „Aktueller Stand“ fortschreiben.
5. Board: erledigte Karten abhaken; wer eine Karte nach `Doing` zieht, lässt sie dort.

## Harte Regeln

- **Keine erfundenen Angaben.** Fristen, Seitenzahlen, Wortlimits und Messwerte nur mit
  Belegstelle (Dokument, Folie, Aufgabe). Unklares wird als `Status: zu klären` markiert.
- **Keine Zahlen ohne Quelle.** Wo eine Zahl fehlt, steht eine Lücke, kein Schätzwert.
  Widersprüche zwischen Dokumenten (3–6 gegen 5–10 Minuten; Kapitel 5 gegen 6) werden als
  Widerspruch notiert, nicht aufgelöst.
- **Trennung von Befund und Meinung.** Empfehlungen gehören in
  `Entscheidungen.md` / `Offene Entscheidungen.md`, nicht in die Sitzungsnotizen.
- **Keine Zugangsdaten oder Tokens** in den Vault schreiben. Keine Matrikelnummer in
  handgeschriebene Notizen tippen; sie steht in der Abgabedatei und auf dem Deckblatt.
- **Datenschutz bei Gruppenarbeit.** Namen, Kontaktdaten und Matrikelnummern anderer
  Personen gehören nicht in den Vault und nicht ins Repository. Der Gruppenteil wird mit
  Kennungen geführt, solange keine Zustimmung vorliegt.
- **Fremde Dateien kennzeichnen.** `Visual 3. Semester/informationsvisualisierung_einstiegsseite.tex`
  ist eine Vorlage mit erfundenen Beispieldaten, nicht die eigene Abgabe. Die eigene Datei
  ist `Do_Trung_*_Einstiegsseite.tex`.
- **Sprache:** Vault-Inhalte auf Deutsch (direkt in Abgaben und Portfolio übernehmbar).
  Chat-Antworten an die Person auf Vietnamesisch, mit deutschen Fachbegriffen.
- **Keine Bot- oder Werkzeug-Attribution in Commits.** Keine `Co-Authored-By:`-Zeile, kein
  „Generated with …“, keine Trailer. Die Commit-Message endet mit ihrem letzten inhaltlichen
  Satz. Commit-Messages auf Deutsch: eine Zeile Zusammenfassung, darunter Stichpunkte. Push
  nur, wenn die Person es verlangt.

## Automatik

`Wissen_Informationsvisualisierung/_tools/daily.sh` ruft `ingest.py`, `board_sync.py` und `discord_notify.py`. Der
geplante Lauf ist **GitHub Actions** (`.github/workflows/tageslauf.yml`, 08:00
Europe/Berlin). Ein lokaler LaunchAgent liegt nur als Datei bei und wird nicht installiert;
zwei Scheduler am selben Tag würden zwei Discord-Berichte erzeugen.

Das Skript schreibt nur:

- `Wissen_Informationsvisualisierung/…(Quelle).md`, `Wissen_Informationsvisualisierung/90 Anhänge/`, `Wissen_Informationsvisualisierung/40 Portfolio/Abgaben/`
- `Wissen_Informationsvisualisierung/10 Kurs/Abgaben (auto).md`
- `Wissen_Informationsvisualisierung/00 Start/Ingest Log.md`, `Neu seit letztem Lauf.md`
- den Block zwischen `<!-- AUTO:START -->` und `<!-- AUTO:END -->` in `Status.md`
- Statusvermerke am Zeilenende der Board-Karten
- optional einen kurzen Discord-Bericht; der Webhook liegt unter
  `~/.config/informationsvisualisierung/discord-webhook` (Rückfall:
  `~/.config/projektplanung/discord-webhook`), nie im Vault.

Handgeschriebene Notizen werden nie überschrieben. Ohne Änderung schreibt der Lauf nichts.
`#person`- und `#team`-Karten werden **nie** automatisch abgehakt, nur mit Belegstand und
Überfälligkeit versehen; nur `#auto`-Karten wandern bei vorhandenem Beleg nach `Done`.
