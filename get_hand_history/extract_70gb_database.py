from pprint import pprint 
import numpy as np
import collections
from zipfile import ZipFile
import os
import pandas as pd
import json

NB_MAX_PLAYERS = 9
def prepare(hhh, mode) :
    global NB_MAX_PLAYERS
    #split by raws and clear
    hhh = [h for h in hhh.split("\n") if h != '\n' and h != '' and h != ' ' and len(h) > 8 and 'left' not in h and 'table' not in h and "hold'em" not in h and 'has' not in h and 'button is in' not in h and 'feeling' not in h]
    #seats analysis and changing names
    #connect seats and names of players
    info, i, stacks = [], 0, [0 for i in range(NB_MAX_PLAYERS)]
    while True :
        if 'seat' in hhh[i] and 'seat #' not in hhh[i] and 'button' not in hhh[i] and 'dealer' not in hhh[i] and 'posts' not in hhh[i] : 
            info.append([hhh[i].split(' ($')[0].split(' ')[-1], int(hhh[i].split('seat ')[1].split(' ')[0])])        
        if 'small blind' in hhh[i] : break 
        i += 1
    #indices and names otdelno
    iii, nnn = [b[1] for b in info], [b[0] for b in info] 
    i, n = info[nnn.index(hhh[i].split(' posts')[0])][1], 1, 
    #renaming seats in shifted order
    while n <= len(info) :
        if i in iii :
            info[iii.index(i)].append(n)
            n += 1
        i += 1
        if i > NB_MAX_PLAYERS : i = 1
    #change all names in text of game into player_#№#_
    for j, h in enumerate(hhh) :
        temp = [a in h for a in nnn]
        if any(temp) :
            hhh[j] = h.replace(nnn[temp.index(True)], 'player_#' + str(info[temp.index(True)][2]) + '#_').replace(' -', '')
    #new shifted order
    iii = [b[2] for b in info]
    #pprint(hhh)
    #while game not started get general info
    i = 0 
    while True :
        #move pocket cards up on 2 positions to make sb and bb action be in preflop not in pregame general info
        if 'pocket cards' in hhh[i] :
            hhh.pop(i)
            hhh.insert(i - 2, "*** pocket cards ***")
            break
        #get stacks
        if mode == 'abs' :
            if 'in chips' in hhh[i] :
                stacks[int(hhh[i].split('_#')[1].split('#_')[0]) - 1] = float(hhh[i].split('($')[1].split(' in chips')[0])
        if mode == 'ftp' :
            if i < NB_MAX_PLAYERS and '($' in hhh[i] :
                stacks[int(hhh[i].split('_#')[1].split('#_')[0]) - 1]  
        #get big blind size in usd
        if 'big' in hhh[i] :
            big_blind_size = float(hhh[i].split(' $')[1].split(' ')[0])
        i += 1
    #print(nnn, iii, info)
   # pprint(hhh)
    
    add_info = {}
    for h in hhh :
        if 'won' in h and '_#' in h and 'seat' in h :
            add_info['winner'] = int(h.split('player_#')[1].split('#_')[0])
            if mode == 'abs' :
                for i in range(len(hhh)) :
                    if 'shows' in hhh[i] and 'player_#' + str(add_info['winner']) + '#_' in hhh[i] :
                        add_info['hand'] = hhh[i].split('shows [')[1].split(']')[0].split(' ') 
            elif mode == 'ftp' or 'ps' :
                add_info['hand'] = h.split('showed [')[1].split(']')[0].split(' ')
        elif 'board' in h :
            add_info['board'] = h.split('[')[1].split(']')[0].split(' ')

    return info, hhh, stacks, big_blind_size, add_info

def extract(hhh, mode) :
    info, hhh, stacks, big_blind_size, add_info = prepare(hhh, mode)

    #all info into matrix
    df = [[['.' for n in range(NB_MAX_PLAYERS)] for i in range(NB_MAX_PLAYERS)] for n in range(16)]
    
    #changing through the game values
    callsize, pot, bets = 0, 0, [0 for i in range(NB_MAX_PLAYERS)]
    
    #helping algoritm
    cycles_offsets, can = {'preflop' : 0, 'flop' : 4, 'turn' : 8, 'river' : 12}, False
    players_alive, action_short = [i for i in range(1, len(info) + 1)], {'calls' : 'c', 'checks' : 'k', 'raises' : 'r', 'bets' : 'r', 'folds' : 'f', 'posts' : 'c', 'all-in(raise)' : 'r', 'all-in' : 'c'}
    # 0 moves
    # 1 amounts
    # 2 bets
    # 3 pots
    # 4 stacks
    # 5 callsizes 
    for h in hhh :
        if '*** pocket cards' in h : cycle, can, incycle_counter = 'preflop', True, 0
        elif '*** flop' in h : cycle, incycle_counter = 'flop', 0
        elif '*** turn' in h : cycle, incycle_counter = 'turn', 0 
        elif '*** river' in h : cycle, incycle_counter = 'river', 0
        elif '*** show down' in h or '*** summary' in h : can = False
        elif can :
            if any([a in h for a in list(action_short.keys())]) :
                if  'player_#' in h :
                    seat = int(h.split('player_#')[1].split('#_')[0])
                    action = h.split(str(seat) + '#_ ')[1].split(' ')[0]
                    offset = cycles_offsets[cycle] + incycle_counter

                    amount = 0
                    if '$' in h :
                        amount = float(h.split('$')[1].split(' ')[0])
                        if action == 'bets' or action == 'raises' or action == 'posts' or 'all-in(raise)' in action :
                            callsize = float(h.split(' $')[-1].split(' ')[0])

                    pot += amount
                    stacks[seat - 1] -= amount
                    bets[seat - 1] += amount

                    df[offset][seat - 1] = [
                        action_short[action],
                        round(amount / big_blind_size, 2),
                        round(bets[seat - 1] / big_blind_size, 2),
                        round(pot / big_blind_size, 2),
                        round(stacks[seat - 1] / big_blind_size, 2),
                        round(callsize / big_blind_size, 2)]

                    if action == 'folds' :
                        players_alive.pop(players_alive.index(seat))
                    
                    if seat >= max(players_alive) :
                        incycle_counter += 1
                else : return False
    df.append(add_info)            
    return df

def save_extracted(path, d1r, loc, filename, n, diagnoz = False) :
    MODE = d1r.split('-')[0].lower()
    
    with open(path + d1r + '/' + loc[0] + '/' + filename, 'r') as f:
        hist = f.read()
        f.close()
    hist = hist.lower().replace(':', '').replace(' -', '').replace(',','').replace('  ',' ').replace('   ', ' ').replace('the ', '').replace('hole', 'pocket').replace('adds', 'calls').replace('button', 'dealer')
    hist = hist.split({'ps' : 'table', 'abs' : 'table', 'ftp' : '\n\n\n\n\n\n\n\n\n'}[MODE])

    hist.pop(0)
    hist_arr = []

    #cleaning according to the mode:
    #single player win after showed hand
    #bb and sb posted
    #everybody in table(no sitout action)
    #no ante only bb and sb
    '''
    not_fit = 0
    for i in range(len(hist)) :
        #if hist[i].split('show') != 2 :
        #    pprint(hist[i])
        if 'show' not in hist[i] :
            not_fit += 1
    print('not fit :', not_fit / len(hist))
    '''
    
    #print(len(hist))
    hist = [h for h in hist if all([cond(h) for cond in pre_cleaning_conditions[MODE]])]
    #print(len(hist))
    
    #extracting
    '''
    ind = 19
    pprint(hist[ind])
    result = extract(hist[ind], mode = MODE)
    pprint([[item[3] for item in raw] for raw in result])
    print(result[-1])
    '''
    z = 0
    for x in range(len(hist)) :
        if diagnoz : print(x)
        try :
            temp = extract(hist[x], mode = MODE)
            if temp :
                hist_arr.append(temp)
                z += 1
        except BaseException  : 
            print('error')
    #'''
    #check for dota
    if hist_arr == [] : print('no data error', path, d1r, loc, filename, n)
    
    #out
    print(n, z)
    
    hist_arr = json.dumps(hist_arr)
    f = open("C:/Users/Danilo/Desktop/poker/get_hand_history/hand_hist_70gb_in_zips_unpacked/"+ str(n) +".json", "w")
    f.write(hist_arr)
    f.close()

NB_MAX_PLAYERS = 9
docs = []
path = "C:/Users/Danilo/Desktop/poker/get_hand_history/hand_hist_70gb_in_zips/"
filenames = [a for a in os.listdir(path) if 'zip' not in a]
a, n = [], 1
for d1r in filenames :
    loc = os.listdir(path + d1r)
    if loc != [] :
        docs = os.listdir(path + d1r + '/' + loc[0])
        for filename in docs :
            a.append((path, d1r, loc, filename, n))
            n += 1
print(len(a))

pre_cleaning_conditions = {
        'abs' : [
            lambda h : len(h.split('collects')) == 2,
            lambda h : 'no small blind' not in h,
            lambda h : 'no big blind' not in h,
            lambda h : 'sitout' not in h,
            lambda h : len(h.split('posts')) == 3, 
            lambda h : 'shows' in h,
            lambda h : 'board' in h,
            lambda h : len(h.split('won')) == 2,
            lambda h : 'ante' not in h
        ],
        'ftp' : [
            lambda h : 'board' in h,
            lambda h : 'showed' in h,
            lambda h : 'no small blind' not in h,
            lambda h : 'no big blind' not in h,
            lambda h : 'sitout' not in h,
            lambda h : 'ante' not in h,
            lambda h : len(h.split('posts')) == 3,
            lambda h : len(h.split('won')) == 2
        ],
        'ps' : [
            lambda h : 'board' in h,
            lambda h : len(h.split('collected')) == 2,
            lambda h : 'no small blind' not in h,
            lambda h : 'no big blind' not in h,
            lambda h : 'sitout' not in h,
            lambda h : len(h.split('posts')) == 3, 
            lambda h : 'shows' in h,
            lambda h : len(h.split('won')) == 2,
            lambda h : 'ante' not in h
        ]
    } 
ranges = {'ABS' : (1, 1277), 'FTP' : (1277, 2589), 'IPN' : (2589, 8712), 'ONG' : (8712, 10363), 'PS' : (10363, 13069), 'PTY' : (13069, len(a))} 
if 1 == 1 :
    for j in range(ranges['PS'][0], ranges['PS'][1]) : 
        path, d1r, loc, filename, n = a[j]
        save_extracted(path, d1r, loc, filename, n)

indexx = 20
print(a[indexx])
path, d1r, loc, filename, n = a[indexx]
save_extracted(path, d1r, loc, filename, n, True)
