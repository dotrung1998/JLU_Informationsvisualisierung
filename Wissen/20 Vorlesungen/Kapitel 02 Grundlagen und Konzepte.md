---
titel: Kapitel 02 Grundlagen und Konzepte
kapitel: 2
stand: 2026-11-22
---

# Kapitel 02 — Grundlagen und Konzepte der Informationsvisualisierung

Quelle: Gesamtfolien Kapitel 2 (PDF-Seiten 37–97); Übungsaufgaben U02, U03, U04.

## Datenexplosion und Beispiele

Das Kapitel beginnt mit der Datenexplosion (Hardware wird billiger, Daten wachsen schneller
als die Aufmerksamkeit) und zeigt dann vier klassische Beispiele:

- **Napoleons Marsch nach und Rückzug aus Moskau** (Minard): sechs Variablen in einer Grafik,
  Breite = Truppenstärke, Farbe = Richtung, Position = Ort und Zeit, Temperatur als
  Zusatzachse.
- **Cholera-Epidemie 1854** (John Snow): Punkte auf einem Stadtplan, Cluster um eine Pumpe —
  Visualisierung als Beweis.
- **Londoner U-Bahn** (Beck): schematische Geometrie statt Geografie; Lesbarkeit vor
  Richtigkeit der Lage.
- Weitere Beispiele für Zeitreihen und Netze.

## Die drei Prüfwerkzeuge von Tufte

**Lie Factor (Lügenfaktor)**

```
Lie Factor = (Änderung der Grafik) / (Änderung der Daten)
```

Ein Wert über 1,05 gilt als Übertreibung. Die Folien zeigen zwei Fälle: einen Balken mit
abgeschnittener Basis und ein Piktogramm, das in **Breite und Höhe** skaliert wird — dort
wächst die Fläche quadratisch, also viel stärker als der Datenwert („mehrdimensionales
Lügen“).

**Data-Ink Ratio (Daten-Tinte-Verhältnis)**

```
Data-Ink Ratio = Tinte für Daten / gesamte Tinte der Grafik
```

Tufte fordert: so viel Daten-Tinte wie nötig, so wenig Nicht-Daten-Tinte wie möglich. Die
Folien nennen fünf Regeln (Daten-Tinte-Regeln) und zeigen dieselbe Grafik vor und nach der
Vereinfachung.

**Chartjunk (Grafikmüll)**

Dekoration, die nichts trägt: 3D-Effekte, Muster, Hintergrundbilder, Gitterlinien ohne
Funktion. Die Folien nennen Vor- und Nachteile (Aufmerksamkeit und Wiedererkennung gegen
Ablenkung und falsche Wahrnehmung).

## Definitionen

- **Visualisierung:** Darstellung eines abstrakten Sachverhalts in einer Form, die das Auge
  erfassen kann; die Folien zitieren mehrere Definitionen, darunter Wikipedia.
- **Informationsvisualisierung:** Verstärkung der Kognition durch visuelle Darstellung
  abstrakter Daten — nicht Fotografie, nicht Illustration.
- **Anwenderaufgaben:** *Searching* (gezielt suchen), *Browsing* (durchblättern), *Analyse*
  (vergleichen, Ausreißer finden, Muster erkennen, kategorisieren, identifizieren,
  behalten). Diese Liste ist das Vokabular für die Begründung im Portfolio.

## Das Bibliotheksbeispiel

Die Folien führen den Datensatz ein, der auch im Handout steht: 100 Arbeitsplätze, sieben
Tage, vier Uhrzeiten ([[Beispieldatensatz Bibliothek]]). Zwei Befunde:

- Die Belegung um 16 Uhr im Wochenvergleich zeigt Mittwoch (96) und Freitag (62) mit
  „34 Plätze“ Unterschied — eine Aussage über **Momentaufnahmen**.
- Die Summe der vier Mittwochswerte (18 + 64 + 96 + 55 = 233) ist **keine Zahl
  unterschiedlicher Besucher**: Personen können mehrfach erfasst werden. Wer die Summe als
  „Besucher“ liest, erzeugt eine falsche Aussage.

## Herausforderungen und Werkzeuge

- Mehrdimensionalität, Auswahl geeigneter Variablen, Skalen und Darstellungen, Filterung,
  Benutzerfreundlichkeit und ihre Bewertung (Plaisant 2004).
- Kommerzielle Lösungen (u. a. Tableau) am Ende des Kapitels.

## Übungen dazu

- **U02 — Eine Übertreibung messen und beheben:** Lie Factor für Basis 40 und für ein
  flächenskaliertes Piktogramm; korrigierte Fassung C.
- **U03 — Eine Frage, eine Grafik:** Titel und Fußzeile prüfen; absolute Zahl gegen Anteil;
  Räume L und P als Beispiel, dass beide Fragen verschiedene Antworten haben.
- **U04 — Daten-Tinte mit Gegenprobe:** in mindestens drei Schritten vereinfachen, einen
  Schritt bewusst zu weit treiben und zurücknehmen.

Daten in [[Prüfungsvorleistung]].

## Bezug zum Portfolio

Lie Factor, Data-Ink Ratio und Chartjunk sind die Kriterien, mit denen der Gruppenteil die
überarbeiteten Darstellungen **begründet** ([[Gruppenarbeit]]). Jede Überarbeitung braucht
eine Aussage der Form: „Die Basis war abgeschnitten, der Lie Factor lag bei X; nach der
Korrektur liest man Y direkt ab.“
