import itertools
import os
import time 
import pymysql
import pymysql.cursors
from pprint import pprint
import sys
#connect
DB_NAME = 'poker'
PASSWORD = 'opangangnamstyle'
try :
    con = pymysql.connect('localhost', 'root', PASSWORD, DB_NAME)
    print('Connected to %s database' % DB_NAME)

    cur = con.cursor(cursor = None)
    run = cur.execute

    cur_unbuff = con.cursor(cursor = pymysql.cursors.SSCursor)
    run_unbuff = cur_unbuff.execute

except BaseException :
    print('COnnection failed')

ARGS = {
    'get_winner_name' : {
        'abs' : ['summary', ['total', 'seat', 'with']],
        'ftp' : ['summary', ['showed', 'won']],
        'ps' : ['summary', ['showed', 'won']]
    },
    'get_board' : {
        'abs' : [],
        'ftp' : [],
        'ps' : []
    },
    'get_bb_size' : {
        'abs' : ['posts big blind $', '\n'],
        'ftp' : ['posts the big blind of $', '\n'],
        'ps' : ['posts big blind $', '\n']
    },
    'get_winner_moves' :{
        'abs' : [],
        'ftp' : [],
        'ps' : []
    },
    'get_winner_hand' :{
        'abs' : lambda h, winner_name : h.split(winner_name)[-1].split('\n')[0].split('[')[-1].split(' ')[0 : 2],
        'ftp' : lambda h, winner_name : h.split(winner_name)[-1].split('\n')[0].split('showed [')[1].split(']')[0].split(' '),
        'ps' : lambda h, winner_name : h.split(winner_name)[-1].split('\n')[0].split('showed [')[1].split(']')[0].split(' ')
    }
}

def get_winner_name(hand, room) :
    args = ARGS['get_winner_name'][room]
    hand = hand.split(args[0])[1].split('\n')
    for h in hand : 
        if all(s in h for s in args[1]) :
            return h.split(' ')[2] 

def get_board(hand, room) :
    args = ARGS['get_board'][room]
    try :
        return [h.replace('10', 't') for h in hand.split('summary')[1].split('board [')[1].split(']')[0].split(' ')]
    except BaseException :
        return None
 
def get_bb_size(hand, room) :
    args = ARGS['get_bb_size'][room]
    try :
        return hand.split(args[0])[1].split(args[1])[0].split(' ')[0]
    except BaseException :
        return None

def prepare_hand(hand) :
    if 'show down' in hand :
        hand = hand.split('*** show down ***')[0] + '*** summary ***'
    else : 
        hand = hand.split('*** summary ***\n')[0] + '*** summary ***'
    hhh = hand.split('\n')
    for j in range(len(hhh)) : 
        if 'seat' not in hhh[j + 1] : 
            hand = '*** pocket cards ***' + hand.split(hhh[j])[1]
            break
    return hand

def get_winner_rows(hand, winner_name, cycle_name) :
    hhh = hand.split(cycle_name + ' ***\n')[1].split('***')[0]
    hhh = [h.split('\n')[0] for h in hhh.split(winner_name)[1 :]]
    hhh = [h.strip() for h in hhh if not any([s in h for s in ['"', 'collect', 'join', 'leav', 'out', 'connec', 'ties', 'has', 'stand', 'win', 'won', 'sit', 'sitting', 'out', 'return', 'said', 'feels', 'muck', 'show']]) and h.replace(' ', '') != '' and len(h.split(' ')) >= 2 and len(h) >= 4]
    return hhh

moves_names = ['checks', 'folds', 'raises', 'calls', 'ante', 'small blind', 'big blind', 'bets', 'allin', 'allin(raise)', 'posts $', 'posts dead $', 'adds']
moves_classes_translation = {'checks' : 'k', 'folds' : 'f', 'raises' : 'r', 'bets' : 'r', 'calls' : 'c', 'ante' : 'c', 'small blind' : 'c', 'big blind' : 'c', 'allin' : 'c', 'allin(raise)' : 'r', 'posts $' : 'c', 'posts dead $' : 'c', 'adds' : 'r'}
def extract_move(h, room) :
    move_name = None
    try :
        move_name = moves_names[[s in h for s in moves_names].index(True)]
    except BaseException :  
        pass
    if move_name != None :
        if move_name in ['checks', 'folds'] : 
            move_amount = '0'
        else :
            move_amount = h.split('$')[1].split(' ')[0] 
        return moves_classes_translation[move_name] + move_amount
    return None

cycles_names = ['pocket cards', 'flop', 'turn','river']
def get_winner_moves(hand, room, winner_name) :
    args = ARGS['get_winner_moves'][room]    
    hand = prepare_hand(hand)
    moves, parts, winner_parts = {}, {}, {}
    for cycle_name in cycles_names :
        moves[cycle_name], hhh = [], get_winner_rows(hand, winner_name, cycle_name)
        for h in hhh :
            move = extract_move(h, room)
            if move != None :
                moves[cycle_name].append(move)
    return moves

def get_winner_hand(hand, room, winner_name, args = ARGS['get_winner_hand']) :
    args = ARGS['get_winner_hand'][room]
    try : 
        return [c.replace('10', 't') for c in args(hand, winner_name)]
    except BaseException :
        return None
    
cur_unbuff.execute("SELECT id, hand, room, winner_name FROM hands where id > 0")
print('got table')
death_note = []
ids = []
while 1 :
    try : 
        id_hand, hand, room, winner_name, *_ = cur_unbuff.fetchone()
    except BaseException :
        cur_unbuff.close()
        print('fetch finished')
        break
    hand = hand.decode('utf-8')
    try : 
        moves = get_winner_moves(hand, room, winner_name)
        board = get_board(hand, room)
        bb_size = get_bb_size(hand, room)
        winner_hand = get_winner_hand(hand, room, winner_name)

        b1, b2, b3, b4, b5 = board
        h1, h2 = winner_hand
        pn, fn, tn, rn = [''.join([n[0] for n in nnn]) for nnn in list(moves.values())]
        tempfunc = lambda x : '0' if x == '' else x
        pa, fa, ta, ra = [tempfunc(';'.join([n[1 : ] for n in nnn])) for nnn in list(moves.values())]
        ids.append([id_hand, bb_size, pn, fn, tn, rn, b1, b2, b3, b4, b5, h1, h2, pa, fa, ta, ra])
        #print(pa, fa, ta, ra)
        [float(a) for a in pa.split(';')]
        [float(a) for a in fa.split(';')]
        [float(a) for a in ta.split(';')]
        [float(a) for a in ra.split(';')]
    except BaseException : 
        
        death_note.append(id_hand)
        print('invalid id %s' % id_hand)

    if id_hand % 1000 == 0 :
        print('\x1b[1A' + 'profgres :' + str(id_hand / 690000))

print(len(death_note))
print(len(ids))


for temp in ids :
    id_hand, bb_size, pn, fn, tn, rn, b1, b2, b3, b4, b5, h1, h2, pa, fa, ta, ra = temp
    #try :
    command__ = ''.join([
        "update hands set ",
        "bb_size = %s, " % bb_size,
        "p_names = '%s', " % pn,
        "f_names = '%s', " % fn,
        "t_names = '%s', " % tn,
        "r_names = '%s', " % rn,
        "p_amounts = '%s', " % pa,
        "f_amounts = '%s', " % fa,
        "t_amounts = '%s', " % ta,
        "r_amounts = '%s', " % ra,
        "board_card_1 = '%s', " % b1,
        "board_card_2 = '%s', " % b2,
        "board_card_3 = '%s', " % b3,
        "board_card_4 = '%s', " % b4,
        "board_card_5 = '%s', " % b5,
        "hand_card_1 = '%s', " % h1,
        "hand_card_2 = '%s' " % h2,
        "where id = %s;" % id_hand
    ])
    command = ''.join([
        "",
    ])
    run(command)
        #run("UPDATE hands SET bb_size = '%s', p_names = '%s', f_names = ,t_names = , r_names = ,board_card_1  WHERE id = %s" % (, id_hand))
    #except BaseException :
    #    print(id_hand, winner_name)

'''
for id_hand in death_note : 
    try :
        run('delete from hands where id = %s' % id_hand)
    except BaseException :
        print('id %s is not deleted' % id_hand)
'''
con.commit()
print('changes commited')

























