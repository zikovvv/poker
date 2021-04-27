import win32gui
import win32con
from pywinauto import Desktop
import itertools
import os
import time 
from pprint import pprint
import pygame as pg
import numpy as np
import kivy
print("<<<<<<<<<<<>>>>>>>>>>>")
width_pokerstars, height_pokerstars = 0, 0
from ocr import * 
from calculate_chanse_and_show import * 

def exit_monitoring() :
    for e in pg.event.get() :
        if e.type == pg.QUIT : 
            exit()

pg.init()
NB_PLAYERS = 6
WINDOW_CAPTION = 'ALABAMA'
WHITE = (255, 255, 255)
AFK = [80] * 3
ACTIVE = [150] * 3
CLICKED = [50, 180, 50]
BG_COLOR = (0, 40, 0)
PG_WINDOW_WIDTH, PG_WINDOW_HEIGHT = 700, 600
surface = pg.display.set_mode((PG_WINDOW_WIDTH, PG_WINDOW_HEIGHT))
pg.display.set_caption(WINDOW_CAPTION)
FONT_SIZE = 30
FONT = pg.font.Font(None, FONT_SIZE)


info = dict.fromkeys(HOLDEM_WINDOWS_HWNDS)




button = None
stacks_initial = np.zeros(NB_PLAYERS).astype(float)
prev_len_board = 0
nb_players_alive = 0
alive = [True] * NB_PLAYERS
nb_players_alive_initial = np.count_nonzero(alive)
max_bet = 0
restart_button = {
    'box' : (400, 20, 180, 70),
    'clicked' : 0,
    'color' : AFK
}
while 1 :
    mouse = pg.mouse.get_pos()
    restart = 0
    surface.fill((0, 0, 0))
    for e in pg.event.get() :
        if e.type == pg.QUIT : 
            exit()
        elif e.type == pg.MOUSEBUTTONUP : 
            if restart_button['box'][0] <= mouse[0] <= restart_button['box'][0] + restart_button['box'][2] and restart_button['box'][1] <= mouse[1] <= restart_button['box'][1] + restart_button['box'][3] and restart_button['clicked'] :
                restart = 1
    #MOVE IF UNDER POKER
    pg_window_handler(WINDOW_CAPTION, width_pokerstars, height_pokerstars, PG_WINDOW_WIDTH, PG_WINDOW_HEIGHT)

    #REAL SHIT
    board, hand, nb_players, cycle = get_table_state()

    run = 1
    err = False
    while run : 
        exit_monitoring()
        SCREENSHOT = d.screenshot(region = (0, 0, width_pokerstars, height_pokerstars))
        try : 
            alive, stacks, pot = stacks_and_pot([1] * NB_PLAYERS, SCREENSHOT)
            SB, BB = pot / 3, pot / 3 * 2 
            if np.count_nonzero(alive) <= 1 :
                raise Exception("No stacks")
            run = 0
            if err :
                print("got good info")
        except BaseException :
            if not err :
                print('waiting for good info...')
                err = True
            
    #NEW GAME STARTED
    if (len(board) == 0 and prev_len_board != 0) or restart :
        button = False
        while not button :
            print("BUTTON")
            button = get_button_pos(100, SCREENSHOT)
        #alive, stacks, pot = stacks_and_pot([1] * NB_PLAYERS, SCREENSHOT)
        nb_players_alive_initial = np.count_nonzero(alive)
        nb_players_alive = nb_players_alive_initial
        stacks_initial = np.array(stacks).astype(float)
        #ADD BB SB LATER
        bets = np.zeros(NB_PLAYERS)
        bets[(button + 1) % NB_PLAYERS] = SB
        bets[(button + 1) % NB_PLAYERS] = BB
        print(stacks_initial, bets)
        print(nb_players_alive_initial)
    else :
        bets = stacks_initial - np.array(stacks).astype(float)
        nb_players_alive = np.count_nonzero(alive)
    prev_len_board = len(board)

    #CALC WIN CHANSES
    if len(hand) == 2 : chanses = get_chanse(board, hand, nb_players_alive_initial) 
    else : chanses = [0, 0, 0]
    #CALC EXPECTED VAL
    try :
        expected_val = (pot - bets[2]) * chanses[0] - bets[2] * chanses[1]
        #max_bet = (pot * chanses[0]) / chanses[1]
        #FORMULA###pot  * chanses[0] = bets[2]
        max_bet = (pot * chanses[0])
    except BaseException :
        expected_val = None

    #RENDER
    try :
        S = ("cycle : %s" % cycle ,
        "board : " + ' '.join(board),
        "hand : " + ' '.join(hand),
        "win : %s" % round(chanses[0] * 100, 1) + "% (" + ("1/%s" % round(1 / chanses[0], 2) if chanses[0] > 0.001 else "INF") + ")",
        "lose : %s" % round(chanses[1] * 100, 1) + "% (" + ("1/%s" % round(1 / chanses[1], 2) if chanses[0] > 0.001 else "INF") + ")",
        "tie : %s" % round(chanses[2] * 100, 1) + "% (" + ("1/%s" % round(1 / chanses[2], 2) if chanses[0] > 0.001 else "INF") + ")",
        "pot : %s" % round(pot, 2), 
        *[("%s%sstack: %s : %s" % (j if j != 2 else "me", " (button) " if j == button else "", stacks[j], bets[j]))if alive[j] else "%s dead" % j for j in range(NB_PLAYERS)])
        for j, line in enumerate(S) :
            surface.blit(FONT.render(line, False, (0, 200, 0)), (10, (FONT_SIZE + 2) * j))
    except BaseException :
        print("bad numbers")

    
    '''
    images, images_rgb, button = get_button_pos(100)
    for j in range(max([len(images), len(images_rgb)])) :
        im, im_rgb = images[j], images_rgb[j]
        surface.blit(im, (100 + j * WIDTH_BUTTON_IMAGE, 500))
        surface.blit(im_rgb, (100 + j * WIDTH_BUTTON_IMAGE, 480))
        pg.draw.circle(surface, (255, 255, 255), (100 + j * WIDTH_BUTTON_IMAGE, 520), 3)
    '''

    pg.draw.rect(surface, restart_button['color'], restart_button['box'])
    surface.blit(FONT.render("RESTART", False, (255, 255, 255)), (restart_button['box'][0],restart_button['box'][1]))
    pg.display.update()
    