import numpy as np
import treys
import itertools
from poker import Range
from pprint import pprint 
import itertools, collections, functools
import time
comb_bias_for_arrays_min_zero = {
    "high card" : -2,
    "pair" : -2,
    "two pair" : 0,
    "three of a kind" : -2,
    "straight" : -1,
    "flush" : 0,
    "full house" : 0,
    "four of a kind" : -2    
}
comb_bias_min_one = {
    "high card" : -1,
    "pair" : -1,
    "two pair" : +1,
    "three of a kind" : -1,
    "straight" : 0,
    "flush" : +1,
    "full house" : +1,
    "four of a kind" : -1    
}
combs_full_ranges_sizes = {
    "high card" : 13,
    "pair" : 13,
    "two pair" : 78,
    "three of a kind" : 13,
    "straight" : 10,
    "flush" : 36,
    "full house" : 156,
    "four of a kind" : 13    
}
combs_names_all_sorted = ["high card", 'pair', "two pair", 'three of a kind', 'straight', 'flush', 'full house', 'four of a kind']
powers_all, kinds_all = [None, None, '2', '3', '4', '5', '6', '7', '8', '9', 't', 'j', 'q', 'k', 'a'], [None, 'h', 'c', 'd', 's']
c_2_13_powers_sort_by_power = sorted([[max(comb), min(comb)] for comb in list(itertools.combinations([power for power in range(2, 15)], 2))])
c_2_13_powers_sort_by_power_with_pairs = c_2_13_powers_sort_by_power + [[c, c] for c in range(2, 15)]
c_2_13_powers_sort_by_power_for_flushes = [c for c in c_2_13_powers_sort_by_power if abs(c[0] - c[1]) >= 5]
c_2_13_powers_sort_by_power_with_reverses_no_pairs = c_2_13_powers_sort_by_power + [list(reversed(c)) for c in c_2_13_powers_sort_by_power]
c_2_4_kinds_with_reverses = list(itertools.combinations_with_replacement([n for n in range(1, 5)], 2)) + list((a[1], a[0]) for a in itertools.combinations_with_replacement([n for n in range(1, 5)], 2) if a[0] != a[1])
all_possible_straights = [[14, 2, 3, 4, 5]] + [[i for i in range(start, start + 5)] for start in range(2, 11)]
nb_combs_all = 13 + 13 + 78 + 13 + 10 + 36 + 156 + 13
ev = treys.Evaluator()
new = treys.Card.new
deck = treys.Deck()
deck_np_array_int = np.array(deck.__dict__['cards']).astype(int)
cycles_names = ['p', 'f', 't', 'r']
f = lambda x : 1 if x == 0 else x
def get_unique_set_of_cards(nb_cards, cards = [], seed = 1): 
    cards = []
    while len(cards) < nb_cards :
        card = np.random.choice(powers_all[2 : ]) + np.random.choice(kinds_all[1 : ])
        if card not in cards :
            cards.append(card)  
    return cards

def text_to_numeric(card) :
    return powers_all.index(card[0]) + (kinds_all.index(card[1])) * 100
temp_1 = np.vectorize(text_to_numeric)
text_to_numeric_vectorized = lambda x : temp_1(x).tolist()

def numeric_to_text(card) :
    return powers_all[card % 100] + kinds_all[card // 100]
temp_2 = np.vectorize(numeric_to_text)
numeric_to_text_vectorized = lambda x : temp_2(x).tolist()


def get_power_of_comb(board, hand) :
    powers, kinds = [c % 100 for c in board + hand], [c // 100 for c in board + hand]
    zip_power_kind = [c for c in zip(powers, kinds)]
    e = ev.class_to_string(ev.get_rank_class(ev.evaluate([new(powers_all[power].upper() + kinds_all[kind]) for power, kind in zip_power_kind[: -2]], [new(powers_all[power].upper() + kinds_all[kind]) for power, kind in zip_power_kind[-2 :]]))).lower()
    if e == 'high card' :
        return e, max(powers)
    elif e == 'pair' or e == 'three of a kind' or e == 'four of a kind' : 
        return e, powers[np.argmax([powers.count(power) for power in powers])]
    elif e == 'two pair' :
        return e, *sorted(sorted([power for power in range(2, 15) if powers.count(power) == 2])[-2:])[::-1]#c_2_13_powers_sort_by_power.index(sorted(sorted([power for power in range(2, 15) if powers.count(power) == 2])[-2:])[::-1])
    #for straight-flush and for straight
    elif 'straight' in e :#straight-flush is rare as shit
        for j, possible_straight in enumerate(all_possible_straights) :
            counter = 0
            for power in powers :
                counter += 1 if power in possible_straight else 0
            if counter >= 5 :
                res = j + 1       
        return 'straight', res
    elif e == 'flush' :
        powers_of_flush = [power for j, power in enumerate(powers) if kinds.count(kinds[j]) >= 5]
        return e, max(powers_of_flush), min(powers_of_flush)#c_2_13_powers_sort_by_power_for_flushes.index([max(powers_of_flush), min(powers_of_flush)])
    elif e == 'full house' :
        #взяти найбільшу тройку і потім взяти найбільше шо є з тройок або двойок які лишилися крім цьої тройки для ситуацій коли є 2 комби по 3
        max_set = max([power for power in powers if powers.count(power) == 3])
        max_bigger_than_1_not_max_set = max([power for power in powers if powers.count(power) > 1 and power != max_set])
        return e, max_set, max_bigger_than_1_not_max_set#c_2_13_powers_sort_by_power_with_reverses_no_pairs.index([max_set, max_bigger_than_1_not_max_set])

def get_power_of_comb_relational(board, hand) :
    powers, kinds = [c % 100 for c in board + hand], [c // 100 for c in board + hand]
    zip_power_kind = [c for c in zip(powers, kinds)]
    e = ev.class_to_string(ev.get_rank_class(ev.evaluate([new(powers_all[power].upper() + kinds_all[kind]) for power, kind in zip_power_kind[: -2]], [new(powers_all[power].upper() + kinds_all[kind]) for power, kind in zip_power_kind[-2 :]]))).lower()
    if e == 'high card' : return e, max(powers)
    if e in ['pair', 'three of a kind', 'four of a kind'] :
        ...
    if e == 'two pair' :
        ...
    if e == 'flush' :
        ...
    if 'straight' in e :
        ...
    if e == 'full house' :
        ...

'''
for i in range(100) :
    cards = get_unique_set_of_cards(7)
    print(cards[: -2], cards[-2 :])
    board, hand = [text_to_numeric(c) for c in cards[-2 : ]], [text_to_numeric(c) for c in cards[: -2]]
    print(get_power_of_comb(board, hand))
'''


class calculate_ranges() :
    def __init__(self) :
        super().__init__()

    def get_hands_from_comb_and_board(self, board, comb_name, comb_power) :
        self.board = board.copy()
        self.comb_name = comb_name
        self.comb_power = comb_power
        self.board_powers = [c % 100 for c in self.board]
        if self.comb_name == 'high card' :
            return self.final_check_possible_hands_with_evaluator(self.iterate_all_powers_with_filters(self.filter_for_high_card))
        elif self.comb_name == 'pair' :
            self.count_for_pair = self.board_powers.count(self.comb_power)
            return self.final_check_possible_hands_with_evaluator(self.iterate_all_powers_with_filters(self.filter_for_pair))
        elif self.comb_name == 'two pair' :
            self.powers_for_two_pair = [c for c in c_2_13_powers_sort_by_power[comb_power]]
            self.counts_for_two_pair = [self.board_powers.count(self.powers_for_two_pair[0]), self.board_powers.count(self.powers_for_two_pair[1])]
            return self.final_check_possible_hands_with_evaluator(self.iterate_all_powers_with_filters(self.filter_for_two_pair))
        elif self.comb_name == 'three of a kind' :
            self.count_for_three_of_a_kind = self.board_powers.count(self.comb_power)
            return self.final_check_possible_hands_with_evaluator(self.iterate_all_powers_with_filters(self.filter_for_three_of_a_kind))
        elif self.comb_name == 'straight' :
            self.possible_straights_additions = []
            for possible_straight in all_possible_straights :
                self.possible_straights_additions.append([power for power in possible_straight if power not in self.board_powers])
            self.possible_straights_additions = [item for item in self.possible_straights_additions if len(item) == 2]
            return self.final_check_possible_hands_with_evaluator(self.iterate_all_powers_with_filters(self.filter_for_straight))
        elif self.comb_name == 'flush' :
            self.min_flush, self.max_flush = sorted(c_2_13_powers_sort_by_power_for_flushes[self.comb_power])
            self.board_kinds = [c // 100 for c in self.board]
            counter = collections.Counter(self.board_kinds)
            values = list(counter.values())
            keys = list(counter.keys())
            self.kind_flush = keys[np.argmax(values)]
            self.powers_in_flush = [c % 100 for c in board if c // 100 == self.kind_flush]
            return self.final_check_possible_hands_with_evaluator(self.iterate_all_hands_for_flushes())
        elif self.comb_name == 'full house' :
            self.powers_for_full_house = [c for c in c_2_13_powers_sort_by_power_with_reverses_no_pairs[comb_power]]
            self.counts_for_full_house = [self.board_powers.count(self.powers_for_full_house[0]), self.board_powers.count(self.powers_for_full_house[1])]
            return self.final_check_possible_hands_with_evaluator(self.iterate_all_powers_with_filters(self.filter_for_full_house))
        elif self.comb_name == 'four of a kind' :
            self.count_for_four_of_a_kind = self.board_powers.count(self.comb_power)
            return self.final_check_possible_hands_with_evaluator(self.iterate_all_powers_with_filters(self.filter_for_four_of_a_kind))

    def filter_for_high_card(self, powers) :
        if powers[0] != powers[1] :
            if not any(power in self.board_powers for power in powers) :
                return True
        return False

    def filter_for_pair(self, powers) :
        counts = collections.Counter(self.board_powers + powers)
        if counts[self.comb_power] == 2 :
            counts[self.comb_power] = 0
            return all(power < 2 for power in counts.values())
        return False

    def filter_for_two_pair(self, powers) :
        temp = self.board_powers + powers
        return temp.count(self.powers_for_two_pair[0]) == 2 and temp.count(self.powers_for_two_pair[1]) == 2

    def filter_for_three_of_a_kind(self, powers) :
        temp = self.board_powers + powers
        return temp.count(self.comb_power) == 3

    def filter_for_straight(self, powers) :
        return any(all(power in possible for power in powers) for possible in self.possible_straights_additions)

    def filter_for_flush(self, kinds) :
        temp = self.board_kinds + kinds
        return any(a >= 5 for a in collections.Counter(temp).values())

    def filter_for_full_house(self, powers) :
        temp = self.board_powers + powers
        return temp.count(self.powers_for_full_house[0]) == 3 and temp.count(self.powers_for_full_house[1]) == 2
    
    def filter_for_four_of_a_kind(self, powers) :
        temp = self.board_powers + powers
        return temp.count(self.comb_power) == 4

    def clean_from_hands_with_same_cards_as_in_board(self, possible_hands) :
        hands = []
        for hand in possible_hands :
            if not any(c in self.board for c in hand) :
                hands.append(hand)
        return hands

    def iterate_all_powers_with_filters(self, filters) :
        possible_hands_powers = []  
        for powers in c_2_13_powers_sort_by_power_with_pairs :
            if filters(powers) :
                possible_hands_powers.append(powers)
        
        possible_hands = []
        for powers in possible_hands_powers :
            for kinds in c_2_4_kinds_with_reverses :
                if powers[0] != powers[1] or powers[0] == powers[1] and kinds[0] != kinds[1] :
                    possible_hands.append([powers[0] + kinds[0] * 100, powers[1] + kinds[1] * 100])
        return self.clean_from_hands_with_same_cards_as_in_board(possible_hands)

    def iterate_all_hands_for_flushes(self) :
        possible_hands = []  
        for powers in c_2_13_powers_sort_by_power : 
            if powers[1] >= self.min_flush and powers[0] <= self.max_flush :
                if powers[0] not in self.powers_in_flush and powers[1] not in self.powers_in_flush :
                    hand = [powers[0] + self.kind_flush * 100, powers[1] + self.kind_flush * 100]
                    possible_hands.append(hand)
        return self.clean_from_hands_with_same_cards_as_in_board(possible_hands)
    
    def final_check_possible_hands_with_evaluator(self, possible_hands) :
        approved_hands = []
        for hand in possible_hands :
            if get_power_of_comb(board, hand) == (self.comb_name, self.comb_power) :
                approved_hands.append(hand)
        return approved_hands
calculate_ranges = calculate_ranges()



'''
t = time.time()
for i in range(1000) :
    cards = get_unique_set_of_cards(7)
    board, hand = [text_to_numeric(c) for c in cards[ : -2]], [text_to_numeric(c) for c in cards[-2 : ]]
    #print(board, hand)
    comb_name, comb_power = get_power_of_comb(board, hand)
    #if comb_name == 'high card' :
    hands = calculate_ranges.get_hands_from_comb_and_board(board, comb_name, comb_power)
    if not sorted(hand) in [sorted(h) for h in hands] :
        print(comb_name, comb_power, cards, hands)
print(time.time() - t)
'''

'''
def iterate_all_hands_with_filters(*filters) :
    possible_hands = []  

    return possible_hands
def get_hands_for_comb_and_board(board, comb_name, comb_power) :
    possible_hands = []
    board_powers = [c % 100 for c in board]
    board_kinds = [c // 100 for c in board]
    if comb_name == 'high card' : 
        for powers in c_2_13_powers_sort_by_power :
            if not any([power in board_powers for power in powers]) :
                for kinds in c_2_4_kinds_with_reverses :
                    #if (board_kinds + list(kinds)).count(kinds[0]) < 5 and (board_kinds + list(kinds)).count(kinds[1]) < 5 : 
                    hand = [powers[0] + kinds[0] * 100, powers[1] + kinds[1] * 100]
                    #if not any([c in board for c in hand]) :
                    if (get_power_of_comb(board, hand)) == ('high card', comb_power) :
                        possible_hands.append(hand)
    elif comb_name == 'pair' : 
        if board_powers.count(comb_power) == 2 : 
        for powers in 

    return possible_hands
'''
'''
t = time.time()
for i in range(0) :
    cards_text = get_unique_set_of_cards(5)
    cards = [text_to_numeric(c) for c in cards_text]
    board = cards[ : 3]
    hand = cards[3 : ]
    comb_name, comb_power = get_power_of_comb(board, hand)
    if comb_name == 'high card' : 
        #print(comb_power, cards_text, cards)
        #t = time.time()
        poss = get_hands_for_comb_and_board(board, comb_name, comb_power)
        #print(time.time() - t)
        txt = np.vectorize(numeric_to_text)(poss)
        #print(txt)
        if not sorted(hand) in [sorted(item) for item in poss] :
            print(cards_text, board, hand, comb_name, comb_power)
            pprint(txt)
        #print(hand, poss)
print(time.time() - t)
'''
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
                evop = 7462 - ev.evaluate(tempboard, opponent)
                opponents.append(evop)
            evhand = 7462 - ev.evaluate(tempboard, hand)
            evop_max = np.max(opponents)
            
            if evhand > evop_max : win += 1
            if evhand < evop_max : lose += 1
            if evhand == evop_max : draw += 1
        if show_time : print(time.time() - time1)
        return np.array([win, lose, draw, win + lose + draw])
    return np.zeros(4)

def get_all_combs_from_flop_to_river(board, hand) :
    board, hand = [text_to_numeric(c) for c in board], [text_to_numeric(c) for c in hand] 
    combs = []
    for board_len in range(3, 6) :
        combs.append(get_power_of_comb(board[: board_len], hand))
    return combs

def calculate_player_state_vector(bb_size, p_names, p_amounts, f_names, f_amounts, t_names, t_amounts, r_names, r_amounts) :
    names = [p_names, f_names, t_names, r_names]
    amounts = [[float(b) / bb_size for b in a.replace(' ', '').split(';') if len(b) > 0] for a in [p_amounts, f_amounts, t_amounts, r_amounts]]
    kcr = {'k' : 0 , 'c' : 0, 'r' : 0}
    gr, gc = 0, 0
    id_move = 0
    vector = np.zeros(18)
    for cycle_index, (names_local, amounts_local) in enumerate(zip(names, amounts)) :
        if names_local != '' :
            r, c = 0, 0
            for name, amount in zip(names_local, amounts_local) :
                kcr[name] += 1   
                if name == 'r' : r, c = amount, 0
                else : c += amount # if k doesnt mean because the amount of k is 0
                rc = r / f(c)
                id_move += 1
                vector[3 + cycle_index * 3 : 3 + cycle_index * 3 + 3] = [r, c, rc]
                vector[0 : 3] = np.array(list(kcr.values())) / sum(list(kcr.values()))
                vector[-3 : ] = [gr + r, gc + c, (gr + r) / f(gc + c)]
                vector = np.round(vector, 5)  
                yield vector, id_move, cycle_index 
            gr += r
            gc += c



































































