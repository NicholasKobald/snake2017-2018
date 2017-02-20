#
#
#

import itertools
import random

#TODO rewrite this out
from copy import deepcopy

from shared import *
from gameObjects import *

def print_snake_data(snake):
    print " --- snake data --"
    for el in snake:
        print el, "::", snake[el]
    print " -- end snake data -- "

def minmax(board, snake_info, us, food_list, depth):
    if depth==5:
        val = score_board(board, us, snake_info, food_list)
        return {'val':val, 'move':None}

    future_games = enumerate_boards(board, snake_info, food_list, us)

    move = None
    node_value = float('-inf')

    for f_info in future_games:
        v = minmax(f_info['board'], f_info['snake_info'], us, f_info['food_list'], depth+1)
        if v['val'] > node_value:
            node_value = v['val']
            move = f_info['our_move']

    return {'val': node_value,'move': move}

def print_future(board, snake_info, food_list, f_info):
    board.print_board()
    for snake in f_info['snake_info']:
        print "Snake:"
        print_snake_data(snake)
    print food_list

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
    our_move = None
    #maybe we can encode the move into snakes, then we can lookup our own
    #Move (or anyone elses) easily..
    for move in move_list:
        key, val = move.items()[0]
        if key == us:
            our_move = val
        enact_move(board, move, snake_info, food_list)

    compute_collisions(snake_info)

    new_board = Board(board.height, board.width, snake_info, food_list)
    game_info = dict(
        board=new_board,
        snake_info=snake_info,
        food_list=food_list,
        our_move=our_move
    )
    return game_info

#NOTE
# -- Look into rules about food getting spawned?
# -- answer may lie in server source code?
# -- predict future food???
def enact_move(board, move_info, snake_info, food_list):
    assert len(move_info) == 1
    snake_id, move = move_info.items()[0]
    snake = snake_info[snake_id]
    head = snake['coords'][0]

    x, y = get_tile_from_move(head, move)
    tile = board.get_tile(x, y)
    if tile and tile.is_food():
        snake['health_points'] = 100
        if [x, y] in food_list:
            food_list.remove([x, y])
    else:
        snake['health_points'] = snake['health_points'] - 1
        snake['coords'].pop() #didn't eat, so the entire body moves forward

    snake['coords'].insert(0, [x, y])


#NOTE primary purpose is sideffect on snake_info
def compute_collisions(snake_info):
    dead_snakes = []

    for s_id, snake in snake_info.iteritems():
        #incantation for head
        cur_snake_head = snake['coords'][0]
        for id_two, other_snake in snake_info.iteritems():
            #only worry about collisions if its not the same snake
            #NOTE this is comparing ID's
            if s_id != id_two:
                other_snake_head = other_snake['coords'][0]
                #head on head collision
                if cur_snake_head == other_snake_head:
                    col_winner(snake, other_snake, dead_snakes)
                #look over the other snakes body.
                for coord in other_snake['coords'][1:]:
                    #snake head ran into another snake body
                    if coord == cur_snake_head:
                        dead_snakes.append(s_id)

    for goner in dead_snakes:
        del snake_info[goner]

def col_winner(snek_one, snek_two, dead_snakes):
    snake_one_length = len(snek_one['coords'])
    snake_two_length = len(snek_two['coords'])

    if snake_one_length > snake_two_length:
        dead_snakes.append(snek_two['id'])
        return
    if snake_two_length > snake_one_length:
        dead_snakes.append(snek_one['id'])
        return

    if snake_one_length == snake_two_length:
        dead_snakes.append(snek_two['id'])
        dead_snakes.append(snek_one['id'])

def score_board(board, us, snake_info, food_list):
    #our_snake = get_snake(us, snake_info)
    our_snake = snake_info[us] #why i did this
    head = our_snake['coords'][0]
    length = len(our_snake['coords'])
    num_moves = len(board.get_valid_moves(head[0], head[1]))
    num_moves = float(num_moves)
    length_con = float(length)/100
    node_val = num_moves + length_con
    return node_val
