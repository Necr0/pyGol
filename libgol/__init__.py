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
    

def compute_generic_convolution_generation(board, kernel, heuristic, wrap=False, fill=0, in_place=False):
    # convoltion that generates a new array that at any position has the amount of 
    convolved = convolve2d(
        board,
        kernel,
        mode="same",
        boundary=("wrap" if wrap else "fill"),#if not wrapping treat out of bounds cells as if they had the state defined for fill
        fillvalue=fill)
    
    new_board = board if in_place else scipy.empty_like(board)
    for (x,y), neighbours in scipy.ndenumerate(convolved):
            new_board[x,y]=heuristic(board[x,y],neighbours,x,y,board)
    return new_board

kernel_gol=scipy.array([
    [1,1,1],
    [1,0,1],
    [1,1,1]])
heuristic_gol = lambda state, neighbours, x, y, board: (DEAD if neighbours<=1 else
                                                        (DEAD if neighbours>=4 else
                                                        (ALIVE if neighbours==3 else
                                                        state)))
def compute_generation(board, wrap = False, fill = DEAD, in_place = False):
    return compute_generic_convolution_generation(board, kernel_gol, heuristic_gol, wrap, fill, in_place)

kernel_knightsmoves=scipy.array([
    [0,1,0,1,0],
    [1,0,0,0,1],
    [0,0,0,0,0],
    [1,0,0,0,1],
    [0,1,0,1,0]])
def compute_knightsmoves_generation(board, wrap=False, fill=DEAD, in_place=False):
    return compute_generic_convolution_generation(board, kernel_knightsmoves, heuristic_gol, wrap, fill, in_place)

# Day and Night (https://en.wikipedia.org/wiki/Day_and_Night_(cellular_automaton)):
heuristic_dayandnight = lambda state, neighbours, x, y, board: (ALIVE if neighbours in [3,6,7,8] and state==DEAD else
                                                                (state if neighbours in [3,4,6,7,8] else DEAD))
def compute_dayandnight_generation(board, wrap = False, fill = DEAD, in_place = False):
    return compute_generic_convolution_generation(board, kernel_gol, heuristic_dayandnight, wrap, fill, in_place)

# Rule 110 (https://en.wikipedia.org/wiki/Rule_110): 
kernel_rule110=scipy.array([
    [0,8,0],
    [1,2,4],
    [0,0,0]])
heuristic_rule110 = lambda state, neighbours, x, y, board: (ALIVE if neighbours>=8 or neighbours in [1,2,3,5,6] else DEAD)
def compute_rule110_generation(board, wrap = False, fill = DEAD, in_place = False):
    return compute_generic_convolution_generation(board, kernel_rule110, heuristic_rule110, wrap, fill, in_place)


def randomize_board(board, ratio=.2, birth_only=False, in_place=False):
    new_board = board if in_place else scipy.empty_like(board)
    for (x,y), v in scipy.ndenumerate(new_board):
        new_board[x,y] = ALIVE if random()<=ratio else (board[x,y] if birth_only else DEAD)
    return new_board