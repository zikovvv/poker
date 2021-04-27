import time
import numpy as np
import csv
import json
import treys
import collections
import poker 
def get_chanse(nb_players, hand, board, nb_simulations, show_time = False) :
    if hand != None :
        time1, win, lose, draw, add_board_len, nb_op = time.time(), 0, 0, 0, 5 - len(board), nb_players - 1
        global deck_np_array_int
        temp_deck_np_array_int = deck_np_array_int.copy().tolist()
        limit, i = 52, 0
        while i < limit :
            if temp_deck_np_array_int[i] in board + hand :
                temp_deck_np_array_int.pop(i)
                limit -= 1
            else : i += 1
        for sindex in range(nb_simulations) :
            deck = treys.Deck()
            tempboard = board.copy()
            np.random.shuffle(temp_deck_np_array_int)
            shit = temp_deck_np_array_int[0 : nb_op * 2 + add_board_len]
            tempboard.extend(shit[2 * nb_op : 2 * nb_op + add_board_len])
            opponents = []
            #print(tempboard, shit, hand, board)
            for i in range(nb_op) :
                opponent = shit[2 * i : 2 * i + 2]
                evop = 7462 - evaluator.evaluate(tempboard, opponent)
                opponents.append(evop)
            evhand = 7462 - evaluator.evaluate(tempboard, hand)
            evop_max = np.max(opponents)
            
            if evhand > evop_max : win += 1
            if evhand < evop_max : lose += 1
            if evhand == evop_max : draw += 1
        if show_time : print(time.time() - time1)
        return np.array([win, lose, draw, win + lose + draw])
    return np.zeros(4)

RAKE = 0.036#mean rake not pct
ev = treys.Evaluator()
deck = treys.Deck
evaluator = treys.Evaluator()
deck = treys.Deck()
deck_np_array_int = np.array(deck.__dict__['cards']).astype(int)



if 1 == 1 :


















'''
powers_dict, kinds_dict, combs_dict = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13,'A':14}, {'h':100, 's':200, 'c':300, 'd':400}, ['high_card', 'pair', 'two_pairs', 'set', 'straight', 'flush', 'full_house', 'kare']
def get_name_combo(hand, board):
    cards = hand + board
    cards = [powers_dict[c[0]] + kinds_dict[c[1]] for c in cards]
    kinds, powers  = [c // 100 for c in cards], [c % 100 for c in cards]
    nb_kinds, nb_powers, combs = collections.Counter(kinds), collections.Counter(powers), ['high_card']
    nb_powers_max, nb_kinds_max = max(nb_powers.values()), max(nb_kinds.values())
    if nb_powers_max == 4 : combs.append('kare')
    if nb_powers_max == 3 :
        if np.count_nonzero(np.array(nb_powers) == 2) != 0 : combs.append('full_house')
        else :
            combs.append('set')
    if nb_powers_max == 2 :
        if np.count_nonzero(np.array(list(nb_powers.values())) == 2) >= 2 : combs.append('two_pairs')
        else : combs.append('pair')
    if nb_kinds[-1] >= 5 : combs.append('flush')
    if True in [all([b in powers for b in range(i, i + 5)]) for i in range(2, 10)] : combs.append('straight')
    return max([combs_dict.index(c) for c in combs])
'''