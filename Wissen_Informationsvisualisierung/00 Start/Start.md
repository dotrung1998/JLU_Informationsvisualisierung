---
titel: Start
stand: 2026-11-25
status: aktiv
---

# Start — Informationsvisualisierung

> **Bắt đầu ở đây (VI):** Đọc theo thứ tự [[Điểm vào (VI)]] → [[Status]] → [[Board]] →
> [[Offene Entscheidungen]]. Việc gấp: **bài tập U01–U14 (Prüfungsvorleistung)** chọn và
> trình bày, **trang 2 (Einstiegsseite)** phải vào portfolio 1:1, **31.03.2027** nộp
> portfolio + code, **09.–10.04.2027** Blockseminar.

## Sitzungsbeginn

Vor dem ersten Lesen und Schreiben den Arbeitsstand auf den aktuellen `main` bringen:

```bash
bash Wissen_Informationsvisualisierung/_tools/sync_pull.sh
```

Das Skript holt `main` und spult nur per Fast-Forward vor. Es committet, pusht und stasht
nichts: Ein unsauberes Arbeitsverzeichnis bricht mit Exit 2 ab, eigene Commits daneben mit
Exit 4 — dann entscheidet die Person, nicht das Skript. Meldet der Cloud-Workspace einen
Fetch-Fehler, den Fetch über die Git-Integration ausführen und danach
`sync_pull.sh --no-fetch` aufrufen. Danach die Pflichtschritte aus `AGENTS.md`
(`ingest.py`, `board_sync.py`, „Neu seit letztem Lauf“).

## Worum es geht

Vorlesung *Informationsvisualisierung* von Prof. Sangam Chatterjee, Ph.D. (I. Physikalisches
Institut, JLU Gießen), Modul 07-BDS-15 / 07-MDS-06 / 07-MDA-11, WiSe 2026/27
([[Modulrahmen]]). Vorlesung wöchentlich plus VOD, Übungen mit Abgabe alle zwei Wochen,
keine Aufzeichnung erlaubt (§24 Abs. 2 AllB).

**Prüfungsvorleistung.** Eine Übungsaufgabe (U01–U14) in 3–6 Minuten vorstellen, entweder
als Video oder im Hörsaal ([[Prüfungsvorleistung]]).
**Modulprüfung.** Ein **e-Portfolio mit 5–10 Seiten und Programmcode**, Bearbeitungszeit
zehn Wochen ([[Portfolio-Vorgaben]]). Jede Person reicht ein eigenes Portfolio ein; der
gemeinsame Gruppenteil muss in allen Portfolios der Gruppe identisch sein.

## Aktueller Stand

- 12.10./14.10.2026: Auftakt mit der Projektion vom 12.10.; Erwartungsabfrage, Ablauf,
  Prüfungsformen ([[Kapitel 00 Organisatorisches]], [[Kapitel 01 Einleitung und Motivation]]).
- Bis 25.10.2026: **Einstiegsseite** über Stud.IP abzugeben (Handout S. 1). Die Datei
  `Do_Trung_*_Einstiegsseite.tex` mit zwei fotografierten Handskizzen liegt im Ordner
  `Visual 3. Semester/`; **ein Abgabenachweis fehlt** und es liegt keine PDF daneben
  ([[Einstiegsseite]]).
- 15.11.2026: Übungsaufgaben zu Kapitel 1–5 (U01–U14) im Lernportal, je Aufgabe eine
  Variante A und B ([[Prüfungsvorleistung]]).
- 18.11.2026: Vorlesungsfolien Kapitel 00–08 als Gesamtdokument (320 Folien)
  ([[Vorlesungsplan]]).
- 19.11.2026: Arbeitsfassung **Kapitel 5 Graphen und Netzwerke** v1.7.1; die
  Kapitelnummer weicht von den Gesamtfolien ab (dort Kapitel 6)
  ([[Kapitel 06 Graphen und Netzwerke]], [[Offene Entscheidungen]]).
- 22.11.2026: Gedächtnis und Automatik eingerichtet — dieser Vault, `ingest.py`,
  `board_sync.py`, GitHub Actions und Discord-Bericht, nach dem Muster des
  Schwesterprojekts `../Projektplanung` ([[Entscheidungen]]).
- 23.11.2026: U02 (Lie Factor) als Entwurf gerechnet und gezeichnet: Lie Factor 5,00 für
den Balken mit Basis 40, 2,20 für das flächenskalierte Piktogramm, Fassung C mit Achse ab 0
([[U02 Lie Factor]]). Nichts abgegeben, Termin offen.
- 23.11.2026: Einstiegsseite abgeschlossen. Die Abgabe am 25.10.2026 ist laut Angabe der
  Person erfolgt, die PDF wurde mit `tectonic` gesetzt (eine Seite A4, „Wortzahl: 119/120“,
  beide Fotos eingebettet) und liegt neben der `.tex` ([[Einstiegsseite]]). Nächster Schritt
  ist die Wahl der Übungsaufgabe ([[Prüfungsvorleistung]]).
- 22.11.2026: Vault-Ordner von `Wissen/` in `Wissen_Informationsvisualisierung/`
  umbenannt; Skripte, Hooks, Workflows und `AGENTS.md` folgen dem neuen Pfad
  ([[Entscheidungen]]).
- 24.11.2026: Der Discord-Bericht ist ausgebaut. Er kommt als zwei Nachrichten: ein Bericht
  mit allen Fristen, jeder offenen Board-Karte, der nächsten Aktion, den offenen
  Entscheidungen und dem Quellenstand, danach eine Kopiervorlage mit allen Aufgaben in einem
  einzigen Code-Block (ein Klick kopiert alles) ([[Entscheidungen]]). Testlauf gegen den
  vorhandenen Webhook: HTTP 204 für beide Nachrichten.
- 24.11.2026: **Lernserver** `Wissen_Informationsvisualisierung/00 Start/lernserver.html`
  angelegt: 17 Kanäle, 108 Nachrichten, Suche über alle Kanäle (Strg K), Merkliste,
  Lernstand, 20-Fragen-Quiz, Lie-Factor-Rechner, Filter-Explorer K–P, Farb- und
  Histogramm-Demo. Quellenangabe je Nachricht; Widersprüche (3–6/5–10 Minuten,
  Kapitel 5/6) markiert; Inhalte deutsch, kurze vietnamesische Hinweise je Kapitel
  ([[Entscheidungen]]).
- 25.11.2026: `sync_pull.sh` angelegt: holt am Sitzungsbeginn `main` und spult nur per
  Fast-Forward vor, damit der Cloud-Workspace nicht auf einem alten Stand arbeitet
  ([[Entscheidungen]]).
- 25.11.2026: Lernserver: jede der 108 Nachrichten hat drei wischbare Seiten — Deutsch,
  vietnamesische Skizze, vietnamesische Übersetzung; die Übersetzungen liegen im JSON-Block
  `#viData` derselben Datei, die Zeichnung wird aus den Stichpunkten erzeugt
  ([[Entscheidungen]]).
- 25.11.2026: Seite 2 zeichnet jede Nachricht aus ihrem eigenen Inhalt (Tabelle, Formel,
  Liste, Datum, Prozent) statt aus einem Kanalmotiv; das grüne Lesehäkchen im Kanalbaum
  lässt sich per Klick zurücksetzen ([[Entscheidungen]]).
- 25.11.2026: Seite 2 ist auf dem Telefon lesbar: responsives HTML-Raster mit 13,5–15 px
  statt fester SVG-Breite, Tabellen als Zeilenkarten; bei 390 px geprüft, 108 Bilder ohne
  Überlauf und ohne Dubletten ([[Entscheidungen]]).
- 25.11.2026: **Lernserver** weitergebaut: Seite 2 trägt je Nachricht einen eigenen Graphen
  (108 Titel, 21 Motivtypen, Daten nur aus der Nachricht), der Kanalbaum ist auf dem Telefon
  per X, Hintergrund und Escape schließbar, und GitHub Actions schreibt `gh-pages` bei jeder
  Änderung von `lernserver.html` auf `main` fort ([[Entscheidungen]]).
- **Offen:** Termine der Übungsabgaben, Termin der eigenen Präsentation, Zeitpunkt der
  Gruppeneinteilung, Wahl der Aufgabe und der Variante ([[Offene Entscheidungen]]).

## Landkarte

| Notiz | Inhalt |
|---|---|
| [[Điểm vào (VI)]] | định hướng nhanh bằng tiếng Việt: việc gấp, hạn, việc của bạn |
| [[Theo dõi dự án (VI)]] | giải thích chi tiết bằng tiếng Việt: portfolio, tiêu chí, việc của Trung |
| `dashboard.html` | bản tương tác: đếm ngược, checklist, Wortzähler, Lie-Factor |
| [[Status]] | Fristen, nächste Aktion, Stand je Person |
| [[Board]] | Kanban mit Belegen, Überfälligkeit wird nachgeführt |
| [[Entscheidungen]] | datiertes Protokoll inkl. verworfener Alternative |
| [[Offene Entscheidungen]] | was noch entschieden werden muss, mit Empfehlung |
| [[Personen]] | Dozent und eigene Rolle; Gruppe noch nicht eingeteilt |
| [[Modulrahmen]] | Modulnummern, Prüfungsformen, Qualifikationsziele, Literatur |
| [[Portfolio-Vorgaben]] | Aufbau, Wortlimits, Quellen, KI-Offenlegung, Blockseminar |
| [[Vorlesungsplan]] | Kapitel 0–8 mit Inhalt und Folienstand |
| [[Prüfungsvorleistung]] | U01–U14, Kriterien, Dateien, Datenbestand Räume K–P |
| [[Abgaben (auto)]] | welche Datei in welchem Abgabeordner liegt (automatisch) |
| [[Kapitel 00 Organisatorisches]] … [[Kapitel 08 Zeitbasierte Daten]] | was gelehrt wurde und was davon ins Portfolio gehört |
| [[Gruppenarbeit]] | Anforderungen an den gemeinsamen Gruppenteil und die Folien |
| [[Beispieldatensatz Bibliothek]] | fiktive Bibliotheksdaten und ihre Fallen |
| [[Offene Punkte]] | Fragen an Lehrende und Gruppe |
| [[Portfolio Trung]] | eigener Portfolio-Stand je Seite |
| [[Einstiegsseite]] | Seite 2: Handskizzen, Text, Wortzahl |
| [[Anhang-Checkliste]] | Programmcode, Quellen, KI-Offenlegung, Wortzahlen |
| [[Schreibregeln für .tex-Abgaben]] | Satz, Layout, Kompilieren |
| [[Projektplan]] | Zeitachse 25.10.2026 bis 10.04.2027 |
| [[Risiken]] | was schiefgehen kann und was dann passiert |

## Arbeitsrhythmus

Nach jeder Vorlesung: `ingest.py` laufen lassen (neue Folien oder Übungsblätter einlesen),
`Status.md` fortschreiben, eine Entscheidung oder einen Befund in `Entscheidungen.md`,
Board abhaken. Vor jeder Abgabe: `Abgaben (auto)` prüfen, ob die eigene Datei im richtigen
Ordner liegt und eine PDF ist.

Der Vault ist das Gedächtnis, die Abgabe in Stud.IP ist die Leistung. Beides getrennt halten.
