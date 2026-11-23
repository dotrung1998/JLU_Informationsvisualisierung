---
titel: Kapitel 04 Multivariate Daten
kapitel: 4
stand: 2026-11-22
---

# Kapitel 04 — Visualisierung univariater bis multivariater Daten

Quelle: Gesamtfolien Kapitel 4 (PDF-Seiten 164–240); Übungsaufgaben U08–U12.

## Grundbegriffe

- **Data Table:** Zeilen = Fälle, Spalten = Variablen; die Tabelle ist die Vorstufe jeder
  Grafik.
- **Dimensionalität:** Zahl der Variablen pro Fall. Univariat (eine), bivariat (zwei),
  multivariat (mehr als zwei).
- **Ziele:** Zuordnung und Ziel sind nicht immer eindeutig — dieselbe Tabelle beantwortet
  verschiedene Fragen verschieden (das ist die Pointe von U03 und U11).

## Univariat und bivariat

- **Histogramm:** Häufigkeit pro Klasse. Die Klassenbreite entscheidet über den Eindruck;
  bei **ungleichen Klassen** muss die **Häufigkeitsdichte** (Häufigkeit ÷ Klassenbreite)
  gezeichnet werden, sonst wirkt die breite Klasse zu schwer (U08).
- **Boxplot:** Median, Quartile, Whisker; Ausreißer nach der 1,5-IQR-Regel.
- **Fehlerbalken:** ohne Angabe der Balkenart nicht interpretierbar — Standardabweichung,
  Standardfehler und Konfidenzintervall beantworten verschiedene Fragen (U09).
- **Zeitbasierte bivariate Daten:** Zeitserien.
- **Geografische bivariate Daten:** Fläche trägt den Anteil, Farbe eine zweite Variable.

## Multivariat

- **Streudiagramm-Matrix:** alle paarweisen Kombinationen; Muster und Ausreißer werden
  sichtbar, viele Panels erschweren das Lesen.
- **Geometrische Transformationen:** Projektionen der mehrdimensionalen Daten in zwei
  Dimensionen; **parallele Koordinaten** (Achsen nebeneinander, jeder Fall eine Linie) sind
  das Standardwerkzeug für viele Variablen — mit dem Nachteil, dass die Reihenfolge der
  Achsen das Bild verändert (U12).
- **Glyphen:** Star Glyphs (radiale Achsen), Chernoff-Gesichter, Strichmännchen; jede Glyphe
  ist ein Fall, die Form trägt mehrere Variablen. Vorteil: viele Variablen gleichzeitig;
  Nachteil: schwer zu vergleichen.
- **Pixelbasierte Techniken:** jeder Wert ein Pixel in fester Farbsequenz, Zeilen = Fälle;
  sehr dicht, aber ohne Achsen; Spirale für Zeitreihen (7 Börsenkurse über 10 Jahre).
- **Dimensionsreduzierung:** Projektion auf niedrigere Dimension, z. B. selbstorganisierte
  Karte (SOM) — Übersicht gewonnen, Details verloren.
- **Rank-by-Feature:** der Nutzer wählt ein Kriterium, das System sortiert die Projektionen;
  beginnt mit 1D-Histogrammen und statistischen Kennwerten.

## Zu große Datendichte (Clutter-Reduktion)

- **Sampling:** weniger Punkte zeigen, dafür ehrlich als Stichprobe benannt.
- **Magic Lens:** nur der Bereich unter der Linse wird detailliert.
- **Konstante Informationsdichte:** Auflösung so wählen, dass pro Fläche gleich viele Punkte
  liegen.
- **Punktverschiebung:** Überlappungen auflösen und Positionen möglichst wenig verändern.

## Übungen dazu

- **U08** Histogramm mit ungleichen Klassen → Häufigkeitsdichte, Boxplot, Rohwerte.
- **U09** Was zeigt der Fehlerbalken → drei beschriftete Felder je Stichprobe.
- **U10** Erfundener Nullpunkt im Streudiagramm → Pearson-Korrelation mit und ohne Punkt O,
  korrekt neu zeichnen, tragfähiger Titel (Matejka & Fitzmaurice 2017).
- **U11** Gesamtquote gegen Gruppenquoten → beide Ebenen und die Aufgabenmischung in einer
  Grafik (Simpson-Paradox).
- **U12** Drei Kriterien, eine Ansicht → parallele Koordinaten mit „besser oben“,
  Pareto-Menge der nicht übertroffenen Räume.

Daten in [[Prüfungsvorleistung]].

## Bezug zum Portfolio

Das Kapitel liefert die Diagrammtypen, aus denen die Gruppe ihre Beispiele auswählt, und die
Sprache für die Optimierung: Klassengrenzen, Achsenreihenfolge, Skalenart, Überlappung. Ein
Beispiel aus der eigenen Einstiegsseite (Strich-Kreis-Diagramm, Zeitspuren) lässt sich mit
diesem Vokabular begründen und verbessern ([[Einstiegsseite]]).
