# Obsidian-Vault: Informationsvisualisierung

Dieser Ordner **ist** der Vault. Öffnen mit Obsidian → „Ordner als Vault öffnen“ →
`Wissen_Informationsvisualisierung/` auswählen. Alles ist reines Markdown mit Wikilinks; das Kanban-Plugin für
[[Board]] liegt unter `Wissen_Informationsvisualisierung/.obsidian/plugins/obsidian-kanban`.

## Aufbau

```
00 Start/       Start, Status, Board, Entscheidungen, offene Entscheidungen, Personen,
                vietnamesische Ansichten, dashboard.html
10 Kurs/        Modulrahmen, Portfolio-Vorgaben, Vorlesungsplan, Prüfungsvorleistung,
                Abgabenstand (auto)
20 Vorlesungen/ Kapitel 00–08: was gelehrt wurde und was davon ins Portfolio gehört
30 Gruppe/      Gruppenarbeit, Beispieldatensatz, offene Punkte
40 Portfolio/   eigenes Portfolio, Einstiegsseite, Anhang-Checkliste, Schreibregeln
50 Plan/        Projektplan, Risiken
90 Anhänge/     automatisch kopierte PDFs, Fotos und Abgaben
_tools/         ingest.py, board_sync.py, daily.sh, daily_guard.sh, discord_notify.py
```

## Einstieg

[[Start]] → [[Status]] → [[Offene Entscheidungen]]

Vietnamesische Leseansicht: [[Điểm vào (VI)]] (kurz) und [[Theo dõi dự án (VI)]]
(ausführlich); interaktives Tracking im Browser: `00 Start/dashboard.html`.

## Wenn etwas Neues dazukommt

1. Datei in den passenden Quellordner legen: neues Kursmaterial nach `00_Materialien/`,
   eigene Abgaben nach `Prüfungsvorleistung/` bzw. `e-Portfolio/…`.
2. Im Projektordner ausführen:

```bash
python3 Wissen_Informationsvisualisierung/_tools/daily.sh
```

3. `00 Start/Neu seit letztem Lauf.md` lesen — dort steht, was neu oder geändert ist.
4. Betroffene Notizen fortschreiben.

Der Ingest überschreibt **nur** `(Quelle)`-Notizen, `90 Anhänge/`,
`40 Portfolio/Abgaben/` und `10 Kurs/Abgaben (auto).md`.
Alle handgeschriebenen Notizen bleiben unberührt.

## Automatik

`_tools/daily.sh` ruft `ingest.py`, `board_sync.py` und `discord_notify.py` auf und schreibt
ein Protokoll nach `_tools/daily.log`. Der geplante Lauf ist **GitHub Actions**
(`.github/workflows/tageslauf.yml`, 08:00 Europe/Berlin, Secret `DISCORD_WEBHOOK`).

Ein lokaler LaunchAgent liegt nur als Datei bei (`_tools/com.infovis.daily.plist`). Wer ihn
stattdessen installieren will:

```bash
cp Wissen_Informationsvisualisierung/_tools/com.infovis.daily.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.infovis.daily.plist
```

Dann aber den Cron in `tageslauf.yml` entfernen — **zwei Scheduler am selben Tag erzeugen
zwei Discord-Berichte** ([[Entscheidungen]]).

Ohne Änderung schreibt kein Lauf etwas. Handgeschriebene Notizen bleiben unangetastet.

## Abdeckung der Quellen

Jede Datei in `00_Materialien/`, in den Abgabeordnern und im Projektordner muss genau einen
Zustand haben: eine automatische `(Quelle)`-Notiz, eine Beschreibung in einer
handgeschriebenen Notiz oder ein begründeter Ausschluss in `_tools/abdeckung-regeln.json`.
Der Lauf zählt alle drei Fälle und meldet **unbekannte** Dateien mit Pfad; gibt es welche,
endet `ingest.py` mit Fehlercode 1. Das Ergebnis steht in `00 Start/Neu seit letztem Lauf.md`
und in `_tools/abdeckung.json`. Wer eine Datei bewusst nicht einlesen will, trägt sie mit
einem Satz Grund in `abdeckung-regeln.json` ein — stilles Überspringen gibt es nicht.
