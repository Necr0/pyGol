import scipy
from scipy.signal import convolve2d
from time import sleep
from random import random

DEAD=0
ALIVE=1

def create_board(width, height, initial_cell_state = DEAD):
    return scipy.full((height, width),initial_cell_state)

def fill_board(board, state = ALIVE, in_place = False):
    if not in_place:
        return scipy.full_like(board,state)
    for (x,y), v in scipy.ndenumerate(board):
        board[x,y] = state
  
# Game of Life
kernel_gol=scipy.array([
    [1,1,1],
    [1,9,1],
    [1,1,1]])
heuristic_gol = [
    3, #spawn if neighbour count is 3
    2+9, #stay alive if neighbour count is 2 or 3
    3+9
]  

def compute_generation(board, kernel=kernel_gol, heuristic=heuristic_gol, wrap=False, fill=0, in_place=False):
    # convoltion that generates a new array that at any position has the <del>amount of neighbours</del> result of the convolution
    convolved = convolve2d(
        board,
        kernel,
        mode="same",
        boundary=("wrap" if wrap else "fill"),#if not wrapping treat out of bounds cells as if they had the state defined for fill
        fillvalue=fill)
    
    new_board = board if in_place else scipy.empty_like(board)
    for (x,y), neighbours in scipy.ndenumerate(convolved):
            new_board[x,y]=ALIVE if neighbours in heuristic else DEAD
    return new_board

def randomize_board(board, ratio=.2, birth_only=False, in_place=False):
    new_board = board if in_place else scipy.empty_like(board)
    for (x,y), v in scipy.ndenumerate(new_board):
        new_board[x,y] = ALIVE if random()<=ratio else (board[x,y] if birth_only else DEAD)
    return new_board


# Game of Life with knightsmoves as neighbourhood
kernel_knightsmoves=scipy.array([
    [0,1,0,1,0],
    [1,0,0,0,1],
    [0,0,9,0,0],
    [1,0,0,0,1],
    [0,1,0,1,0]])

# Seeds (https://en.wikipedia.org/wiki/Seeds_(cellular_automaton)):
heuristic_seeds = [2]

# Day and Night (https://en.wikipedia.org/wiki/Day_and_Night_(cellular_automaton)):
heuristic_dayandnight = [
    3,6,7,8,
    4+9
]

# Highlife (https://en.wikipedia.org/wiki/Highlife_(cellular_automaton)):
heuristic_highlife = [
    3,6,
    9+2,9+3
]

# Rule 110 (https://en.wikipedia.org/wiki/Rule_110): 
kernel_rule110=scipy.array([
    [0,8,0],
    [1,2,4],
    [0,0,0]])
heuristic_rule110 = [
    1,2,3,5,6,
    8,9,10,11,12,13,14,15#move the cell upward
]

# Rule 90 (https://en.wikipedia.org/wiki/Rule_90):
heuristic_rule90 = [
    1,3,4,6,
    8,9,10,11,12,13,14,15#move the cell upward
]
# Rule 30 (https://en.wikipedia.org/wiki/Rule_30):
heuristic_rule30 = [
    1,2,3,4,
    8,9,10,11,12,13,14,15#move the cell upward
]