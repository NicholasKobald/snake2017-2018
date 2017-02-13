#
#
#
from helper import *

#given a snake list, and a board, returns the list of boards that
#arise from any combination of moves.
#
#this implementation only works on a snake_list of length 2
#To expand to the general case, see iter.tools

#something like this:
#import itertools
#list(itertools.product(*all_move_mapped))
def do_minmax(game, snake_list):
    pass



def enumerate_boards(us, them, board):
    board_list = [] #max of 9 in a 1v1, so it's ok to generate them at once
    for our_move in get_valid_moves(us):
        for their_move in get_valid_moves(us):
            gbfm(us, our_move, them, their_move, board)
    return board_list

#gen board from moves
#TODO realize the existence of food
def gbfm(us, us_move, them, them_move, board):
    pass


def convert_to_internal_board(board):
    internal_rep = []
    print "In convert.--"
    for i in range(len(board)):
        row = []
        for j in range(len(board[0])):
            tile = board[i][j]
            if tile['state'] == 'empty':
                row.append('e')
            elif tile['state']=='head':
                row.append('h'+tile['snake'])
            elif tile['state']=='body':
                row.append('s'+tile['snake'])
            elif tile['state']=='food':
                row.append('f')
        internal_rep.append(row)
    return internal_rep

def print_board(board):
    print "----- PRINT BOARD ----\n"
    for i in range(len(board)):
        row_repr = '|'
        for j in range(len(board[0])):
            row_repr += board[i][j] + '|'
            if board[i][j]=='e' or board[i][j]=='f':
                row_repr+=' '
        print row_repr
        print('-' * len(row_repr) )
    print "\n----- PRINT BOARD FIN ----"

def get_moveset(snake, board):
    return dict(
        snek=snake,
        moves=get_valid_moves(snake, board)
    )

def get_specific_snake(snake_list, snake_name):
    for snake in snake_list:
        if snake['name'] == snake_name:
            return snake

#walls are at -1 and val of width or height
def get_dir(coords):
    #moved east
    if coords[0][0] < coords[1][0]:
        return 'right'
    #moved west
    if coords[0][0] > coords[1][0]:
        return 'left'
    #northturn
    if coords[0][1] < coords[1][1]:
        return 'up'
    return 'down'

def print_board_two(board):
    brs = ''
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board['state']=='empty':
                brs+='E'
            else:
                brs+='S'

def get_valid_moves(snake, board):
    candidate_moves = ['up', 'right', 'down', 'left']
    head = snake['coords'][0]
    snake_square = lambda s: s.startswith('h') or s.startswith('s')
    not_safe = lambda y,x: snake_square(board[x][y]) or snake_square(board[x][y])

    y = head[0]
    x = head[1]

    if x == width-1 or not_safe(x+1, y):
        candidate_moves.remove('right')
    if head[0] == 0 or not_safe(x-1, y):
        candidate_moves.remove('left')
    if head[1] == height-1 or not_safe(x, y+1):
        candidate_moves.remove('right')
    if head[1] == 0 or not_safe(x, y-1):
        candidate_moves.remove('up')

    return candidate_moves
