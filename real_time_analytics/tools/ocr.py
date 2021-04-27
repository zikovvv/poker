from pywinauto import Desktop
import win32gui
import win32con    
import pyautogui as pag
import d3dshot
import cv2
import numpy as np
import time
from PIL import Image
import pygame
import os
import json
from pprint import pprint
import collections
import itertools
import functools
from windows_handler import *
import pygame as pg
#import pytesseract



def to_binary(image, thresh) :
    new_image = np.zeros((image.shape[0], image.shape[1]))
    for y, raw in enumerate(image) :
        for x, pix in enumerate(raw) :
            new_image[y][x] = 1 if sum(pix) / 3 > thresh else 0
            #new_image[y][x] = 1 if sum(pix) / 3 > thresh else 0
    return new_image.astype(int)

def crop(image) :
    if np.count_nonzero(image) :
        while 1 not in image[0 : , 0] : image = np.delete(image, 0, axis = 1)
        while 1 not in image[0 : , -1] : image = np.delete(image, -1, axis = 1)
        while 1 not in image[0] : image = np.delete(image, 0, axis = 0)
        while 1 not in image[-1] : image = np.delete(image, -1, axis = 0)
        return image
    return np.array([[]])
            
def to_symbols(image, height_number, small_font = False) :
    symbols = []
    i = 0
    while i < image.shape[1] :
        column = image[0 : , i]
        if np.count_nonzero(column) > (1 if small_font else 0) :
            symbol = []
            #тому шо 4 і 7 і 34 і 44 і тд з'єднуються разом того шо дуже довгий хвостик і він шириною в 1 пх зазвичай тому можна нахуй його відрізати
            while np.count_nonzero(column) > (1 if small_font else 0) :
                symbol.append(column)
                if i < image.shape[1] :
                    column = image[0 : , i]
                    i += 1
                else : break
            symbols.append(crop(np.rot90(np.array(symbol))[::-1]))
        i += 1
    new_symbols = []
    for symbol in symbols :
        new_symbol = np.zeros((height_number, height_number)).astype(int)
        for j in range(symbol.shape[0]) :
            for i in range(symbol.shape[1]) :
                if i == height_number or j == height_number : break
                new_symbol[j][i] += symbol[j][i]
        new_symbols.append(new_symbol)
    return new_symbols

def to_str(binary) :
    string = ""
    for raw in binary :
        for pix in raw :
            string += str(pix)
        string += ';'
    return string

def str_to_np1(symbol) :
    symbol = symbol.split(';')[ : -1]
    npsym = np.zeros((len(symbol), len(symbol[0])))
    for j, raw in enumerate(symbol) :
        for i, pix in enumerate(raw) :
            npsym[j][i] = int(symbol[j][i])
    return npsym.astype(int)

def str_to_np(symbol) :
    return np.fromiter(symbol.replace(';', ''), int).reshape(-1, len(symbol.split(';')[0]))

def recognize_symbol(symbol, symbols_recognized_np, symbols_recognized_chars) :
    errs = dict.fromkeys(POSSIBLE_CHARS, 1)
    nb_sym = np.count_nonzero(symbol)
    len_symbol, width_symbol = symbol.shape 
    s = len_symbol * width_symbol
    for recognized, possible_char in zip(symbols_recognized_np, symbols_recognized_chars) :
        nb_diff = np.count_nonzero(np.abs(recognized - symbol))
        err = nb_diff / s
        errs[possible_char] = err if err < errs[possible_char] else errs[possible_char] 
    res = POSSIBLE_CHARS[np.argmin(list(errs.values()))]
    if res == '.' and 1 == 0 and len_symbol < 20 :
        print('SYMBOL : \n', symbol)
        pprint(errs)
        for recognized, possible_char in zip(symbols_recognized_np, symbols_recognized_chars) :
            nb_diff = np.count_nonzero(np.abs(recognized - symbol))
            if possible_char == '.' or possible_char == '1' :
                pass
                #print('recognized\n', recognized, '\ndiff\n', '''np.abs(recognized - symbol)'''  '\nchar\n', possible_char, '\ncount_diff\n', nb_diff)
    return res

def stacks_and_pot(alive, image = None) :
    if type(image) == type(None) :
        image = d.screenshot(region = (0, 0, width_pokerstars, height_pokerstars))
    stacks = []
    for stack_coord, live in zip(STACKS_RECTS_COORDS, alive) :
        if live :
            symbols = to_symbols(crop(to_binary(image[stack_coord[1] : stack_coord[3], stack_coord[0] : stack_coord[2]], 100)), HEIGHT_SYMBOL_STACK)
            recognized_stack = functools.reduce(lambda string, symbol : string + recognize_symbol(symbol, symbols_recognized_stack_np, symbols_recognized_stack_chars), [''] + symbols)
            try : 
                if 'bb' in recognized_stack :
                    stacks.append(float(recognized_stack[ : -2]))   
                elif '$' in recognized_stack :
                    stacks.append(float(recognized_stack))  
                elif 'allin' in recognized_stack : 
                    stacks.append(0)
                else :
                    stacks.append(float(recognized_stack.replace('.', '')))
            except BaseException : 
                if 'b' in recognized_stack : 
                    print(recognized_stack)
                stacks.append(None)
        else :             
            stacks.append(None)

    symbols = to_symbols(crop(to_binary(image[POT_RECT_COORD[1] : POT_RECT_COORD[3], POT_RECT_COORD[0] : POT_RECT_COORD[2]], 100)), HEIGHT_SYMBOL_POT, True)
    recognized_pot = functools.reduce(lambda string, symbol : string + recognize_symbol(symbol, symbols_recognized_pot_np, symbols_recognized_pot_chars), [''] + symbols)
    try :
        recognized_pot = recognized_pot.split(':')[-1] 
        if 'b' in recognized_pot : pot = float(recognized_pot[ : -2])    
        else : pot = float(recognized_pot.replace('.', ''))
    except BaseException : 
        pot = None  

    return [s != None for s in stacks], stacks, pot

def get_button_pos(thresh = 100, image = None) :
    if type(image) == type(None) :
        image = d.screenshot(region = (0, 0, width_pokerstars, height_pokerstars))
    size = [WIDTH_BUTTON_IMAGE] * 2
    colors = [
        [219, 224, 222],
        [163, 163, 166],
        [137, 138, 140],
        [223, 220, 219],
        [223, 220, 219]
    ]
    for j, coord in enumerate(COORDS_BUTTON) :
        button_image = image[coord[1] : coord[3], coord[0] : coord[2]] 
        white = 0
        for y in range(W) :
            for x in range(W) :
                if np.mean(button_image[y][x]) > thresh : 
                    white += 1
        if white > 10 :
            return j 
    return False

def mining_symbols(PARAM_draw_big_image = 0,
        PARAM_add_new_txt_symbols_stacks = 0,
        PARAM_add_new_txt_symbols_pot = 0,
        PARAM_draw_binary_picture_stacks = 1,
        PARAM_draw_binary_picture_pot = 0,
        PARAM_display_fps = 1) :
    
    #INIT WINDOW
    pygame.init()
    FONT_SIZE = 40
    font = pygame.font.Font(None, FONT_SIZE)
    PROGRAM_WINDOW_WIDTH, PROGRAM_WINDOW_HEIGHT = 1200, 700
    surface = pygame.display.set_mode((PROGRAM_WINDOW_WIDTH, PROGRAM_WINDOW_HEIGHT))
    def draw_binary_picture(symbol, scale_koef, offset_x, offset_y, koef_offset_x, koef_offset_y, j, n) :
        for y, row in enumerate(symbol) :  
            for x, pix in enumerate(row) :
                if pix :
                    pygame.draw.circle(surface, (255, 255, 255), (x * scale_koef + n * koef_offset_x + offset_x, y * scale_koef + j * koef_offset_y + offset_y), 1)
        pygame.draw.circle(surface, (0, 0, 255), (n * koef_offset_x + offset_x, j * koef_offset_y + offset_y), 3)

    if PARAM_add_new_txt_symbols_stacks :
        file_txt_symbols_stacks = open(FOLDER_ABS_PATH + "\\txt\\symbols.txt", "r+") 
        set_txt_symbols_stacks = set(file_txt_symbols_stacks.read().split('\n'))
        file_txt_symbols_stacks.close()
        file_txt_symbols_stacks = open(FOLDER_ABS_PATH + "\\txt\\symbols.txt", "w")
    
    if PARAM_add_new_txt_symbols_pot :
        file_txt_symbols_pot = open(FOLDER_ABS_PATH + "\\txt\\symbols_pot.txt", "r+") 
        set_txt_symbols_pot = set(file_txt_symbols_pot.read().split('\n'))
        print(set_txt_symbols_pot)
        file_txt_symbols_pot.close()
        file_txt_symbols_pot = open(FOLDER_ABS_PATH + "\\txt\\symbols_pot.txt", "w")

    while 1 :
        for e in pygame.event.get():
            if e.type == pygame.QUIT :
                if PARAM_add_new_txt_symbols_stacks :
                    for s in set_txt_symbols_stacks:
                        file_txt_symbols_stacks.write(s)
                        file_txt_symbols_stacks.write('\n')
                    file_txt_symbols_stacks.close()
                if PARAM_add_new_txt_symbols_pot :
                    for s in set_txt_symbols_pot:
                        file_txt_symbols_pot.write(s)
                        file_txt_symbols_pot.write('\n')
                    file_txt_symbols_pot.close()
                exit()
        surface.fill((5, 0, 30))

        if PARAM_display_fps : 
            time_frame_start = time.time()
        image = d.screenshot(region = (0, 0, width_pokerstars, height_pokerstars))
        #STACKS
        for j, stack_coord in enumerate(STACKS_RECTS_COORDS) :
            stack = crop(to_binary(image[stack_coord[1] : stack_coord[3], stack_coord[0] : stack_coord[2]], 110))
            symbols = to_symbols(stack, HEIGHT_SYMBOL_STACK)
            for n, symbol in enumerate(symbols) :
                if PARAM_draw_binary_picture_stacks :
                    draw_binary_picture(symbol, 2, 30, 40, 50, 30, j, n)
                
        if PARAM_add_new_txt_symbols_stacks :
            l = len(set_txt_symbols_stacks)
            set_txt_symbols_stacks.add(to_str(symbol))
            if l < len(set_txt_symbols_stacks) : 
                print(symbol)
            surface.blit(font.render("stack symbols unique got : " + str(len(set_txt_symbols_stacks)), False, WHITE), (400, 20))

        #POT
        pot = crop(to_binary(image[POT_RECT_COORD[1] : POT_RECT_COORD[3], POT_RECT_COORD[0] : POT_RECT_COORD[2]], 120))
        symbols = to_symbols(pot, HEIGHT_SYMBOL_POT, True)
        for n, symbol in enumerate(symbols) :
            if PARAM_draw_binary_picture_pot :
                draw_binary_picture(symbol, 2, 400, 40, 20, 30, 1, n)

        if PARAM_add_new_txt_symbols_pot :
            set_txt_symbols_pot.add(to_str(symbol))
            surface.blit(font.render("pot symbols unique got : " + str(len(set_txt_symbols_pot)), False, WHITE), (400, 20))

        if PARAM_display_fps :
            surface.blit(font.render("FPS " + str(round(1 / (time.time() - time_frame_start), 2)), False, WHITE), (0, 0))

        pygame.display.update()

WIDTH_BUTTON_IMAGE = 15
COORDS_BUTTON = [
        [775, 247],
        [727, 408],
        [400, 445],
        [204, 340],
        [218, 253],
        [537, 192]
    ]
for i in range(6) :
    COORDS_BUTTON[i].extend([COORDS_BUTTON[i][0] + WIDTH_BUTTON_IMAGE, COORDS_BUTTON[i][1] + WIDTH_BUTTON_IMAGE])


GAME_WINDOW_WIDTH = 1000; 
POSSIBLE_CHARS = ['', '.', ':', '$', 'b', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'allin']
WHITE = (255, 255, 255)
HEIGHT_SYMBOL_STACK = 20
WIDTH_SYMBOLS_STACK = 100
STACKS_RECTS_COORDS = [[815, 196],
                [844, 407],
                [473, 530],
                [48, 404],
                [74, 196],
                [416, 130]]
for i in range(6) :
    STACKS_RECTS_COORDS[i].extend([STACKS_RECTS_COORDS[i][0] + WIDTH_SYMBOLS_STACK,
                                    STACKS_RECTS_COORDS[i][1] + HEIGHT_SYMBOL_STACK])

HEIGHT_SYMBOL_POT = 15
POT_RECT_COORD = (430, 230, 730, 230 + HEIGHT_SYMBOL_POT)
FOLDER_ABS_PATH = os.path.dirname(os.path.abspath(__file__))

symbols_recognized_stack = json.load(open(FOLDER_ABS_PATH + "\\txt\\symbols.json", "r+"))
len_stack = len(list(symbols_recognized_stack.values()))
symbols_recognized_stack_np = np.empty((len_stack, HEIGHT_SYMBOL_STACK, HEIGHT_SYMBOL_STACK)).astype(int)
symbols_recognized_stack_chars = [''] * len_stack
for j, temp in enumerate(list(symbols_recognized_stack.items())) :
    symbols_recognized_stack_np[j] = str_to_np(temp[0]) 
    symbols_recognized_stack_chars[j] = temp[1]

symbols_recognized_pot = json.load(open(FOLDER_ABS_PATH + "\\txt\\symbols_pot.json", "r+"))
len_pot = len(list(symbols_recognized_pot.values()))
symbols_recognized_pot_np = np.empty((len_pot, HEIGHT_SYMBOL_POT, HEIGHT_SYMBOL_POT)).astype(int)
symbols_recognized_pot_chars = [''] * len_pot
for j, temp in enumerate(list(symbols_recognized_pot.items())) :
    symbols_recognized_pot_np[j] = str_to_np(temp[0]) 
    symbols_recognized_pot_chars[j] = temp[1]

d = d3dshot.create(capture_output = "numpy")
move_all_holdem_windows(GAME_WINDOW_WIDTH)
_, _, width_pokerstars, height_pokerstars = win32gui.GetWindowRect(HOLDEM_WINDOWS_HWNDS[0])
print('ocr loaded')




'''
hwnd = find_all_hwnds_by_substr("ALABAMA")[0]
win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
win32gui.SetForegroundWindow(hwnd)
width_pokerstars, height_pokerstars = holdem_game_window_transform_and_change_pos(GAME_WINDOW_WIDTH)
'''















'''
switch = 3 
if switch == 0 : 
    while 1 :
        asd = stacks_and_pot()
        f = open(FOLDER_ABS_PATH + "\\txt\\stacks_and_pot.txt", "r+")
        f.truncate(0)
        f.write(str(asd[0]) + str(asd[1]))
        #print(str(asd[0]) + str(asd[1]))
        f.close()
elif switch == 1 :
    mining_symbols()
'''





