import itertools
import os
import time 
import pymysql
import pymysql.cursors
from pprint import pprint
import sys
import numpy as np
from mysql_tools import connect
from PIL import Image
from matplotlib import pyplot as plt

con, cur, cur_unbuff, run, run_unbuff = connect()
#def correlation(col1, col2) :
cur_unbuff.execute("SELECT ,  FROM hands where id > 0")
print('got table')
while 1 :
    try : 
        hand = cur_unbuff.fetchone()

    except BaseException :
        print('fetch finished')
        break


