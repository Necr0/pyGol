from scipy import array, ndenumerate, empty_like
from scipy.signal import convolve2d

DEAD=0
ALIVE=1

def compute_generic_convolution_generation(board, kernel, heuristic, wrap=False, fill=0, in_place=False):
    # convoltion that generates a new array that at any position has the amount of 
    convolved = convolve2d(
        board,
        kernel,
        mode="same",
        boundary=("wrap" if wrap else "fill"),#if not wrapping treat out of bounds cells as if they had the state defined for fill
        fillvalue=fill)
    
    new_board = board if in_place else empty_like(board)
    for (x,y), neighbours in ndenumerate(convolved):
            new_board[x,y]=heuristic(board[x,y],neighbours,x,y,board)
    return new_board

kernel_gol=array([
    [1,1,1],
    [1,0,1],
    [1,1,1]])
heuristic_gol = lambda state, neighbours, x, y, board: (DEAD if neighbours<=1 else
                                                        (DEAD if neighbours>=4 else
                                                        (ALIVE if neighbours==3 else
                                                        state)))

kernel_knightsmoves=array([
    [0,1,0,1,0],
    [1,0,0,0,1],
    [0,0,0,0,0],
    [1,0,0,0,1],
    [0,1,0,1,0]
])
def compute_knightsmoves_generation(board, wrap=False, fill=0, in_place=False):
    compute_generic_convolution_generation(board, kernel_knightsmoves, heuritic_gol, wrap, fill, in_place)