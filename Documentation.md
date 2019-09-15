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
