---
titel: "Übungsaufgaben Kapitel 01–05"
quelle: "00_Materialien/InfoVis_Uebungen_Kapitel_01-05.pdf"
stand: 2026-11-15
hash: 75f6167c4da6
automatisch: true
---

> Automatisch eingelesen aus `00_Materialien/InfoVis_Uebungen_Kapitel_01-05.pdf` am 2026-11-23. Nicht bearbeiten —
> inhaltliche Arbeit gehört in die handgeschriebenen Notizen.

# Übungsaufgaben Kapitel 01–05 (Quelle)

Anhang: `90 Anhänge/Übungsaufgaben Kapitel 01–05.pdf`

## Inhalt (automatisch extrahiert)

~~~~
Informationsvisualisierung
Übungsaufgaben zu Kapitel 1 bis 5
Wintersemester 2026/27 · Prof. Dr. Sangam Chatterjee · JLU Gießen

Bearbeitung und Bewertung
Wählen Sie eine Aufgabe (U01–U14) und bearbeiten Sie alle Teilaufträge für eine der beiden Varianten. Für
Variante B gilt der gemeinsame Arbeitsauftrag mit den dort angegebenen Änderungen. Zeigen Sie die für
Ihre Variante geforderten Berechnungen, Grafiken oder Zustände.
Stellen Sie Ihre Lösung in 3–6 Minuten vor, entweder als aufgezeichnetes Video oder persönlich im
Hörsaal. Ein Live-Vortrag per Videoschalte ist nicht möglich. Einen Termin für den Hörsaalvortrag
vereinbaren Sie per E-Mail mit dem Dozenten oder persönlich vor oder nach der Veranstaltung.
Die Prüfungsvorleistung ist erbracht, wenn Sie alle drei Kriterien erfüllen und beide unten genannten
Dateien abgeben.
1. Problem zeigen. Zeigen Sie an einer konkreten Stelle der Vorher-Darstellung, welche Information schwer
   ablesbar ist oder welche Fehlinterpretation entstehen kann.
2. Aufgabe vollständig und fachlich korrekt lösen. Zeigen Sie alle für Ihre Variante geforderten Ergebnisse.
   Werte, Einheiten, Beschriftungen und Zustände müssen stimmen, soweit sie für die Aufgabe relevant sind.
3. Änderungen begründen. Erklären Sie an einem konkreten Beispiel aus Ihrer Aufgabe, wie sich die gesuchte
   Information in Ihrer Nachher-Darstellung besser ablesen oder interpretieren lässt.
Laden Sie für beide Präsentationsformen die folgenden zwei Dateien in Stud.IP hoch.
    1. Nachname_Vorname_zustimmung.pdf oder Nachname_Vorname_ablehnung.pdf
       Geben Sie in dieser PDF an, ob Sie der Präsentation in der Veranstaltung mit Livestream und ohne
       Aufzeichnung zustimmen oder sie ablehnen.
    2. Nachname_Vorname_vorleistung.mp4
       Reichen Sie Ihre Lösung als MP4-Videodatei mit maximal 25 MB ein.
Hochgeladene Dateien können Sie nicht löschen. Hängen Sie bei einer neuen Version „_VXX“ vor die
Dateiendung, zum Beispiel „Nasenbaer_Theo_zustimmung_V01.pdf“.

Gemeinsamer Übungsbestand Räume K bis P
Alle Werte gelten zum selben fiktiven Beobachtungszeitpunkt.
Geräuschwerte liegen auf einer dimensionslosen Übungsskala von 0 bis 100.
Freie Plätze = Kapazität − belegte Plätze. Auslastung = belegte Plätze ÷ Kapazität.
Raum        Kapazität      Belegt      Frei      Auslastung         Geräusch   Weg (min)       Steckdosen
K              40            20         20          50 %               20         5            ja
L             100            80         20          80 %               55         10           ja
M              20            15         5           75 %               15         8            nein
N              60            30         30          50 %               35         15           ja
O              30            0          30           0%               fehlt       12           nein
P              50            40         10          80 %               25         6            ja

Regel für Geräuschfilter Weisen Sie einen fehlenden Geräuschwert gesondert als „nicht beurteilbar“ aus.
Der Wert bleibt unbekannt.




                                                                                           Informationsvisualisierung · 1
Aufgabenübersicht
Nr.    Kapitel   Titel
U01      1       Einheiten auf einer Achse
U02      2       Eine Übertreibung messen und beheben
U03      2       Eine Frage, eine Grafik
U04      2       Daten-Tinte mit Gegenprobe
U05      3       Treffer sichtbar machen
U06      3       Eine Farbskala prüfen
U07      3       Bivariat: Farbe gegen Position
U08      4       Histogramm mit ungleichen Klassen
U09      4       Was zeigt der Fehlerbalken?
U10      4       Ein erfundener Nullpunkt im Streudiagramm
U11      4       Gesamtquote gegen Gruppenquoten
U12      4       Drei Kriterien, eine Ansicht
U13      5       Filterzustand sichtbar machen
U14      5       Lockern und Rückgängig




                                                             Informationsvisualisierung · 2
U01 Einheiten auf einer Achse
Daten Gerät X benötigt 0,3 Wh pro Vorgang und wird 1 000-mal am Tag genutzt. Gerät Y läuft dauerhaft
mit 50 W. In Teil 2 kommt hinzu: X hat zusätzlich 5 W Bereitschaftsleistung rund um die Uhr.
Vorher




Aufgabe Benennen Sie, welche zwei Größen im Vorher-Diagramm vermischt werden. Rechnen Sie beide
Geräte auf eine gemeinsame Größe um und zeichnen Sie das Diagramm neu. Zeigen Sie in Teil 2, wie sich
das Verhältnis ändert, wenn die Systemgrenze die Bereitschaft einschließt, und wie Ihr Diagramm diese
Grenze ausweist.

Variante B
X benötigt 0,5 Wh pro Vorgang bei 600 Vorgängen am Tag; Y läuft dauerhaft mit 20 W; Bereitschaft von X:
3 W. Aufgabe wie oben.




                                                                               Informationsvisualisierung · 3
U02 Eine Übertreibung messen und beheben
Daten Zwei synthetische Messwerte, 50 und 60 Einheiten. Fassung A: Balken mit sichtbarer Basis bei 40.
Fassung B: Piktogramm, dessen Symbol für 60 in Breite und Höhe um den Faktor 60/50=1,2 vergrößert ist.
Vorher




Aufgabe Bestimmen Sie für A und B die relative Datenänderung, die relative grafische Änderung und den
Lie Factor (Bezug jeweils der erste Wert; bei B gilt die Fläche als wahrgenommene Größe). Zeichnen Sie
eine korrigierte Fassung C. Zeigen Sie A, B und C nebeneinander und beantworten Sie an jeder die
Leseaufgabe „Um wie viel Prozent ist der zweite Wert größer?“.

Variante B
Werte 80 und 100, sichtbare Basis bei 70, Piktogramm-Faktor 1,25. Aufgabe wie oben.




                                                                               Informationsvisualisierung · 4
U03 Eine Frage, eine Grafik
Daten Räume K–P.
Vorher




Aufgabe Prüfen Sie Titel und Fußzeile: Welche Größe zeigt die Grafik tatsächlich, und welche behaupten
Titel und Fußzeile? Zeichnen Sie je eine passende Grafik für (a) „Wo sitzen die meisten Personen?“ und (b)
„Welcher Raum ist am stärksten ausgelastet?“. Erläutern Sie am Paar L/P, warum beide Fragen
ver
… (gekürzt)
~~~~
