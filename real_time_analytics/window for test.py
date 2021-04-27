import win32gui
import win32con
from pywinauto import Desktop
import itertools
import os
import time 
from pprint import pprint
import pygame as pg
import numpy as np
import win32gui
import win32con
import winxpgui
import win32api
pg.init()
WINDOW_CAPTION = 'ALABAMA'
WHITE = (255, 255, 255)
PG_WINDOW_WIDTH, PG_WINDOW_HEIGHT = 700, 400
screen = pg.display.set_mode((PG_WINDOW_WIDTH, PG_WINDOW_HEIGHT))
surface = pg.Surface((PG_WINDOW_WIDTH, PG_WINDOW_HEIGHT))
pg.display.set_caption(WINDOW_CAPTION)
FONT_SIZE = 30
FONT = pg.font.Font(None, FONT_SIZE)
static_text = [FONT.render('win : ', False, WHITE), FONT.render('lose : ', False, WHITE), FONT.render('tie : ', False, WHITE)]
COLOR = np.array((150, 20, 140))
surface.fill(COLOR)

'''
time.sleep(1)
hwnd = win32gui.FindWindow(None, "ALABAMA")  ## The caption of my empty notepad (MetaPad)
win32gui.SetWindowLong (hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong (hwnd, win32con.GWL_EXSTYLE ) | win32con.WS_EX_LAYERED )
winxpgui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*COLOR), 120, win32con.LWA_COLORKEY)
'''

while 1 :
    time.sleep(0.1)
    surface.fill(COLOR)
    #COLOR += 10;
    for e in pg.event.get() :
        if e.type == pg.QUIT : 
            exit()
    pg.draw.circle(surface, (100, 100, 120), (100, 100), 15)
    screen.blit(surface, (0, 0))
    pg.display.update()