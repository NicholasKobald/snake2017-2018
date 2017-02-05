#
#
#

from helper import *

#given a snake list, and a board, returns the list of boards that
#arise from any combination of moves.
#
#this implementation only works on a snake_list of length 2
#To expand to the general case, see iter.tools
def enumerate_boards(us, them, board):
    board_list = [] #max of 9 in a 1v1, so it's ok to generate them at once
    for our_move in get_valid_moves(us):
        for their_move in get_valid_moves(us):
            gbfm(us, our_move, them, their_move, board)

#gen board from moves
#
#TODO realize the existence of food
def gbfm(us, us_move, them, them_move, board):
    pass
