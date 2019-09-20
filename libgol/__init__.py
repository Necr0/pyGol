import random
from math import ceil, floor
from time import sleep
from typing import Dict, Tuple

import scipy as _sci

from .chunk import *
from .common import *


def modi(a:int, b:int) -> int:
    return a - a // b * b

class Board:
    def __init__(self, chunk_size:Tuple[int,int] = 16, max_chunk_count = 0):
        self.chunks : Dict[Position,Chunk]  = {}
        self.chunk_width, self.chunk_height = chunk_size
        self.max_chunk_count = max_chunk_count 

    def __chunk_for(self, pos:Position):
        chunk_pos= (pos[0]//self.chunk_width, pos[1]//self.chunk_height)
        if chunk_pos in self.chunks:
            return self.chunks[chunk_pos]
        return None

    def __create_chunk(self, pos):
        chunk = self.chunks[pos] = Chunk(self.chunk_width, self.chunk_height)
        return chunk

    def __getitem__(self, key):
        #TODO: Add a possibility to add a function that defines what undefined cells state is
        #Problem: if an out of bounds cell may have a value
        chunk = self.__chunk_for(key)
        return chunk[
                modi(key[0],self.chunk_width),
                modi(key[1],self.chunk_height)] if chunk else 0
    
    def __setitem__(self, key, value):
        chunk = self.__chunk_for(key)
        in_chunk_pos= (modi(key[0],self.chunk_width), modi(key[1],self.chunk_height))
        if not chunk:
            if not value or (self.max_chunk_count and len(self.chunks)>=self.max_chunk_count):
                return
            chunk = self.__create_chunk((key[0]//self.chunk_width, key[1]//self.chunk_height))
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
                (chunk_pos[0]*self.chunk_width+in_chunk_pos[0], chunk_pos[1]*self.chunk_height+in_chunk_pos[1]),
                state
            )
            for chunk_pos, chunk in self.chunks.items()
            for in_chunk_pos, state in chunk)

    def reach_for_kernel(self, kernel):
        return (
            ceil(kernel.shape[0]/self.chunk_width),
            ceil(kernel.shape[1]/self.chunk_height))
    
    def convolve_at(self, pos: Position, kernel: _sci.ndarray):
        offset_x = (kernel.shape[0]-1)//2
        offset_y = (kernel.shape[1]-1)//2
        return sum(
            self[pos[0]+x-offset_x,pos[1]+y-offset_y] * weight
            for (x, y), weight in _sci.ndenumerate(kernel)
        )

    def compute_generation_at(self, pos: Position, ruleset):
        convolved = self.convolve_at(pos, ruleset["kernel"])

        if "transitions" in ruleset:  # if there is a simple dictionary for transitions given use it
            for transtion_state, transition_rule in ruleset['transitions'].items():
                if convolved in transition_rule:
                    return transtion_state
        if "transition_function" in ruleset:  # if a transition function is given use it instead
            return ruleset["transition_function"](convolved)
        return 0

    def compute_generation(self, ruleset):
        new_chunks = {}
        chunks_to_compute = list(self.chunks)

        kernel_reach_x, kernel_reach_y = self.reach_for_kernel(ruleset["kernel"])

        for chunk_pos_x, chunk_pos_y in self.chunks:
            for compute_y in range(chunk_pos_y-kernel_reach_y, chunk_pos_y+kernel_reach_y+1):
                for compute_x in range(chunk_pos_x-kernel_reach_x, chunk_pos_x+kernel_reach_x+1):
                    if (compute_x,compute_y) not in chunks_to_compute:
                        chunks_to_compute.append((compute_x,compute_y))
        
        #TODO: Multi-threading, it sounds insane for a small hobbist project but I am being serious
        for chunk_pos in chunks_to_compute:
            chunk = Chunk(self.chunk_width, self.chunk_height)
            for in_chunk_pos, _ in chunk:
                chunk[in_chunk_pos] = self.compute_generation_at(
                    (chunk_pos[0]*self.chunk_width+in_chunk_pos[0],chunk_pos[1]*self.chunk_height+in_chunk_pos[1]),
                    ruleset)
            if not chunk.empty() and (not self.max_chunk_count or len(new_chunks)<self.max_chunk_count):
                new_chunks[chunk_pos] = chunk
        
        self.chunks = new_chunks

# Game of Life
ruleset_gol = {
    'kernel': _sci.array([[1, 1, 1],
                          [1, 9, 1],
                          [1, 1, 1]]),
    'transitions': {
        1: [
            3,  # spawn if neighbour count is 3
            2+9,  # stay alive if neighbour count is 2 or 3
            3+9
        ]
    }
}
