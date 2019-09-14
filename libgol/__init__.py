from enum import Enum
import scipy
from scipy import misc
from scipy import signal
from time import sleep
from random import random 

DEAD=0
ALIVE=1

def create_board(width, height, initial_cell_state = DEAD):
    return scipy.full((height, width),initial_cell_state)

convolution_pattern = scipy.array([
    [1,1,1],
    [1,0,1],
    [1,1,1]])

def compute_generation(board, wrap = False, fill = DEAD, in_place = False):
    # convoltion that generates a new array that at any position has the amount of 
    convolved = signal.convolve2d(
        board,
        convolution_pattern,
        mode="same",
        boundary=("wrap" if wrap else "fill"),#if not wrapping treat out of bounds cells as if they had the state defined for fill
        fillvalue=fill)
    
    new_board = board if in_place else scipy.empty_like(board)
    for (x,y), neighbours in scipy.ndenumerate(convolved):
            new_board[x,y]=(DEAD if neighbours<=1 else
                            (DEAD if neighbours>=4 else
                            (ALIVE if neighbours==3 else
                            board[x,y])))
    return new_board

def randomize_board(board, ratio=.2, birth_only=False, in_place=False):
    new_board = board if in_place else scipy.empty_like(board)
    for (x,y), v in scipy.ndenumerate(new_board):
        new_board[x,y] = ALIVE if random()<=ratio else (board[x,y] if birth_only else DEAD)
    return new_board