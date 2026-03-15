import pygame
import pygame as pg
import asyncio
import sys
import os
import math
import random
import numpy as np
import time
import player_
from player_ import Player
from chunk_gen import * 
pygame.init()
pg.init()

# Init Music
introsong = pygame.mixer.Sound(os.path.join('assets', 'songs', 'intro.ogg'))
bgsong1 = pygame.mixer.Sound(os.path.join('assets', 'songs', 'background1.ogg'))
slash = pygame.mixer.Sound(os.path.join('assets', 'songs', 'slash.ogg'))
walk = pygame.mixer.Sound(os.path.join('assets', 'songs', 'walk.ogg'))
sprint = pygame.mixer.Sound(os.path.join('assets', 'songs', 'sprint.ogg'))
introchannel = pygame.mixer.Channel(0)
bgchannel = pygame.mixer.Channel(1)
noisechannel = pygame.mixer.Channel(2)

# Screen Size
screen_width = 1280
screen_height = 720
#display = pygame.display.set_mode((pygame.transform.scale(game_canvas, screen.get_size())))
display = pygame.display.set_mode((screen_width, screen_height))

# Player and it's hitbox. 32px by 50px was painstakingly measured by hand and needs work
player = Player((screen_width / 2), (screen_height / 2), 32, 50)
player_hitbox = pygame.Rect((screen_width / 2), (screen_height / 2), 32, 50)

player_hitbox_up = pygame.Rect((screen_width / 2), (screen_height / 2) - 8, 32, 50)
player_hitbox_down = pygame.Rect((screen_width / 2), (screen_height / 2) + 8, 32, 50)
player_hitbox_left = pygame.Rect((screen_width / 2) - 8, (screen_height / 2), 32, 50)
player_hitbox_right = pygame.Rect((screen_width / 2) + 8, (screen_height / 2), 32, 50)

player_hitbox_UP = pygame.Rect((screen_width / 2), (screen_height / 2) - 32, 32, 50)
player_hitbox_DOWN = pygame.Rect((screen_width / 2), (screen_height / 2) + 32, 32, 50)
player_hitbox_LEFT = pygame.Rect((screen_width / 2) - 32, (screen_height / 2), 32, 50)
player_hitbox_RIGHT = pygame.Rect((screen_width / 2) + 32, (screen_height / 2), 32, 50)

#pygame.mixer.music.play(loops=1)
introchannel.play(introsong, loops=0)

# Main Game Loop
async def main(): 
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
    gslime_hitbox = []
    pslime_hitbox = []
    bslime_hitbox = []
    yslime_hitbox = []
    LAST_BUTTON = ''
    tile_size = 64
    deleted_slimes = []
    attack = False
    slimelist = []
    coins = 0
    start_time = time.time()
    
    # Load Tiles
    floor,wall = pg.image.load(os.path.join('assets', 'images', 'floor tile.png')).convert(),pg.image.load(os.path.join('assets', 'images', 'wall tile.png')).convert()
    wallr = wall.get_rect()


    tilemap = {}
    CHUNK_SIZE = 8
    
    # Music
    introsong = pygame.mixer.Sound(os.path.join('assets', 'songs', 'intro.ogg'))
    bgsong1 = pygame.mixer.Sound(os.path.join('assets', 'songs', 'background1.ogg'))
    slash = pygame.mixer.Sound(os.path.join('assets', 'songs', 'slash.ogg'))
    walk = pygame.mixer.Sound(os.path.join('assets', 'songs', 'walk.ogg'))
    sprint = pygame.mixer.Sound(os.path.join('assets', 'songs', 'sprint.ogg'))
    introchannel = pygame.mixer.Channel(0)
    bgchannel = pygame.mixer.Channel(1)
    noisechannel = pygame.mixer.Channel(2) 
    
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

    coin1 = pg.image.load(os.path.join('assets', 'ui', 'coin1.png')).convert_alpha()
    coin2 = pg.image.load(os.path.join('assets', 'ui', 'coin2.png')).convert_alpha()
    coin3 = pg.image.load(os.path.join('assets', 'ui', 'coin3.png')).convert_alpha()
    coin4 = pg.image.load(os.path.join('assets', 'ui', 'coin4.png')).convert_alpha()


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
    
    # Green Blob
    f1slimegreen = pg.image.load(os.path.join('assets', 'images', 'blob', 'gslimejump1.png')).convert_alpha()
    f2slimegreen = pg.image.load(os.path.join('assets', 'images', 'blob', 'gslimejump2.png')).convert_alpha()
    f3slimegreen = pg.image.load(os.path.join('assets', 'images', 'blob', 'gslimejump3.png')).convert_alpha()
    f4slimegreen = pg.image.load(os.path.join('assets', 'images', 'blob', 'gslimejump4.png')).convert_alpha()
    f5slimegreen = pg.image.load(os.path.join('assets', 'images', 'blob', 'gslimejump5.png')).convert_alpha()
    f6slimegreen = pg.image.load(os.path.join('assets', 'images', 'blob', 'gslimejump6.png')).convert_alpha()
    f7slimegreen = pg.image.load(os.path.join('assets', 'images', 'blob', 'gslimejump7.png')).convert_alpha()
    f8slimegreen = pg.image.load(os.path.join('assets', 'images', 'blob', 'gslimejump8.png')).convert_alpha()
    
    # Purple Blob
    f1slimepurple = pg.image.load(os.path.join('assets', 'images', 'blob', 'pslimejump1.png')).convert_alpha()
    f2slimepurple = pg.image.load(os.path.join('assets', 'images', 'blob', 'pslimejump2.png')).convert_alpha()
    f3slimepurple = pg.image.load(os.path.join('assets', 'images', 'blob', 'pslimejump3.png')).convert_alpha()
    f4slimepurple = pg.image.load(os.path.join('assets', 'images', 'blob', 'pslimejump4.png')).convert_alpha()
    f5slimepurple = pg.image.load(os.path.join('assets', 'images', 'blob', 'pslimejump5.png')).convert_alpha()
    f6slimepurple = pg.image.load(os.path.join('assets', 'images', 'blob', 'pslimejump6.png')).convert_alpha()
    f7slimepurple = pg.image.load(os.path.join('assets', 'images', 'blob', 'pslimejump7.png')).convert_alpha()
    f8slimepurple = pg.image.load(os.path.join('assets', 'images', 'blob', 'pslimejump8.png')).convert_alpha()

    # Blue Blob
    f1slimeblue = pg.image.load(os.path.join('assets', 'images', 'blob', 'bslimejump1.png')).convert_alpha()
    f2slimeblue = pg.image.load(os.path.join('assets', 'images', 'blob', 'bslimejump2.png')).convert_alpha()
    f3slimeblue = pg.image.load(os.path.join('assets', 'images', 'blob', 'bslimejump3.png')).convert_alpha()
    f4slimeblue = pg.image.load(os.path.join('assets', 'images', 'blob', 'bslimejump4.png')).convert_alpha()
    f5slimeblue = pg.image.load(os.path.join('assets', 'images', 'blob', 'bslimejump5.png')).convert_alpha()
    f6slimeblue = pg.image.load(os.path.join('assets', 'images', 'blob', 'bslimejump6.png')).convert_alpha()
    f7slimeblue = pg.image.load(os.path.join('assets', 'images', 'blob', 'bslimejump7.png')).convert_alpha()
    f8slimeblue = pg.image.load(os.path.join('assets', 'images', 'blob', 'bslimejump8.png')).convert_alpha()

    # Yellow Blob
    f1slimeyellow = pg.image.load(os.path.join('assets', 'images', 'blob', 'yslimejump1.png')).convert_alpha()
    f2slimeyellow = pg.image.load(os.path.join('assets', 'images', 'blob', 'yslimejump2.png')).convert_alpha()
    f3slimeyellow = pg.image.load(os.path.join('assets', 'images', 'blob', 'yslimejump3.png')).convert_alpha()
    f4slimeyellow = pg.image.load(os.path.join('assets', 'images', 'blob', 'yslimejump4.png')).convert_alpha()
    f5slimeyellow = pg.image.load(os.path.join('assets', 'images', 'blob', 'yslimejump5.png')).convert_alpha()
    f6slimeyellow = pg.image.load(os.path.join('assets', 'images', 'blob', 'yslimejump6.png')).convert_alpha()
    f7slimeyellow = pg.image.load(os.path.join('assets', 'images', 'blob', 'yslimejump7.png')).convert_alpha()
    f8slimeyellow = pg.image.load(os.path.join('assets', 'images', 'blob', 'yslimejump8.png')).convert_alpha()

    # Icon & Title
    iconold = pg.image.load(os.path.join('assets', 'images', 'favicon.png')).convert_alpha()
    icon = pygame.transform.smoothscale(iconold, (32, 32))
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Under the Depths')



    #Index Tiles
    tile_index = {0:floor,
                  1:wall}
    # 1 = green
    gslime_index = {0:f1slimegreen,
                   1:f2slimegreen,
                   2:f3slimegreen,
                   3:f4slimegreen,
                   4:f5slimegreen,
                   5:f6slimegreen,
                   6:f7slimegreen,
                   7:f8slimegreen,
                }    

    # 2 = purple
    pslime_index = {0:f3slimepurple,
                   1:f4slimepurple,
                   2:f5slimepurple,
                   3:f6slimepurple,
                   4:f7slimepurple,
                   5:f8slimepurple,
                   6:f1slimepurple,
                   7:f2slimepurple,
                }  

    # 3 = blue
    bslime_index = {0:f5slimeblue,
                   1:f6slimeblue,
                   2:f7slimeblue,
                   3:f8slimeblue,
                   4:f1slimeblue,
                   5:f2slimeblue,
                   6:f3slimeblue,
                   7:f4slimeblue,
                }  

    # 4 = yellow
    yslime_index = {0:f7slimeyellow,
                   1:f8slimeyellow,
                   2:f1slimeyellow,
                   3:f2slimeyellow,
                   4:f3slimeyellow,
                   5:f4slimeyellow,
                   6:f5slimeyellow,
                   7:f6slimeyellow,
                }  

    nindex = {
        0:zero,
        1:one,
        2:two,
        3:three,
        4:four,
        5:five,
        6:six,
        7:seven,
        8:eight,
        9:nine,
    }
    # Starting Frame
    framename = 'fwdstand'

    # 36 so the player is within 1 tile
    display_scroll = [0,36]
    
    attack_cooldown = 0

    coinframe = 0

    # To fix spawning on a wall, used so it doesn't run as hard in the background
    FIRST_LOOP = True
    #global coins
    #global clock
    #global countplayeranimation
    #global wall_hitbox
    #global slime_hitbox
    #global LAST_BUTTON
    #global deleted_slimes
    #global attack
    #global slimelist
    #global tilemap
    #global framename
    #global display_scroll
    #global FIRST_LOOP
    running = True
    while running:
        display.fill((50, 50, 50))
        
        # Application Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

        # Calc Tiles/Seconds
        dt = clock.tick(60)*64 / 1000
    
        wall_hitbox = []
        slime_hitbox = []
        gslime_hitbox = []
        pslime_hitbox = []
        bslime_hitbox = []
        yslime_hitbox = []
    
        # Get Key Presses
        keys = pygame.key.get_pressed()
    
        # Controls
        # Sprint
        if keys[pygame.K_LSHIFT]:
            mspeed = 16
        else:
            mspeed = 8
        # Left
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            #display_scroll[0] -= mspeed * dt
            LEFT = 1
        else:
            LEFT = 0
        
        # Right
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            #display_scroll[0] += mspeed * dt
            RIGHT = 1
        else:
            RIGHT = 0
        #  Up
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            #display_scroll[1] -= mspeed * dt
            UP = 1
        else:
            UP = 0
        # Down
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            #display_scroll[1] += mspeed * dt
            DOWN = 1
        else:
            DOWN = 0
    
        # Tilemap Generator
        for y in range(round(screen_height / 512) + 2):
            for x in range(round(screen_width / 512) + 2):
                target_x = x - 1 + int(round(display_scroll[0] / (CHUNK_SIZE*tile_size)))
                target_y = y - 1 + int(round(display_scroll[1] / (CHUNK_SIZE*tile_size)))
                target_chunk = str(target_x) + ';' + str(target_y)
                if target_chunk not in tilemap:
                    tilemap[target_chunk] = generate_chunk(target_x, target_y, coins)
                for i, tile in enumerate(tilemap[target_chunk]):
                    if tile[1] == 1:
                        # Wall Code (Rect)
                        x_rect = (tile[0][0]*tile_size)-display_scroll[0] + (tile_size / 2)
                        y_rect = (tile[0][1]*tile_size)-display_scroll[1] + (tile_size / 2)
                        #wallr.center = (x_rect,y_rect)
                        #display.blit(wall, wallr)
                        display.blit(tile_index[1], ((tile[0][0]*tile_size)-display_scroll[0], (tile[0][1]*tile_size)-display_scroll[1]))
                        wall_hitbox.append(pygame.Rect(x_rect - 48, y_rect - (tile_size / 2), tile_size, tile_size))
                        #wall_mask = pygame.mask.from_surface(wallimg)
                    else: 
                        # Non Wall/Blockade Code (Blit)
                        display.blit(tile_index[0], ((tile[0][0]*tile_size)-display_scroll[0], (tile[0][1]*tile_size)-display_scroll[1]))
                        if tile[2] == 1:
                            n = int(time.time() * 8) % 8
                            x_rect = (tile[0][0]*tile_size)-display_scroll[0] + (tile_size / 2)
                            y_rect = (tile[0][1]*tile_size)-display_scroll[1] + (tile_size / 2)
                            slime_hitbox.append(pygame.Rect(x_rect, y_rect, tile_size, tile_size))
                            gslime_hitbox.append(pygame.Rect(x_rect, y_rect, tile_size, tile_size))
                            xy_rect = (math.floor(x_rect/64), math.floor(y_rect/64))
                            yx_rect = (math.ceil(x_rect/64), math.ceil(y_rect/64))
                            if xy_rect in slimelist or yx_rect in slimelist:
                                tilemap[target_chunk][i][2] = 0
                            #if pygame.Rect(x_rect, y_rect, tile_size, tile_size).collidelist(deleted_slimes) > 0: 
                            #    
                            #    print(x_rect, y_rect)
                            #    tilemap[target_chunk][tile][2] = False
                            else:
                                display.blit(gslime_index[n], ((tile[0][0]*tile_size)-display_scroll[0], (tile[0][1]*tile_size)-display_scroll[1]))

                        if tile[2] == 2:
                            n = int(time.time() * 8) % 8
                            x_rect = (tile[0][0]*tile_size)-display_scroll[0] + (tile_size / 2)
                            y_rect = (tile[0][1]*tile_size)-display_scroll[1] + (tile_size / 2)
                            slime_hitbox.append(pygame.Rect(x_rect, y_rect, tile_size, tile_size))
                            pslime_hitbox.append(pygame.Rect(x_rect, y_rect, tile_size, tile_size))
                            xy_rect = (math.floor(x_rect/64), math.floor(y_rect/64))
                            yx_rect = (math.ceil(x_rect/64), math.ceil(y_rect/64))
                            if xy_rect in slimelist or yx_rect in slimelist:
                                tilemap[target_chunk][i][2] = 0
                            #if pygame.Rect(x_rect, y_rect, tile_size, tile_size).collidelist(deleted_slimes) > 0: 
                            #    
                            #    print(x_rect, y_rect)
                            #    tilemap[target_chunk][tile][2] = False
                            else:
                                display.blit(pslime_index[n], ((tile[0][0]*tile_size)-display_scroll[0], (tile[0][1]*tile_size)-display_scroll[1]))
                            #print(tilemap[target_chunk][tile[2]])
    
                        if tile[2] == 3:
                            n = int(time.time() * 8) % 8
                            x_rect = (tile[0][0]*tile_size)-display_scroll[0] + (tile_size / 2)
                            y_rect = (tile[0][1]*tile_size)-display_scroll[1] + (tile_size / 2)
                            slime_hitbox.append(pygame.Rect(x_rect, y_rect, tile_size, tile_size))
                            bslime_hitbox.append(pygame.Rect(x_rect, y_rect, tile_size, tile_size))
                            xy_rect = (math.floor(x_rect/64), math.floor(y_rect/64))
                            yx_rect = (math.ceil(x_rect/64), math.ceil(y_rect/64))
                            if xy_rect in slimelist or yx_rect in slimelist:
                                tilemap[target_chunk][i][2] = 0
                            #if pygame.Rect(x_rect, y_rect, tile_size, tile_size).collidelist(deleted_slimes) > 0: 
                            #    
                            #    print(x_rect, y_rect)
                            #    tilemap[target_chunk][tile][2] = False
                            else:
                                display.blit(bslime_index[n], ((tile[0][0]*tile_size)-display_scroll[0], (tile[0][1]*tile_size)-display_scroll[1]))

                        if tile[2] == 4:
                            n = int(time.time() * 4) % 8
                            x_rect = (tile[0][0]*tile_size)-display_scroll[0] + (tile_size / 2)
                            y_rect = (tile[0][1]*tile_size)-display_scroll[1] + (tile_size / 2)
                            slime_hitbox.append(pygame.Rect(x_rect, y_rect, tile_size, tile_size))
                            yslime_hitbox.append(pygame.Rect(x_rect, y_rect, tile_size, tile_size))
                            xy_rect = (math.floor(x_rect/64), math.floor(y_rect/64))
                            yx_rect = (math.ceil(x_rect/64), math.ceil(y_rect/64))
                            if xy_rect in slimelist or yx_rect in slimelist:
                                tilemap[target_chunk][i][2] = 0
                            #if pygame.Rect(x_rect, y_rect, tile_size, tile_size).collidelist(deleted_slimes) > 0: 
                            #    
                            #    print(x_rect, y_rect)
                            #    tilemap[target_chunk][tile][2] = False
                            else:
                                display.blit(yslime_index[n], ((tile[0][0]*tile_size)-display_scroll[0], (tile[0][1]*tile_size)-display_scroll[1]))

                        #display.blit(tile_index[tile[1]], ((tile[0][0]*tile_size)-display_scroll[0], (tile[0][1]*tile_size)-display_scroll[1]))
       
        deleted_slimes = []
        slimelist = []
        # Debug Code
        #print(player_hitbox.collidelist(wall_hitbox))
        
        if FIRST_LOOP == True: 
            if player_hitbox.collidelist(wall_hitbox) > 0 or player_hitbox_UP.collidelist(wall_hitbox) > 0 or player_hitbox_DOWN.collidelist(wall_hitbox) > 0 or player_hitbox_LEFT.collidelist(wall_hitbox) > 0 or player_hitbox_RIGHT.collidelist(wall_hitbox) > 0:
                    display_scroll[1] += tile_size
                    if player_hitbox.collidelist(wall_hitbox) <= 0 and player_hitbox_UP.collidelist(wall_hitbox) <= 0 and player_hitbox_DOWN.collidelist(wall_hitbox) <= 0 and player_hitbox_LEFT.collidelist(wall_hitbox) <= 0 and player_hitbox_RIGHT.collidelist(wall_hitbox) <= 0:
                        FIRST_LOOP = False
            else:
                FIRST_LOOP = False

        if player_hitbox.collidelist(wall_hitbox) > 0:
            #print('collision')
            if LEFT == 1:
                LEFT = 0
            if RIGHT == 1:
                RIGHT = 0
            if UP == 1:
                UP = 0
            if DOWN == 1:
                DOWN = 0



        #if player_hitbox.collidelist(slime_hitbox) > 0 and attack == True:
        #    selected_slime = None
        #    for i in slime_hitbox:
        #        if player_hitbox.colliderect(i):
        #            selected_slime = i
        #            print(i)
        #            slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
        #            slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
        #            slime_hitbox.remove(i)
        #            deleted_slimes.append(i.copy())
        #            if player_hitbox.collidelist(gslime_hitbox) > 0:
        #                add = 1
        #            elif player_hitbox.collidelist(pslime_hitbox) > 0:
        #                add = random.randint(1,2)
        #            elif player_hitbox.collidelist(bslime_hitbox) > 0:
        #                add = random.randint(3,4)
                        #print('gfse')
                    #elif player_hitbox.collidelist(yslime_hitbox) > 0:
                    #    add = random.randint(10,20)
                        #print('something')
        #            else: 
                        #print('error')
        #                add = random.randint(10,20)

        #    attack_cooldown = 30
        #    attack = False
        #    coins += add
            #print(coins)
            #print(selected_slime.x, selected_slime.y)
   
        if player_hitbox.collidelist(gslime_hitbox) > 0 and attack == True:
            selected_slime = None
            # Slash noise
            if noisechannel.get_sound() != slash: 
                noisechannel.play(slash, loops=0)
            for i in gslime_hitbox:
                if player_hitbox.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy())
            attack_cooldown = 30
            attack = False
            coins += random.randint(1,2)

        elif player_hitbox.collidelist(pslime_hitbox) > 0 and attack == True:
            selected_slime = None
            # Slash noise
            if noisechannel.get_sound() != slash: 
                noisechannel.play(slash, loops=0)
            for i in pslime_hitbox:
                if player_hitbox.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy())
            attack_cooldown = 30
            attack = False
            coins += random.randint(3,5)

        elif player_hitbox.collidelist(bslime_hitbox) > 0 and attack == True:
            selected_slime = None
            # Slash noise
            if noisechannel.get_sound() != slash:  
                noisechannel.play(slash, loops=0)
            for i in bslime_hitbox:
                if player_hitbox.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy())
            attack_cooldown = 30
            attack = False
            coins += random.randint(6,8)

        elif player_hitbox.collidelist(yslime_hitbox) > 0 and attack == True:
            selected_slime = None
            # Slash noise
            if noisechannel.get_sound() != slash:
                noisechannel.play(slash, loops=0)
            for i in yslime_hitbox:
                if player_hitbox.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy())
            attack_cooldown = 30
            attack = False
            coins += random.randint(10,20)



        #elif player_hitbox_DOWN.collidelist(slime_hitbox) > 0 and attack == True and (framename == 'f1sword' or framename == 'f2sword' or framename == 'f3sword' or framename == 'f4sword'):
        #    selected_slime = None
        #    for i in slime_hitbox:
        #        if player_hitbox_DOWN.colliderect(i):
        #            selected_slime = i
                    #print(i)
        #            slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
        #            slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
        #            slime_hitbox.remove(i)
        #            deleted_slimes.append(i.copy())
        #            if player_hitbox_DOWN.collidelist(gslime_hitbox) > 0:
        #                add = 1
        #            elif player_hitbox_DOWN.collidelist(pslime_hitbox) > 0:
        #                add = random.randint(1,2)
        #            elif player_hitbox_DOWN.collidelist(bslime_hitbox) > 0:
        #                add = random.randint(3,4)
                        #print('fsdf')
                    #elif player_hitbox_DOWN.collidelist(yslime_hitbox) > 0:
                    #    add = random.randint(10,20)
                        #print('somethign')
        #            else:
        #                #print('error')
        #                add = random.randint(10,20)

        #    attack_cooldown = 30
        #    attack = False
        #    coins += add
            #print(coins)

        elif player_hitbox_DOWN.collidelist(gslime_hitbox) > 0 and attack == True and (framename == 'f1sword' or framename == 'f2sword' or framename == 'f3sword' or framename == 'f4sword'):
            selected_slime = None
            # Slash noise
            if noisechannel.get_sound() != slash:
                noisechannel.play(slash, loops=0)
            for i in gslime_hitbox:
                if player_hitbox_DOWN.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy())
            attack_cooldown = 30
            attack = False
            coins += random.randint(1,2)

        elif player_hitbox_DOWN.collidelist(pslime_hitbox) > 0 and attack == True and (framename == 'f1sword' or framename == 'f2sword' or framename == 'f3sword' or framename == 'f4sword'):
            selected_slime = None
            # Slash noise
            if noisechannel.get_sound() != slash:
                noisechannel.play(slash, loops=0)
            for i in pslime_hitbox:
                if player_hitbox_DOWN.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy())
            attack_cooldown = 30
            attack = False
            coins += random.randint(3,5)

        elif player_hitbox_DOWN.collidelist(bslime_hitbox) > 0 and attack == True and (framename == 'f1sword' or framename == 'f2sword' or framename == 'f3sword' or framename == 'f4sword'):
            selected_slime = None
            # Slash noise
            if noisechannel.get_sound() != slash: 
                noisechannel.play(slash, loops=0)
            for i in bslime_hitbox:
                if player_hitbox_DOWN.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy())
            attack_cooldown = 30
            attack = False
            coins += random.randint(6,8)

        elif player_hitbox_DOWN.collidelist(yslime_hitbox) > 0 and attack == True and (framename == 'f1sword' or framename == 'f2sword' or framename == 'f3sword' or framename == 'f4sword'):
            selected_slime = None
            # Slash noise
            if noisechannel.get_sound() != slash: 
                noisechannel.play(slash, loops=0)
            for i in yslime_hitbox:
                if player_hitbox_DOWN.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy())
            attack_cooldown = 30
            attack = False
            coins += random.randint(10,20)



        #elif player_hitbox_UP.collidelist(slime_hitbox) > 0 and attack == True and (framename == 'b1sword' or framename == 'b2sword' or framename == 'b3sword' or framename == 'b4sword'):
        #    selected_slime = None
        #    for i in slime_hitbox:
        #        if player_hitbox_UP.colliderect(i):
        #            selected_slime = i
        #            #print(i)
        #            slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
        #            slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
        #            slime_hitbox.remove(i)
        #            deleted_slimes.append(i.copy())
        #            if player_hitbox_UP.collidelist(gslime_hitbox) > 0:
        #                add = 1
        #            elif player_hitbox_UP.collidelist(pslime_hitbox) > 0:
        #                add = random.randint(1,2)
        #            elif player_hitbox_UP.collidelist(bslime_hitbox) > 0:
        #                add = random.randint(3,4)
                    #elif player_hitbox_UP.collidelist(yslime_hitbox) > 0:
                    #    add = random.randint(10,20)
        #            else:
                        #print('error')
        #                add = random.randint(10,20)
 
        #    attack_cooldown = 30
        #    attack = False
        #    coins += add
            #print(coins)
    
        elif player_hitbox_UP.collidelist(gslime_hitbox) > 0 and attack == True and (framename == 'b1sword' or framename == 'b2sword' or framename == 'b3sword' or framename == 'b4sword'):
            selected_slime = None
            # Slash noise
            if noisechannel.get_sound() != slash: 
                noisechannel.play(slash, loops=0)
            for i in gslime_hitbox:
                if player_hitbox_UP.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy())
            attack_cooldown = 30
            attack = False
            coins += random.randint(1,2)

        elif player_hitbox_UP.collidelist(pslime_hitbox) > 0 and attack == True and (framename == 'b1sword' or framename == 'b2sword' or framename == 'b3sword' or framename == 'b4sword'):
            selected_slime = None
            # Slash noise
            if noisechannel.get_sound() != slash: 
                noisechannel.play(slash, loops=0)
            for i in pslime_hitbox:
                if player_hitbox_UP.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy())
            attack_cooldown = 30
            attack = False
            coins += random.randint(3,5)

        elif player_hitbox_UP.collidelist(bslime_hitbox) > 0 and attack == True and (framename == 'b1sword' or framename == 'b2sword' or framename == 'b3sword' or framename == 'b4sword'):
            selected_slime = None
            # Slash noise
            if noisechannel.get_sound() != slash: 
                noisechannel.play(slash, loops=0)
            for i in bslime_hitbox:
                if player_hitbox_UP.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy())
            attack_cooldown = 30
            attack = False
            coins += random.randint(6,8)

        elif player_hitbox_UP.collidelist(yslime_hitbox) > 0 and attack == True and (framename == 'b1sword' or framename == 'b2sword' or framename == 'b3sword' or framename == 'b4sword'):
            selected_slime = None
            # Slash noise
            if noisechannel.get_sound() != slash: 
                noisechannel.play(slash, loops=0)
            for i in yslime_hitbox:
                if player_hitbox_UP.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy())
            attack_cooldown = 30
            attack = False
            coins += random.randint(10,20)


        
        #elif player_hitbox_RIGHT.collidelist(slime_hitbox) > 0 and attack == True and (framename == 'r1sword' or framename == 'r2sword' or framename == 'r3sword' or framename == 'r4sword'):
        #    selected_slime = None
        #    for i in slime_hitbox:
        #        if player_hitbox_RIGHT.colliderect(i):
        #            selected_slime = i
                    #print(i)
        #            slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
        #            slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
        #            slime_hitbox.remove(i)
        #            deleted_slimes.append(i.copy())        
        #            if player_hitbox_RIGHT.collidelist(gslime_hitbox) > 0:
        #                add = 1
        #            elif player_hitbox_RIGHT.collidelist(pslime_hitbox) > 0:
        #                add = random.randint(1,2)
        #            elif player_hitbox_RIGHT.collidelist(bslime_hitbox) > 0:
        #                add = random.randint(3,4)
                    #elif player_hitbox_RIGHT.collidelist(yslime_hitbox) > 0:
                    #    add = random.randint(10,20)
        #            else:
                        #print('error')
        #                add = random.randint(10,20)
 
        #    attack_cooldown = 30
        #    attack = False
        #    coins += add
            #print(coins)
    
        elif player_hitbox_RIGHT.collidelist(gslime_hitbox) > 0 and attack == True and (framename == 'r1sword' or framename == 'r2sword' or framename == 'r3sword' or framename == 'r4sword'):
            selected_slime = None
            # Slash noise
            if noisechannel.get_sound() != slash: 
                noisechannel.play(slash, loops=0)
            for i in gslime_hitbox:
                if player_hitbox_RIGHT.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy()) 
            attack_cooldown = 30
            attack = False
            coins += random.randint(1,2)

        elif player_hitbox_RIGHT.collidelist(pslime_hitbox) > 0 and attack == True and (framename == 'r1sword' or framename == 'r2sword' or framename == 'r3sword' or framename == 'r4sword'):
            selected_slime = None
            # Slash noise
            if noisechannel.get_sound() != slash: 
                noisechannel.play(slash, loops=0)
            for i in pslime_hitbox:
                if player_hitbox_RIGHT.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy()) 
            attack_cooldown = 30
            attack = False
            coins += random.randint(3,5)

        elif player_hitbox_RIGHT.collidelist(bslime_hitbox) > 0 and attack == True and (framename == 'r1sword' or framename == 'r2sword' or framename == 'r3sword' or framename == 'r4sword'):
            selected_slime = None
            # Slash noise
            if noisechannel.get_sound() != slash: 
                noisechannel.play(slash, loops=0)
            for i in bslime_hitbox:
                if player_hitbox_RIGHT.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy()) 
            attack_cooldown = 30
            attack = False
            coins += random.randint(6,8)

        elif player_hitbox_RIGHT.collidelist(yslime_hitbox) > 0 and attack == True and (framename == 'r1sword' or framename == 'r2sword' or framename == 'r3sword' or framename == 'r4sword'):
            selected_slime = None
            # Slash noise
            if noisechannel.get_sound() != slash: 
                noisechannel.play(slash, loops=0)
            for i in yslime_hitbox:
                if player_hitbox_RIGHT.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy()) 
            attack_cooldown = 30
            attack = False
            coins += random.randint(10,20)
    


        #elif player_hitbox_LEFT.collidelist(slime_hitbox) > 0 and attack == True and (framename == 'l1sword' or framename == 'l2sword' or framename == 'l3sword' or framename == 'l4sword'):
        #    selected_slime = None
        #    for i in slime_hitbox:
        #        if player_hitbox_LEFT.colliderect(i):
        #            selected_slime = i
        #            #print(i)
        #            slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
        #            slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
        #            slime_hitbox.remove(i)
        #            deleted_slimes.append(i.copy())        
        #            if player_hitbox_LEFT.collidelist(gslime_hitbox) > 0:
        #                add = 1
        #            elif player_hitbox_LEFT.collidelist(pslime_hitbox) > 0:
        #                add = random.randint(1,2)
        #            elif player_hitbox_LEFT.collidelist(bslime_hitbox) > 0:
        #                add = random.randint(3,4)
        #            elif player_hitbox_LEFT.collidelist(yslime_hitbox) > 0:
        #                add = random.randint(10,20)
        #            else:
                        #print('error')
        #                add = 1
            
        #    attack_cooldown = 30
        #    attack = False
        #    coins += add
            #print(coins)
    
        elif player_hitbox_LEFT.collidelist(gslime_hitbox) > 0 and attack == True and (framename == 'l1sword' or framename == 'l2sword' or framename == 'l3sword' or framename == 'l4sword'):
            selected_slime = None
            # Slash noise
            if noisechannel.get_sound() != slash: 
                noisechannel.play(slash, loops=0)
            for i in gslime_hitbox:
                if player_hitbox_LEFT.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy())
            attack_cooldown = 30
            attack = False
            coins += random.randint(1,2)

        elif player_hitbox_LEFT.collidelist(pslime_hitbox) > 0 and attack == True and (framename == 'l1sword' or framename == 'l2sword' or framename == 'l3sword' or framename == 'l4sword'):
            selected_slime = None
            # Slash noise
            if noisechannel.get_sound() != slash: 
                noisechannel.play(slash, loops=0)
            for i in pslime_hitbox:
                if player_hitbox_LEFT.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy())
            attack_cooldown = 30
            attack = False
            coins += random.randint(3,5)

        elif player_hitbox_LEFT.collidelist(bslime_hitbox) > 0 and attack == True and (framename == 'l1sword' or framename == 'l2sword' or framename == 'l3sword' or framename == 'l4sword'):
            selected_slime = None
            # Slash noise
            if noisechannel.get_sound() != slash:
                noisechannel.play(slash, loops=0)
            for i in bslime_hitbox:
                if player_hitbox_LEFT.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy())
            attack_cooldown = 30
            attack = False
            coins += random.randint(6,8)

        elif player_hitbox_LEFT.collidelist(yslime_hitbox) > 0 and attack == True and (framename == 'l1sword' or framename == 'l2sword' or framename == 'l3sword' or framename == 'l4sword'):
            selected_slime = None
            # Slash noise
            if noisechannel.get_sound() != slash:
                noisechannel.play(slash, loops=0)
            for i in yslime_hitbox:
                if player_hitbox_LEFT.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy())
            attack_cooldown = 30
            attack = False
            coins += random.randint(10,20)


    
        elif attack == True:
            attack = False

    






        # Movements
        if LEFT == 1 and RIGHT != 1 and UP != 1 and DOWN != 1 and player_hitbox_left.collidelist(wall_hitbox) < 0 and framename != 'f1sword' and framename != 'f2sword' and framename != 'f3sword' and framename != 'f4sword' and framename != 'b1sword' and framename != 'b2sword' and framename != 'b3sword' and framename != 'b4sword' and framename != 'r1sword' and framename != 'r2sword' and framename != 'r3sword' and framename != 'r4sword' and framename != 'l1sword' and framename != 'l2sword' and framename != 'l3sword' and framename != 'l4sword':
            LAST_BUTTON = 'LEFT'
            display_scroll[0] -= mspeed * dt
            if mspeed == 8 and noisechannel.get_sound() != walk:
                noisechannel.play(walk, loops=-1)
            elif mspeed == 16 and not noisechannel.get_sound() != sprint:
                noisechannel.play(sprint, loops=-1)
        elif LEFT == -1:
            display_scroll[0] += mspeed * dt
    
        if RIGHT == 1 and LEFT != 1 and UP != 1 and DOWN != 1 and player_hitbox_right.collidelist(wall_hitbox) < 0 and framename != 'f1sword' and framename != 'f2sword' and framename != 'f3sword' and framename != 'f4sword' and framename != 'b1sword' and framename != 'b2sword' and framename != 'b3sword' and framename != 'b4sword' and framename != 'r1sword' and framename != 'r2sword' and framename != 'r3sword' and framename != 'r4sword' and framename != 'l1sword' and framename != 'l2sword' and framename != 'l3sword' and framename != 'l4sword':
            LAST_BUTTON = 'RIGHT'
            display_scroll[0] += mspeed * dt
            if mspeed == 8 and noisechannel.get_sound() != walk:
                noisechannel.play(walk, loops=-1)
            elif mspeed == 16 and noisechannel.get_sound() != sprint:
                noisechannel.play(sprint, loops=-1)
        elif RIGHT == -1:
            display_scroll[0] -= mspeed * dt
    
        if UP == 1 and LEFT != 1 and RIGHT != 1 and DOWN != 1 and player_hitbox_up.collidelist(wall_hitbox) < 0 and framename != 'f1sword' and framename != 'f2sword' and framename != 'f3sword' and framename != 'f4sword' and framename != 'b1sword' and framename != 'b2sword' and framename != 'b3sword' and framename != 'b4sword' and framename != 'r1sword' and framename != 'r2sword' and framename != 'r3sword' and framename != 'r4sword' and framename != 'l1sword' and framename != 'l2sword' and framename != 'l3sword' and framename != 'l4sword':
            LAST_BUTTON = 'UP'
            display_scroll[1] -= mspeed * dt
            if mspeed == 8 and noisechannel.get_sound() != walk:
                noisechannel.play(walk, loops=-1)
            elif mspeed == 16 and noisechannel.get_sound() != sprint:
                noisechannel.play(sprint, loops=-1)
        elif UP == -1:
            display_scroll[1] += mspeed * dt
    
        if DOWN == 1 and LEFT != 1 and RIGHT != 1 and UP != 1 and player_hitbox_down.collidelist(wall_hitbox) < 0 and framename != 'f1sword' and framename != 'f2sword' and framename != 'f3sword' and framename != 'f4sword' and framename != 'b1sword' and framename != 'b2sword' and framename != 'b3sword' and framename != 'b4sword' and framename != 'r1sword' and framename != 'r2sword' and framename != 'r3sword' and framename != 'r4sword' and framename != 'l1sword' and framename != 'l2sword' and framename != 'l3sword' and framename != 'l4sword':
            LAST_BUTTON = 'DOWN'
            display_scroll[1] += mspeed * dt
            if mspeed == 8 and noisechannel.get_sound() != walk:
                noisechannel.play(walk, loops=-1)
            elif mspeed == 16 and noisechannel.get_sound() != sprint:
                noisechannel.play(sprint, loops=-1)
        elif DOWN == -1:
            display_scroll[1] -= mspeed * dt
    
        # Movement Priority (UP, RIGHT, LEFT, DOWN)
        if (UP == 1 and LEFT == 1 and RIGHT != 1 and DOWN != 1) or (UP == 1 and LEFT != 1 and RIGHT == 1 and DOWN != 1) and player_hitbox_up.collidelist(wall_hitbox) < 0 and framename != 'f1sword' and framename != 'f2sword' and framename != 'f3sword' and framename != 'f4sword' and framename != 'b1sword' and framename != 'b2sword' and framename != 'b3sword' and framename != 'b4sword' and framename != 'r1sword' and framename != 'r2sword' and framename != 'r3sword' and framename != 'r4sword' and framename != 'l1sword' and framename != 'l2sword' and framename != 'l3sword' and framename != 'l4sword':
            LAST_BUTTON = 'UP'
            display_scroll[1] -= mspeed * dt
            if mspeed == 8 and noisechannel.get_sound() != walk:
                noisechannel.play(walk, loops=-1)
            elif mspeed == 16 and noisechannel.get_sound() != sprint:
                noisechannel.play(sprint, loops=-1)
    
        if RIGHT == 1 and LEFT != 1 and UP != 1 and DOWN == 1 and player_hitbox_right.collidelist(wall_hitbox) < 0 and framename != 'f1sword' and framename != 'f2sword' and framename != 'f3sword' and framename != 'f4sword' and framename != 'b1sword' and framename != 'b2sword' and framename != 'b3sword' and framename != 'b4sword' and framename != 'r1sword' and framename != 'r2sword' and framename != 'r3sword' and framename != 'r4sword' and framename != 'l1sword' and framename != 'l2sword' and framename != 'l3sword' and framename != 'l4sword':
            LAST_BUTTON = 'RIGHT'
            display_scroll[0] += mspeed * dt
            if mspeed == 8 and noisechannel.get_sound() != walk:
                noisechannel.play(walk, loops=-1)
            elif mspeed == 16 and noisechannel.get_sound() != sprint:
                noisechannel.play(sprint, loops=-1)
    
        if LEFT == 1 and RIGHT != 1 and UP != 1 and DOWN == 1 and player_hitbox_left.collidelist(wall_hitbox) < 0 and framename != 'f1sword' and framename != 'f2sword' and framename != 'f3sword' and framename != 'f4sword' and framename != 'b1sword' and framename != 'b2sword' and framename != 'b3sword' and framename != 'b4sword' and framename != 'r1sword' and framename != 'r2sword' and framename != 'r3sword' and framename != 'r4sword' and framename != 'l1sword' and framename != 'l2sword' and framename != 'l3sword' and framename != 'l4sword':
            LAST_BUTTON = 'LEFT'
            display_scroll[0] -= mspeed * dt
            if mspeed == 8 and noisechannel.get_sound() != walk:
                noisechannel.play(walk, loops=-1)
            elif mspeed == 16 and noisechannel.get_sound() != sprint:
                noisechannel.play(sprint, loops=-1)

        # Slash noise
#        if not noisechannel.get_busy() and (framename == 'f1sword' or framename == 'f2sword' or framename == 'f3sword' or framename == 'f4sword' or framename == 'l1sword' or framename == 'l2sword' or framename == 'l3sword' or framename == 'l4sword' or framename == 'r1sword' or framename == 'r2sword' or framename == 'r3sword' or framename == 'r4sword' or framename == 'b1sword' or framename == 'b2sword' or framename == 'b3sword' or framename == 'b4sword'):
#            noisechannel.play(slash, loops=-1)
        #print(noisechannel.get_sound())


        # Turn off noises
        if UP != 1 and LEFT != 1 and RIGHT != 1 and DOWN != 1 and not (keys[pygame.K_f] or keys[pygame.K_SPACE]):
            noisechannel.stop()
 
        if player_hitbox.collidelist(wall_hitbox) > 0:
            UP = 0
            DOWN = 0
            LEFT = 0
            RIGHT = 0
    
            if LAST_BUTTON == 'LEFT':
                display_scroll[0] += mspeed * dt
                framename = 'lftstand'
            elif LEFT == -1:
                display_scroll[0] -= mspeed * dt

            if LAST_BUTTON == 'RIGHT':
                display_scroll[0] -= mspeed * dt
                framename = 'rgtstand'
            elif RIGHT == -1:
                display_scroll[0] += mspeed * dt
    
            if LAST_BUTTON == 'UP':
                display_scroll[1] += mspeed * dt
                framename = 'bckstand'
            elif UP == -1:
                display_scroll[1] -= mspeed * dt

            if LAST_BUTTON == 'DOWN':
                display_scroll[1] -= mspeed * dt
                framename = 'fwdstand'
            elif DOWN == -1:
                display_scroll[1] += mspeed * dt
    
        if introchannel.get_busy() == False and bgchannel.get_busy() == False:
            if random.randint(1, 1800) == 1:
                bgchannel.play(bgsong1, loops=0)
        
    
        # Player Render
        framename, attack = player.main(display, framename, UP, DOWN, LEFT, RIGHT, attack)
        if attack_cooldown > 0:
            attack = False
            attack_cooldown -= 1
        
            
        # UI
        display.blit(ui, (screen_width-408, 0))
        if int(coinframe / 10) % 4 == 0:
            display.blit(coin1, (screen_width-408, 0))
        elif int(coinframe / 10) % 4 == 1:
            display.blit(coin2, (screen_width-408, 0))
        elif int(coinframe / 10) % 4 == 2:
            display.blit(coin3, (screen_width-408, 0))
        elif int(coinframe / 10) % 4 == 3:
            display.blit(coin4, (screen_width-408, 0))
        coinframe += 1
        
        # Temp coin count
        if coins == 0:
            numbera = zero
            numberb = zero
            numberc = zero
            numberd = zero
            numbere = zero
        elif coins < 100000:
            numbera = nindex[coins % 10]
            numberb = nindex[(coins // 10) % 10]
            numberc = nindex[(coins // 100) % 10]
            numberd = nindex[(coins // 1000) % 10]
            numbere = nindex[(coins // 10000) % 10]
        elif coins >= 100000:
            numbera = nindex[random.randint(0,9)]
            numberb = nindex[random.randint(0,9)]
            numberc = nindex[random.randint(0,9)]
            numberd = nindex[random.randint(0,9)]
            numbere = nindex[random.randint(0,9)]
        
        display.blit(numbera, (screen_width-111, 0)) # Old Value: 148
        display.blit(numberb, (screen_width-168, 0)) # Old Value: 224
        display.blit(numberc, (screen_width-225, 0)) # Old Value: 300
        display.blit(numberd, (screen_width-282, 0)) # Old Value: 376
        display.blit(numbere, (screen_width-339, 0)) # Old Value: 452
        
        # Frame Updater
        clock.tick(60)
        await asyncio.sleep(0)
        # Debug
        #print(attack)
        #print(clock.get_fps())
        if FIRST_LOOP == False:
            pygame.display.update()
    
# The Real Main Game Loop
if __name__ == "__main__":
    asyncio.run(main())


