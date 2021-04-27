import treys
from matplotlib import pyplot as plt
import numpy as np
import itertools, collections, functools
import treys
from random import *
from pprint import pprint
import os
import json

'''
path_1 = "F:/hand_hist_70gb_in_zips/"
NB_MAX_PLAYERS = 9
docs = []
path = path_1
filenames = [a for a in os.listdir(path) if 'zip' not in a]
a, n = [], 1
for d1r in filenames :
    loc = os.listdir(path + d1r)
    if loc != [] :
        docs = os.listdir(path + d1r + '/' + loc[0])
        for filename in docs :
            a.append((path, d1r, loc[0], filename, n))
            n += 1
was = {'abs' : 0, 'ftp' : 0, 'ipn' : 0, 'ong' : 0, 'ps' : 0, 'pty' : 0} 
for j in range(len(a)) :
    print(a[j])
    path, d1r, loc, filename, n = a[j]
    mode = d1r.split('-')[0].lower()
    #print(j, was[mode], mode)
    if mode != 'abs' : break

    path_to_orig = path + '/' + d1r + '/' + loc + '/' + filename

    orig = open(path_to_orig, 'r')    
    text = orig.read()
    orig.close()
    if text.replace(' ','') != '' :
        was[mode] += 1
        path_to_modif =  'C:/Users/Danilo/Desktop/poker/get_hand_history/hand_hist_database/' + mode + '/' + str(was[mode]) + '.txt'
        modif = open(path_to_modif, 'w')
        modif.write(text)
        modif.close()
'''


def cleaning_1_abs(hhh) :
    '''
    hhh = hhh.lower().replace(':', '').replace(' -', '').replace(',', '').replace('-', '').replace(' in chips', '')
    for i in range(6) :
        hhh = hhh.replace('\n' * (8 - i), '\n').replace(' ' * (8 - i), ' ')
    ddd = hhh.split('\n')
    hhh = ''
    for dota in ddd:
        if 'table' in dota : dota = 'opangangnamstyle\n'
        elif 'stage' in dota or 'total pot' in dota : dota = ''
        elif '*** flop' in dota : dota = '*** flop ***\n'
        elif 'pocket cards' in dota : dota = ''
        elif '*** turn' in dota : dota = '*** turn ***\n'
        elif '*** river' in dota : dota = '*** river ***\n'
        elif 'summary' in dota : dota = '*** summary ***\n'
        else : dota = dota.strip() + '\n'
        hhh = hhh + dota
    return hhh
    '''
def cleaning_1_ftp(hhh) :
    ''''
    hhh = hhh.lower().replace(':', '').replace(' -', '').replace(',', '').replace('-', '').replace(' in chips', '').replace(' table ', '\ntable').replace('button', 'dealer')
    for i in range(6) :
        hhh = hhh.replace('\n' * (8 - i), '\n').replace(' ' * (8 - i), ' ')
    ddd = hhh.split('\n')
    hhh = ''
    for dota in ddd:
        if 'table' in dota : dota = 'opangangnamstyle\n'
        elif 'tilt' in dota or 'dealer is in seat' in dota : dota = ''
        elif dota.replace(' ', '') == '' : dota = ''
        elif '*** flop' in dota : dota = '*** flop ***\n'
        elif 'hole cards' in dota : dota = ''
        elif '*** turn' in dota : dota = '*** turn ***\n'
        elif '*** river' in dota : dota = '*** river ***\n'
        elif 'summary' in dota : dota = '*** summary ***\n'
        elif 'total pot' in dota and 'rake' in dota : dota = ''
        else : dota = dota.strip() + '\n'
        hhh = hhh + dota
    return hhh
    '''
    
def cleaning_1_ong(hhh) :
    '''
    hhh = hhh.lower().replace(':', '').replace(' -', '').replace(',', '').replace('-', '').replace(' in chips', '').replace('button', 'dealer')
    for i in range(6) :
        hhh = hhh.replace('\n' * (8 - i), '\n').replace(' ' * (8 - i), ' ')
    ddd = hhh.split('\n')
    hhh = ''
    for dota in ddd:
        if 'table' in dota : dota = 'opangangnamstyle\n'
        elif any(temp in dota for temp in ['hand', 'dealer seat', 'players in round']) : dota = ''
        elif 'dealing flop' in dota : dota = '*** flop ***\n'
        elif 'dealing pocket cards' in dota : dota = '*** pocket cards ***\n'
        elif 'dealing turn' in dota : dota = '*** turn ***\n'
        elif 'dealing river' in dota : dota = '*** river ***\n'
        elif 'summary' in dota : dota = '*** summary ***\n'
        elif 'pocket cards' in dota : dota = ''
        elif 'pot' in dota and 'won' in dota and '$' in dota : dota = ''
        elif dota.replace(' ', '') == '' : dota = ''
        else : dota = dota.strip() + '\n'
        hhh = hhh + dota
    return hhh
    '''
def cleaning_1_ps(hhh) :
    hhh = hhh.lower().replace(':', '').replace(' -', '').replace(',', '').replace('-', '').replace(' in chips', '').replace(' table ', '\ntable').replace('button', 'dealer')
    for i in range(6) :
        hhh = hhh.replace('\n' * (8 - i), '\n').replace(' ' * (8 - i), ' ')
    ddd = hhh.split('\n')
    hhh = ''
    for dota in ddd:
        dota = dota.strip()
        if dota.split(' ')[0].strip() == 'table' and "'" in dota and 'is the dealer' in dota  and 'joins' not in dota and 'leaves' not in dota : dota = 'opangangnamstyle\n'
        elif any(temp in dota for temp in ['pokerstars', 'dealer seat', 'players in round', 'joins', 'leaves']) : dota = ''
        elif dota.replace(' ', '') == '' : dota = ''
        elif '*** flop' in dota : dota = '*** flop ***\n'
        elif 'hole cards' in dota : dota = '*** pocket cards ***\n'
        elif '*** turn' in dota : dota = '*** turn ***\n'
        elif '*** river' in dota : dota = '*** river ***\n'
        elif 'summary' in dota : dota = '*** summary ***\n'
        elif 'pocket cards' in dota : dota = ''
        elif 'total pot' in dota and 'rake' in dota : dota = ''
        else : dota = dota.strip() + '\n'
        hhh = hhh + dota
    return hhh

def sub_cleaning_ps_1(hhh) :
    ddd = hhh.split('\n')
    hhh = ''
    for dindex in range(2, len(ddd)) :
        if 'opangangnamstyle' in ddd[dindex] : 
            if ddd[dindex - 1].split(' ')[0] == 'seat' and ddd[dindex + 1].split(' ')[0] == 'seat' : hhh += ddd[dindex].strip() + '\n'        
        else : hhh += ddd[dindex].strip() + '\n'
    return hhh


NB_MAX_PLAYERS = 9
path = "C:/Users/Danilo/Desktop/poker/get_hand_history/hand_hist_database/"

mode = 'ps'
for j in range(1, len(os.listdir(path + mode)) + 1) : 
    print(j)
    path_to_orig = path + mode + '/' + str(j) + '.txt'
    path_to_modif = path_to_orig
    #path_to_modif = path + mode + '/' + 'modif' + str(j) + '.txt'
    
    orig = open(path_to_orig, 'r')
    hhh = orig.read()
    orig.close()

    modif = open(path_to_modif, 'w')
    modif.write(sub_cleaning_ps_1(hhh))
    modif.close()
    









#print(np.array([1, 2, 3])[::-1])
#a = 12
#print(a % 24)
#print(np.dot(np.array([[1, 2], [3, 4]]), np.ones((2, 2))))



'''
from matplotlib import pyplot as plt

tile_coord = (5, 5)
tile_width = 25
raw = tile_coord[1]
tile = tile_coord[0]

EPS = 0.000001
x, y = tile_coord
points = np.array([[x - 0.5, y - 0.5], [x + 0.5, y - 0.5], [x + 0.5, y + 0.5], [x - 0.5, y + 0.5]])
player_pos = np.array([1, 1])
k = 0.8
pairs = [[0, 1], [1, 2], [2, 3], [3, 0]]
points_adj = points - player_pos
vectors = np.array([points[pair[1]] - points[pair[0]] for pair in pairs])
def kal(point, vector, k) :
    if vector[0] == 0 : temp = EPS
    else : temp = vector[1] / vector[0]
    x = (-point[0] * temp + point[1]) / (k - temp)

    new_point = np.array([x, x * k])
    print(point, vector, temp, x, k*x)
    
    plt.show()
    if vector[0] == 0 and point[1] <= new_point[1] <= point[1] + vector[1] :
        return new_point
    if vector[1] == 0 and point[0] <= new_point[0] <= point[0] + vector[0] :
        return new_point
    return False 
for i in range(1, 100) :
    print(kal(points_adj[0], vectors[0], 1 + 1 / i))

'''