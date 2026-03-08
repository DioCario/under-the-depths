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
    
    # Load Tiles
floor,wallimg = pg.image.load(os.path.join('assets', 'images', 'floor tile.png')).convert(),pg.image.load(os.path.join('assets', 'images', 'wall tile.png')).convert()
wall = wallimg.get_rect()


tilemap = {}
CHUNK_SIZE = 8
    
    # Music
introsong = pygame.mixer.Sound(os.path.join('assets', 'songs', 'intro.ogg'))
bgsong1 = pygame.mixer.Sound(os.path.join('assets', 'songs', 'background1.ogg'))
introchannel = pygame.mixer.Channel(0)
bgchannel = pygame.mixer.Channel(1)
    
    
    # UI
zero = pg.image.load(os.path.join('assets', 'ui', '0.png')).convert_alpha()
one = pg.image.load(os.path.join('assets', 'ui', '1.png')).convert_alpha()
two = pg.image.load(os.path.join('assets', 'ui', '2.png')).convert_alpha()
three = pg.image.load(os.path.join('assets', 'ui', '3.png')).convert_alpha()
four = pg.image.load(os.path.join('assets', 'ui', '4.png')).convert_alpha()
five = pg.image.load(os.path.join('assets', 'ui', '5.png')).convert_alpha()
six = pg.image.load(os.path.join('assets', 'ui', '6.png')).convert_alpha()
seven = pg.image.load(os.path.join('assets', 'ui', '7.png')).convert_alpha()
eight = pg.image.load(os.path.join('assets', 'ui', '8.png')).convert_alpha()
nine = pg.image.load(os.path.join('assets', 'ui', '9.png')).convert_alpha()

ui = pg.image.load(os.path.join('assets', 'ui', 'coinui.png')).convert_alpha()
    
    

    # Load Player Animations
    # Down
fwdstand = pg.image.load(os.path.join('assets', 'images', 'player', 'fwdstand.png')).convert_alpha()
fwdwalk1 = pg.image.load(os.path.join('assets', 'images', 'player', 'fwdwalk1.png')).convert_alpha()
fwdwalk2 = pg.image.load(os.path.join('assets', 'images', 'player', 'fwdwalk2.png')).convert_alpha()
    
    # Up
bckstand = pg.image.load(os.path.join('assets', 'images', 'player', 'bckstand.png')).convert_alpha()
bckwalk1 = pg.image.load(os.path.join('assets', 'images', 'player', 'bckwalk1.png')).convert_alpha()
bckwalk2 = pg.image.load(os.path.join('assets', 'images', 'player', 'bckwalk2.png')).convert_alpha()
    
    # Right
rgtstand = pg.image.load(os.path.join('assets', 'images', 'player', 'rgtstand.png')).convert_alpha()
rgtwalk1 = pg.image.load(os.path.join('assets', 'images', 'player', 'rgtwalk1.png')).convert_alpha()
rgtwalk2 = pg.image.load(os.path.join('assets', 'images', 'player', 'rgtwalk2.png')).convert_alpha()
    
    # Left
lftstand = pg.image.load(os.path.join('assets', 'images', 'player', 'lftstand.png')).convert_alpha()
lftwalk1 = pg.image.load(os.path.join('assets', 'images', 'player', 'lftwalk1.png')).convert_alpha()
lftwalk2 = pg.image.load(os.path.join('assets', 'images', 'player', 'lftwalk2.png')).convert_alpha()
    
    # Forward Sword
f1sword = pg.image.load(os.path.join('assets', 'images', 'player', 'f1sword.png')).convert_alpha()
f2sword = pg.image.load(os.path.join('assets', 'images', 'player', 'f2sword.png')).convert_alpha()
f3sword = pg.image.load(os.path.join('assets', 'images', 'player', 'f3sword.png')).convert_alpha()
f4sword = pg.image.load(os.path.join('assets', 'images', 'player', 'f4sword.png')).convert_alpha()
    
    # Right Sword
r1sword = pg.image.load(os.path.join('assets', 'images', 'player', 'r1sword.png')).convert_alpha()
r2sword = pg.image.load(os.path.join('assets', 'images', 'player', 'r2sword.png')).convert_alpha()
r3sword = pg.image.load(os.path.join('assets', 'images', 'player', 'r3sword.png')).convert_alpha()
r4sword = pg.image.load(os.path.join('assets', 'images', 'player', 'r4sword.png')).convert_alpha()

    # Left Sword
l1sword = pg.image.load(os.path.join('assets', 'images', 'player', 'l1sword.png')).convert_alpha()
l2sword = pg.image.load(os.path.join('assets', 'images', 'player', 'l2sword.png')).convert_alpha()
l3sword = pg.image.load(os.path.join('assets', 'images', 'player', 'l3sword.png')).convert_alpha()
l4sword = pg.image.load(os.path.join('assets', 'images', 'player', 'l4sword.png')).convert_alpha()

    # Backward Sword
b1sword = pg.image.load(os.path.join('assets', 'images', 'player', 'b1sword.png')).convert_alpha()
b2sword = pg.image.load(os.path.join('assets', 'images', 'player', 'b2sword.png')).convert_alpha()
b3sword = pg.image.load(os.path.join('assets', 'images', 'player', 'b3sword.png')).convert_alpha()
b4sword = pg.image.load(os.path.join('assets', 'images', 'player', 'b4sword.png')).convert_alpha()
    
    # Blob
f1slimegreen = pg.image.load(os.path.join('assets', 'images', 'blob', 'slimejump1.png')).convert_alpha()
f2slimegreen = pg.image.load(os.path.join('assets', 'images', 'blob', 'slimejump2.png')).convert_alpha()
f3slimegreen = pg.image.load(os.path.join('assets', 'images', 'blob', 'slimejump3.png')).convert_alpha()
f4slimegreen = pg.image.load(os.path.join('assets', 'images', 'blob', 'slimejump4.png')).convert_alpha()
f5slimegreen = pg.image.load(os.path.join('assets', 'images', 'blob', 'slimejump5.png')).convert_alpha()
f6slimegreen = pg.image.load(os.path.join('assets', 'images', 'blob', 'slimejump6.png')).convert_alpha()
f7slimegreen = pg.image.load(os.path.join('assets', 'images', 'blob', 'slimejump7.png')).convert_alpha()
f8slimegreen = pg.image.load(os.path.join('assets', 'images', 'blob', 'slimejump8.png')).convert_alpha()
    


    #Index Tiles
tile_index = {0:floor,
              1:wall}
    
slime_index = {0:f1slimegreen,
               1:f2slimegreen,
               2:f3slimegreen,
               3:f4slimegreen,
               4:f5slimegreen,
               5:f6slimegreen,
               6:f7slimegreen,
               7:f8slimegreen,
                }    

    # Starting Frame
framename = 'fwdstand'

    # 36 so the player is within 1 tile
display_scroll = [0,36]

    # To fix spawning on a wall, used so it doesn't run as hard in the background
FIRST_LOOP = True

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
            else:
                greenslimechance = 0.025 * (local_diff + 1)
            if seed.random() <= 0.025:
                slime_here = 1
            # Temp Random Tile Gen (1 in 5 chance of being a wall) replace with perlin noise when possible
            elif seed.random() <= 0.2:
                tile_type = 1 # Wall
            # Add Tile to Chunk
            chunk_data.append([[target_x, target_y], tile_type, slime_here])
    return chunk_data
