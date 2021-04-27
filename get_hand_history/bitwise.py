import time
import numpy as np
import os
import csv
import json
import treys
import json
from pprint import pprint
import itertools, collections, functools
from my_poker_tools import *
from numba import jit
def index_log(mass, elem, l) :
    floating, step = l / 2, l / 4
    while step > 0.5 :
        floating += step * (-1 if elem < mass[int(floating)] else 1)
        step /= 2
    return int(floating)
def straights_algo(bbb) :
    powers = bbb[0] | bbb[1] | bbb[2] | bbb[3]  
    straight_power = 0
    counter = 0
    for i in range(2, powers.bit_length() - 1) :
        counter += 1 if (powers >> i) & 1 else -counter
        if counter >= 4 :
            straight_power = i
    if straight_power == 0 :
        return 1
    else :
        return straight_power - 4
def numeric_to_bin_multi(cards) :
    res = [0, 0, 0, 0]
    for c in cards :
        res[c // 100 - 1] += 1 << (c % 100)
    return res

def numeric_to_bin_multi(cards) :
    res = [0, 0, 0, 0]
    for c in cards :
        res[c // 100 - 1] |= 1 << (c % 100)
    return res

a = "ks4has9ctdqc7h"
cards = [a[i * 2 : i * 2 + 2] for i in range(int(len(a) / 2))]
#print(cards)
cards = text_to_numeric_vectorized(cards)
#print(cards)
#print(numeric_to_bin_multi(cards))
straights_all_bin = list(reversed([16444, 124, 248, 496, 992, 1984, 3968, 7936, 15872, 31744]))

def get_power_of_comb_pure_bin(bbb) :
    #highest card
    powers = bbb[0] | bbb[1] | bbb[2] | bbb[3]
    current_power_offset = 14
    while current_power_offset > 1 :
        if (powers >> current_power_offset) & 1 :
            max_power = current_power_offset
            break
        current_power_offset -= 1

    #pair kare set and full house
    three_power = 0
    pair_power_1 = 0
    pair_power_2 = 0
    current_power_offset = max_power
    while current_power_offset > 1 : 
        #print('kal1')
        counter = 0
        for kind_num in bbb : 
            if (kind_num >> current_power_offset) & 1 : 
                counter += 1
        if counter == 2 :
            if not pair_power_1 :
                pair_power_1 = current_power_offset
            elif not pair_power_2 :
                pair_power_2 = current_power_offset
            
            if three_power :
                #fulll house with current pair and max set
                return 6, [three_power, pair_power_1]
        elif counter == 3 :
            if not three_power :
                three_power = current_power_offset
                if pair_power_1 :
                    #full fouse max set max pair
                    return 6, [three_power, pair_power_1]
            else :
                #full house with two sets
                return 6, [three_power, current_power_offset]
        elif counter == 4 :
            #kare
            return 7, current_power_offset
        current_power_offset -= 1

    #flush
    for kind_num in bbb :
        counter = 0
        current_power_offset = max_power
        while current_power_offset > 1 :
            #print('kal2')

            if (kind_num >> current_power_offset) & 1 :
                counter += 1
                if counter == 5 :
                    min_flush_power = current_power_offset
                    current_power_offset = max_power
                    while 1 :
                        #print('kal3')
                        if (kind_num >> current_power_offset) & 1 :
                            #flush, we found the min valuee of it and now знову починаєм з кінця і шукаєм максимальне, цикл точно мусить закінчитися тому вайл 1 і ш це потрібно для того шоб не провіряти на кожній ітерації чи макс нульова чи ні
                            return 5, [current_power_offset, min_flush_power]
                        current_power_offset -= 1
            current_power_offset -= 1

    #straight
    j = 10
    for straight in straights_all_bin :
        if powers & straight == straight :
            return 4, j 
        j -= 1
    
    #set
    if three_power :
        return 3, three_power

    #two pair
    if pair_power_1 and pair_power_2 : 
        return 2, [pair_power_1, pair_power_2]

    #pair
    if pair_power_1 :
        return 1, pair_power_1

    #high card
    return 0, max_power
        

for i in range(0) :
    cards = get_unique_set_of_cards(7)
    print(cards, ''.join(cards))
    board, hand = text_to_numeric_vectorized(cards[ : -2]), text_to_numeric_vectorized(cards[-2 : ])
    cards = text_to_numeric_vectorized(cards)
    comb_name, comb_power = get_power_of_comb(board, hand)
    print(comb_name, comb_power)


N = 0
ttt1 = 0
ttt2 = 0
ttt3 = 0
ttt4 = 0
ttt5 = 0
for iteration in range(N) :
    t = time.time()
    cards = get_unique_set_of_cards(7)
    board, hand = text_to_numeric_vectorized(cards[ : -2]), text_to_numeric_vectorized(cards[-2 : ])
    cards = text_to_numeric_vectorized(cards)
    ttt5 += time.time() - t


    t = time.time()
    bbb = numeric_to_bin_multi(cards) 
    comb_name, comb_power = get_power_of_comb_pure_bin(bbb)
    ttt1 += time.time() - t
    
    t = time.time()
    comb_name, comb_power = get_power_of_comb(board, hand)
    ttt2 += time.time() - t

#print(ttt1, ttt2, ttt3, ttt4, ttt5)
    
    