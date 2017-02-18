#
#
#

class Tile:

    def __init__(self, data=None):
        if data == None:
            self.data = dict(type='empty')
        else:
            self.data = data

    def is_safe(self):
        return (self.data['type'] != 'snake')

    def set_tile_type(self, tile_data):
        self.data = tile_data


class Board:

    def __init__(height, width, board):
        self.height = height
        self.width = width
        self.board = board      # expects a 2D array of Tile objects

    # returns list of moves that will not result in instant death (wall or snake)
    def get_valid_moves(col, row):
        valid_moves = []
        if(col < width-1 and get_tile(col+1, row).is_safe()):
            valid_moves.append('right')
        if(row < height-1 and get_tile(col, row+1).is_safe()):
            valid_moves.append('down')
        if(col > 0 and get_tile(col-1, row).is_safe()):
            valid_moves.append('left')
        if(row > 0 and get_tile(col, row-1).is_safe()):
            valid_moves.append('down')

        return valid_moves

    def get_tile(col, row):
        return board[row][col]
