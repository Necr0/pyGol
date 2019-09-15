import scipy
from scipy.signal import convolve2d
from time import sleep
from random import random
from yaml import load

DEAD=0
ALIVE=1

def create_board(width, height, initial_cell_state = DEAD):
    return scipy.full((height, width),initial_cell_state)

def fill_board(board, state = ALIVE, in_place = False):
    if not in_place:
        return scipy.full_like(board,state)
    for (x,y), _ in scipy.ndenumerate(board):
        board[x,y] = state
  
# Game of Life
ruleset_gol={
    'kernel' : [[1,1,1],
                [1,9,1],
                [1,1,1]],
    'transitions' : {
        1 : [
            3, #spawn if neighbour count is 3
            2+9, #stay alive if neighbour count is 2 or 3
            3+9
        ]
    }
}

def compute_generation(board, ruleset=ruleset_gol, wrap=False, fill=0, in_place=False):
    # convoltion that generates a new array that at any position has the <del>amount of neighbours</del> result of the convolution
    convolved = convolve2d(
        board,
        ruleset["kernel"],
        mode="same",
        boundary=("wrap" if wrap else "fill"),#if not wrapping treat out of bounds cells as if they had the state defined for fill
        fillvalue=fill)
    
    #modify a new board if in_place is false else modify the existing board
    new_board = board if in_place else scipy.empty_like(board)

    for (x,y), neighbours in scipy.ndenumerate(convolved):
        new_state=0
        for transtion_state, transition_rule in ruleset['transitions'].items():
            if neighbours in transition_rule:
                new_state=transtion_state
                break
        new_board[x,y] = new_state

    return new_board

def randomize_board(board, ratio=.2, birth_only=False, in_place=False):
    new_board = board if in_place else scipy.empty_like(board)
    for (x,y), _ in scipy.ndenumerate(new_board):
        new_board[x,y] = ALIVE if random()<=ratio else (board[x,y] if birth_only else DEAD)
    return new_board