#
#
#

import itertools
import random

from shared import *
from gameObjects import *

depth_score = [10000, 5000, 250, 12, 6, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0]

def print_snake_data(snake):
    print " --- snake data --"
    for el in snake:
        print el, ":", snake[el]
    print " -- end snake data -- "

def start_minmax(board, snake_info, us, food_list):
    all_move_combinations = get_all_move_comb(board, snake_info, food_list)
    node_val = float('-inf')
    move = None
    for current_moveset in all_move_combinations:
        our_move = get_our_move_now(current_moveset, us)
        dead_snakes = get_board_from_moves(board, current_moveset, snake_info, food_list, us, 1)
        cur = minmax(board, snake_info, us, food_list, 1)
        if cur>node_val:
            node_val = cur
            move = our_move
        undo_move_set(board, current_moveset, dead_snakes, snake_info, food_list, 1)
    return move

def minmax(board, snake_info, us, food_list, depth):
    if depth==4 or len(snake_info)==1:
        return score_board(board, us, snake_info, food_list, depth)

    all_move_combinations = get_all_move_comb(board, snake_info, food_list)
    node_val = float('-inf')
    best = node_val
    for current_moveset in all_move_combinations:
        our_move = get_our_move_now(current_moveset, us)
        dead_snakes = get_board_from_moves(board, current_moveset, snake_info, food_list, us, depth)
        node_val = minmax(board, snake_info, us, food_list, depth+1)
        undo_move_set(board, current_moveset, dead_snakes, snake_info, food_list, depth)
        if node_val > best:
            best = node_val
    return best

def get_our_move_now(move_set, us):
    for move in move_set:
        if move['snake'] == us:
            return move['move']

def undo_move_set(board, prev_moveset, dead_snakes, snake_info, food_list, depth):
    for s_id, ded in dead_snakes.iteritems():
        snake_info[s_id] = ded

    for move in prev_moveset:
        undo_move(move, snake_info[move['snake']], food_list, board, depth)

def undo_move(move, snake, food_list, board, depth):
    head_tile = board.get_tile(snake['coords'][0][0], snake['coords'][0][1])
    if snake['ate'].pop():
        snake['health_points'] = snake['old_hp']
        food_list.append(snake['food_eaten'].pop())
        head_tile.set_tile_type(dict(type='food'))
        del snake['coords'][0]
        snake['eaten'] = snake['eaten'] - depth_score[depth]
        board.get_tile(snake['coords'][0][0], snake['coords'][0][1]).set_tile_type(dict(
            type='snake',
            head=True
        ))
    else:
        snake['health_points'] += 1
        head_tile.set_tile_type(dict(type='empty'))
        del snake['coords'][0]
        board.get_tile(snake['coords'][0][0], snake['coords'][0][1]).set_tile_type(dict(
            type='snake',
            head=True
        ))
    #this now looking at the PREVIOUS Turn.
    if not snake['ate'][-1]:
        t_x, t_y = snake['old_tails'].pop()
        snake['coords'].append([t_x, t_y])
        board.get_tile(t_x, t_y).set_tile_type(dict(
            type='snake',
            head=False
        ))

def print_future(board, snake_info, food_list):
    print " ------------ BEGIN DATA ------------ "
    board.print_board()
    for s_id, snake in snake_info.iteritems():
        print_snake_data(snake)
    print food_list
    print " ------------ END DATA ---------------"

def get_all_move_comb(board, snake_info, food_list):
    move_set = []
    for snake in snake_info:
        snake_moves = []
        head = snake_info[snake]['coords'][0]
        for valid_move in board.naive_get_valid_moves(head[0], head[1]):
            new_x, new_y = get_pos_from_move(head, valid_move)
            tile = board.get_tile(new_x, new_y)
            if tile.is_food():
                snake_moves.append(dict(
                    move=valid_move,
                    snake=snake,
                    ate=True,
                ))
            else:
                snake_moves.append(dict(
                    move=valid_move,
                    ate=False,
                    snake=snake
                ))
        move_set.append(snake_moves)
    return itertools.product(*move_set)

def get_board_from_moves(board, move_list, snake_info, food_list, us, depth):
    #map moves to snakes
    for move_info in move_list:
        enact_move(board, move_info, snake_info[move_info['snake']], food_list, depth)
    #who is a goner?
    dead = {}
    for s_id, snake in snake_info.iteritems():
        if len(board.naive_get_valid_moves(snake['coords'][0][0], snake['coords'][0][1])) == 0:
            dead[s_id] = snake

    for s_id in dead:
        del snake_info[s_id]

    return dead

def enact_move(board, move_info, snake, food_list, depth):
    head = snake['coords'][0]
    x, y = get_pos_from_move(head, move_info['move'])
    tile = board.get_tile(x, y)
    if not snake['ate'][-1]: #list.peek()
        tail = snake['coords'].pop()
        snake['old_tails'].append([tail[0], tail[1]])
        tail_tile = board.get_tile(tail[0], tail[1])
        tail_tile.set_tile_type(dict(type='empty'))

    if tile.is_food():
        snake['ate'].append(True)
        snake['eaten'] += depth_score[depth]
        snake['food_eaten'].append([x, y])
        snake['old_hp'] = snake['health_points']
        snake['health_points'] = 100
        food_list.remove([x, y])
    else:
        snake['ate'].append(False)
        snake['health_points'] = snake['health_points'] - 1

    snake['coords'].insert(0, [x, y])
    board.get_tile(head[0], head[1]).set_tile_type(dict(
        type='snake',
        head=False
    ))
    tile = board.get_tile(x, y)
    tile.set_tile_type(dict(
        type='snake',
        head=True
    ))

def score_board(board, us, snake_info, food_list, depth):
    if us not in snake_info:
        return -1000*depth_score[depth]

    if len(snake_info) == 1:
        return 1000*depth_score[depth]

    return snake_info[us]['eaten']
