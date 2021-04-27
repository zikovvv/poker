'''
import itertools
import os
import time 
import pymysql
import pymysql.cursors
from pprint import pprint
'''
import numpy as np
hist = np.zeros(5)

N = 100000
is4 = 0
for i in range(N) :
    a = sorted((np.random.rand(5) * 5).astype(int).tolist())
    if 4 in a : is4 += 1
    for index in range(1, 4) : 
        hist[a[-index]] += 1
print(is4 / N)
print(hist / N)