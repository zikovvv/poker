import pyautogui as pag
import time
import numpy as np
from pywinauto import Desktop
import win32gui
import win32con
import win32clipboard
import csv
import json
import treys
with open('get_hand_history/hist.txt', 'r') as f:
    hist = f.read()
    f.close()
hist = hist.split('PokerStars')
hist.pop(0)
print(len(hist))
hist_dict = {}
rake_pct_global = 0
def transform_to_dict(hhh, k):
    
    #split by raws
    hhh = hhh.split("\n")
    
    #clean
    j = 0
    while j < len(hhh) :
        if hhh[j] == '' or hhh[j] == ' ' : hhh.pop(j) 
        else : j += 1
    
    #seats analysis and changing names
    i, nb_players, seats, names, seats_inversed, pot_usd, seats_shifted, seats_shifted_inversed, new_names = 0, 0, {}, [], {}, 0, {}, {}, {}
    info = []
    while True :
        if 'Seat' in hhh[i] and 'Seat #' not in hhh[i] :
            nb_players += 1
            info.append([hhh[i].split(': ')[1].split(' ($')[0], hhh[i].split('Seat ')[1].split(': ')[0]])
        if 'posts small blind' in hhh[i] : 
            sb_name = hhh[i].split(': posts')[0]
            sb_seat = seats[sb_name]
            i, n, iii, nnn = sb_seat, 1, [b[1] for b in info], [b[0] for b in info] 
            while n <= nb_players :
                if i in iii :
                    info[iii.index(i)].append(n)
                    n += 1
                i += 1
                if i > 6 : i = 1
            
                hhh = [h.replace(info[nnn.index(h.split(': ')[0])][0], str(info[nnn.index(h.split(': ')[0])][0])) for h in hhh ]
            

                

            
            break
        i += 1
    hole_cards_index = i + 1

    #get_seats_shifted

    for i in range(len()) :


    #print
    if k == 1951 :
        print(names, seats)

    if nb_players >= 2 :  
        #define
        pot, callsize, stacks, bets = 0, 0, {'1' : 0, '2' : 0, '3' : 0, '4' : 0, '5' : 0, '6' : 0}, {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0}
        hand = {'preflop' : [], 'flop' : [], 'turn' : [], 'river' : [], 'board' : []}
        hand['nb_players'] = nb_players
        hand['id'] = int(hhh[0].split('Hand #')[1].split(': ')[0])
        hand['big_blind_size'] = float(hhh[0].split(' ($')[1].split('/')[0])
        hand['names'] = names
        hand['seats'] = seats
        hand['seats_inversed'] = seats_inversed
        
        

        #get small blind big blind pos and name annd amount and stacks
        i = 0
        while 'HOLE CARDS' not in hhh[i] :
            nnn = hhh[i].split(": ")[0]
            if nnn in names :
                move = {}
                move['player_name'] = nnn
                move['player_seat'] = seats[nnn]
                move['action_full'] = hhh[i].split(': ')[1]
                move['action_class'] = move['action_full'].split(' $')[0]
                amount = float(move['action_full'].split(' $')[1].split(' ')[0]) 
                move['amount'] = amount

                stacks[str(seats[nnn])] -= amount
                bets[str(seats[nnn])] += amount
                pot += amount
                callsize = amount
                move['callsize'] = callsize
                move['pot'] = pot
                move['player_stack'] = stacks[str(seats[nnn])]
                move['betted'] = bets[str(move['player_seat'])]
                hand['preflop'].append(move)

            elif 'Seat' in hhh[i] and 'Seat #' not in hhh[i] :
                stacks[hhh[i].split('Seat ')[1].split(': ')[0]] = float(hhh[i].split(' in chips')[0].split('($')[1])
            i += 1

        #shifting seats(small blind position is 1 and ...)


        
        #get moves
        cycle = 'preflop'
        i = hole_cards_index
        while "SHOW DOWN" not in hhh[i] :
            if 'FLOP' in hhh[i] : cycle, incycle_index, callsize, bets = 'flop', 0, 0, {'1' : 0, '2' : 0, '3' : 0, '4' : 0, '5' : 0, '6' : 0}
            elif 'TURN' in hhh[i] : cycle, incycle_index, callsize, bets = 'turn', 0, 0, {'1' : 0, '2' : 0, '3' : 0, '4' : 0, '5' : 0, '6' : 0}
            elif 'RIVER' in hhh[i] : cycle, incycle_index, callsize, bets = 'river', 0, 0, {'1' : 0, '2' : 0, '3' : 0, '4' : 0, '5' : 0, '6' : 0}
            
            elif hhh[i].split(': ')[0] in names :
                #current move
                move = {}
                move['player_name'] = hhh[i].split(':')[0]
                move['player_seat'] = seats[move['player_name']]
                move['action_full'] = hhh[i].split(': ')[1]
                move['action_class'] = move['action_full'].split(' ')[0]
                if move['action_class'] == 'raises' :
                    amount = float(hhh[i].split('to $')[1].split(' ')[0]) - bets[str(move['player_seat'])]
                    callsize = float(hhh[i].split('to $')[1].split(' ')[0])
                elif move['action_class'] == 'bets' :
                    amount = float(hhh[i].split('bets $')[1].split(' ')[0])
                    callsize = amount
                elif move['action_class'] == 'calls' :
                    amount = float(hhh[i].split('calls $')[1].split(' ')[0])
                else : amount = 0

                bets[str(move['player_seat'])] += amount
                pot += amount
                stacks[str(move['player_seat'])] -= amount
                move['amount'] = amount
                move['player_stack'] = stacks[str(move['player_seat'])]
                move['pot'] = pot
                move['callsize'] = callsize
                move['betted'] = bets[str(move['player_seat'])]
                hand[cycle].append(move)
            i += 1

        #get_winner_name and seat and hand
        for i in range(len(hhh)) :
            if 'won' in hhh[i] :
                hand['winner'] = {}
                hand['winner']['seat'] = hhh[i].split(': ')[0].split(' ')[1]
                hand['winner']['name'] = seats_inversed[hand['winner']['seat']]
                hand['winner']['hand'] = hhh[i].split('showed [')[1].split(']')[0].split(' ')
                break
        
        #get board cards
        was_summary = False
        for i in range(len(hhh)) :
            if 'SUMMARY' in hhh[i] : was_summary = True
            elif was_summary and 'Board' in hhh[i] :
                hand['board'] = hhh[i].split('[')[1].split(']')[0].split(' ')

        hand['original_text'] = hhh
    return hand
n = 1
prev_ids = []
for k in range(len(hist)) :
    temp = hist[k].split('SUMMARY')[1] 
    if 'showed' in temp and 'Board' in temp and 'won' in temp and 'Side pot' not in temp :  
        kal = False
        was = False
        for string in temp.split('\n') :
            if 'won' in string and 'showed' in string and 'with' in string :
                if not was :
                    was = True
                elif was :
                    kal = True     
        if not kal : 
            hand = transform_to_dict(hist[k], k)
            hand['real_index'] = k
            if hand['id'] not in prev_ids :
                hist_dict[str(n)] = hand
                prev_ids.append(hand['id'])
                n += 1
   # print(k, n)


from pprint import pprint
hist_dict = json.dumps(hist_dict)
f = open("hist.json", "w")
f.write(hist_dict)
f.close()
f = open("hist.json", "r")
hist_dict = json.load(f)
f.close()

index = 200
print(json.dumps(hist_dict[str(index)], sort_keys = False, indent = 4))
print(len(hist_dict))
