import pygame
import pygame as pg
import sys
import os
import math
import random
import time
import numpy as np
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

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def main(self, display, framename, UP, DOWN, LEFT, RIGHT, attack):
        keys = pygame.key.get_pressed()
        # Player

        # Sprint
        if keys[pygame.K_LSHIFT]:
            aspeed = 8
        else:
            aspeed = 4


        # Forward Sword
        if keys[pygame.K_f] and (framename == 'f1sword' or framename == 'f2sword' or framename == 'f3sword' or framename == 'f4sword' or (keys[pygame.K_f] and framename == 'fwdstand')) and DOWN != 1:
        
            # Frame 1
            if int(time.time() * aspeed) % 4 == 1:
                frame = f1sword
                framename = 'f1sword'
            
            # Frame 2
            elif int(time.time() * aspeed) % 4 == 2:
                frame = f2sword
                framename = 'f2sword'

            # Frame 3
            if int(time.time() * aspeed) % 4 == 3:
                frame = f3sword
                framename = 'f3sword'
                attack = True

            # Frame 4
            elif int(time.time() * aspeed) % 4 == 0:
                frame = f4sword
                framename = 'f4sword'

            # Reset
            if keys[pygame.K_f] != True and (framename == 'f1sword' or framename == 'f2sword' or framename == 'f3sword' or framename == 'f4sword'):
                frame = fwdstand
                framename = 'fwdstand'

        # Right Sword
        elif keys[pygame.K_f] and (framename == 'r1sword' or framename == 'r2sword' or framename == 'r3sword' or framename == 'r4sword' or (keys[pygame.K_f] and framename == 'rgtstand')) and RIGHT != 1:
        
            # Frame 1
            if int(time.time() * aspeed) % 4 == 1:
                frame = r1sword
                framename = 'r1sword'
            
            # Frame 2
            elif int(time.time() * aspeed) % 4 == 2:
                frame = r2sword
                framename = 'r2sword'

            # Frame 3
            if int(time.time() * aspeed) % 4 == 3:
                frame = r3sword
                framename = 'r3sword'
                attack = True

            # Frame 4
            elif int(time.time() * aspeed) % 4 == 0:
                frame = r4sword
                framename = 'r4sword'

            # Reset
            if keys[pygame.K_f] != True and (framename == 'r1sword' or framename == 'r2sword' or framename == 'r3sword' or framename == 'r4sword'):
                frame = rgtstand
                framename = 'rgtstand'

        # Left Sword
        elif keys[pygame.K_f] and (framename == 'l1sword' or framename == 'l2sword' or framename == 'l3sword' or framename == 'l4sword' or (keys[pygame.K_f] and framename == 'lftstand')) and LEFT != 1:
        
            # Frame 1
            if int(time.time() * aspeed) % 4 == 1:
                frame = l1sword
                framename = 'l1sword'
            
            # Frame 2
            elif int(time.time() * aspeed) % 4 == 2:
                frame = l2sword
                framename = 'l2sword'

            # Frame 3
            if int(time.time() * aspeed) % 4 == 3:
                frame = l3sword
                framename = 'l3sword'
                attack = True

            # Frame 4
            elif int(time.time() * aspeed) % 4 == 0:
                frame = l4sword
                framename = 'l4sword'

            # Reset
            if keys[pygame.K_f] != True and (framename == 'l1sword' or framename == 'l2sword' or framename == 'l3sword' or framename == 'l4sword'):
                frame = lftstand
                framename = 'lftstand'

        # Backward Sword
        elif keys[pygame.K_f] and (framename == 'b1sword' or framename == 'b2sword' or framename == 'b3sword' or framename == 'b4sword' or (keys[pygame.K_f] and framename == 'bckstand')) and UP != 1:
        
            # Frame 1
            if int(time.time() * aspeed) % 4 == 1:
                frame = b1sword
                framename = 'b1sword'
            
            # Frame 2
            elif int(time.time() * aspeed) % 4 == 2:
                frame = b2sword
                framename = 'b2sword'

            # Frame 3
            if int(time.time() * aspeed) % 4 == 3:
                frame = b3sword
                framename = 'b3sword'
                attack = True


            # Frame 4
            elif int(time.time() * aspeed) % 4 == 0:
                frame = b4sword
                framename = 'b4sword'

            # Reset
            if keys[pygame.K_f] != True and (framename == 'b1sword' or framename == 'b2sword' or framename == 'b3sword' or framename == 'b4sword'):
                frame = bckstand
                framename = 'bckstand'


        # Movement Animations
        # Down
        elif DOWN == 1 and LEFT != 1 and RIGHT != 1 and UP != 1:
            # Down Frame 1
            if int(time.time() * aspeed) % 2 == 1:
                frame = fwdwalk1
                framename = 'fwdwalk1'
            
            # Down Frame 2
            elif int(time.time() * aspeed) % 2 == 0:
                frame = fwdwalk2
                framename = 'fwdwalk2'

        # Up
        elif UP == 1 and DOWN != 1:
            # Up Frame 1
            if int(time.time() * aspeed) % 2 == 1:
                frame = bckwalk1
                framename = 'bckwalk1'

            # Up Frame 2
            elif int(time.time() * aspeed) % 2 == 0:
                frame = bckwalk2
                framename = 'bckwalk2'

        # Right
        elif RIGHT == 1 and LEFT != 1 and UP != 1:
            # Right Frame 1
            if int(time.time() * aspeed) % 2 == 1:
                frame = rgtwalk1
                framename = 'rgtwalk1'

            # Right Frame 2
            elif int(time.time() * aspeed) % 2 == 0:
                frame = rgtwalk2
                framename = 'rgtwalk2'

        # Left
        elif LEFT == 1 and RIGHT != 1 and UP != 1:
            # Left Frame 1
            if int(time.time() * aspeed) % 2 == 1:
                frame = lftwalk1
                framename = 'lftwalk1'

            # Left Frame 2
            elif int(time.time() * aspeed) % 2 == 0:
                frame = lftwalk2
                framename = 'lftwalk2'

        else:
            # Still and facing Down
            if framename == 'fwdwalk1' or framename == 'fwdwalk2' or framename == 'fwdstand' or framename == 'f1sword' or framename == 'f2sword' or framename == 'f3sword' or framename == 'f4sword':
                frame = fwdstand
                framename = 'fwdstand'

            # Still and facing Up
            elif framename == 'bckwalk1' or framename == 'bckwalk2' or framename == 'bckstand' or framename == 'b1sword' or framename == 'b2sword' or framename == 'b3sword' or framename == 'b4sword':
                frame = bckstand
                framename = 'bckstand'
            
            # Still and facing Right
            elif framename == 'rgtwalk1' or framename == 'rgtwalk2' or framename == 'rgtstand' or framename == 'r1sword' or framename == 'r2sword' or framename == 'r3sword' or framename == 'r4sword':
                frame = rgtstand
                framename = 'rgtstand'

            # Still and facing Left
            elif framename == 'lftwalk1' or framename == 'lftwalk2' or framename == 'lftstand' or framename == 'l1sword' or framename == 'l2sword' or framename == 'l3sword' or framename == 'l4sword':
                frame = lftstand
                framename = 'lftstand'

            else:
                frame = fwdstand
                framename = 'fwdstand'

        # Generate Frame
        display.blit(frame, (self.x, self.y))

        # To ensure it doesn't default to fwdstand
        return framename, attack
