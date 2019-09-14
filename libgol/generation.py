def compute_generic_convolution_generation(board, kernel, heuristic):
    # convoltion that generates a new array that at any position has the amount of 
    convolved = signal.convolve2d(
        board,
        kernel,
        mode="same",
        boundary=("wrap" if wrap else "fill"),#if not wrapping treat out of bounds cells as if they had the state defined for fill
        fillvalue=fill)
    
    new_board = board if in_place else scipy.empty_like(board)
    for (x,y), neighbours in scipy.ndenumerate(convolved):
            new_board[x,y]=heuristic(board[x,y],neighbours,x,y,board)
    return new_board