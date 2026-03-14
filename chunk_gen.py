import pygame
import pygame as pg
import math
import random
import numpy as np
import time
import os
#from main import *
pygame.init()
pg.init()


# Screen Size
    #screen_width = 1280
    #screen_height = 720
    #display = pygame.display.set_mode((pygame.transform.scale(game_canvas, screen.get_size())))
    #display = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
seed = np.random.default_rng()
countplayeranimation = 0
pygame.mouse.set_visible(False)
wall_hitbox = []
slime_hitbox = []
LAST_BUTTON = ''
tile_size = 64
deleted_slimes = []
attack = False
slimelist = []
coins = 0
start_time = time.time()
    
tilemap = {}
CHUNK_SIZE = 8
    

def generate_chunk(x,y, coins):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            slime_here = 0
            tile_type = 0 # Floor
            local_diff = ((time.time() - start_time)/720) + (coins/1000)
            if local_diff >= 1:
                greenslimechance = 0.05
                purpleslimechance = 0.025
                blueslimechance = 0.0125
                yellowslimechance = 0.001
            else:
                greenslimechance = 0.025 * (local_diff + 1)
                purpleslimechance = 0.005 * ((local_diff * 5) + 1)
                blueslimechance = 0.00125 * ((local_diff * 10) + 1)
                yellowslimechance = 0.00001 * ((local_diff * 100) + 1)

            if seed.random() <= greenslimechance:
                slime_here = 1
            elif seed.random() <= purpleslimechance:
                slime_here = 2
            elif seed.random() <= blueslimechance:
                slime_here = 3
            elif seed.random() <= yellowslimechance:
                slime_here = 4
            # Temp Random Tile Gen (1 in 5 chance of being a wall) replace with perlin noise when possible
            elif seed.random() <= 0.2:
                tile_type = 1 # Wall
            # Add Tile to Chunk
            chunk_data.append([[target_x, target_y], tile_type, slime_here])
    return chunk_data


