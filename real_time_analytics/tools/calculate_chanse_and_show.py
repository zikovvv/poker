from pywinauto import Desktop
import win32gui
import win32con    
import pyautogui as pag
import d3dshot
import cv2
import numpy as np
import time
from PIL import Image
import pygame as pg
import os
APPDATA_PATH = os.getenv('APPDATA').split('Roaming')[0]
FOLDER_ABS_PATH = os.path.dirname(os.path.abspath(__file__))
def get_table_state(filepath = APPDATA_PATH + 'Local/PokerStars/PokerStars.log.0', state_index = -1, verbose = []) :
    current = open(filepath).read().split('CocosTableState')[state_index].split('\n')[0]
    #current = '(p2_11): type:20,o:5, board(5,1)[0: - - - - -], players:  0:No+ uunpB uunpB 1:No+ uunpB uunpB 2:No+ uunpB uunpB 3:Ne+ - - 4:No+ uunpB uunpB 5:Lo+ 8cnpB 9dnpB'
    #out
    if 0 in verbose : print(current)

    txtboard, txthand, board, hand = current.split('[0: ')[1].split(']')[0].split(' '), current.split('players: ')[1].split(':'), [], []
    
    #out
    if 1 in verbose : print(txtboard, txthand, board, hand)

    nb_players = 1
    hand = ['None']
    for i, s in enumerate(txthand) :
        temp = s.split(' ')
        if len(temp) == 4 and len(temp[3]) == 1 : temp.pop(3)

        #out
        if 3 in verbose : print(i, temp)

        if len(temp) == 3 :
            if '-' not in temp and 'uun' not in temp[1] :
                hand = [temp[1][ : 2].lower(), temp[2][ : 2].lower(), ]
            if 'uun' in temp[1] : nb_players += 1

    #out
    if 4 in verbose : print(txthand, txtboard)

    for i in range(5) : 
        if txtboard[i] != '-' : 
            board.append(txtboard[i][0 : 2].lower())

    if len(board) == 0 : cycle = 1
    elif len(board) > 0 : cycle = len(board) - 1
    return board, hand, nb_players, cycle


def get_chanse(board, hand, nb_players) :
    cards_str = ' '.join(board + hand)
    #print('cmd /c "'+ FOLDER_ABS_PATH +'\c_functions chanse %s %s"' % (cards_str, nb_players))
    os.system('cmd /c "'+ FOLDER_ABS_PATH +'\c_functions chanse %s %s"' % (cards_str, nb_players))
    with open(FOLDER_ABS_PATH + "\\txt\\chanses.txt", "r+") as f :
        chanses = f.read().split(';')[ : 3]
        f.close()
    return [float(c) for c in chanses]

print('calc loaded')

'''
while 1 :
    board, hand, nb_players, cycle = get_table_state()
    print(get_chanse(board, hand, 6))
'''



