'''
import itertools
import os
import time 
import pymysql
import pymysql.cursors
from pprint import pprint
'''
from matplotlib import pyplot as plt
import numpy as np
hist = np.zeros(5)

N = 10000
NB_PLAYERS = 2
MAX_PLAYERS = 6
RANGE = 1000
graph1 =  np.zeros(RANGE)
graph2 = np.zeros(RANGE)


number = 800.5
win1, win2 = 0, 0
for i in range(N) :
    a = np.sort(np.random.rand(MAX_PLAYERS) * RANGE).astype(int)[ MAX_PLAYERS - NB_PLAYERS : ]
    win1 += 1 if (a < number).all() else 0

for i in range(N) :
    a = (np.random.rand(MAX_PLAYERS) * RANGE).astype(int)
    win2 += 1 if (a < number).all() else 0

print(win1, win2)    