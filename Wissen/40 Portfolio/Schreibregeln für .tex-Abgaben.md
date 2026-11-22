---
titel: Schreibregeln für .tex-Abgaben
stand: 2026-11-22
---

# Schreibregeln für .tex-Abgaben

Gilt für alle eigenen Dateien (Trung). Beleg: die vorhandene Einstiegsseite
`Visual 3. Semester/Do_Trung_*_Einstiegsseite.tex`, die bereits so aufgebaut ist.

## Zeichensetzung

- **Kein Semikolon** im Fließtext. Statt `;` ein Punkt oder ein Komma.
- **Kein Gedankenstrich als Satzzeichen** im Fließtext. Stattdessen Punkt oder Komma;
  Bindestriche in Komposita bleiben (`Strich-Kreis-Diagramm`).
- `--` nur in Überschriften und in der Titelzeile.
- `\enquote{…}` statt `"…"`.
- Zahlen mit Einheit und Quelle nennen, keine gerundete Zahl ohne Beleg.

## Aufbau (pdfLaTeX)

Preamble wie in der Einstiegsseite:

```latex
\documentclass[a4paper,10pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[ngerman]{babel}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{enumitem}
\usepackage{xcolor}
\usepackage{csquotes}
\usepackage{float}
\usepackage{titlesec}
\geometry{a4paper, left=1.2cm, right=1.2cm, top=1.2cm, bottom=1.2cm}
\setlength{\parindent}{0pt}
\setlength{\parskip}{2pt}
\setlist[itemize]{nosep, leftmargin=*, topsep=0pt, parsep=0pt}
\titlespacing*{\section}{0pt}{4pt}{2pt}
\titleformat{\section}{\normalfont\large\bfseries}{\thesection}{1em}{}
```

Titelblock:

```latex
\begin{center}
\textbf{\large Informationsvisualisierung} \\
\small Einstiegsseite -- Handskizze und Erwartungen, WiSe 2026/27 \\
\textbf{Trung Do} | Matrikelnummer: siehe Deckblatt
\end{center}
\vspace{-3mm}
\noindent\rule{\textwidth}{0.3pt}
```

Danach `\section*{Teil A -- …}` und `\section*{Teil B -- …}`. **Kein `fontspec`** in der
Abgabedatei.

## Länge und Layout

- Eine Seite ist das Ziel. Für das Portfolio zählt jede Seite; was nicht auf die Seite passt,
  gehört nicht hinein.
- Wenn es nicht passt, in dieser Reihenfolge: Sätze straffen, `\parskip` senken,
  `\titlespacing` senken, zuletzt `\fontsize{9}{10.5}\selectfont`.
- Wortzahl im Dokument als Makro führen (`\newcommand{\Wortzahl}{119}`) und im Text als
  `Wortzahl: \Wortzahl/120` ausgeben. Nach jeder Textänderung neu zählen.

## Bilder

- Fotos im selben Ordner wie die `.tex`-Datei ablegen; `\IfFileExists{…}` zeigt sonst einen
  roten Platzhalter statt eines Fehlers.
- Breite über `\linewidth`, Höhe über `\textheight` begrenzen, `keepaspectratio` setzen.
- Bildunterschrift **unter** dem Bild, im Portfolio nummeriert.

## Kompilieren

- **Lokal:** `tectonic` (XeTeX) ist installiert; die Einstiegsseite setzt damit ß korrekt,
  weil sie `fontspec` nicht verwendet.
- **Für die Abgabe:** pdfLaTeX (z. B. texpage.com), weil `inputenc` + `T1` dort der Standard
  sind. Die PDF aus dem Ordner muss aus der eingereichten `.tex` erzeugbar sein.
- Prüfen: Seitenzahl, keine `Overfull`-Warnung, alle Bilder vorhanden, Wortzahl korrekt.

## Zahlen und Quellen

- Keine Zahl ohne Quelle; jede Grafik mit Datenquelle in der Fußnote.
- Die Datenbestände stehen in [[Beispieldatensatz Bibliothek]] und
  [[Prüfungsvorleistung]]; KI-Hilfe beim Code wird in der Fußnote genannt.
