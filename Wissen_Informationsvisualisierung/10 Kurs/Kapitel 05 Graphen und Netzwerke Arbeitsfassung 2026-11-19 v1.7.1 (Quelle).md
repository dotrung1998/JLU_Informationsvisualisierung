---
titel: "Kapitel 05 Graphen und Netzwerke Arbeitsfassung 2026-11-19 v1.7.1"
quelle: "00_Materialien/Kapitel_05_Graphen_und_Netzwerke_Arbeitsfassung_2026-11-19_v1.7.1.pdf"
stand: 2026-11-19
hash: 57aa32e91a22
automatisch: true
---

> Automatisch eingelesen aus `00_Materialien/Kapitel_05_Graphen_und_Netzwerke_Arbeitsfassung_2026-11-19_v1.7.1.pdf` am 2026-11-23. Nicht bearbeiten —
> inhaltliche Arbeit gehört in die handgeschriebenen Notizen.

# Kapitel 05 Graphen und Netzwerke Arbeitsfassung 2026-11-19 v1.7.1 (Quelle)

Anhang: `90 Anhänge/Kapitel 05 Graphen und Netzwerke Arbeitsfassung 2026-11-19 v1.7.1.pdf`

## Inhalt (automatisch extrahiert)

~~~~
JUSTUS-LIEBIG-UNIVERSITÄT GIESSEN




Kapitel 5
Graphen und Netzwerke
                                                                            JUSTUS-LIEBIG-UNIVERSITÄT GIESSEN




Was lernen wir in diesem Kapitel?
              Was ist ein Graph?
              Welche Objekte stellen wir als Knoten dar, welche Beziehungen als Kanten?


              Welche Art von Graph brauchen wir?
              Wie stellen wir eine Richtung, mehrere Verbindungen
              oder eine gemeinsame Beziehung zwischen mehreren Objekten dar?


              Wie zeichnen wir einen Graphen?
              Wie ordnen wir die Knoten an und wie führen wir die Kanten,
              damit sich eine Verbindung gut verfolgen lässt?
                                             JUSTUS-LIEBIG-UNIVERSITÄT GIESSEN




Graphen
          Ein Graph ist in der Graphentheorie eine abstrakte
          Struktur, die eine Menge von Objekten zusammen
          mit den zwischen diesen Objekten bestehenden
          Verbindungen repräsentiert. Die mathematischen
          Abstraktionen der Objekte werden dabei Knoten
          (auch Ecken) des Graphen genannt. Die paarweisen
          Verbindungen zwischen Knoten heißen Kanten
          (manchmal auch Bögen). Die Kanten können
          gerichtet oder ungerichtet sein. Häufig werden
          Graphen anschaulich gezeichnet, indem die Knoten
          durch Punkte und die Kanten durch Linien
          dargestellt werden.
                                                                      JUSTUS-LIEBIG-UNIVERSITÄT GIESSEN




Graphen
          Graphen können jede Art der Information Darstellen, die als Objekte und
          Verbindungen zwischen diesen Objekten modelliert werden kann
          Objekte werden durch Knoten repräsentiert
          Die Beziehungen zwischen Objekten werden durch Kanten (oder Bögen)
          repräsentiert
          Häufig visualisiert als Knoten-Verbindungs-Diagramme
          Graphen sollen in der Informationsvisualisierung das Verständnis komplexer
          Muster erleichtern
                                                                     JUSTUS-LIEBIG-UNIVERSITÄT GIESSEN




Beispiele




Von Stefan Kühn, Quirin Schroll - Wikimedia Commons, CC BY-SA 3.0,
https://commons.wikimedia.org/w/index.php?curid=31105072
                                                                          JUSTUS-LIEBIG-UNIVERSITÄT GIESSEN




Herausforderungen beim Erstellen von Graphen
             Layout und Positionierung (Graphenvisualisierung)
             • Wie muss ein Graph dargestellt werden, um leicht lesbar und
               interpretierbar zu sein, also die meiste Information zu vermitteln
             Maßstab
             • Leistung von Layout-Algorithmen
             • Begrenzter verfügbarer Anzeigebereich
             Navigation und Interaktion
             • Wie kann der Benutzer durch den Graphen navigieren und Teile des
               Graphen detaillierter zu betrachten
                                                       JUSTUS-LIEBIG-UNIVERSITÄT GIESSEN




Ungerichteter Graph
                      In ungerichteten Graphen werden die Verbindungen
                      zwischen Knoten durch Kanten gekennzeichnet. Die
                      Kanten haben keine Richtung. Jede Kante kann in
                      beide Richtungen durchlaufen werden.
                                                       JUSTUS-LIEBIG-UNIVERSITÄT GIESSEN




Gerichteter Graph
                    In Digraphen (von englisch directed graph, auch
                    gerichtete Graphen genannt) werden Kanten statt
                    durch Linien durch Pfeile gekennzeichnet, wobei der
                    Pfeil von ihrem Anfangs- zu ihrem Endknoten zeigt.
                    Dies verdeutlicht, dass jede Kante des Graphen nur
                    in eine Richtung durchlaufen werden kann.
                    In einem gerichteten Graphen können A → B und B
                    → A vorkommen. Bei einem orientierten Graphen
                    ist höchstens eine dieser beiden Richtungen
                    vorhanden.
                                             JUSTUS-LIEBIG-UNIVERSITÄT GIESSEN




Bäume
        Ein Baum ist ein zusammenhängender,
        ungerichteter Graph ohne Zyklen.
        Bei allen Bäumen ist die Anzahl der Knoten um 1
        größer als die Anzahl der Kanten.
        Bäume haben viele Anwendungen in der Informatik,
        oft werden Algorithmen mithilfe von Bäumen
        programmiert.
        Im Bereich der künstlichen Intelligenz und der
        Strategiespiele ist die Alpha-Beta-Suche wichtig. Sie
        basiert auf Suchbäumen.
                                                 JUSTUS-LIEBIG-UNIVERSITÄT GIESSEN




Multigraph
             Anders als in einfachen Graphen können in
             Multigraphen Knoten auch durch mehrere Kanten
             verbunden sein.
             Multigraphen dürfen Schleifen enthalten: Kanten,
             die zum selben Knoten führen, von dem sie
             ausgehen.
             Sind Knoten durch mehrere Kanten verbunden, wird
             häufig nur eine Kante gezeichnet und die Anzahl der
             Kanten zwischen diesen beiden Knoten als
             Kantengewicht an die eine Kante geschrieben.
             Im Beispiel gibt es 60 Kanten zwischen Knoten A
             und D. Anstatt alle 60 Kanten zu zeichnen, wird eine
             Kante mit dem Kantengewicht 60 gezeichnet.
Was bedeutet das Gewicht einer Kante?
          Fahrzeit in Minuten


                                            Direkt von A nach C:
                    B                       1 Kante, 12 Minuten


      4 min                     5 min       Von A über B nach C:
                                            2 Kanten, 4 + 5 = 9 Minuten



  A                                     C
                  12 min
… (gekürzt)
~~~~
