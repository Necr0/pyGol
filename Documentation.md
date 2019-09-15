```
German version below
Deutsche Version unten
```

# Preparation

## General considerations

I created an empty git repository to keep track of my progress
and I decided to go with the Unlicese because it is my license
of choice for leisure projects.

## Choice of programming language and frameworks

Python was chosen as it can be used for fast prototyping while 
the language itself has things such as classes and modules to
help structuring the code and significant whitespace keeping the
code clean even if the project grows older and larger. The
simple PyGame framework was chosen because it provides most of
the functionality necessary for displaying and interacting with
the application. NumPy will be used for more efficiently
implemented matricies/arrays.

## Project structure

The project will be split into two parts:
1. the Game of Life logic which computes the generations
* * <del>Board class with bounds and the state of each cell</del>
* * *  ditched in favor of just using the NumPy arrays without unnessary overhead without any benifit
* * A function that takes a board state and computes the next generation
* * *  <del>A function used by that function in order to determine the state of that cell in the next generation</del>
* * * * ditched in favor of a single function using convolution using SciPy
2. the Presentation/Application layer which displays the board and allows interaction written in pyGame

# Implementation
1. Implemented the game's generation function "next_generation" as well as a helper function
2. Implement a visualization of the game for a MVP
3. Add interactivity (added some keys)
4. Custom Generator Functions
6. Added mouse drawing
5. All Generator functions can be expressed as a kernel(=convolution matrix) and an array containing the results after convolution that cause the cell to be alive (the cells own state is contained in the convolution matrix)
6. Load rulesets from file
7. Allow more than 1 state in a ruleset
    * the amount of rules increases exponentially with the number of states, wireworld(4 states) has 4^9= 4^9=262144 potential rules
    * * solution: allow loading python functions from file
8. Allow saving/loading of patterns
9. "fancier" interface
    * this was done by actually displaying keyboard shortcuts available
10. Next step: changable board size and cell size
    * changing the cell size and board size may be easy but would cause saving and loading to break and would also have to change the window size

# Convolution

## What is convolution?

Convolution involves having a matrix and applying a kernel to each cell. The kernel is centered on the cell in question and describes weights for a cell and the cells neighborhood. The cell and neighbous are then multiplied with the corresponding weight in the kernel and then summed. The resulting sum is the value for the cell at the same position in the resulting matrix.

## Applying it to the Game of Life

```
[[1 1 1]
 [1 0 1]
 [1 1 1]]
```

The above kernel has a weight of 1 for all cells in the center cell's [Moore neighborhood](https://en.wikipedia.org/wiki/Moore_neighborhood), assuming that a living cell has a value of 1, this will mean convolution using this kernel, will result in the neighbor count of a cell in the resulting cell.

```
[[0 0 0 0]       [[2 3 2 1] 
 [1 1 1 0]   =>   [2 4 3 2] 
 [0 1 1 0]        [3 4 3 2] 
 [0 0 0 0]]       [1 2 2 1]]
```

Given matrix containing the cell A and the convolved matrix B we can say that for any given cell at x, y of A the count of neighbors is contained in B at x, y. Thus for any cell x, y cotained within A we can decide wether the next generation lives on the basis of the values A[x,y] and B[x,y].
This simplifies the problem a lot because we don't have to implement counting neighbors ourselves but can use existing convolution functions instead.

## Getting rid of matrix A

Since the count of living neighbors can never exceed 8 we can define the center of the kernel to have a value of 9:

```
[[1 1 1]
 [1 9 1]
 [1 1 1]]
```

This the convolution result not only contains the amount of living neighbors but also wether or not the cell itself is alive or dead. If the cell of the convolutions result is more than or equal to 9 the original cell must have been alive, otherwise it must have been dead. To get the amount of alive neighbours we can simply subtract 9 if the value is above 9 or leave it as is otherwise.
This way we can decide wether or not wether or not the next generation lives on the basis of B[x,y] alone. Since we now have just one value to base our decision on we can simply express the rules for wether or not the cell should be alive in the next generation in a flat array. If the value is contained within said array it is alive, otherwise it is dead. This way we can express the game of lifes ruleset in just 2 objects: 1. a kernel, 2. a list of results leading to a living cell.

## But why?

I heard it's possible to implement the Game of Life using convolution, so I just did it. 
  
---
  
# Vorbereitung

## Allgemeine Überlegungen

Ich habe ein leeres Git-Repository erstellt, um meinen Fortschritt zu verfolgen.
und ich habe mich für die Unlicese entschieden, weil sie meine erste Wahl für Freizeitprojekte ist.

## Wahl der Programmiersprache und der Frameworks

Python wurde gewählt, da es für das schnelle Prototyping verwendet werden kann, während die die Sprache selbst hat Dinge wie Klassen und Module, die helfen den Code zu strukturieren. Das einfache PyGame Framework wurde gewählt, da es die Funktionalität, die für die Anzeige und Interaktion mit dem Benutzer erforderlich ist bereitstellt. NumPy wird effizientere Matrizen/Arrays genutzt.

## Projektstruktur

Das Projekt wird in zwei Teile gegliedert:
1. die Game of Life Logik, die die Generationen berechnet.
    * <del>Board-Klasse mit Grenzen und dem Zustand jeder Zelle</del>.
    * * zugunsten der Verwendung der NumPy-Arrays ohne unnötigen Overhead fallen gelassen
    * * Eine Funktion, die einen Board-Zustand nimmt und die nächste Generation berechnet
    * * * <del>Eine Funktion, die von dieser Funktion verwendet wird, um den Zustand einer einzelnen Zelle in der nächsten Generation zu bestimmen</del>.
    * * *  zugunsten einer einzelnen Funktion unter Verwendung von Faltungmatrizen mit SciPy weggeworfen
2. die Darstellungs-/Anwendungsschicht, die das Board anzeigt und die Interaktion durch PyGame ermöglicht
2. die Darstellungs-/Anwendungsschicht, die das Board anzeigt und die Interaktion durch PyGame ermöglicht
 zugunsten der Verwendung der NumPy-Arrays ohne unnötigen Overhead fallen gelassen
    * * Eine Funktion, die einen Board-Zustand nimmt und die nächste Generation berechnet
    * * * <del>Eine Funktion, die von dieser Funktion verwendet wird, um den Zustand einer einzelnen Zelle in der nächsten Generation zu bestimmen</del>.
    * * *  zugunsten einer einzelnen Funktion unter Verwendung von Faltungmatrizen mit SciPy weggeworfen.
 fallen gelassen
    * * Eine Funktion, die einen Board-Zustand nimmt und die nächste Generation berechnet
    * * * <del>Eine Funktion, die von dieser Funktion verwendet wird, um den Zustand einer einzelnen Zelle in der nächsten Generation zu bestimmen</del>.
    * * *  zugunsten einer einzelnen Funktion unter Verwendung von Faltungmatrizen mit SciPy weggeworfen.
* * * * * <del>Eine Funktion, die von dieser Funktion verwendet wird, um den Zustand dieser Zelle in der nächsten Generation zu bestimmen</del>.
* zugunsten einer einzelnen Funktion unter Verwendung von Faltungmatrizen mit SciPy weggeworfen.
die Anwendung. NumPy wird für eine effizientere Nutzung genutzt.
implementierte Matrizen/Arrays.
## Projektstruktur

Das Projekt wird in zwei Teile gegliedert:
1. die Game of Life Logik, die die Generationen berechnet.
* * <del>Board-Klasse mit Grenzen und dem Zustand jeder Zelle</del>.
 * zugunsten der Verwendung der NumPy-Arrays ohne unnötigen Aufwand ohne Nutzen.
* * * Eine Funktion, die einen Board-Status annimmt und die nächste Generation berechnet.
* * * * * <del>Eine Funktion, die von dieser Funktion verwendet wird, um den Zustand dieser Zelle in der nächsten Generation zu bestimmen</del>.
* zugunsten einer einzelnen Funktion unter Verwendung von Faltung mit SciPy weggeworfen.
2. die Präsentations-/Anwendungsschicht, die das Board anzeigt und die Interaktion im PyGame ermöglicht.

# Implementierung
1. Implementiert wurde die Generierungsfunktion "next_generation" des Spiels sowie eine Helferfunktion.
2. Implementierung einer Visualisierung des Spiels für ein MVP
3. Interaktivität hinzufügen (einige Keybindings hinzugefügt)
4. Benutzerdefinierte Generatorfunktionen
6. Zeichnen mit der Maus hinzugefügt
5. Alle Generatorfunktionen können als Kernel (=Faltungsmatrix) und als Array mit den Ergebnissen nach der Faltung ausgedrückt werden, die die Zelle lebendig machen (der eigene Zustand der Zelle ist in der Faltungsmatrix enthalten).
6. Regelsätze aus Datei laden
7. Mehr als einen Zustand in einem Regelsatz erlauben
    * Die Anzahl der Regeln steigt exponentiell mit der Anzahl der Zustände, Wireworld(4 Zustände) hat 4^9= 4^9= 4^9=262144 mögliche Regeln.
    * Lösung: Ermöglichen des Ladens von Python-Funktionen aus einer Datei.
8. Ermöglichen des Speicherns/Ladens von Mustern.
9. besseres Interface
    * Dies geschah durch die Anzeige der verfügbaren Tastenkombinationen.
10. Nächster Schritt: Veränderbare Platinengröße und Zellengröße
    * Das Ändern der Zellengröße und der Boardgröße kann einfach sein, würde aber dazu führen, dass das Speichern und Laden abbricht und auch die Fenstergröße ändern müsste.

# Faltung

## Was ist eine Faltung?

Bei der Faltung wird eine Matrix verwendet und ein Kernel auf jede Zelle angewendet. Der Kernel ist auf die betroffene Zelle zentriert und beschreibt Gewichte für die Zelle und die Nachbarschaft der Zellen. Die Zelle und die Nachbarn werden dann mit dem entsprechenden Gewicht im Kernel multipliziert und dann summiert. Die resultierende Summe ist der Wert für die Zelle an der gleichen Position in der resultierenden Matrix.

## Auf das Spiel des Lebens anwenden

```
[[1 1 1]
 [1 0 1]
 [1 1 1]]
```

Der obige Kernel hat ein Gewicht von 1 für alle Zellen in der [Moore-Nachbarschaft](https://en.wikipedia.org/wiki/Moore_neighborhood) der Mittelzelle, vorausgesetzt, dass eine lebende Zelle einen Wert von 1 hat, bedeutet dies eine Faltung mit diesem Kernel, führt zu der Nachbarzahl einer Zelle in der resultierenden Zelle.

```
[[0 0 0 0]       [[2 3 2 1] 
 [1 1 1 0]   =>   [2 4 3 2] 
 [0 1 1 0]        [3 4 3 2] 
 [0 0 0 0]]       [1 2 2 1]]
```

Bei einer gegebenen Matrix, die die Zelle A und die gefaltete Matrix B enthält, können wir sagen, dass für jede beliebige Zelle bei x, y von A die Anzahl der Nachbarn in B bei x, y enthalten ist. Somit können wir für jede Zelle x, y, die in A enthalten ist entscheiden ob die nächste Generation lebt auf der Grundlage der Werte A[x, y] und B[x, y].
Dies vereinfacht das Problem sehr, da wir das Zählen der Nachbarn nicht selbst implementieren müssen, sondern stattdessen bestehende Faltungsfunktionen verwenden können.

## Matrix A loszuwerden.

Da die Anzahl der lebenden Nachbarn niemals 8 überschreiten kann, können wir das Zentrum des Kernels so definieren, dass es einen Wert von 9 hat:

```
[[1 1 1]
 [1 9 1]
 [1 1 1]]
```

Dabei enthält das Faltungsergebnis nicht nur die Anzahl der lebenden Nachbarn, sondern auch, ob die Zelle selbst lebendig oder tot ist oder nicht. Wenn die Zelle des Faltungsergebnisses größer oder gleich 9 ist, muss die ursprüngliche Zelle lebendig gewesen sein, sonst muss sie tot gewesen sein. Um die Anzahl der lebenden Nachbarn zu erhalten, können wir einfach 9 abziehen, wenn der Wert über 9 liegt, oder ihn wie sonst belassen wie er ist.
Auf diese Weise können wir auf der Grundlage von B[x,y] allein entscheiden, ob die nächste Generation lebt oder nicht. Da wir jetzt nur noch einen Wert haben, auf dem wir unsere Entscheidung basieren, können wir einfach die Regeln dafür ob die Zelle in der nächsten Generation lebendig sein soll oder nicht, durch einen flachen Array ausdrücken . Wenn der Wert in dem Array enthalten ist, ist es lebendig, andernfalls ist es tot. Auf diese Weise können wir das Regelwerk des Spiels des Lebens in nur 2 Objekten ausdrücken: 1. ein Kernel, 2. eine Liste von Ergebnissen, die zu einer lebenden Zelle führen.

## Aber warum?

Ich habe gehört, dass es möglich ist, das Spiel des Lebens mit Faltung zu implementieren, also habe ich es einfach getan. 

Übersetzt mit www.DeepL.com/Translator