import ctypes
import time
from ctypes import *
import numpy as np
from my_poker_tools import *

#path = "C:\\Users\\Danilo\\Desktop\\poker\\get_hand_history\\"
c_functions = CDLL(".\\c_functions.dll")

c_functions.init_random()

get_power_of_comb_c = c_functions.get_power_of_comb
get_power_of_comb_c.argtypes = [POINTER(c_int), c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), ]
get_power_of_comb_c.restype = c_int
comb_power = c_int()
comb_attr0 = c_int()
comb_attr1 = c_int()

get_set_of_cards_numeric = c_functions.get_set_of_cards_numeric
get_set_of_cards_numeric.argtypes = [POINTER(c_int), c_int, ]
#get_set_of_cards_numeric.restype = POINTER(c_int)

get_chanse_c = c_functions.get_chanse
get_chanse_c.argtypes = [POINTER(c_int), c_int, c_int, POINTER(c_float), POINTER(c_float), ]
#get_chanse_c.restype = c_int
mem = c_int * 7
#cards in foramt first 5 is board and 2 last are hand vector of dim 7 if number of cards is smaller then all of them to zero
def get_chanse_aprior(cards, nb_players, cards_are_numeric = False, nb_interations = 50000) :
    win = c_float(0.0)
    lose = c_float(0.0)
    tie = c_float(0.0)
    if not cards_are_numeric :
        cards = text_to_numeric_vectorized(cards)
    print(cards)
    cards_7_vector = [0] * 7
    cards_7_vector[ : len(cards) - 2] = cards[ : -2]
    cards_7_vector[-2 : ] = cards[-2 : ]
    cards_c = mem(*cards_7_vector)
    get_chanse_c(cards_c, nb_players, nb_interations, byref(win), byref(lose), byref(tie))
    return [win.value, lose.value, tie.value]

