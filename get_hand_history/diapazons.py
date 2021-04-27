import time
import numpy as np
import os
import csv
import json
import treys
import json
from pprint import pprint
import itertools, collections, functools
import mysql_tools, c_functions
from my_poker_tools import *
#import plotly.express as px
from matplotlib import pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import c_functions

con, cur, cur_unbuff, run, run_unbuff = mysql_tools.connect()
RAKE = 0.036#mean rake not pct
np.set_printoptions(precision = 1)

# взяти кожен рух в всых матчах і записати в вектор в нову базу буд більше ляма
# вектор такий : перші 3 це кількість колів чеків і рейзів нормалізована а процентному відношенні
# дальшк йдуть 4 вектори по 3 цифри : перша це кількість бабла яке було рейзнуте на префлопі флопі і тл відповідно дальше кільки заколено і дальше співвідношення цих величин
# дальше вектор в 3 цифри де є сума всіх рейзів і колів і їх співвідношення
# дальше придумати але вроді достатньо : відображає кількість, перевагу якихось дій над якимось і чисельно перевагу якихось дій над якимось преоблоданіє тобто
# цього стає мб
# перевірити теорію про то шо ті вектори які найкраще позожі одне на оджногь будуть співпадати по кратах, тобто групи векторів, бо один вектор дуже малоймовірно буде ту саму комбінацію мати 

tasks = [
    #'create and save to db vectors of all states except preflop moves',
    #'create and sae vectors of all states made on preflop',
    'calculate winners chanses n preflop'
]
if 'calculate winners chanses n preflop' in tasks :
    cur_unbuff.execute("SELECT id, bb_size, p_names, p_amounts, f_names, f_amounts, t_names, t_amounts, r_names, r_amounts, f_comb, t_comb, r_comb, board_card_1, board_card_2, board_card_3, board_card_4, board_card_5, hand_card_1, hand_card_2 FROM hands where id < 1000")
    print('got table')
    while 1 :
        try : 
            id_hand, bb_size, p_names, p_amounts, f_names, f_amounts, t_names, t_amounts, r_names, r_amounts, f_comb, t_comb, r_comb, *cards = cur_unbuff.fetchone()
        except BaseException : 
            print('fetch finished')
            break
        print(c_functions.get_chanse_aprior(cards, 6))
        if id_hand % 10000 == 0 : print(id_hand / 700000 * 100, '% fetched')



if 'create and save to db vectors of all states except preflop moves' in tasks :
    for start in range(1) :
        vectors = []
        #cur_unbuff.execute("SELECT id, bb_size, p_names, p_amounts, f_names, f_amounts, t_names, t_amounts, r_names, r_amounts, board_card_1, board_card_2, board_card_3, board_card_4, board_card_5, hand_card_1, hand_card_2 FROM hands where id > %s and id < %s" % (start * 100000, start * 100000 + 100000))
        cur_unbuff.execute("SELECT id, bb_size, p_names, p_amounts, f_names, f_amounts, t_names, t_amounts, r_names, r_amounts, f_comb, t_comb, r_comb, board_card_1, board_card_2, board_card_3, board_card_4, board_card_5, hand_card_1, hand_card_2 FROM hands where id < 1000")
        print('got table')
        while 1 :
            try : 
                id_hand, bb_size, p_names, p_amounts, f_names, f_amounts, t_names, t_amounts, r_names, r_amounts, f_comb, t_comb, r_comb, *cards = cur_unbuff.fetchone()
            except BaseException : 
                print('fetch finished')
                break

            current_combs = [None, f_comb, t_comb, r_comb]
            for vector, id_move, cycle_index in calculate_player_state_vector(bb_size, p_names, p_amounts, f_names, f_amounts, t_names, t_amounts, r_names, r_amounts) :
                if cycle_index > 0 :
                    values = [
                        *[str(item) for item in vector.tolist()],
                        "'" + str(current_combs[cycle_index]) + "'",
                        str(id_hand),
                        str(id_move), 
                        "'" + ';'.join([numeric_to_text(c) for c in get_hands_for_comb_and_board([text_to_numeric(c) for c in cards[ : 2 + cycle_index]], current_combs[cycle_index][0], current_combs[cycle_index][1])]) + "'"
                    ] 
                    vectors.append(values)
            if id_hand % 10000 == 0 : print(id_hand / 700000 * 100, '% fetched')

        for values in vectors :
            command = 'INSERT vectors_and_combs values(%s)' % (', '.join(values))
            if int(values[-2]) % 10000 == 0 : print(values[-2], 'inserted')
            run(command)  
        con.commit()
        print('changes commited')

if 'get 3 combs names and combs powers from every hand and write in field' in tasks :
    cur_unbuff.execute("SELECT id, bb_size, p_names, p_amounts, f_names, f_amounts, t_names, t_amounts, r_names, r_amounts, board_card_1, board_card_2, board_card_3, board_card_4, board_card_5, hand_card_1, hand_card_2 FROM hands where id > 0")
    print('got table')
    to_insert = []
    while 1 :
        try : 
            id_hand, bb_size, p_names, p_amounts, f_names, f_amounts, t_names, t_amounts, r_names, r_amounts, *cards = cur_unbuff.fetchone()
        except BaseException : 
            print('fetch finished')
            break
        current_combs = [['']] + get_all_combs_from_flop_to_river(cards[ : 5], cards[5 : ])
        to_insert.append((*[';'.join([str(item) for item in comb]) for comb in current_combs], id_hand))
        if id_hand % 10000 == 0 : print(id_hand / 700000 * 100, '% fetched')
        

    for values in to_insert :
        command = "update hands set p_comb = '%s', f_comb = '%s', t_comb = '%s', r_comb = '%s' where id = %s" % (values)
        run(command)
        if int(values[-1]) % 10000 == 0 : print(int(values[-1]) / 700000 * 100, '% fetched')

    con.commit()
    print('changes commited')

if ''























'''
default_histogram_values = [[0] * k for k in [13, 13, 78, 13, 10, 45, 156, 13]]
def find_normal_possib_for_hands(board_len, nb_iterations) :
    histogram_aprior = {}
    for j, c_name in enumerate(comb_names_all) : histogram_aprior[c_name] = default_histogram_values[j]
    
    for i in range(nb_iterations) :
        cards = []
        while len(cards) < 2 + board_len :
            card = np.random.randint(1, 5) * 100 + np.random.randint(2, 15)
            if card not in cards : cards.append(card)  
        comb_name, comb_rank = get_power_of_comb(cards[0 : 2], cards[2 : ])
        if comb_name != None and comb_rank != None :
            histogram_aprior[comb_name][comb_rank + comb_bias[comb_name]] += 1
    return histogram_aprior
histogram_global_flop = {}
cycles_names = ['p', 'f', 't', 'r']
cur_unbuff.execute("SELECT id, bb_size, p_names, p_amounts, f_names, f_amounts, t_names, t_amounts, r_names, r_amounts, hand_card_1, hand_card_2, board_card_1, board_card_2, board_card_3, board_card_4, board_card_5 FROM hands where id < 6000")
print('got table')
while 1 :
    try : 
        id_hand, bb_size, p_names, p_amounts, f_names, f_amounts, t_names, t_amounts, r_names, r_amounts, *cards = cur_unbuff.fetchone()
    except BaseException : 
        print('fetch finished')
        cur_unbuff.close()
        break

    cards = [(kinds_all.index(c[1]) + 1) * 100 + powers_all.index(c[0]) for c in cards] 

    board = cards[2 :]
    hand = cards[0 : 2]

    raw_sequences = {
        'p' : zip(p_names, p_amounts.split(';')),
        'f' : zip(f_names, f_amounts.split(';')),
        't' : zip(t_names, t_amounts.split(';')),
        'r' : zip(r_names, r_amounts.split(';'))
    }
    #create sequences for all trading cycles
    sequences = {'p' : [], 'f' : [], 't' : [], 'r' : []} 
    betted_global = 0
    for cycle_name in cycles_names : 
        betted = 0
        for name, amount in raw_sequences[cycle_name]: 
            amount = float(amount)
            if name == 'c' : 
                betted += amount
            elif name == 'r' : 
                betted = amount
            sequences[cycle_name].append(betted_global + betted)
        betted_global += betted

        if cycle_name == 'f' : 
            flop_board = board[ : 3]
            flop_comb_name, flop_comb_rank = get_power_of_comb(flop_board, hand)

            for betted in sequences[cycle_name] :
                histogram_betted_index_str = str(round(betted / bb_size, 0))
                if histogram_betted_index_str not in list(histogram_global_flop.keys()) :
                    histogram_global_flop[histogram_betted_index_str] = {}
                    for j, c_name in enumerate(comb_names_all) : histogram_global_flop[histogram_betted_index_str][c_name] = default_histogram_values[j].copy()
                histogram_global_flop[histogram_betted_index_str][flop_comb_name][flop_comb_rank + comb_bias[flop_comb_name]] += 1 
        #print(histogram_global_flop[])

fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')

#print(json.dumps(histogram_global_flop, indent=4))
print(list(histogram_global_flop.keys()))

X, Y, Z = [], [], []
for j, key in enumerate(list(histogram_global_flop.keys())) :
    z = np.array([b for a in histogram_global_flop[key].values() for b in a]).astype(float)
    z = z / np.max(z)
    x = np.arange(len(z))
    y = np.ones(len(z)) * float(key)

    X.extend(x)
    Y.extend(y)
    Z.extend(z)
    #ax.plot(x, y, z)
Z_ = [0] * len(X)
Z_.extend(Z)
X, Y, Z = np.array(X), np.array(Y), np.array(Z_).reshape(-1, len(X))
ax.plot_surface(X, Y, Z, cmap = cm.coolwarm)

key = list(histogram_global_flop.keys())[0]
z = np.array([b for a in histogram_global_flop[key].values() for b in a]).astype(float)
print(np.sum(z))
z = z / np.max(z)
x = np.arange(len(z))
y = np.ones(len(z)) * float(key)

ax.plot(x, y, z)
z = np.polyfit(x, z, 360)
z = np.poly1d(z)(x)
ax.plot(x, y, z)


plt.show()


#print(X.shape,Y.shape,Z.shape )
#ax.plot_surface(X, Y, Z, cmap = cm.coolwarm)
#ax.plot_surface(np.array([1, 2, 3]), np.array([1, 2, 3]), np.array([[1, 2, 3], [700, 6, 5]]), cmap=cm.coolwarm)
#fig.canvas.draw()
#fig = plt.figure()
#ax = fig.add_subplot(111, projection = '3d')
#ax.plot_surface(np.array([1, 2, 3]), np.array([1, 2, 3]), np.array([[1, 2, 3], [700, 6, 5]]), cmap=cm.coolwarm)
#ax.plot_wireframe(np.array([1, 2, 3, 1, 2, 3, 5]), np.array([1, 2, 3, 4, 5, 6, 2]), np.array([[1, 2, 5, -1, 2, 50, 1]]))
#plt.show()
'''



