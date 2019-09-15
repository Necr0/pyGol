#!/usr/bin/env python3
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

NUMBER_KEYS = [
    pygame.K_0,
    pygame.K_1,
    pygame.K_2,
    pygame.K_3,
    pygame.K_4,
    pygame.K_5,
    pygame.K_6,
    pygame.K_7,
    pygame.K_8,
    pygame.K_9]

if __name__ == "__main__":
    root = Tk()
    root.withdraw()

    WIDTH = 1280
    HEIGHT = 720
    CELL_SIZE = 10

    wrap = True
    paused = False

    drawing = False
    draw_mode = libgol.ALIVE

    active_ruleset = load_ruleset("./rulesets/gol.yml")

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    board = libgol.create_board(WIDTH//CELL_SIZE, HEIGHT//CELL_SIZE)
    board = libgol.randomize_board(board)

    print("R: Randomize board")
    print("W: Toggle wrapping")
    print("C: Clear board")
    print("A: Load ruleset from file")
    print("1-9: Change state for drawing")
    print("Mouse Click+Drag: Draw state")
    print("Q: Quit")

    draw_board(screen, board)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN: #Handle key presses
                if event.key == pygame.K_q: #Quit on Q
                    sys.exit()
                if event.key == pygame.K_r: #Randomize on R
                    board = libgol.randomize_board(board, active_ruleset["states"])
                elif event.key == pygame.K_p: #Pause on P
                    paused = not paused
                elif event.key == pygame.K_w: #Toggle board wrapping on W
                    wrap = not wrap
                    print("Wrapping is now {}.".format("on" if wrap else "off"))
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
                        active_ruleset = load_ruleset(file)
                        print("Changed active ruleset to {}".format(file))
                elif event.key in NUMBER_KEYS:
                    draw_mode = NUMBER_KEYS.index(event.key)
                    print("Now drawing with cell state={}".format(draw_mode))
            elif event.type == pygame.MOUSEBUTTONDOWN: #Handle mouse drawing start
                if event.button == 1:
                    pos=screen_pos_to_cell(event.pos,CELL_SIZE)
                    board[pos] = draw_mode
                    drawing = True
            elif event.type == pygame.MOUSEBUTTONUP: #Handle mouse drawing end
                if event.button == 1:
                    drawing = False
            elif event.type == pygame.MOUSEMOTION: #Handle mouse drawing movement
                if drawing:
                    pos=screen_pos_to_cell(event.pos,CELL_SIZE)
                    board[pos] = draw_mode

        if not paused:
            board = libgol.compute_generation(board, ruleset=active_ruleset, wrap = wrap, fill=0)
        draw_board(
            screen,
            board,
            color_scheme=active_ruleset["colors"] if "colors" in active_ruleset else color_scheme_default)
        pygame.display.flip()
        sleep(.01)