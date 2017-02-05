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

def print_board(board):
    for row in board:
        print row
def get_valid_moves(snake, board, width=10, height=10):
    candidate_moves = ['n', 'e', 's', 'w']
    candidate_moves.remove(flip_dict[get_dir(snake['coords'])])
    head = snake['coords'][0]
    print_board(board)
    
    if head[0] == width-1:
        candidate_moves.remove('e')
    if head[0] == 0:
        candidate_moves.remove('w')
    if head[1] == height-1:
        candidate_moves.remove('s')
    if head[1] == 0:
        candidate_moves.remove('n')

    return candidate_moves
