# Preparation

## General considerations

I created an empty git repository to keep track of my progress
and I decided to go with the Unlicese because it is my license
of choice for leisure projects.

## Choice of programming language and frameworks

Python was chosen as it can be used for fast prototyping while 
the language itself has things such as classes and modules to
help structuring the code and significant whitespace keeping the
code clean even if the project gro ws older and larger. The
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