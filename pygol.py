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

if __name__ == "__main__":
    WIDTH = 600
    HEIGHT = 400
    CELL_SIZE = 10

    COLOR_DEAD = (255,255,255)
    COLOR_ALIVE = (0,0,0)

    WRAP = True
    PAUSED = False

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

        sleep(.01)
        if not PAUSED:
            board = libgol.compute_generation(board, WRAP)
            draw_board(screen, board)

        pygame.display.flip()