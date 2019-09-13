from enum import Enum
import scipy
from scipy import misc
from scipy import signal
from time import sleep

DEAD=0
ALIVE=1

def create_board(width, height, initial_cell_state = DEAD):
    return scipy.full((height, width),initial_cell_state)

convolution_pattern = scipy.array([
    [1,1,1],
    [1,0,1],
    [1,1,1]])

def compute_generation(board, wrap = False, fill = DEAD):
    # convoltion that generates a new array that at any position has the amount of 
    convolved = signal.convolve2d(
        board,
        convolution_pattern,
        mode="same",
        boundary=("wrap" if wrap else "fill"),#if not wrapping treat out of bounds cells as if they had the state defined for fill
        fillvalue=fill)
    
    new_board = scipy.empty_like(board)
    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            new_board[y][x]=(DEAD if convolved[y][x]<=1 else
                            (DEAD if convolved[y][x]>=4 else
                            (ALIVE if convolved[y][x]==3 else
                            board[y][x])))
    return new_board

#Example test program demonstrating a glider and a blinker below
if __name__ == "__main__":
    a=create_board(14,14)
    #glider:
    a[0][1] = ALIVE
    a[1][2] = ALIVE
    a[2][0] = ALIVE
    a[2][1] = ALIVE
    a[2][2] = ALIVE
    #blinker:
    a[9][0] = ALIVE
    a[9][1] = ALIVE
    a[9][2] = ALIVE
    print(a)

    #game loop
    while True:
        a=compute_generation(a, True)
        print("-"*32)
        print(a)
        sleep(.15)