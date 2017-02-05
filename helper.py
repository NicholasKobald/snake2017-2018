#
#
#

flip_dict = {
    'n':'s',
    's':'n',
    'e':'w',
    'w':'e'
}

def get_specific_snake(snake_list, snake_name):
    for snake in snake_list:
        if snake['name'] == snake_name:
            return snake

#walls are at -1 and val of width or height
def get_dir(coords):
    #moved east
    if coords[0][0] < coords[1][0]:
        return 'e'
    #moved west
    if coords[0][0] > coords[1][0]:
        return 'w'
    #northturn
    if coords[0][1] < coords[1][1]:
        return 'n'
    return 's'
def print_board_two(board):
    brs = ''
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board['state']=='empty':
                brs+='E'
            else:
                brs+='S'

def print_board(board):
    for row in board:
        row_rep  = []
        for entry in row:
            if entry['state']=='empty':
                row_rep.append('e')
            else:
                row_rep.append('S')
        print row_rep

def get_valid_moves(snake, board, width=10, height=10):
    candidate_moves = ['n', 'e', 's', 'w']

    head = snake['coords'][0]
    not_safe = lambda y, x:board[x][y]['state']=='head' or board[x][y]['state']=='body'

    y = head[0]
    x = head[1]

    if x == width-1 or not_safe(x+1, y):
        candidate_moves.remove('e')
    if head[0] == 0 or not_safe(x-1, y):
        candidate_moves.remove('w')
    if head[1] == height-1 or not_safe(x, y+1):
        candidate_moves.remove('s')
    if head[1] == 0 or not_safe(x, y-1):
        candidate_moves.remove('n')

    return candidate_moves
