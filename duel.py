#
#
#

import itertools
import random

from copy import deepcopy

from shared import *
from gameObjects import *

def print_snake_data(snake):
    print " --- snake data --"
    for el in snake:
        print el, "::", snake[el]
    print " -- end snake data -- "

def minmax(board, snake_list, us, food_list, depth):
    if depth==4:
        val = score_board(board, us, snake_list, food_list)
        return {'val':val, 'move':None}

    future_games = enumerate_boards(board, snake_list, food_list, us)

    move = None
    node_value = float('-inf')

    for f_info in future_games:
        
        v = minmax(f_info['board'], f_info['snake_list'], us, f_info['food_list'], depth+1)
        if v['val'] > node_value:
            node_value = v['val']
            move = f_info['our_move']

    return {'val': node_value,'move': move}

def enumerate_boards(board, snake_list, food_list, us):
    move_set = []
    for snake in snake_list:
        snake_moves = []
        cur_snake_obj = get_snake(snake['id'], snake_list)
        head = get_head_coords(cur_snake_obj)
        for valid_move in board.get_valid_moves(head[0], head[1]):
            snake_moves.append({snake['id'] : valid_move})
        move_set.append(snake_moves)

    info_list = []
    all_move_comb = itertools.product(*move_set)
    new_snake_list = snake_list[:]
    for comb in all_move_comb:
        #NOTE hardcopy of snakelist and food. we change things from here on out
        info_list.append(get_board_from_moves(board, comb, deepcopy(snake_list), deepcopy(food_list), us))

    return info_list

#movelist should be a list of keyvalue pairs,
# { id: move} where move is a valid move.
def get_board_from_moves(board, move_list, snake_list, food_list, us):
    our_move = None
    for move in move_list:
        key, val = move.items()[0]
        if key == us:
            our_move = val
        enact_move(board, move, snake_list, food_list)

    compute_collisions(snake_list)

    new_board = Board(board.height, board.width, snake_list, food_list)
    game_info = dict(
        board=new_board,
        snake_list=snake_list,
        food_list=food_list,
        our_move=our_move
    )
    return game_info

#NOTE
# -- Look into rules about food getting spawned?
# -- answer may lie in server source code?
# -- predict future food???
def enact_move(board, move_info, snake_list, food_list):
    assert len(move_info) == 1
    snake_id, move = move_info.items()[0]
    snake = get_snake(snake_id, snake_list)
    head = get_head_coords(snake)
    x, y = get_tile_from_move(head, move)
    tile = board.get_tile(x, y)
    if tile and tile.is_food():
        snake['health_points'] = 100
        food_list.remove([x, y])
    else:
        snake['health_points'] = snake['health_points'] - 1
        snake['coords'].pop() #didn't eat, so the entire body moves forward

    snake['coords'].insert(0, [x, y])

def compute_collisions(snake_list):
    dead_snakes = []

    for snake in snake_list:
        cur_snake_head = get_head_coords(snake)
        for other_snake in snake_list:
            #only worry about collisions if its not the same snake
            if not other_snake['id'] == snake['id']:
                other_snake_head = get_head_coords(other_snake)

                #head on head collision
                if cur_snake_head == other_snake_head:
                    col_winner(snake, other_snake, dead_snakes)

                #look over the other snakes body.
                for coord in other_snake['coords'][1:]:
                    #snake head ran into another snake body
                    if coord == cur_snake_head:
                        dead_snakes.append(snake['id'])

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

def score_board(board, us, snake_list, food_list):
    our_snake = get_snake(us, snake_list)
    length = len(our_snake['coords'])
    num_moves = len(get_moves_from_id(us, snake_list, board))
    num_moves = float(num_moves)
    length_con = float(length)/100
    node_val = num_moves + length_con
    return node_val
