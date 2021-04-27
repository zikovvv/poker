#include <iostream>
#include <cstdlib>
#include <cmath>
#include <ctime>
#include <string>
#include <Windows.h>
#include <fstream>
using namespace std;
/*
#include <stdio.h>
#include <stdlib.h>
#include <string.h>f
#include <math.h>
#include <time.h>
#include <stdbool.h>
*/
const unsigned int MAX_PLAYERS = 6;
string powers_all("--23456789tjqka");
string kinds_all("hcds");

const int LEN_CHAR = sizeof(char);
const int LEN_INT = sizeof(int);
const int LEN_FLOAT = sizeof(float); 

const int LEN_STRAIGHTS = 10;
int STRAIGHTS_ALL_BIN[10] = {16444, 124, 248, 496, 992, 1984, 3968, 7936, 15872, 31744};

//returned values
int* cards_numeric_reallocable;
int* random_set_of_cards_numeric_reallocable;
int* kickers = {0};
int zero_array[100] = {0};

//functions
void print_array(int* arr, int len, int shift = 0)
{
    for (size_t i = shift; i < len; i++)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

void arr_to_zero(int* arr, int l)
{
    memcpy(arr, zero_array, l * LEN_INT);
}

void init_random()
{
    srand(time(0));
}

void bin(unsigned n)
{
    unsigned i;
    for (i = 1 << 31; i > 0; i = i / 2)
        (n & i) ? printf("1") : printf("0");
    printf("\n");
}

int index_in_arr(int* arr, int elem, int len)
{
    //end index not included
    for (int i = 0; i < len; i++)
    {
        //cout << arr[i] << endl;
        if(arr[i] == elem) return i;
    }
    return -1;
}

void get_set_of_cards_numeric(int* cards_numeric, int nb_cards)
{
    int card, i = 0;
    while(cards_numeric[nb_cards - 1] == 0)
    {
        while(cards_numeric[i] != 0) i++;
        card = (rand() % 13 + 2) + (rand() % 4 + 1) * 100;       
        if (index_in_arr(cards_numeric, card, nb_cards) == -1) cards_numeric[i] = card;
    }
}

void numeric_to_bin(int* cards, int* bbb, int len_cards)
{
    for (size_t i = 0; i < len_cards; i++)
    {
        bbb[cards[i] / 100 - 1] |= 1 << (cards[i] % 100);
    }
}

int get_kickers(int powers, int* counts, int* arr, int kickers_amount)
{
    int kicker_index = 3;
    int power;
    int count;
    for (int power = 14; power >= 2; power--)
    {
        if((powers >> power) & 1)
        {
            if(power != arr[1] && power != arr[2])
            {
                //printf("%d,%d  ", power, counts[power]);
                for (size_t i = 0; i < counts[power]; i++)
                {
                    arr[kicker_index] = power;
                    kicker_index++;
                    if (kicker_index == 3 + kickers_amount)
                    {
                        //printf("\n");
                        return 1;
                    }
                }
            }
        }
    }
    return 0;
}
//NO STRAIGHT FLUSH!!!!!!!!!!!!!!!!!!!!!1
//NO STRAIGHT FLUSH!!!!!!!!!!!!!!!!!!!!!1
//NO STRAIGHT FLUSH!!!!!!!!!!!!!!!!!!!!!1
//NO STRAIGHT FLUSH!!!!!!!!!!!!!!!!!!!!!1
//NO STRAIGHT FLUSH!!!!!!!!!!!!!!!!!!!!!1
int get_power_of_comb(int* cards, int cards_len, int* attr)
{
    arr_to_zero(attr, 7);
    int bbb[4] = {0};
    numeric_to_bin(cards, bbb, cards_len);

    int current_power_offset;
    int max_power = 0;
    int powers = bbb[0] | bbb[1] | bbb[2] | bbb[3];
    int counts[15] = {0};
    for (current_power_offset = 14; current_power_offset > 1; current_power_offset--)
    {
        if ((powers >> current_power_offset) & 1)
        {
            max_power == 0 ? max_power = current_power_offset : 0;
            for (int i = 0; i < 4; i++) (bbb[i] >> current_power_offset) & 1 ? counts[current_power_offset] ++ : 0;
        }
    }
    //pair kare set and full house
    int three_power = 0;
    int pair_power_1 = 0;
    int pair_power_2 = 0;
    int counter = 0;
    for(current_power_offset = max_power; current_power_offset > 1; current_power_offset -- )
    {
        counter = counts[current_power_offset];
        switch(counter)
        {
            case 2 :
                if(pair_power_1 == 0) pair_power_1 = current_power_offset;
                else if(pair_power_2 == 0) pair_power_2 = current_power_offset;
                //fulll house with current pair and max set
                if(three_power != 0)
                {
                    attr[0] = 6;
                    attr[1] = three_power;
                    attr[2] = pair_power_1;
                    return 6;
                }
                break;
            case 3 :
                if(three_power == 0)
                {
                    three_power = current_power_offset;
                    //full fouse max set max pair from previously
                    if(pair_power_1 != 0)
                    {
                        attr[0] = 6;
                        attr[1] = three_power;
                        attr[2] = pair_power_1;
                        return 6;
                    }
                }
                //full house with two sets
                else
                {
                    attr[0] = 6;
                    attr[1] = three_power;
                    attr[2] = current_power_offset;
                    return 6;
                }
                break;
            case 4 :
                //kare
                attr[0] = 7;
                attr[1] = current_power_offset; 
                get_kickers(powers, counts, attr, 1);
                return 7;
        }
    }
    
    //flush
    int min_flush_power;
    for (int i = 0; i < 4; i ++)
    {
        counter = 0;
        for(current_power_offset = max_power; current_power_offset > 1; current_power_offset --)
        {
            if ((bbb[i] >> current_power_offset) & 1)
            {
                counter ++;
                if (counter == 5)
                {
                    min_flush_power = current_power_offset;
                    current_power_offset = max_power;
                    while (1)
                    {
                        //flush, we found the min valuee of it and now знову починаєм з кінця і шукаєм максимальне, цикл точно мусить закінчитися тому вайл 1 і ш це потрібно для того шоб не провіряти на кожній ітерації чи макс нульова чи ні
                        if ((bbb[i] >> current_power_offset) & 1)
                        {
                            attr[0] = 5;
                            attr[1] = current_power_offset; 
                            attr[2] = min_flush_power;
                            return 5;
                        }
                        current_power_offset --;
                    }
                }
            }
        }
    }

    //straight
    int straight;
    for (int j = LEN_STRAIGHTS - 1; j >= 0; j--)
    {
        straight = STRAIGHTS_ALL_BIN[j];
        if ((int)(powers & straight) == straight)
        {
            attr[0] = 4;
            attr[1] = j + 1;
            return 4;
        }
    }
    //set
    if (three_power != 0)
    {
        attr[0] = 3;
        attr[1] = three_power;
        get_kickers(powers, counts, attr, 2);
        return 3;
    }

    if (pair_power_1 != 0)
    {
        attr[1] = pair_power_1;
        //two pair
        if (pair_power_2 != 0)
        {   
            attr[0] = 2;
            attr[2] = pair_power_2;
            get_kickers(powers, counts, attr, 1);
            return 2;
        } 
        //pair
        attr[0] = 1;
        get_kickers(powers, counts, attr, 3);
        return 1;
    }

    //high card
    attr[0] = 0;
    attr[1] = max_power;
    get_kickers(powers, counts, attr, 4);
    return 0;
}
void voidfunc(){}
//input cards - int array of len 7 board then hand, hand is last 2 cards, if no card on board then 0
void get_chanse(int* input_cards, int nb_players, int max_iterations, float* win, float* lose, float* tie)
{  
    bool was_win, was_lost, was_tie, show = 1 != 1;

    int temp = index_in_arr(input_cards, 0, 5);
    int static_board_len = temp == -1 ? 5 : temp;
    int dynamic_board_len = 5 - static_board_len;
    int dynamic_cards_amount = dynamic_board_len + 2 * (nb_players - 1);
    int all_cards_amount = static_board_len + 2 + dynamic_cards_amount;
    //int all_cards_amount = 17;

    int* cards_numeric_reallocable = new int[all_cards_amount]{0};
    int* temp_board_and_hand = new int[7]{0};

    float win_count = 0;
    float lose_count = 0;
    float tie_count = 0;

    memcpy(temp_board_and_hand, input_cards, static_board_len * LEN_INT);
    memcpy(cards_numeric_reallocable, input_cards, 7 * LEN_INT);

    //comb power, atr1, atr2,  + four kickers in high card = 7
    int player_comb_params[7]{0};
    int enemy_comb_params[7]{0};

    for (int iteration = 0; iteration < max_iterations; iteration++)
    {
        get_set_of_cards_numeric(cards_numeric_reallocable, all_cards_amount);
        
        show ? print_array(cards_numeric_reallocable, all_cards_amount) : voidfunc();
        
        memcpy(temp_board_and_hand + static_board_len, cards_numeric_reallocable + static_board_len, dynamic_board_len * LEN_INT);
        memcpy(temp_board_and_hand + 5, input_cards + 5, 2 * LEN_INT);
        
        get_power_of_comb(temp_board_and_hand, 7, player_comb_params);

        show ? print_array(temp_board_and_hand, 7) : voidfunc();                
        show ? print_array(player_comb_params, 7) : voidfunc();

        was_win = 0;
        was_lost = 0;
        was_tie = 0;
        for (size_t i = 1; i < nb_players; i++)
        { 
            memcpy(temp_board_and_hand + 5, cards_numeric_reallocable + 5 + 2 * i, 2 * LEN_INT);
            get_power_of_comb(temp_board_and_hand, 7, enemy_comb_params);

            show ? print_array(temp_board_and_hand, 7) : voidfunc();
            show ? print_array(enemy_comb_params, 7) : voidfunc();

            for (size_t n = 0; n < 7; n++)
            {
                if (enemy_comb_params[n] > player_comb_params[n])
                {                    
                    lose_count ++;
                    was_lost = 1;
                    i = nb_players;
                    break;
                }
                else if (enemy_comb_params[n] < player_comb_params[n])
                {
                    was_win = 1;
                    break;
                }
                else if(n == 6) was_tie = 1;
                //attrs count
            }            
        }
        if(!was_lost)
        {
            if (was_tie) tie_count++;
            else win_count++;
        }

        show ? printf("%f, %f, %f\n", win_count, lose_count, tie_count) : 0;
        
        memcpy(cards_numeric_reallocable + static_board_len, zero_array, dynamic_board_len * LEN_INT);
        memcpy(cards_numeric_reallocable + 7, zero_array, (nb_players - 1) * 2 * LEN_INT);
        show ? printf("iteration\n") : 0;
    }
    show ? printf("win %f, lose %f, tie %f\n", win_count / max_iterations, lose_count / max_iterations, tie_count / max_iterations) : 0;

    *win = win_count / max_iterations;
    *lose = lose_count / max_iterations;
    *tie = tie_count / max_iterations;
    free(cards_numeric_reallocable);
    free(temp_board_and_hand);
}

template<typename arr_numbers_type> void save_array(arr_numbers_type* arr, int size, string filename)
{
    ofstream f(filename, ios_base::trunc);
    for (size_t i = 0; i < size; i++)
    {
        f << to_string(arr[i]) << ';';
    }
}

int text_to_numeric(string card)
{
    return (kinds_all.find(card[1]) + 1) * 100 + powers_all.find(card[0]);
}

//NO STRAIGHT FLUSH!!!!!!!!!!!!!!!!!!!!!1
//NO STRAIGHT FLUSH!!!!!!!!!!!!!!!!!!!!!1
//NO STRAIGHT FLUSH!!!!!!!!!!!!!!!!!!!!!1
//NO STRAIGHT FLUSH!!!!!!!!!!!!!!!!!!!!!1
//NO STRAIGHT FLUSH!!!!!!!!!!!!!!!!!!!!!1
int main(int argc, char** argv)
{
    init_random();
    if(argc > 1)
    {
        int* input_cards = new int[argc - 2]{0};
        for (size_t i = 2; i < argc; i++) input_cards[i - 2] = text_to_numeric(argv[i]);//(kinds_all.find(card[1]) + 1) * 100 + powers_all.find(card[0]);
        //get power of single comb
        if(strcmp(argv[1], "comb") == 0) {
            int* attr = new int[7]{0};   
            get_power_of_comb(input_cards, argc - 2, attr);
            string filename("txt/comb_power.txt");
            save_array<int>(attr, 7, filename);
        }
        else if(strcmp(argv[1], "chanse") == 0)
        {
            //hcds
            int* compatible_input_cards = new int[7]{0};
            int nb_players = stoi(argv[argc - 1]);
            compatible_input_cards[6] = text_to_numeric(argv[argc - 2]);
            compatible_input_cards[5] = text_to_numeric(argv[argc - 3]);
            if(argc > 5 && argc <= 10) {
                for (size_t i = 2; i < argc - 3; i++) compatible_input_cards[i - 2] = text_to_numeric(argv[i]);
            }
            //print_array(compatible_input_cards, 7);
            float* a = new float[3];
            get_chanse(compatible_input_cards, nb_players, 100000, &a[0], &a[1], &a[2]);
            string filename("txt/chanses.txt");
            save_array<float>(a, 3, filename);
        }
    }
    else
    {
        cout << "type comb or chance mode and cards in str format lowercase board first and then 2 cards hand, debil!" << endl;
        getchar();
    }
    return 0; 
}
