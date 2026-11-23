---
titel: Kapitel 06 Graphen und Netzwerke
kapitel: 6
stand: 2026-11-22
---

# Kapitel 06 — Graphen und Netzwerke

Quellen: Gesamtfolien Kapitel 6 (PDF-Seiten 242–260) und die ausführlichere
**Arbeitsfassung** `Kapitel_05_Graphen_und_Netzwerke_Arbeitsfassung_2026-11-19_v1.7.1.pdf`
(23 Folien). Die Arbeitsfassung nennt sich „Kapitel 5“ — Nummerierung offen
([[Vorlesungsplan]]).

## Leitfragen des Kapitels

1. Was ist ein Graph?
2. Welche Objekte werden Knoten, welche Beziehungen Kanten?
3. Welche Art von Graph braucht man (gerichtet, mehrere Verbindungen, gemeinsame
   Beziehung)?
4. Wie zeichnet man ihn: Anordnung der Knoten, Führung der Kanten, damit eine Verbindung
   verfolgbar bleibt?

## Grundbegriffe

- **Graph:** Menge von Objekten mit den Verbindungen zwischen ihnen; Objekte = **Knoten**
  (Ecken), Verbindungen = **Kanten** (Bögen).
- **Ungerichtet:** Kanten ohne Richtung, in beide Richtungen begehbar.
- **Gerichtet (Digraph):** Kanten als Pfeile vom Anfangs- zum Endknoten; A → B und B → A
  können beide vorkommen. Im **orientierten** Graphen ist höchstens eine Richtung vorhanden.
- **Baum:** zusammenhängender, ungerichteter Graph ohne Zyklen; Knotenzahl = Kantenzahl + 1.
- **Multigraph:** mehrere Kanten zwischen demselben Knotenpaar, Schleifen erlaubt; statt
  vieler Kanten wird eine Kante mit **Kantengewicht** gezeichnet (Beispiel: 60 Kanten
  zwischen A und D).
- **Kantengewicht:** z. B. Fahrzeit in Minuten; direkte Kante A–C 12 Min. gegen Weg über B
  4 + 5 = 9 Min.
- **Planarer Graph:** in der Ebene zeichenbar ohne Kantenschnitt; jeder planare Graph hat
  einen **dualen** Graphen (jede Fläche ein Knoten), die Dualität ist gegenseitig.
- **Hypergraph:** eine (Hyper-)Kante verbindet mehrere Knoten; Darstellung als eingekreiste
  Punktmengen oder als bipartiter Metagraph (Knoten ↔ Hyperkanten).

## Wie zeichnet man einen Graphen

- Knoten als Kreise, Kanten als offene Kurven; Kodierung über Farbe, Größe, Form;
  Beschriftung ist wegen Überlagerung schwierig.
- **Layout-Algorithmen:** planar (kreuzungsfrei), gerade / polylinien / gekrümmt,
  orthogonal (nur horizontale und vertikale Segmente), gitterbasiert (ganzzahlige
  Koordinaten), aufwärts/abwärts für gerichtete azyklische Graphen (Fluss in eine Richtung,
  gut für Hierarchien).
- **Ästhetik:** Kreuzungen minimieren, Fläche minimieren, Summe der Kantenlängen minimieren,
  gleichmäßige Kantenlängen, Biegungen minimieren, Symmetrie darstellen, minimale Winkel
  zwischen Kanten maximieren.
- **Empirie:** Purchase 1997 verglich fünf Graphpaare und fand den **größten Effekt bei der
  Verringerung der Kreuzungszahl**. Ware et al. 2002 (kürzester Pfad in Spring-Layout-Graphen)
  priorisieren: Länge des kürzesten Pfads (Anzahl Kanten), Kontinuität (Multi-Kanten-Pfade so
  gerade wie möglich), Anzahl der Kreuzungen **entlang des betrachteten Pfads**.

## Alternative Darstellung

**Adjazenzmatrix:** Zeilen und Spalten = Knoten, 1 = direkt verbunden, 0 = nicht. Dieselbe
Information wie das Knoten-Kanten-Bild, besser lesbar bei dichten Graphen, schlechter bei
der Frage „welcher Weg führt von A nach D“.

## Anwendungsbeispiel

**They Rule** (theyrule.net): Knoten = Personen und Unternehmen, Kante = Person sitzt im
Gremium des Unternehmens; die Frage „wie sind zwei Unternehmen über eine Person verbunden“
wird zur Wegsuche im Graphen.

## Bezug zum Portfolio

Kein Übungsblatt (U01–U14 enden bei Kapitel 5). Als Material für den Gruppenteil taugt das
Kapitel, wenn eine eigene Darstellung als Netz vorliegt (z. B. Verbindungen zwischen
Literatur, Orten oder Aufgaben). Die Begriffe Layout, Kreuzung, Kantenführung liefern dann
die Begründung ([[Gruppenarbeit]]).
