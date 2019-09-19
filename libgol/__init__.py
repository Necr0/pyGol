import random
from time import sleep
from math import floor, ceil

import scipy
from scipy.signal import convolve2d

DEAD = 0
ALIVE = 1

from typing import Tuple, Dict
Position = Tuple[int, int]

def modi(a:int, b:int) -> int:
    return a - a // b * b

class Chunk:
    def __init__(self, width:int, height:int):
        self.__occupied_cells = 0
        self.width = width
        self.height = height
        self.__array : scipy.ndarray = scipy.full((width, height), 0)

    def __getitem__(self, key:Position) -> int:
        return self.__array[key]

    def __setitem__(self, key:Position, value:int) -> None:
        if self.__array[key]==value:
            return
        self.__array[key]=value
        self.__occupied_cells += 1 if value else -1
    
    def empty(self) -> bool:
        return not self.__occupied_cells
    
    def __iter__(self):
        return (((x,y),self.__array[x,y]) for y in range(self.height) for x in range(self.width))

class Board:
    def __init__(self, chunk_size:int = 16):
        self.chunks : Dict[Position,Chunk]  = {}
        self.__CHUNK_SIZE = chunk_size

    def __chunk_for(self, pos:Position):
        chunk_pos= (pos[0]//self.__CHUNK_SIZE, pos[1]//self.__CHUNK_SIZE)
        if chunk_pos in self.chunks:
            return self.chunks[chunk_pos]
        return None

    def __create_chunk(self, pos):
        chunk = self.chunks[pos] = Chunk(self.__CHUNK_SIZE, self.__CHUNK_SIZE)
        return chunk

    def __getitem__(self, key):
        #TODO: Add a possibility to add a function that defines what undefined cells state is
        #Problem: if an out of bounds cell may have a value
        chunk = self.__chunk_for(key)
        return chunk[
                modi(key[0],self.__CHUNK_SIZE),
                modi(key[1],self.__CHUNK_SIZE)] if chunk else 0
    
    def __setitem__(self, key, value):
        chunk = self.__chunk_for(key)
        in_chunk_pos= (modi(key[0],self.__CHUNK_SIZE), modi(key[0],self.__CHUNK_SIZE))
        if not chunk:
            if not value:
                return
            chunk = self.__create_chunk((key[0]//self.__CHUNK_SIZE, key[1]//self.__CHUNK_SIZE))
        chunk[in_chunk_pos] = value
    
    def clear(self):
        self.chunks = {}

    def clean(self):
        for key in list(self.chunks.keys()):
            if self.chunks[key].empty():
                del self.chunks[key]
    
    def __iter__(self):
        return (
            (
                (chunk_pos[0]*self.__CHUNK_SIZE+in_chunk_pos[0], chunk_pos[1]*self.__CHUNK_SIZE+in_chunk_pos[1]),
                state
            )
            for chunk_pos, chunk in self.chunks.items()
            for in_chunk_pos, state in chunk)

    def reach_for_kernel(self, kernel):
        return (
            ceil(kernel.size[0]/self.__CHUNK_SIZE),
            ceil(kernel.size[1]/self.__CHUNK_SIZE))
    
    def convolve_at(self, pos: Position, kernel: scipy.ndarray):
        offset_x = (kernel.size[0]-1)//2
        offset_y = (kernel.size[1]-1)//2
        return sum(
            self[pos[0]+x-offset_x,pos[1]+y-offset_y] * weight
            for (x, y), weight in scipy.ndenumerate(kernel)
        )

    def compute_generation_at(self, pos: Position, ruleset):
        convolved = self.convolve_at(pos, ruleset["kernel"])

        if "transitions" in ruleset:  # if there is a simple dictionary for transitions given use it
            for transtion_state, transition_rule in ruleset['transitions'].items():
                if convolved in transition_rule:
                    return transtion_state
        if "transition_function" in ruleset:  # if a transition function is given use it instead
            return ruleset["transition_function"](convolved)

    def compute_generation(self, ruleset):
        new_chunks = {}
        chunks_to_compute = []

        kernel_reach_x, kernel_reach_y = self.reach_for_kernel(ruleset["kernel"])

        for chunk_pos_x, chunk_pos_y in self.chunks:
            for compute_y in range(chunk_pos_y-kernel_reach_y, chunk_pos_y+kernel_reach_y+1):
                for compute_x in range(chunk_pos_x-kernel_reach_x, chunk_pos_x+kernel_reach_x+1):
                    if (compute_x,compute_y) not in chunks_to_compute:
                        chunks_to_compute.append((compute_x,compute_y))
        
        #TODO: Multi-threading, it sounds insane for a small hobbist project but I am being serious
        for chunk_pos in chunks_to_compute:
            chunk = Chunk(self.__CHUNK_SIZE, self.__CHUNK_SIZE)
            for in_chunk_pos in chunk:
                chunk[in_chunk_pos] = self.compute_generation_at(
                    (chunk_pos[0]*self.__CHUNK_SIZE+in_chunk_pos[0],chunk_pos[1]*self.__CHUNK_SIZE+in_chunk_pos[1]),
                    ruleset)
            if not chunk.empty():
                new_chunks[chunk_pos] = chunk
        
        self.chunks = new_chunks
        
#b = Board()
#b[12,4] = 1
#b[2,16] = 1
#print(b.chunks)
#for pos, state in b:
#    print(pos)


def create_board(width:int, height:int, initial_cell_state:int=DEAD) -> scipy.ndarray:
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

def fill_board(board:scipy.ndarray, state:int=ALIVE, in_place:bool=False) -> scipy.ndarray:
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
