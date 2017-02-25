#
#
#

#bassically a wrapper for the game data

class Tile:

    def __init__(self, data=None):
        if data == None:
            self.data = dict(type='empty')
        else:
            self.data = data

    def is_safe(self):
        return self.data['type'] != 'snake'

    def is_food(self):
        return self.data['type'] == 'food'

    def set_tile_type(self, tile_data):
        self.data = tile_data

    def __str__(self):
        if self.data['type'] == 'snake' and self.data['head']:
            return 'h'
        return self.data['type'][:1]


class Board:

    def __init__(self, height, width, snake_dict, food):
        self.height = height
        self.width = width
        self.board = self.create_board_from_data(snake_dict, food)      # expects a 2D array of Tile objects

    # returns list of moves that will not result in instant death (wall or snake)
    def get_valid_moves(self, col, row):
        valid_moves = []
        if col < self.width-1 and self.get_tile(col+1, row).is_safe():
            valid_moves.append('right')
        if row < self.height-1 and self.get_tile(col, row+1).is_safe():
            valid_moves.append('down')
        if col > 0 and self.get_tile(col-1, row).is_safe():
            valid_moves.append('left')
        if row > 0 and self.get_tile(col, row-1).is_safe():
            valid_moves.append('up')

        return valid_moves

    def safe_get_tile(self, col, row):
        if self.not_valid_tile(row, col):
            return None
        return self.board[row][col]

    def get_tile(self, col, row):
        return self.board[row][col]

    def not_valid_tile(self, row, col):
        print row, col
        if row > self.width-1 or row < 0:
            return True
        if col > self.height-1 or col < 0:
            return True

    def create_board_from_data(self, snakes, food_list):
        board = []
        height, width = self.height, self.width

        # creates board of empty Tile objects
        for i in range(height):
            row = []
            for j in range(width):
                #init empty board
                tile=Tile()
                row.append(tile)
            board.append(row)

        # encode snakes into board by setting Tile object type to 'snake'
        for s_id, snake in snakes.iteritems():
            at_head = True
            for coord in snake['coords']:
                x, y = coord[0], coord[1]
                board[y][x].set_tile_type(dict(
                    type='snake',
                    snake_id=s_id,
                    head=at_head
                ))
                at_head = False

        # encode food into board by setting Tile object type to 'food'
        for food in food_list:
            x, y = food[0], food[1]
            board[y][x].set_tile_type(dict(type='food'))
        return board


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
