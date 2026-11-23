---
titel: "Prüfungsvorleistung"
quelle: "Abgabe/Prüfungsvorleistung"
stand: 2026-11-23
hash: e292e6ebf099
automatisch: true
---

> Automatisch eingelesen aus `Abgabe/Prüfungsvorleistung` am 2026-11-23. Nicht bearbeiten —
> inhaltliche Arbeit gehört in die handgeschriebenen Notizen.

# Prüfungsvorleistung (Quelle)

Eine Übungsaufgabe U01–U14 vorstellen; Termin nicht dokumentiert. Frist: nicht dokumentiert. Quelle: `Prüfungsvorleistung`

## Dateien

| Datei | Größe | Typ | Herkunft |
|---|---|---|---|
| `U02_Lie_Factor_Entwurf.pdf` | 45 KB | PDF | Fremddatei oder Vorlage |
| `U02_Lie_Factor_Entwurf.tex` | 7 KB | TEX | Fremddatei oder Vorlage |
| `U02_Vorschau.png` | 331 KB | PNG | Fremddatei oder Vorlage |

> **Keine eigene Datei in diesem Ordner.** Was hier liegt, ist nicht die
> eigene Abgabe ([[Portfolio Trung]]).

## Inhalt

### U02_Lie_Factor_Entwurf.pdf

~~~~
Informationsvisualisierung
                          Übungsaufgabe U02 – Eine Übertreibung messen und beheben, Variante A
                       Trung Do | Matrikelnummer: 8229831 | Entwurf vom 23.11.2026, nicht abgegeben



1 Rechnung
Daten: zwei Messwerte, 50 und 60 Einheiten. Bezug ist jeweils der erste Wert.


                                                      Fassung A                    Fassung B            Fassung C
                                                  Balken, Basis bei 40       Piktogramm, Faktor 1,2      korrigiert
                  relative Datenänderung                     20 %                       20 %                20 %
                  relative graﬁsche Änderung                100 %                       44 %                20 %
                  Lie Factor                                5,00                        2,20                1,00

• Daten: (60 − 50)/50 = 0,20 = 20 %.
• Fassung A: Die Balken beginnen bei 40. Die Höhen sind 50 − 40 = 10 und 60 − 40 = 20, also (20 − 10)/10 = 2,0 = 100 %.
• Fassung B: Das Symbol wächst in Breite und Höhe um 1,2. Die Fläche wächst mit dem Quadrat, 1,22 = 1,44, also 44 %.
• Lie Factor: 1,00/0,20 = 5,00 für A und 0,44/0,20 = 2,20 für B.
Beide Fassungen liegen über der Schwelle 1,05 aus Kapitel 2. Fassung A übertreibt den Unterschied um das Fünﬀache, Fassung
B um mehr als das Doppelte.

2 Drei Fassungen, eine Leseaufgabe

                                                                                                      60



                                                                                                      40

         60
         55                                                                   60
                                                       50                                             20
         50
         45
         40                                                                                             0
                 50      60                        Fläche 1,00            Fläche 1,44                         50      60

               Fassung A                                        Fassung B                                   Fassung C
           Balken, Achse 40–60                              Piktogramm, Fläche                           Balken, Achse 0–60
          gelesen: 100 % größer                             gelesen: 44 % größer                        gelesen: 20 % größer

Fassung C ist die Korrektur: beide Balken beginnen bei 0, die Höhe ist linear zum Wert, es gibt nur eine Dimension und keine
Flächenskalierung. Die Achse reicht bis 60, damit der größere Wert vollständig sichtbar bleibt.

3 Die drei Kriterien
(1) Problem zeigen. In Fassung A beginnt die Achse bei 40. Der Balken für 50 ist 10 Einheiten hoch, der für 60 doppelt so
hoch. Wer die Balken vergleicht, liest „doppelt so viel“ statt „ein Fünftel mehr“. In Fassung B wächst das Symbol in Breite und
Höhe. Das Auge liest die Fläche, und die wächst quadratisch: Der Unterschied erscheint als 44 Prozent statt als 20 Prozent. Die
konkrete Fehlinterpretation ist in beiden Fassungen dieselbe: Die 60 wirkt fast doppelt so groß wie die 50, tatsächlich ist sie nur
ein Fünftel größer.
(2) Aufgabe vollständig und fachlich korrekt lösen. Für A und B sind die relative Datenänderung (20 Prozent), die
relative graﬁsche Änderung (100 Prozent, 44 Prozent) und der Lie Factor (5,00, 2,20) angegeben, mit Bezug auf den ersten Wert
und bei B mit der Fläche als wahrgenommener Größe. Fassung C ist gezeichnet. Die Leseaufgabe ist an allen drei Fassungen
beantwortet: 100 Prozent, 44 Prozent, 20 Prozent.
(3) Änderungen begründen. Die Korrektur ist messbar, nicht nur optisch. Bei Fassung A liest man einen Unterschied von
100 Prozent, bei Fassung B von 44 Prozent, bei Fassung C von 20 Prozent. Der Lie Factor fällt von 5,00 und 2,20 auf 1,00.
In Fassung C entspricht die Balkenhöhe dem Wert, weil die Achse bei 0 beginnt und nur die Höhe skaliert wird. Die gesuchte
Information, um wie viel Prozent der zweite Wert größer ist, lässt sich direkt an der Achse ablesen.




Datenquelle: Übungsblatt Informationsvisualisierung – Übungsaufgaben zu Kapitel 1 bis 5, U02, Variante A (Werte 50 und 60, Basis 40,
Piktogrammfaktor 1,2), S. 4. Schwelle 1,05 und Flächenskalierung: Vorlesung Kapitel 2. Variante B des Übungsblatts (Werte 80 und 100,
Basis 70, Faktor 1,25) ergibt 25 Prozent Datenänderung, 200 Prozent graﬁsche Änderung für den Balken (Lie Factor 8,00) und 56,25 Prozent
für die Fläche (Lie Factor 2,25). KI-Hilfe: Rechnung, Formulierung der Begründung und LaTeX-/TikZ-Code dieses Entwurfs wurden mit
dem KI-Assistenten Codebuﬀ erstellt. Die einreichende Person prüft Rechnung und Begründung und verantwortet sie vor der Abgabe.


                                                                     1
~~~~
### U02_Lie_Factor_Entwurf.tex

~~~~
\documentclass[a4paper,10pt]{article}

% Pakete
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
\usepackage{booktabs}
\usepackage{tikz}

\geometry{a4paper, left=1.5cm, right=1.5cm, top=1.3cm, bottom=1.3cm}

\setlength{\parindent}{0pt}
\setlength{\parskip}{2pt}
\setlist[itemize]{nosep, leftmargin=*, topsep=1pt, parsep=0pt}
\setlist[enumerate]{nosep, leftmargin=*, topsep=1pt, parsep=0pt}

\titlespacing*{\section}{0pt}{6pt}{2pt}
\titleformat{\section}{\normalfont\large\bfseries}{}{0pt}{}
\titlespacing*{\subsection}{0pt}{5pt}{1pt}
\titleformat{\subsection}{\normalfont\normalsize\bfseries}{}{0pt}{}

\hypersetup{colorlinks=true, linkcolor=blue, urlcolor=blue}

\begin{document}
\small

% Titelbereich
\begin{center}
\textbf{\large Informationsvisualisierung} \\
\small Übungsaufgabe U02 -- Eine Übertreibung messen und beheben, Variante A \\
\textbf{Trung Do} | Matrikelnummer: 8229831 | \textit{Entwurf vom 23.11.2026, nicht abgegeben}
\end{center}
\vspace{-3mm}
\noindent\rule{\textwidth}{0.3pt}

% ---------------------------------------------------------------- Rechnung
\section*{1\ \ Rechnung}

Daten: zwei Messwerte, 50 und 60 Einheiten. Bezug ist jeweils der erste Wert.

\begin{center}
\renewcommand{\arraystretch}{1.15}
\begin{tabular}{@{}lccc@{}}
\toprule
 & \textbf{Fassung A} & \textbf{Fassung B} & \textbf{Fassung C} \\
 & Balken, Basis bei 40 & Piktogramm, Faktor 1,2 & korrigiert \\
\midrule
relative Datenänderung & $20\,\%$ & $20\,\%$ & $20\,\%$ \\
relative grafische Änderung & $100\,\%$ & $44\,\%$ & $20\,\%$ \\
\textbf{Lie Factor} & $\mathbf{5{,}00}$ & $\mathbf{2{,}20}$ & $\mathbf{1{,}00}$ \\
\bottomrule
\end{tabular}
\end{center}

\begin{itemize}
\item Daten: $(60-50)/50 = 0{,}20 = 20\,\%$.
\item Fassung A: Die Balken beginnen bei 40. Die Höhen sind $50-40=10$ und $60-40=20$,
      also $(20-10)/10 = 2{,}0 = 100\,\%$.
\item Fassung B: Das Symbol wächst in Breite und Höhe um 1,2. Die Fläche wächst mit dem
      Quadrat, $1{,}2^2 = 1{,}44$, also $44\,\%$.
\item Lie Factor: $1{,}00/0{,}20 = 5{,}00$ für A und $0{,}44/0{,}20 = 2{,}20$ für B.
\end{itemize}

Beide Fassungen liegen über der Schwelle 1,05 aus Kapitel 2. Fassung A übertreibt den
Unterschied um das Fünffache, Fassung B um mehr als das Doppelte.

% ---------------------------------------------------------------- Abbildung
\section*{2\ \ Drei Fassungen, eine Leseaufgabe}

\begin{center}
% --- Fassung A -------------------------------------------------------
\begin{minipage}[b]{0.315\linewidth}\centering
  \begin{tikzpicture}[x=1cm, y=0.09cm, font=\scriptsize]
    \draw (0,40) -- (0,64);
    \draw (0,40) -- (2.7,40);
    \foreach \v in {40,45,50,55,60}{%
      \draw (-0.06,\v) -- (0,\v);
      \node[left] at (-0.08,\v) {\v};}
    \fill[gray!30] (0.35,40) rectangle (0.95,50);
    \fill[gray!30] (1.45,40) rectangle (2.05,60);
    \node[below] at (0.65,40) {50};
    \node[below] at (1.75,40) {60};
  \end{tikzpicture}

  \smallskip
  {\footnotesize\textbf{Fassung A}\\ Balken, Achse 40--60\\[1pt]
   \textit{gelesen: 100\,\% grö\ss{}er}}
\end{minipage}\hfill
% --- Fassung B -------------------------------------------------------
\begin{minipage}[b]{0.315\linewidth}\centering
  \begin{tikzpicture}[x=1cm, y=1cm, font=\scriptsize]
    \fill[gray!30] (0,0) rectangle (2.0,2.0);
    \node at (1.0,1.0) {50};
    \fill[gray!30] (2.6,0) rectangle (5.0,2.4);
    \node at (3.8,1.2) {60};
    \node[below] at (1.0,0) {Fläche 1,00};
    \node[below] at (3.8,0) {Fläche 1,44};
  \end{tikzpicture}

  \smallskip
  {\footnotesize\textbf{Fassung B}\\ Piktogramm, Fläche\\[1pt]
   \textit{gelesen: 44\,\% grö\ss{}er}}
\end{minipage}\hfill
% --- Fassung C -------------------------------------------------------
\begin{minipage}[b]{0.315\linewidth}\centering
  \begin{tikzpicture}[x=1cm, y=0.058cm, font=\scriptsize]
    \draw (0,0) -- (0,68);
    \draw (0,0) -- (2.7,0);
    \foreach \v in {0,20,40,60}{%
      \draw (-0.06,\v) -- (0,\v);
      \node[left] at (-0.08,\v) {\v};}
    \draw[gray!45, very thin] (0,20) -- (2.5,20);
    \draw[gray!45, very thin] (0,40) -- (2.5,40);
    \draw[gray!45, very thin] (0,60) -- (2.5,60);
    \fill[gray!30] (0.35,0) rectangle (0.95,50);
    \fill[gray!30] (1.45,0) rectangle (2.05,60);
    \node[below] at (0.65,0) {50};
    \node[below] at (1.75,0) {60};
  \end{tikzpicture}

  \smallskip
  {\footnotesize\textbf{Fassung C}\\ Balken, Achse 0--60\\[1pt]
   \textit{gelesen: 20\,\% grö\ss{}er}}
\end{minipage}
\end{center}

Fassung C ist die Korrektur: beide Balken beginnen bei 0, die Höhe ist linear zum Wert, es
gibt nur eine Dimension und keine Flächenskalierung. Die Achse reicht bis 60, damit der
grö\ss{}ere Wert vollständig sichtbar bleibt.

% ---------------------------------------------------------------- Kriterien
\section*{3\ \ Die drei Kriterien}

\textbf{(1) Problem zeigen.} In Fassung A beginnt die Achse bei 40. Der Balken für 50 ist
10 Einheiten hoch, der für 60 doppelt so hoch. Wer die Balken vergleicht, liest \enquote{doppelt so
viel} statt \enquote{ein Fünftel mehr}. In Fassung B wächst das Symbol in Breite und Höhe. Das Auge
liest die Fläche, und die wächst quadratisch: Der Unterschied erscheint als 44 Prozent statt
als 20 Prozent. Die konkrete Fehlinterpretation ist in beiden Fassungen dieselbe: Die 60
wirkt fast doppelt so gro\ss{} wie die 50, tatsächlich ist sie nur ein Fünftel grö\ss{}er.

\textbf{(2) Aufgabe vollständig und fachlich korrekt lösen.} Für A und B sind die relative
Datenänderung (20 Prozent), die relative grafische Änderung (100 Prozent, 44 Prozent) und der
Lie Factor (5,00, 2,20) angegeben, mit Bezug auf den ersten Wert und bei B mit der Fläche als
wahrgenommener Grö\ss{}e. Fassung C ist gezeichnet. Die Leseaufgabe ist an allen drei Fassungen
beantwortet: 100 Prozent, 44 Prozent, 20 Prozent.

\textbf{(3) Änd
… (gekürzt)
~~~~
### U02_Vorschau.png

_Kein Text extrahiert (Bild). Inhalt noch nicht beschrieben — als offenen Punkt im Vault vermerken._
