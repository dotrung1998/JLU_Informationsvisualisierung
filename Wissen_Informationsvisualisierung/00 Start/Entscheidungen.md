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

## 2026-11-23 — Einstiegsseite gilt als abgegeben, PDF mit `tectonic` gesetzt

**Entscheidung.** Die Einstiegsseite gilt als am 25.10.2026 über Stud.IP eingereicht. Beleg
ist die Angabe der einreichenden Person in der Sitzung vom 23.11.2026; eine Quittung aus
Stud.IP liegt nicht im Projekt. Aus `Do_Trung_8229831_Einstiegsseite.tex` wurde mit
`tectonic` eine PDF erzeugt und neben der Quelle abgelegt
(`Visual 3. Semester/Do_Trung_8229831_Einstiegsseite.pdf`).

**Grund.** Die Frage „abgegeben oder nicht“ stand seit dem 22.11. als offene Entscheidung
und blockierte die Planung der Pflichtseite 2. Die Person hat sie beantwortet; ohne diese
Festlegung beginnt jede Sitzung mit derselben Rückfrage. Die PDF war die letzte fehlende
Datei zu einer bereits abgegebenen Seite und wird für das 1:1-Übernehmen ins Portfolio
gebraucht. `tectonic` ist lokal installiert und kompiliert die Datei mit beiden Fotos ohne
Nacharbeit. Geprüft: eine Seite A4, beide Fotos eingebettet, kein Platzhalter, Wortzahlzeile
„119/120“.

**Verworfen.** Auf die Stud.IP-Quittung warten und die Seite weiter als unbestätigt führen
(blockiert die Planung ohne Erkenntnisgewinn); die PDF über texpage.com setzen (kein lokaler
Beleg, zusätzlicher Arbeitsschritt); die `.tex` vor dem Setzen noch glätten (verletzt die
Vorgabe „unverändert 1:1“).

## 2026-11-23 — Literales „ß“ in `.tex` durch `\ss{}` ersetzen

**Entscheidung.** In eigenen `.tex`-Dateien wird kein literales „ß“ mehr geschrieben,
sondern `\ss{}`. Die Regel steht in [[Schreibregeln für .tex-Abgaben]].

**Grund.** `tectonic` (XeTeX mit `inputenc` und `T1`) setzt das Zeichen in jedem Schnitt als
zwei Großbuchstaben „SS“: „größer“ wurde zu „größSer“. Ein Minimalbeispiel mit demselben
Präambel wie die Abgaben zeigt den Fehler für aufrechten, kursiven, fetten und kleinen Satz
und zeigt gleichzeitig, dass `\ss{}` richtig gesetzt wird. Die Schreibregeln empfehlen
`tectonic` namentlich, deshalb ist das kein Einzelfall, sondern betrifft jede künftige Datei.

**Verworfen.** Auf pdfLaTeX (texpage.com) für die Arbeitsfassungen umstellen (kein lokaler
Lauf, jeder Zwischenstand wäre ein Upload); `fontspec` mit einer Systemschrift laden (die
Schreibregeln schließen `fontspec` in der Abgabedatei aus, und die Vorschau soll dieselbe
Kette nutzen wie die Abgabe); das ß umschreiben („groesser“ wäre eine falsche Schreibweise
im abgegebenen Text).

## 2026-11-23 — U02 als Übungsaufgabe vorbereitet, Variante A

**Entscheidung.** Für die Prüfungsvorleistung wird **U02 „Eine Übertreibung messen und
beheben“** in **Variante A** vorbereitet (Werte 50 und 60, Basis 40, Piktogrammfaktor 1,2).
Der Entwurf liegt als `U02_Lie_Factor_Entwurf.tex` und `.pdf` in `Prüfungsvorleistung/`
([[U02 Lie Factor]]). Nichts ist abgegeben, die Wahl ist noch bestätigbar.

**Grund.** Die Aufgabe braucht nur zwei Wertepaare und eine korrigierte Fassung, deckt aber
alle drei Bewertungskriterien des Übungsblatts in einem Zug ab: Die abgeschnittene Basis und
die Flächenskalierung sind zwei verschiedene Fehlerbilder, der Lie Factor beziffert beide,
und Fassung C zeigt die Korrektur. Die Zahlen sind mit dem Übungsblatt belegt, die
Begründung stützt sich auf Kapitel 2 der Vorlesung.

**Verworfen.** U05 „Treffer sichtbar machen“ (näher an der eigenen Bibliotheksskizze, aber
mehr Zeichenarbeit und eine Präattentiv-Diskussion ohne belastbaren Messwert); U09
(Fehlerbalken, mehr Rechnung bei gleicher Vortragszeit); eine Aufgabe aus Kapitel 1 ohne
Bezug zu den Kriterien aus Kapitel 2 und 3.

## 2026-11-23 — Variante A bleibt, KI-Offenlegung erweitert

**Entscheidung.** U02 bleibt bei **Variante A** (50 und 60, Basis 40, Piktogrammfaktor 1,2),
kein Wechsel auf B. Die Fußnote des Entwurfs nennt seit demselben Tag drei Arbeitsschritte
als KI-gestützt: Rechnung, Formulierung der Begründung und LaTeX-/TikZ-Code; die
Verantwortung für die Richtigkeit bleibt bei der einreichenden Person.

**Grund.** Die Person hat Variante A bestätigt. Die alte Fußnote deckte nur den Satz ab,
obwohl Rechnung und Begründung ebenfalls mit dem Assistenten entstanden sind. Das Handout
verlangt die Kennzeichnung der Arbeitsschritte, nicht nur des Codes.

**Verworfen.** Wechsel auf Variante B (Lie Factor 8,00 statt 5,00, aber eine neue Zeichnung
und kein zusätzlicher Erkenntnisgewinn für den Vortrag); die Fußnote im alten Wortlaut
lassen (unvollständige Offenlegung).

## 2026-11-24 — Discord-Bericht trägt die Aufgaben selbst, Kopiervorlage in einem Block

**Entscheidung.** `discord_notify.py` sendet zwei Nachrichten je Lauf.

1. **Bericht.** Kopf mit Zählern (Karten erledigt/offen/in Arbeit, Fristen bis sieben Tage,
   Quellen) und Warnungen (überfällig, Quelle ohne Abdeckung, Ordner ohne Frist); alle
   Fristen aus `fristen.json` mit Datum, Abstand und Zuständigkeit; jede offene Board-Karte
   aus `To Do` und `Doing` mit Kennung, Titel, Tag, Frist, Belegstand, Kurzbeschreibung und
   Zielnotiz; die Abschnitte „Nächste Aktion“ und „Zu klären“ aus [[Status]]; die offenen
   Punkte aus [[Offene Entscheidungen]] mit dem, was sie blockieren; der Quellenstand des
   letzten Laufs.
2. **Kopiervorlage.** Alle Aufgaben als `- [ ]`-Zeilen — Fristen, offene Karten, nächste
   Schritte, offene Fragen, Abgabeordner — in **genau einem** Code-Block. Ein Klick auf das
   Kopiersymbol kopiert den vollständigen Text.

**Grund.** Vorgabe der bearbeitenden Person in der Sitzung vom 24.11.2026: der Bericht soll
so ausführlich sein, dass die Arbeit allein aus Discord erledigt werden kann, und alles
Kopierbare soll in einem Block stehen. Discord begrenzt `content` plus Embeds gemeinsam auf
6000 Zeichen; Bericht (3927) und Kopiervorlage (4032) passen deshalb nur als zwei Nachrichten
vollständig hinein. Die Kopiervorlage bliebe in einer Nachricht bei rund 4000 Zeichen
abgeschnitten. Alle Angaben stammen unverändert aus `fristen.json`, [[Board]], [[Status]],
[[Offene Entscheidungen]] und `abdeckung.json`; fehlt eine Angabe, bleibt die Lücke stehen.

**Verworfen.** Eine einzige Nachricht (die Kopiervorlage würde am Zeichenlimit abgeschnitten,
zuletzt fiel der Abschnitt „Belege/Ordner“ weg); mehrere kleine Code-Blöcke je Abschnitt
(mehrere Kopierknöpfe statt einem); die Kopiervorlage auf eine Kurzfassung kürzen (dann
fehlen in Discord genau die Angaben, die die Nachricht ersetzt).

**Nebenfolge.** Die Datei weicht damit bewusst von der Kopie im Schwesterprojekt ab
(Entscheidung vom 22.11.2026: Werkzeuge gleich halten). Der Bericht dort bleibt unverändert,
bis er dort ebenfalls gebraucht wird.

## 2026-11-24 — Lernserver als eine HTML-Datei in `00 Start/`

**Entscheidung.** Der Stoff liegt zusätzlich als interaktive Lernfassung in
`Wissen_Informationsvisualisierung/00 Start/lernserver.html`: 17 Kanäle in der Form eines
Discord-Servers, 108 Nachrichten, Suche über alle Kanäle (Strg K), Merkliste, Lernstand,
20-Fragen-Quiz, Lie-Factor-Rechner, Filter-Explorer für Räume K–P, Farb- und
Histogramm-Demo. Inhalte aus Gesamtfolien (18.11.2026), Übungsblatt (15.11.2026), Handout
und Arbeitsfassung Kapitel 5 (19.11.2026); jede inhaltliche Nachricht nennt ihre Quelle.
Widersprüche (3–6 gegen 5–10 Minuten, Kapitel 5 Interaktion gegen Graphen) bleiben
markiert. Eine einzelne Datei ohne externe Bibliotheken, ohne Build und ohne Server.

**Grund.** Der Stoff liegt über 320 Folien und 17 Übungsseiten verstreut; zum Nachschlagen
vor dem U02-Vortrag und für den Gruppenteil braucht es eine durchsuchbare Fassung mit
Quellenangabe. Eine einzelne HTML-Datei läuft offline im Browser und bleibt neben
`dashboard.html`, das weiterhin nur Fristen, Checkliste und Wortzähler führt.

**Verworfen.** `dashboard.html` erweitern (mischt Fristen-Cockpit und Stoff, macht beide
unübersichtlich); nur Markdown-Notizen im Vault (keine Suche, keine Interaktion); Wiki oder
Notion (zweiter Ort neben dem Vault, kein Bezug zu den Dateien).

## 2026-11-24 — Lernserver: Spoiler per Tastatur, Bibliotheksvergleich ergänzt

**Entscheidung.** `lernserver.html` öffnet Spoiler zusätzlich mit Enter und Leertaste
(eigener `keydown`-Handler). Die Bibliotheksnachricht in Kapitel 2 nennt den Unterschied
zwischen Mittwoch (96) und Freitag (62) um 16:00 ausdrücklich: 34 Plätze, gültig für diesen
Zeitpunkt.

**Grund.** Die Prüfung des Blobs aus `origin/main` zeigte zwei Lücken: Der Spoiler war mit
`tabindex="0"` fokussierbar, ließ sich aber nur per Klick öffnen; die Kapitel-2-Notiz nennt
den 34-Plätze-Vergleich, die Nachricht zeigte nur die Tabelle. Beides ist ohne neue Quelle
behebbar (96 − 62 = 34).

**Verworfen.** Spoiler als `<button>` umbauen (größerer Eingriff in Textfluss und Layout);
den 34-Plätze-Satz weglassen (dann fehlt der im Quellenstand notierte Vergleich).
## 2026-11-25 — `sync_pull.sh` statt Pull in `daily.sh`

**Entscheidung.** Ein eigenes Skript `Wissen_Informationsvisualisierung/_tools/sync_pull.sh`
bringt den Arbeitsstand am Sitzungsbeginn auf `main`: `git fetch origin main`, danach
`git merge --ff-only FETCH_HEAD`. Es committet, pusht und stasht nichts. Ein unsauberes
Arbeitsverzeichnis bricht mit Exit 2 ab, eigene Commits daneben mit Exit 4. `--no-fetch`
vergleicht gegen einen bereits geholten Stand (Cloud-Workspace: Fetch über die
Git-Integration). `daily.sh` bleibt unverändert.

**Grund.** Der Cloud-Workspace arbeitet in einem eigenen Klon und sieht einen Push auf
`main` erst nach einem Fetch; ohne den Schritt wird auf einem alten Stand gelesen und
geschrieben. Der Vergleich läuft über `FETCH_HEAD`, weil dieses Repository beim Fetch kein
`origin/main`-Ref schreibt (geprüft am 25.11.2026: `git fetch origin main` lässt `origin/main`
fehlen und schreibt nur `FETCH_HEAD`).

**Verworfen.** Den Pull in `daily.sh` einbauen (der Lauf startet in GitHub Actions auf einem
losen HEAD aus `actions/checkout`; ein Merge dort bricht den Tageslauf ab, auf dem Mac würde
er ohne Zutun der Person mergen); `git pull` ohne `--ff-only` (könnte einen eigenen Stand
zusammenführen, statt ihn zu melden); automatisches Stashen (versteckt unfertige Arbeit).
