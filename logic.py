#
#
#

def do_minmax(board, game_info, depth=None):
    possible = eb(game_info['our_snake'], game_info['snake_list'], board)
    print "got possible boards."
    print_board(possible[1])

    print "Number of resulting boards:", len(possible)


#EnumerateBoards
def eb(us, opponent, board):
    board_list = [] #max of 9 in a 1v1, so it's ok to generate them at once
    opponent = opponent.pop()
    for our_move in get_valid_moves(us['coords'][0], board, 10, 10):
        for their_move in get_valid_moves(opponent['coords'][0], board, 10, 10):
            board_list.append(gbfm(us, our_move, opponent, their_move, board))

    return board_list

def gbfm(us, us_move, them, them_move, board):
    print us['name'], "moving", us_move, "them:", them['name'], "moving", them_move
    new_board = [row[:] for row in board]
    enact_move(us, us_move, board)
    enact_move(them, them_move, board)
    return new_board


def enact_move(snake, direc, board):
    head = snake['coords'][0]
    new_head = get_new_head(head, direc)
    snake['coords'].insert(0, new_head)
    board[new_head[0]][new_head[1]] = 'h'+snake['name']
    board[head[0]][head[1]] = 's'+snake['name']
    if board[new_head[0]][new_head[1]] == 'f':
        return
    snake['coords'].pop()

def get_new_head(h, direction):
    head = h[:]
    if direction == 'up':
        head[0] -= 1
    if direction == 'down':
        head[0] += 1
    if direction == 'left':
        head[1] -= 1
    if direction == 'right':
        head[1] += 1
    return head

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

def get_valid_moves(head, board, height, width):
    candidate_moves = ['up', 'right', 'down', 'left']

    snake_square = lambda s: s.startswith('h') or s.startswith('s')
    not_safe = lambda y,x: snake_square(board[x][y]) or snake_square(board[x][y])

    y = head[0] #how many lists in we go
    x = head[1] #how many elements over

    if x == width-1 or not_safe(x+1, y):
        candidate_moves.remove('right')
    if x == 0 or not_safe(x-1, y):
        candidate_moves.remove('left')
    if y == height-1 or not_safe(x, y+1):
        candidate_moves.remove('right')
    if y == 0 or not_safe(x, y-1):
        candidate_moves.remove('up')

    return candidate_moves
