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

# Implementation
1. Implemented the games generation function "next_generation" as well as a helper function
2. Implement a visualization of the game for a MVP
3. Add interactivity (added some keys)
4. Custom Generator Functions
6. Added mouse drawing
5. All Generator functions can be expressed as a kernel(=convolution matrix) and an array containing the results after convolution that cause the cell to be alive (the cells own state is contained in the convolution matrix)
6. Next step: load patterns from file
7. Next step: Allow more than 1 state
8. Next step: Allow saving/loading of patterns