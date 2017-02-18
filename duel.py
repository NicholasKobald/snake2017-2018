#
#
#

import itertools

from shared import *
from gameObjects import *



def minmax(board, snake_list, us):
    possible_boards = enumerate_boards(board, snake_list)

def enumerate_boards(board, snake_list):
    move_set = []
    for snake in snake_list:
        snake_moves = []
        cur_snake_obj = get_snake(snake['id'], snake_list)
        head = get_head_coords(cur_snake_obj)
        for valid_move in board.get_valid_moves(head[0], head[1]):
            snake_moves.append({snake['id'] : valid_move})
        move_set.append(snake_moves)

    board_list = []
    all_move_comb = itertools.product(*move_set)
    for comb in all_move_comb:
        #NOTE hardcopy of snakelist
        get_board_from_moves(board, comb, snake_list[:])

#movelist should be a list of keyvalue pairs,
# { id: move} where move is a valid move.
def get_board_from_moves(board, move_list, snake_list):
    for move in move_list:
        enact_move(move, snake_list)

def enact_move(move_info, snake_list):
    assert len(move_info) == 1
    snake_id, move = move_info.items()[0]
    snake = get_snake(snake_id, snake_list)
    head = get_head_coords(snake)
    




def score_board(board, us):
    pass
