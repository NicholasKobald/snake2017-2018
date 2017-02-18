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

    def __str__(self):
        return self.data['type'][:1]


class Board:

    def __init__(self, height, width, board):
        self.height = height
        self.width = width
        self.board = board      # expects a 2D array of Tile objects

    # returns list of moves that will not result in instant death (wall or snake)
    def get_valid_moves(self, col, row):
        valid_moves = []
        if(col < self.width-1 and self.get_tile(col+1, row).is_safe()):
            valid_moves.append('right')
        if(row < self.height-1 and self.get_tile(col, row+1).is_safe()):
            valid_moves.append('down')
        if(col > 0 and self.get_tile(col-1, row).is_safe()):
            valid_moves.append('left')
        if(row > 0 and self.get_tile(col, row-1).is_safe()):
            valid_moves.append('up')

        return valid_moves

    def get_tile(self, col, row):
        return self.board[row][col]

    def print_board(self):
        board = self.board
        for i in range(self.height):
            row = ''
            for j in range(self.width):
                space_val = str(self.get_tile(j, i))
                if space_val == 'e':
                    row += '  |'
                else:
                    row += (str(self.get_tile(j, i))) + ' |'

            print row
            print '-'*self.width*3
