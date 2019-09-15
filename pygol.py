import pygame
import libgol
import sys
from time import sleep
from os import listdir
import yaml

def draw_board(surface, board):
    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            pygame.draw.rect(
                surface,
                COLOR_ALIVE if board[y][x] else COLOR_DEAD,
                (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def screen_pos_to_cell(pos,cell_size):
    return (pos[0]//cell_size,pos[1]//cell_size)

print(yaml.dump(lambda x,y: x))

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

    RULESETS = []
    with open("./rulesets/day_and_night.yml", 'r') as stream:
        RULESETS.append(yaml.safe_load(stream))
    ACTIVE_RULESET = 0
    print(RULESETS)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    board=libgol.create_board(WIDTH//CELL_SIZE,HEIGHT//CELL_SIZE)
    board = libgol.randomize_board(board,.5)

    draw_board(screen, board)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN: #Handle key presses
                if event.key == pygame.K_r: #Randomize on R
                    board = libgol.randomize_board(board)
                elif event.key == pygame.K_p: #Pause on P
                    PAUSED = not PAUSED
                elif event.key == pygame.K_w: #Toggle board wrapping on W
                    WRAP = not WRAP
                elif event.key == pygame.K_c: #Clear on C
                    board = libgol.fill_board(board, libgol.DEAD)
            elif event.type == pygame.MOUSEBUTTONDOWN: #Handle mouse drawing start
                if event.button == 1:
                    pos=screen_pos_to_cell(event.pos,CELL_SIZE)
                    board[pos[1],pos[0]] = DRAW_MODE = libgol.ALIVE if board[pos[1],pos[0]]==libgol.DEAD else libgol.DEAD
                    DRAWING = True
            elif event.type == pygame.MOUSEBUTTONUP: #Handle mouse drawing end
                if event.button == 1:
                    DRAWING = False
            elif event.type == pygame.MOUSEMOTION: #Handle mouse drawing movement
                if DRAWING:
                    pos=screen_pos_to_cell(event.pos,CELL_SIZE)
                    board[pos[1],pos[0]] = DRAW_MODE

        if not PAUSED:
            board = libgol.compute_generation(board, ruleset=RULESETS[ACTIVE_RULESET], wrap = WRAP, fill=1)
        draw_board(screen, board)
        pygame.display.flip()
        sleep(.01)