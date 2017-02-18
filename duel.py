#
#
#
from shared import *
from gameObjects import *


def minmax(board, snake_list, us):
    possible_boards = enumerate_boards(board, snake_list)

def enumerate_boards(board, snake_list):
    move_set = dict()
    for snake in snake_list
        move_set[snake['id']] = board.get_valid_moves()

#movelist should be a list of keyvalue pairs,
# { id: move} where move is a valid move.
def get_board_from_moves(board, movelist):
    pass

def score_board(board, us):
    pass
