import pygame
import libgol
import sys
from time import sleep
from os import listdir, path
import yaml
import importlib.util
import scipy
from tkinter import Tk
from tkinter.filedialog import askopenfilename

color_scheme_default = {
    0: (255, 255, 255),
    1: (0,   0,   0  )
}

def draw_board(surface, board, color_scheme=color_scheme_default):
    for (x,y), state in scipy.ndenumerate(board):
        pygame.draw.rect(
            surface,
            color_scheme[state] if state in color_scheme else (0,0,0),
            (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def screen_pos_to_cell(pos,cell_size):
    return (pos[0]//cell_size,pos[1]//cell_size)

def load_ruleset(yaml_path):
    with open(yaml_path, 'r') as stream:

        ruleset=yaml.safe_load(stream) #parse yaml

        if "transition_function_file" in ruleset:
            spec = importlib.util.spec_from_file_location(
                __name__,
                path.join(path.dirname(yaml_path),
                        ruleset["transition_function_file"])
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            ruleset["transition_function"] = module.transition
        
        if "states" not in ruleset:
            ruleset["states"]=[0,1]
        
        return ruleset

if __name__ == "__main__":
    root = Tk()
    root.withdraw()

    WIDTH = 600
    HEIGHT = 400
    CELL_SIZE = 10

    WRAP = True
    PAUSED = False

    DRAWING = False
    DRAW_MODE = libgol.ALIVE # libgol.ALIVE | libgol.DEAD

    ACTIVE_RULESET = load_ruleset("./rulesets/gol.yml")

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    board = libgol.create_board(WIDTH//CELL_SIZE, HEIGHT//CELL_SIZE)
    board = libgol.randomize_board(board)

    draw_board(screen, board)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN: #Handle key presses
                if event.key == pygame.K_r: #Randomize on R
                    board = libgol.randomize_board(board, ACTIVE_RULESET["states"])
                elif event.key == pygame.K_p: #Pause on P
                    PAUSED = not PAUSED
                elif event.key == pygame.K_w: #Toggle board wrapping on W
                    WRAP = not WRAP
                elif event.key == pygame.K_c: #Clear on C
                    board = libgol.fill_board(board, libgol.DEAD)
                elif event.key == pygame.K_a: #Load ruleset
                    file = askopenfilename(
                                initialdir="./rulesets/",
                                title="Select ruleset",
                                filetypes=(
                                    ("YAML files","*.yml *.yaml"),
                                    ("All files","*.*")))
                    if file:
                        ACTIVE_RULESET = load_ruleset(file)
            elif event.type == pygame.MOUSEBUTTONDOWN: #Handle mouse drawing start
                if event.button == 1:
                    pos=screen_pos_to_cell(event.pos,CELL_SIZE)
                    board[pos[0],pos[1]] = DRAW_MODE = libgol.ALIVE if board[pos]==libgol.DEAD else libgol.DEAD
                    DRAWING = True
            elif event.type == pygame.MOUSEBUTTONUP: #Handle mouse drawing end
                if event.button == 1:
                    DRAWING = False
            elif event.type == pygame.MOUSEMOTION: #Handle mouse drawing movement
                if DRAWING:
                    pos=screen_pos_to_cell(event.pos,CELL_SIZE)
                    board[pos[0],pos[1]] = DRAW_MODE

        if not PAUSED:
            board = libgol.compute_generation(board, ruleset=ACTIVE_RULESET, wrap = WRAP, fill=0)
        draw_board(
            screen,
            board,
            color_scheme=ACTIVE_RULESET["colors"] if "colors" in ACTIVE_RULESET else color_scheme_default)
        pygame.display.flip()
        sleep(.01)