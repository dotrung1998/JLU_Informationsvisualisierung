---
titel: Kapitel 07 Hierarchien und Bäume
kapitel: 7
stand: 2026-11-22
---

# Kapitel 07 — Hierarchien und Bäume

Quelle: Gesamtfolien Kapitel 7 (PDF-Seiten 261–300).

## Hierarchische Daten

Hierarchien beschreiben Teil-von-Beziehungen (Dateisystem, Organisation, Klassifikation).
Sie treten in vielen Kontexten auf und werden meist als **visuelle Baumstrukturen**
dargestellt. Zwei Grundformen:

- **Node-Link-Diagramm:** Knoten und Kanten; das gängigste Layout, gut für kleine Bäume,
  schlecht für Tiefe und Größe.
- **Flächenfüllende Verfahren (Treemap):** die Fläche trägt die Größe, die Verschachtelung
  die Hierarchie.

## Navigations- und Platztechniken

- **Hyperbolischer Baum-Browser:** vergleichbar mit einer Fischaugen-Verzerrung; der Fokus
  bleibt groß, der Rest schrumpft, ohne zu verschwinden.
- **Space Tree:** Mechanismen zur Exploration und Navigation großer Bäume.
- **Cheops:** Platz sparende Darstellung durch Wiederverwendung von Teilbäumen.
- **Degree-of-Interest-Baum:** interaktive Anzeige von Hierarchien im Browser, mit animierten
  Übergängen für Teile, die sonst gekürzt oder zusammengeklappt würden.
- **Dreidimensionale Visualisierung:** die zusätzliche Dimension für mehr Knoten; die
  Usability-Bewertung von Cockburn & McKenzie 2000 fällt zurückhaltend aus (Nutzen rechtfertigt
  den Aufwand selten).

## Treemaps

- Johnson & Shneiderman 1992: verschachtelte Rechtecke, Fläche proportional zum Wert.
- **Slice-and-Dice:** abwechselnd horizontal und vertikal teilen; erzeugt lange, dünne
  Rechtecke, die schwer zu vergleichen sind.
- Problem: das **Seitenverhältnis** der Rechtecke; mehrere Algorithmen verbessern es.
- **Geordnete Treemaps:** die Reihenfolge der Daten bleibt erhalten, benachbarte Werte bleiben
  benachbart (Strip Treemap, Bederson & Shneiderman 2002); Tests mit mehreren Datensätzen und
  Anwendung auf reale Daten.

## Merkpunkte

- Fläche ist ein schwacher Kanal: kleine Unterschiede sind in Rechtecken kaum zu sehen,
  Länge und Position sind genauer.
- Ein Treemap ohne Ordnung ist ein Diagramm ohne Aussage; die Sortierung ist die Aussage.
- Bei Tiefe über zwei bis drei Ebenen wird Beschriftung zum Hauptproblem.

## Bezug zum Portfolio

Für den Gruppenteil relevant, wenn eine eigene Darstellung eine **Hierarchie** zeigt (z. B.
Semester → Woche → Tag, oder Dokument → Kapitel → Abschnitt). Die Treemap-Kritik
(Seitenverhältnis, Sortierung, schwacher Flächenkanal) ist eine fertige Begründung für eine
Überarbeitung ([[Gruppenarbeit]]).
