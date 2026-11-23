---
titel: Entscheidungen
stand: 2026-11-23
---

# Entscheidungen

Nur ergänzen, nie rückwirkend umschreiben. Jede Zeile: Datum, Entscheidung, Grund,
verworfene Alternative.

## 2026-11-22 — Gedächtnis liegt im Projektordner, eigener Vault

**Entscheidung.** Der Kursordner `Vorlesung_mit_Übung_07-BDS-15__07-MDS-06__07-MDA-11_Informationsvisualisierung`
bekommt einen eigenen Obsidian-Vault `Wissen/` mit derselben Ordnung wie das
Schwesterprojekt `../Projektplanung`: `00 Start`, `10 Kurs`, `20 Vorlesungen`, `30 Gruppe`,
`40 Portfolio`, `50 Plan`, `90 Anhänge`, `_tools`. Die Quellen bleiben unverändert daneben
liegen.

**Grund.** Die Unterlagen kommen wöchentlich dazu (Folien, Übungsblätter, eigene Abgaben).
Ein zweiter Ort würde doppelt gepflegt und liefe auseinander. Die gleiche Ordnung macht die
beiden Kurse parallel lesbar: gleiche Dateinamen, gleiche Board-Konventionen, gleiche
Werkzeuge.

**Verworfen.** Eigene Struktur nur für diesen Kurs (zwei Gedächtnisformen, keine
Wiederverwendung der Skripte); Notion oder eine Tabelle als führender Ort (kein Bezug zu den
Dateien, zwei Stände).

## 2026-11-22 — Automatik und Werkzeuge aus dem Schwesterprojekt übernommen

**Entscheidung.** `ingest.py`, `board_sync.py`, `daily.sh`, `daily_guard.sh`,
`discord_notify.py` und `author_guard.py` sind Kopien der Skripte aus
`../Projektplanung`, angepasst nur an die Quellordner dieses Kurses. Der Ablauf bleibt:
einlesen → Abdeckung prüfen → Board und Fristenblock fortschreiben → Discord-Bericht.

**Grund.** Der Ablauf ist erprobt (dort seit dem 21.11. im Einsatz) und kursunabhängig: er
schreibt nur automatisch erzeugte Notizen, Anhänge und Statusblöcke. Eine Neuentwicklung
würde dieselben Fehler noch einmal machen.

**Verworfen.** Ein gemeinsames Repository für beide Kurse (die Abgaben und Fristen sind
getrennt, die Repositories bleiben getrennt); die Skripte nur zu verlinken (die Ordner
liegen in verschiedenen Repositories, ein Link würde beim Klonen brechen).

## 2026-11-22 — Kursmaterial nach `00_Materialien/`, Abgabeordner bleiben am Platz

**Entscheidung.** Die fünf PDFs und die Download-Liste liegen ab jetzt in
`00_Materialien/`. Die Ordner `Visual 3. Semester/`, `Prüfungsvorleistung/` und
`e-Portfolio/` bleiben unverändert am Projektort und werden als Abgabeordner eingelesen.

**Grund.** `00_Materialien/` ist im Schwesterprojekt der Ort für Kursmaterial; dort sucht
`ingest.py` zuerst. Die Abgabeordner haben ihre Namen aus dem Lernportal und werden von Hand
befüllt — sie umzubenennen würde die Ablage der Lehrenden und die eigene Gewohnheit
auseinanderbringen.

**Verworfen.** Alles in `00_Materialien/` verschieben (die Abgabeordner wären dann keine
Abgaben mehr); alles am Ort lassen (dann läge Kursmaterial neben eigenen Abgaben, und der
Ingest müsste raten, was was ist).

## 2026-11-22 — Nur belegte Termine im Fristenblock

**Entscheidung.** `_tools/fristen.json` enthält nur Termine, die in einem Dokument stehen:
Portfolio und Programmcode bis **31.03.2027**, Blockseminar **09./10.04.2027** (Handout
S. 1). Die Einstiegsseite (bis 25.10.2026) steht in der menschlichen Checkliste in
[[Status]] und in der Abgaben-Tabelle, nicht im automatischen Fristenblock. Termine für
Übungsabgaben, Präsentation und Gruppeneinteilung fehlen ganz, statt geschätzt zu werden.

**Grund.** Ein AUTO-Block, der jeden Tag „überfällig seit 28 Tagen“ für eine längst
abgegebene Seite zeigt, verliert seine Warnfunktion. Für die Übungen nennt kein Dokument ein
Datum: das Übungsblatt sagt nur „Abgabe alle 2 Wochen“, das Handout „Bearbeitungszeit
2 Wochen“. Eine erfundene Frist wäre schlimmer als eine Lücke.

**Verworfen.** Alle Termine schätzen (Rhythmus „alle 2 Wochen“ ab Vorlesungsbeginn);
Einstiegsseite im AUTO-Block lassen (Dauerwarnung ohne Bedeutung).

## 2026-11-22 — GitHub Actions ist der Scheduler, kein launchd-Job

**Entscheidung.** Der geplante Tageslauf läuft ausschließlich auf GitHub Actions
(`.github/workflows/tageslauf.yml`, 08:00 Europe/Berlin). Der LaunchAgent liegt nur als
Datei `_tools/com.infovis.daily.plist` bei und wird **nicht** installiert.

**Grund.** Wie im Schwesterprojekt: zwei Scheduler am selben Tag erzeugen zwei
Discord-Berichte und konkurrierende Commits. Actions läuft auch, wenn der Mac aus ist.

**Verworfen.** launchd zusätzlich installieren (doppelte Berichte); nur lokal laufen
(kein Bericht bei geschlossenem Rechner).

## 2026-11-22 — Discord: eigener Webhook mit Rückfall auf den vorhandenen

**Entscheidung.** `discord_notify.py` liest zuerst `$DISCORD_WEBHOOK`, dann
`~/.config/informationsvisualisierung/discord-webhook`, zuletzt den vorhandenen Webhook
unter `~/.config/projektplanung/discord-webhook`. Im Repository liegt nur das Secret
`DISCORD_WEBHOOK`.

**Grund.** Der vorhandene Webhook funktioniert sofort; ein eigener Kanal für diesen Kurs
kann später ohne Codeänderung nachgezogen werden. Der Webhook selbst bleibt außerhalb des
Vaults und außerhalb des Repos.

**Verworfen.** Den Webhook in eine Datei im Projekt schreiben (Geheimnis im Repository);
einen neuen Kanal erzwingen, bevor einer existiert (der Bericht würde ausfallen).

## 2026-11-22 — Material wird wörtlich kopiert, Inhalt nicht geglättet

**Entscheidung.** `ingest.py` legt von jeder Quelle eine `(Quelle)`-Notiz mit dem
extrahierten Text an und kopiert die Datei nach `90 Anhänge/`. Handschriftliche Notizen
enthalten nur Einordnung, keine Korrektur der Quelle. Widersprüche zwischen Dokumenten
werden als Widerspruch notiert, nicht aufgelöst.

**Grund.** Die Prüfungsordnung und die Lehrenden sind die Quelle, nicht dieser Vault. Die
Regel „keine Zahl ohne Beleg“ verlangt, dass beide Fassungen sichtbar bleiben.

**Verworfen.** Widersprüche stillschweigend zu einer Fassung zusammenziehen (Belegstelle
wäre nicht mehr nachvollziehbar); Quellen nur verlinken (die Dateien würden beim Aufräumen
des Download-Ordners verloren gehen).

## 2026-11-22 — Vault-Ordner heißt `Wissen_Informationsvisualisierung/`

**Entscheidung.** Der Obsidian-Vault liegt ab jetzt in
`Wissen_Informationsvisualisierung/` statt in `Wissen/`. Alle Pfade im Repository wurden
mitgezogen: `AGENTS.md`, `.gitignore`, die Git-Hooks in `.githooks/`, die Workflows in
`.github/workflows/`, `README.md` im Vault sowie die Aufruf- und Hinweistexte in
`ingest.py`, `board_sync.py`, `author_guard.py`, `discord_notify.py` und
`com.infovis.daily.plist`. Die Skripte selbst bleiben ortsunabhängig, weil sie ihren
Wurzelordner aus `Path(__file__)` ableiten. Der ältere Eintrag oben bleibt wörtlich stehen;
sein Pfad `Wissen/` gilt nicht mehr.

**Grund.** Vorgabe der bearbeitenden Person in der Sitzung vom 22.11.2026: der Ordnername
soll den Kurs tragen, damit der Vault beim Arbeiten neben anderen Vaults eindeutig
zuzuordnen ist.

**Verworfen.** Den alten Ordnernamen behalten und nur in den Notizen umbenennen (die
Dateipfade würden auseinanderlaufen); eine zweite Kopie oder einen Symlink anlegen (zwei
Stände, die gepflegt werden müssten).

## 2026-11-23 — Commit-Sperre prüft Trailer und Bot-/Werkzeugnamen

**Entscheidung.** `author_guard.py` ist die einzige Quelle der Regeln und prüft jede
Commit-Nachricht auf Co-Authored-By- und verwandte Trailer-Zeilen (`generated with/by`,
`assisted by`, `AI-assisted`, `made with`, `powered by`), auf Bot- und Werkzeugnamen
(`codebuff`, `buffy`, `claude`, `anthropic`, `chatgpt`, `openai`, `copilot`, `codex`,
`aider`), auf `[bot]`, auf `noreply@anthropic.com` bzw. `noreply@openai.com` und auf das
Roboter-Emoji. Der Hook `.githooks/commit-msg` ruft das Skript mit `--message-file` und
`--config` auf und bricht den Commit bei einem Treffer mit Exit-Code 1 ab; derselbe Aufruf
prüft die Commits im Workflow `author-guard.yml`.

**Grund.** Die Regel „keine Bot- oder Werkzeug-Attribution in Commits“ aus `AGENTS.md` war
bisher nur eine Absprache. Der Hook macht sie lokal durchsetzbar, der Workflow deckt
Commits ab, die am Hook vorbei entstehen. Das einzelne Wort „Bot“ bleibt erlaubt, weil
`discord_notify.py` einen Discord-Bot anspricht und Commit-Texte dazu sonst fälschlich
scheitern würden.

**Verworfen.** Die Regeln zusätzlich im Hook duplizieren (zwei Listen, die auseinanderlaufen);
nur den Workflow prüfen (der Commit wäre schon geschrieben); jedes Vorkommen von „bot“
sperren (false positives beim Discord-Bot).
