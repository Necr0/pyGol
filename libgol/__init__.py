import random
from time import sleep

import scipy
from scipy.signal import convolve2d
from yaml import load

DEAD = 0
ALIVE = 1


def create_board(width, height, initial_cell_state=DEAD):
    """
    Creates a new 2D NumPy array representing a board with the given dimensions
    and returns it.

    Parameters
    ----------
    width : int
        The width of the created board.
    width : int
        The height of the created board.
    initial_cell_state : int, Optional
        The state that all board cells should be initialized with.
        (default: DEAD)
    """
    return scipy.full((width, height), initial_cell_state)


def fill_board(board, state=ALIVE, in_place=False):
    """
    Takes a board and fills all cells with the given state or ALIVE

    Parameters
    ----------
    board : scipy.ndarray
        A 2 dimensional NumPy array representing the board.
    state : int, optional 
        The state to fill the cells with. (default: ALIVE)
    in_place : Boolean, optional
        wether or not the given board object should be modified or a new array
        should be created (default: False)
    """
    if not in_place:
        return scipy.full_like(board, state)
    for (x, y), _ in scipy.ndenumerate(board):
        board[x, y] = state


# Game of Life
ruleset_gol = {
    'kernel': [[1, 1, 1],
               [1, 9, 1],
               [1, 1, 1]],
    'transitions': {
        1: [
            3,  # spawn if neighbour count is 3
            2+9,  # stay alive if neighbour count is 2 or 3
            3+9
        ]
    }
}


def compute_generation(board, ruleset=ruleset_gol, wrap=False, fill=DEAD, in_place=False):
    """
    Takes a board and computes the next generation for that board according to
    the given ruleset or the Game of Life ruleset.

    Parameters
    ----------
    board : scipy.ndarray
        A 2 dimensional NumPy array representing the board
    ruleset : dict, optional 
        A dictionary defining the ruleset. Defaults to ruleset_gol.
        according to the schema 
        {
            kernel:<2d array-like object with uneven dimensions>,
            transitions?:{<result state>:[<convolution results>]},
            transition_function?: (<convolution result>:int)->int
        }  
    wrap : Boolean, optional
        wether or not the board should wrap around for out of bounds positions
        (default: False)
    fill : int, optional
        what cell state to treat the out of bounds borders as when wrapping
        is off (default: DEAD)
    in_place : Boolean, optional
        wether or not the given board object should be modified or a new array
        should be created (default: False)
    """
    #convoltion that generates a new array that at any position has the <del>amount of neighbours</del> result of the convolution
    convolved = convolve2d(
        board,
        ruleset["kernel"],
        mode="same",
        # if not wrapping treat out of bounds cells as if they had the state defined for fill
        boundary=("wrap" if wrap else "fill"),
        fillvalue=fill)

    # modify a new board if in_place is false else modify the existing board
    new_board = board if in_place else scipy.empty_like(board)

    # iterate every cell in the convolved array
    for (x, y), neighbours in scipy.ndenumerate(convolved):

        new_state = 0  # default to 0 for new state

        if "transitions" in ruleset:  # if there is a simple dictionary for transitions given use it
            for transtion_state, transition_rule in ruleset['transitions'].items():
                if neighbours in transition_rule:
                    new_state = transtion_state
                    break
        elif "transition_function" in ruleset:  # if a transition function is given use it instead
            new_state = ruleset["transition_function"](neighbours)

        new_board[x, y] = new_state  # set the cells new state to the result

    return new_board


def randomize_board(board, states=[DEAD, ALIVE], in_place=False):
    """
    Takes a board and  randomly fills each cell with one of the given states.

    Parameters
    ----------
    board : scipy.ndarray
        A 2 dimensional NumPy array representing the board.
    states : sequence, optional 
        A sequence of states to randomly fill the board cells from.
        Multiple copies a state can be contained within the sequence to give
        give a higher weight to the state in question.
        (default: [ALIVE, DEAD])
    in_place : Boolean, optional
        wether or not the given board object should be modified or a new array
        should be created (default: False)
    """
    new_board = board if in_place else scipy.empty_like(board)
    for (x, y), _ in scipy.ndenumerate(new_board):
        new_board[x, y] = random.choice(states)
    return new_board
