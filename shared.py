from gameObjects import *

def create_board_from_data(data):
    height = data['height']
    width = data['width']
    board = []
    #i iterates over rows
    for i in range(height):
        row = []
        for j in range(width):
            #init empty board
            tile=Tile()
            row.append(tile)
        board.append(row)

    snake_list = data['snakes']
    print "Snake list:", snake_list
    for snake in snake_list:
        first = True
        for coord in snake['coords']:
            x, y = coord[0], coord[1]
            board[y][x].set_tile_type(dict(
                type='snake',
                snake_id=snake['id'],
                head=True if first else False
            ))
            first = False
    for food in data['food']:
        x, y = food[0], food[1]
        board[y][x].set_tile_type(dict(type='food'))
        
    print_board(board)
    return board

def print_board(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            print board[i][j]
