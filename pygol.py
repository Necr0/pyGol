import pygame
import libgol
import sys
from time import sleep

def draw_board(surface, board):
    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            pygame.draw.rect(
                surface,
                COLOR_ALIVE if board[y][x] else COLOR_DEAD,
                (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def screen_pos_to_cell(pos,cell_size):
    return (pos[0]//cell_size,pos[1]//cell_size)

if __name__ == "__main__":
    WIDTH = 600
    HEIGHT = 400
    CELL_SIZE = 10

    COLOR_DEAD = (255,255,255)
    COLOR_ALIVE = (0,0,0)

    WRAP = True
    PAUSED = False

    DRAWING = False
    DRAW_MODE = libgol.ALIVE # libgol.ALIVE | libgol.DEAD

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    board=libgol.create_board(WIDTH//CELL_SIZE,HEIGHT//CELL_SIZE)
    board = libgol.randomize_board(board)

    draw_board(screen, board)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = libgol.randomize_board(board)
                elif event.key == pygame.K_p:
                    PAUSED = not PAUSED
                elif event.key == pygame.K_w:
                    WRAP = not WRAP
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos=screen_pos_to_cell(event.pos,CELL_SIZE)
                    board[pos[1],pos[0]] = DRAW_MODE = libgol.ALIVE if board[pos[1],pos[0]]==libgol.DEAD else libgol.DEAD
                    DRAWING = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    DRAWING = False
            elif event.type == pygame.MOUSEMOTION:
                if DRAWING:
                    pos=screen_pos_to_cell(event.pos,CELL_SIZE)
                    board[pos[1],pos[0]] = DRAW_MODE

        if not PAUSED:
            board = libgol.compute_knightsmoves_generation(board, WRAP)
        draw_board(screen, board)
        pygame.display.flip()
        sleep(.01)