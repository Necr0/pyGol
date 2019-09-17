#!/usr/bin/env python3
import importlib.util
import sys
from os import listdir, path
from time import sleep
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

import pygame
import scipy
import yaml

import libgol

color_scheme_default = {
    0: (255, 255, 255),
    1: (0,   0,   0)
}


def draw_board(surface, board, cell_size, color_scheme=color_scheme_default):
    for (x, y), state in scipy.ndenumerate(board):
        pygame.draw.rect(
            surface,
            color_scheme[state] if state in color_scheme else color_scheme_default[1],
            (x*cell_size, y*cell_size, cell_size, cell_size))

def draw_cursor(surface, pos, cell_size):
    if cell_size<3:
        return
    pygame.draw.rect(
        screen,
        (0,0,0),
        (pos[0]*cell_size,pos[1]*cell_size, cell_size, cell_size),
        2)
    pygame.draw.rect(
        screen,
        (255,255,255),
        (pos[0]*cell_size,pos[1]*cell_size, cell_size, cell_size),
        1)

def screen_pos_to_cell(pos, cell_size):
    return (pos[0]//cell_size, pos[1]//cell_size)


def load_yaml_file(yaml_path):
    with open(yaml_path, 'r') as stream:
        return yaml.safe_load(stream)  # parse yaml


def load_ruleset(yaml_path):
    ruleset = load_yaml_file(yaml_path)

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
        ruleset["states"] = [0, 1]

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
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF|pygame.HWSURFACE)

    board = libgol.create_board(WIDTH//CELL_SIZE, HEIGHT//CELL_SIZE)
    board = libgol.randomize_board(board)

    INTERVAL_STEPS = .01
    interval = .02

    print("P: Toggle pause")
    print("N: Progress single generation")
    print("R: Randomize board")
    print("W: Toggle wrapping")
    print("C: Clear board")
    print("A: Load ruleset from file")
    print("S: Save snapshot to file")
    print("L: Load snapshot from file")
    print("Right: Increase speed")
    print("Left: Decrease speed")
    print("0-9: Change state for drawing")
    print("Mouse Click+Drag: Draw state")
    print("Q: Quit")

    draw_board(screen, board, CELL_SIZE)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # Handle key presses

                if event.key == pygame.K_q:  # Quit on Q
                    sys.exit()

                if event.key == pygame.K_r:  # Randomize on R
                    board = libgol.randomize_board(
                        board, active_ruleset["states"])

                elif event.key == pygame.K_p:  # Pause on P
                    paused = not paused
                    print("Game is now {}.".format(
                        "paused" if paused else "unpaused"))

                elif event.key == pygame.K_w:  # Toggle board wrapping on W
                    wrap = not wrap
                    print("Wrapping is now {}.".format(
                        "on" if wrap else "off"))

                elif event.key == pygame.K_c:  # Clear on C
                    board = libgol.fill_board(board, libgol.DEAD)

                elif event.key == pygame.K_a:  # Load ruleset
                    file = askopenfilename(
                        initialdir="./rulesets/",
                        title="Select ruleset",
                        filetypes=(
                            ("YAML files", "*.yml *.yaml"),
                            ("All files", "*.*")))
                    if file:
                        active_ruleset = load_ruleset(file)
                        print("Changed active ruleset to {}".format(file))

                elif event.key == pygame.K_s:  # Save snapshot
                    file = asksaveasfilename(
                        initialdir="./snapshots/",
                        title="Save snapshot")
                    if file:
                        scipy.save(file, board)
                        print("Saved snapshot to {}".format(file))

                elif event.key == pygame.K_l:  # Load snapshot
                    file = askopenfilename(
                        initialdir="./snapshots/",
                        title="Load snapshot",
                        filetypes=(
                            ("NumPy array files", "*.npy"),
                            ("All files", "*.*")))
                    if file:
                        board = scipy.load(file)
                        print("Loaded snapshot from {}".format(file))

                elif event.key == pygame.K_n:  # Progress single generation and pause on N
                    if not paused:
                        paused = True
                    board = libgol.compute_generation(
                        board, ruleset=active_ruleset, wrap=wrap)

                elif event.key == pygame.K_RIGHT:  # Increase speed on Right Arrow
                    interval = max(interval-INTERVAL_STEPS, 0)
                    print("Interval is now {} seconds.".format(interval))

                elif event.key == pygame.K_LEFT:  # Decrease speed on Left Arrow
                    interval = min(interval+INTERVAL_STEPS, 60)
                    print("Interval is now {} seconds.".format(interval))

                elif event.key in NUMBER_KEYS:
                    draw_mode = NUMBER_KEYS.index(event.key)
                    print("Now drawing with cell state={}".format(draw_mode))

            elif event.type == pygame.MOUSEBUTTONDOWN:  # Handle mouse drawing start
                if event.button == 1:
                    pos = screen_pos_to_cell(event.pos, CELL_SIZE)
                    board[pos] = draw_mode
                    drawing = True
            elif event.type == pygame.MOUSEBUTTONUP:  # Handle mouse drawing end
                if event.button == 1:
                    drawing = False
            elif event.type == pygame.MOUSEMOTION:  # Handle mouse drawing movement
                if drawing:
                    pos = screen_pos_to_cell(event.pos, CELL_SIZE)
                    board[pos] = draw_mode

        if not paused:
            board = libgol.compute_generation(
                board, ruleset=active_ruleset, wrap=wrap)
        draw_board(
            screen,
            board,
            CELL_SIZE,
            color_scheme=active_ruleset["colors"] if "colors" in active_ruleset else color_scheme_default)
        draw_cursor(
            screen,
            screen_pos_to_cell(pygame.mouse.get_pos(), CELL_SIZE),
            CELL_SIZE)
        
        pygame.display.flip()
        sleep(interval)
