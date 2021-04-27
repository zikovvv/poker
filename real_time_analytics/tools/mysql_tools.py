import itertools
import os
import time 
import pymysql
import pymysql.cursors
from pprint import pprint
import sys

def connect() :
    DB_NAME = 'poker'
    PASSWORD = 'opangangnamstyle'
    try :
        con = pymysql.connect('localhost', 'root', PASSWORD, DB_NAME)
        print('Connected to %s database' % DB_NAME)

        cur = con.cursor(cursor = None)
        run = cur.execute

        cur_unbuff = con.cursor(cursor = pymysql.cursors.SSCursor)
        run_unbuff = cur_unbuff.execute
        return con, cur, cur_unbuff, run, run_unbuff
    except BaseException :
        print('COnnection failed')
        return None, None, None, None, None
