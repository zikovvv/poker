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
FOLDER_ABS_PATH = os.path.dirname(os.path.abspath(__file__))
GAME_WINDOW_WIDTH = 1000; 

def to_str(binary) :
    string = ""
    for raw in binary :
        for pix in raw :
            string += str(pix)
        string += ';'
    return string

def str_to_np(symbol) :
    symbol = symbol.split(';')[ : -1]
    npsym = np.zeros((len(symbol), len(symbol[0])))
    for j, raw in enumerate(symbol) :
        for i, pix in enumerate(raw) :
            npsym[j][i] = int(symbol[j][i])
    return npsym.astype(int)

PROGRAM_WINDOW_WIDTH, PROGRAM_WINDOW_HEIGHT = 1200, 700

switch = 0
if switch == 0 :
    #f = open(FOLDER_ABS_PATH + "\\txt\\symbols.json", "r+") 
    #keys = list(json.load(f))
    #f.close()

    SYMBOLS_GLOBAL = {}
    f = open(FOLDER_ABS_PATH + "\\txt\\symbols.txt", "r+") 
    for elem in f.read().split('\n')[1 : ] :
        for raw in elem.split(';') :
            print(raw.replace('0', ' '))            
        SYMBOLS_GLOBAL[elem] = input()
    f.close()

    f = open(FOLDER_ABS_PATH + "\\txt\\symbols.json", "r+")
    f.truncate(0)
    json.dump(SYMBOLS_GLOBAL, f)
    f.close()
elif switch == 1 :
    f = open(FOLDER_ABS_PATH + "\\txt\\symbols_pot.txt", "r+")
    for key in f.read().split('\n') :
        print(str_to_np(key))
elif switch == 2 :
    f = open(FOLDER_ABS_PATH + "\\txt\\symbols.json", "r+")
    SYMBOLS_GLOBAL_DOTA = json.load(f)
    SYMBOLS_GLOBAL = {}
    for key, val in SYMBOLS_GLOBAL_DOTA.items() :
        a = str_to_np(key)
        if val != 'asddd' :
            print(a, val)
            i = input()
            if i == '-' :
                print(SYMBOLS_GLOBAL_DOTA[key])
            else :
                SYMBOLS_GLOBAL[key] = i
        else :
            SYMBOLS_GLOBAL[key] = val
    f.close()
    
    f = open(FOLDER_ABS_PATH + "\\txt\\symbols.json", "r+")
    f.truncate(0)
    json.dump(SYMBOLS_GLOBAL, f)
    f.close()
    
elif switch == 3 :
    SYMBOLS_GLOBAL = {}
    f = open(FOLDER_ABS_PATH + "\\txt\\symbols.json", "r+") 
    for key, val in json.load(f).items() :
        if val == "" :
            print(str_to_np(key))
            SYMBOLS_GLOBAL[key] = input()
    f.close()
elif switch == 4 :
    SYMBOLS_GLOBAL = {}
    f = open(FOLDER_ABS_PATH + "\\txt\\symbols.json", "r+") 
    keys = list(json.load(f))
    f.close()

    file_txt_symbols_stacks = open(FOLDER_ABS_PATH + "\\txt\\symbols.txt", "w")
    for s in keys :
        file_txt_symbols_stacks.write(s)
        file_txt_symbols_stacks.write('\n')
    file_txt_symbols_stacks.close()












