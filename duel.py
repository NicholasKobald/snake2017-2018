#
#
#

import itertools
import random

from shared import *
from gameObjects import *

def print_snake_data(snake):
    print " --- snake data --"
    for el in snake:
        print el, ":", snake[el]
    print " -- end snake data -- "

def minmax(board, snake_info, us, food_list, depth):
    if depth==3:
        val = score_board(board, us, snake_info, food_list)
        return {'val':val, 'move':None}

    all_move_combinations = get_all_move_comb(board, snake_info, food_list)

    print all_move_combinations
    best = float('-inf')
    node_val = dict()  #rewrite dict returning, making a 'start' func.
    node_val['val'] = best
    node_val['our_move'] = None
    for current_moveset in all_move_combinations:
        print current_moveset
        dead_snakes = get_board_from_moves(board, current_moveset, snake_info, food_list, us)
        node_val['val'] = minmax(board, snake_info, us, food_list, depth+1)
        undo_move_set(board, current_moveset, dead_snakes, snake_info, food_list)
        if node_val['val'] > best:
            best = node_val['val']
            move = node_val['our_move']

    return {'val': node_val['val'],'move': move}

def undo_move_set(board, prev_moveset, dead_snakes, snake_info, food_info):


def print_future(board, snake_info, food_list, f_info):
    board.print_board()
    for snake in f_info['snake_info']:
        print "Snake:"
        print_snake_data(snake)
    print food_list

def get_all_move_comb(board, snake_info, food_list):
    move_set = []
    for snake in snake_info:
        snake_moves = []
        head = snake_info[snake]['coords'][0]
        for valid_move in board.get_valid_moves(head[0], head[1]):
            new_x, new_y = get_tile_from_move(head, valid_move)
            tile = board.get_tile(new_x, new_y)
            if tile and tile.is_food():
                snake_moves.append(dict(
                    move=valid_move,
                    snake=snake,
                    ate=True,
                    health_points=snake_info[snake]['health_points']
                ))
            else:
                snake_moves.append(dict(
                    move=valid_move,
                    ate=False,
                    snake=snake
                ))

        move_set.append(snake_moves)

    return itertools.product(*move_set)

def enumerate_boards(board, snake_info, food_list, us):
    move_set = []
    for snake in snake_info:
        snake_moves = []
        head = snake_info[snake]['coords'][0]
        for valid_move in board.get_valid_moves(head[0], head[1]):
            snake_moves.append({snake: valid_move})
        move_set.append(snake_moves)

    info_list = []
    all_move_comb = itertools.product(*move_set)
    for comb in all_move_comb:
        #NOTE hardcopy of snakelist and food. we change things from here on out
        info_list.append(get_board_from_moves(board, comb, deepcopy(snake_info), deepcopy(food_list), us))

    return info_list

#movelist should be a list of keyvalue pairs,
# { id: move} where move is a valid move.
def get_board_from_moves(board, move_list, snake_info, food_list, us):
    #map moves to snakes
    for move_info in move_list:
        enact_move(board, move_info, snake_info[move_info['snake']], food_list)

    #who is a goner?
    dead = {}
    for s_id, snake in snake_info.iteritems():
        if len(board.get_valid_moves(snake['coords'][0][0], snake['coords'][0][1])) == 0:
            dead[s_id] = snake

    #we'll use this dead dict to place the snakes back in after recursing.
    for s_id in dead:
        del snake_info[s_id]

    return dead

def enact_move(board, move_info, snake, food_list):
    head = snake['coords'][0]
    x, y = get_tile_from_move(head, move_info['move'])
    tile = board.get_tile(x, y)
    if tile and tile.is_food():
        
        snake['eaten'] += 1
        snake['health_points'] = 100
        food_list.remove([x, y])
    else:
        snake['health_points'] = snake['health_points'] - 1
        snake['coords'].pop() #didn't eat, so the entire body moves forward

    snake['coords'].insert(0, [x, y])

#NOTE Yikes
def score_board(board, us, snake_info, food_list):
    #obvious loss/win conditions.
    if us not in snake_info:
        return float('-inf')
    if us in snake_info and len(snake_info)==1:
        return float('inf')

    our_snake = snake_info[us] #why i did this
    length = len(our_snake['coords'])
    head = our_snake['coords'][0]
    num_moves = float(len(board.get_valid_moves(head[0], head[1])))
    length_con = float(length)/100
    node_val = num_moves + length_con
    health = float(our_snake['health_points'])/100
    #past a certain length (this should be a function of)
    #board size, not cutting ourself off is important.
    if length>20:
        return (count_reachable(board, head)) + float(our_snake['eaten'])/health
    return node_val
