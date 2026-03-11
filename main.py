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


# Screen Size
screen_width = 1280
screen_height = 720
#display = pygame.display.set_mode((pygame.transform.scale(game_canvas, screen.get_size())))
display = pygame.display.set_mode((screen_width, screen_height))

# Player and it's hitbox. 32px by 54px was painstakingly measured by hand and needs work
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
                            xy_rect = (math.floor(x_rect/64), math.floor(y_rect/64))
                            yx_rect = (math.ceil(x_rect/64), math.ceil(y_rect/64))
                            if xy_rect in slimelist or yx_rect in slimelist:
                                tilemap[target_chunk][i][2] = 0
                            #if pygame.Rect(x_rect, y_rect, tile_size, tile_size).collidelist(deleted_slimes) > 0: 
                            #    
                            #    print(x_rect, y_rect)
                            #    tilemap[target_chunk][tile][2] = False
                            else:
                                display.blit(slime_index[n], ((tile[0][0]*tile_size)-display_scroll[0], (tile[0][1]*tile_size)-display_scroll[1]))
                            #print(tilemap[target_chunk][tile[2]])
    
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
    
        if player_hitbox.collidelist(slime_hitbox) > 0 and attack == True:
            selected_slime = None
            for i in slime_hitbox:
                if player_hitbox.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy())        
            attack = False
            coins += 1
            print(coins)
            #print(selected_slime.x, selected_slime.y)
    

        elif player_hitbox_DOWN.collidelist(slime_hitbox) > 0 and attack == True and (framename == 'f1sword' or framename == 'f2sword' or framename == 'f3sword' or framename == 'f4sword'):
            selected_slime = None
            for i in slime_hitbox:
                if player_hitbox_DOWN.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy())        
            attack = False
            coins += 1
            print(coins)
    

        elif player_hitbox_UP.collidelist(slime_hitbox) > 0 and attack == True and (framename == 'b1sword' or framename == 'b2sword' or framename == 'b3sword' or framename == 'b4sword'):
            selected_slime = None
            for i in slime_hitbox:
                if player_hitbox_UP.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy())        
            attack = False
            coins += 1
            print(coins)
    
        
        elif player_hitbox_RIGHT.collidelist(slime_hitbox) > 0 and attack == True and (framename == 'r1sword' or framename == 'r2sword' or framename == 'r3sword' or framename == 'r4sword'):
            selected_slime = None
            for i in slime_hitbox:
                if player_hitbox_RIGHT.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy())        
            attack = False
            coins += 1
            print(coins)
    
    
        elif player_hitbox_LEFT.collidelist(slime_hitbox) > 0 and attack == True and (framename == 'l1sword' or framename == 'l2sword' or framename == 'l3sword' or framename == 'l4sword'):
            selected_slime = None
            for i in slime_hitbox:
                if player_hitbox_LEFT.colliderect(i):
                    selected_slime = i
                    #print(i)
                    slimelist.append((math.floor(i.x/64), math.floor(i.y/64)))
                    slimelist.append((math.ceil(i.x/64), math.ceil(i.y/64)))
                    slime_hitbox.remove(i)
                    deleted_slimes.append(i.copy())        
            attack = False
            coins += 1
            print(coins)
    
    
        elif attack == True:
            attack = False

    

        # Movements
        if LEFT == 1 and RIGHT != 1 and UP != 1 and DOWN != 1 and player_hitbox_left.collidelist(wall_hitbox) < 0 and framename != 'f1sword' and framename != 'f2sword' and framename != 'f3sword' and framename != 'f4sword' and framename != 'b1sword' and framename != 'b2sword' and framename != 'b3sword' and framename != 'b4sword' and framename != 'r1sword' and framename != 'r2sword' and framename != 'r3sword' and framename != 'r4sword' and framename != 'l1sword' and framename != 'l2sword' and framename != 'l3sword' and framename != 'l4sword':
            LAST_BUTTON = 'LEFT'
            display_scroll[0] -= mspeed * dt
        elif LEFT == -1:
            display_scroll[0] += mspeed * dt
    
        if RIGHT == 1 and LEFT != 1 and UP != 1 and DOWN != 1 and player_hitbox_right.collidelist(wall_hitbox) < 0 and framename != 'f1sword' and framename != 'f2sword' and framename != 'f3sword' and framename != 'f4sword' and framename != 'b1sword' and framename != 'b2sword' and framename != 'b3sword' and framename != 'b4sword' and framename != 'r1sword' and framename != 'r2sword' and framename != 'r3sword' and framename != 'r4sword' and framename != 'l1sword' and framename != 'l2sword' and framename != 'l3sword' and framename != 'l4sword':
            LAST_BUTTON = 'RIGHT'
            display_scroll[0] += mspeed * dt
        elif RIGHT == -1:
            display_scroll[0] -= mspeed * dt
    
        if UP == 1 and LEFT != 1 and RIGHT != 1 and DOWN != 1 and player_hitbox_up.collidelist(wall_hitbox) < 0 and framename != 'f1sword' and framename != 'f2sword' and framename != 'f3sword' and framename != 'f4sword' and framename != 'b1sword' and framename != 'b2sword' and framename != 'b3sword' and framename != 'b4sword' and framename != 'r1sword' and framename != 'r2sword' and framename != 'r3sword' and framename != 'r4sword' and framename != 'l1sword' and framename != 'l2sword' and framename != 'l3sword' and framename != 'l4sword':
            LAST_BUTTON = 'UP'
            display_scroll[1] -= mspeed * dt
        elif UP == -1:
            display_scroll[1] += mspeed * dt
    
        if DOWN == 1 and LEFT != 1 and RIGHT != 1 and UP != 1 and player_hitbox_down.collidelist(wall_hitbox) < 0 and framename != 'f1sword' and framename != 'f2sword' and framename != 'f3sword' and framename != 'f4sword' and framename != 'b1sword' and framename != 'b2sword' and framename != 'b3sword' and framename != 'b4sword' and framename != 'r1sword' and framename != 'r2sword' and framename != 'r3sword' and framename != 'r4sword' and framename != 'l1sword' and framename != 'l2sword' and framename != 'l3sword' and framename != 'l4sword':
            LAST_BUTTON = 'DOWN'
            display_scroll[1] += mspeed * dt
        elif DOWN == -1:
            display_scroll[1] -= mspeed * dt
    
        # Movement Priority (UP, RIGHT, LEFT, DOWN)
        if (UP == 1 and LEFT == 1 and RIGHT != 1 and DOWN != 1) or (UP == 1 and LEFT != 1 and RIGHT == 1 and DOWN != 1) and player_hitbox_up.collidelist(wall_hitbox) < 0 and framename != 'f1sword' and framename != 'f2sword' and framename != 'f3sword' and framename != 'f4sword' and framename != 'b1sword' and framename != 'b2sword' and framename != 'b3sword' and framename != 'b4sword' and framename != 'r1sword' and framename != 'r2sword' and framename != 'r3sword' and framename != 'r4sword' and framename != 'l1sword' and framename != 'l2sword' and framename != 'l3sword' and framename != 'l4sword':
            LAST_BUTTON = 'UP'
            display_scroll[1] -= mspeed * dt
    
        if RIGHT == 1 and LEFT != 1 and UP != 1 and DOWN == 1 and player_hitbox_right.collidelist(wall_hitbox) < 0 and framename != 'f1sword' and framename != 'f2sword' and framename != 'f3sword' and framename != 'f4sword' and framename != 'b1sword' and framename != 'b2sword' and framename != 'b3sword' and framename != 'b4sword' and framename != 'r1sword' and framename != 'r2sword' and framename != 'r3sword' and framename != 'r4sword' and framename != 'l1sword' and framename != 'l2sword' and framename != 'l3sword' and framename != 'l4sword':
            LAST_BUTTON = 'RIGHT'
            display_scroll[0] += mspeed * dt
    
        if LEFT == 1 and RIGHT != 1 and UP != 1 and DOWN == 1 and player_hitbox_left.collidelist(wall_hitbox) < 0 and framename != 'f1sword' and framename != 'f2sword' and framename != 'f3sword' and framename != 'f4sword' and framename != 'b1sword' and framename != 'b2sword' and framename != 'b3sword' and framename != 'b4sword' and framename != 'r1sword' and framename != 'r2sword' and framename != 'r3sword' and framename != 'r4sword' and framename != 'l1sword' and framename != 'l2sword' and framename != 'l3sword' and framename != 'l4sword':
            LAST_BUTTON = 'LEFT'
            display_scroll[0] -= mspeed * dt
        
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
        display.blit(ui, (screen_width-544, 0))
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


