#
#
#

TILE_DEBUG = True

class Tile:

    def __init__(self, data=None):
        if data == None:
            self.data = dict(type='empty')
        else:
            self.data = data

    def is_safe(self, ate_last_turn):
        # TODO (if check_tails) add check for whether this snake's head is near food
        if self.is_tail():
            snake_id = self.get_snake_id()
            assert snake_id!=None
            safe_tail = snake_id not in ate_last_turn
            return safe_tail
        return (not self.is_snake())

    def is_food(self):
        return self.data['type'] == 'food'

    def set_tile_type(self, tile_data):
        self.data = tile_data

    def is_snake(self):
        return (self.data['type'] == 'snake')

    def get_snake_id(self):
        if self.is_snake():
            return self.data['snake_id']
        return None

    def is_head(self):
        return (self.is_snake() and self.data['head'])

    def is_tail(self):
        return (self.is_snake() and self.data['tail'])

    def __str__(self):
        if self.data['type'] == 'snake' and self.data['head']:
            return 'h'
        elif self.data['type'] == 'snake' and self.data['tail']:
            return 't'
        return self.data['type'][:1]


class Board:

    def __init__(self, height, width, snake_dict, food):
        self.height = height
        self.width = width
        self.board = self.create_board_from_data(snake_dict, food)      # expects a 2D array of Tile objects

    # returns list of moves that will not result in instant death (wall or snake)
    def get_valid_moves(self, col, row, ate_last_turn=[]):
        valid_moves = []
        # TODO add check for snake tails (may be safe!)
        if col < self.width-1 and self.get_tile(col+1, row).is_safe(ate_last_turn):
            valid_moves.append('right')
        if row < self.height-1 and self.get_tile(col, row+1).is_safe(ate_last_turn):
            valid_moves.append('down')
        if col > 0 and self.get_tile(col-1, row).is_safe(ate_last_turn):
            valid_moves.append('left')
        if row > 0 and self.get_tile(col, row-1).is_safe(ate_last_turn):
            valid_moves.append('up')

        return valid_moves

    def find_losing_head_collisions(self, col, row, my_snake_id, snake_dict, ate_last_turn):
        valid_moves = self.get_valid_moves(col, row, ate_last_turn)

        losing_head_collisions = []
        for move in valid_moves:
            valid_pos = self.get_pos_from_move((col, row), move)
            for adj in ['right', 'left', 'up', 'down']:
                adj_pos = self.get_pos_from_move(valid_pos, adj)
                # skip if this is our head
                if adj_pos[0] == col and adj_pos[1] == row:
                    continue

                adj_tile = self.safe_get_tile(adj_pos[0], adj_pos[1])
                if adj_tile == None or not (adj_tile.is_head()):
                    # skip if we are outside the board or we're not at a snake's head
                    continue

                enemy_snake_id = adj_tile.get_snake_id()
                if enemy_snake_id == None:
                    continue
                enemy_snake, my_snake = snake_dict[enemy_snake_id], snake_dict[my_snake_id]

                enemy_snake_len = len(enemy_snake['coords'])
                if enemy_snake in ate_last_turn:
                    enemy_snake_len += 1

                my_snake_len = len(my_snake['coords'])
                if my_snake in ate_last_turn:
                    my_snake_len += 1

                # ensure not to insert duplicates
                if enemy_snake_len >= my_snake_len and move not in losing_head_collisions:
                    losing_head_collisions.append(move)

        return losing_head_collisions


    def safe_get_tile(self, col, row):
        if self.not_valid_tile(row, col):
            return None
        return self.board[row][col]

    def get_tile(self, col, row):
        return self.board[row][col]

    def not_valid_tile(self, row, col):
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
            for index, coord in enumerate(snake['coords']):
                x, y = coord[0], coord[1]
                at_head, at_tail = (index == 0), (index==len(snake['coords'])-1)
                # TODO implement a more robust edge case treatment
                # --> in early game, we may over-write tiles (snakes are stacked)
                if board[y][x].is_head():
                    continue
                else:
                    board[y][x].set_tile_type(dict(
                        type='snake',
                        snake_id=s_id,
                        head=at_head,
                        tail=at_tail
                    ))

        # encode food into board by setting Tile object type to 'food'
        for food in food_list:
            x, y = food[0], food[1]
            board[y][x].set_tile_type(dict(type='food'))
        return board

    # computes position resulting from current position and move
    # clunky, big, annoying to write... put it in a function!
    def get_pos_from_move(self, cur_pos, move):
        col, row = cur_pos[0], cur_pos[1]
        if move == 'up' and row-1 >= 0:
            return (col, row-1)
        elif move == 'down' and row+1 < height:
            return (col, row+1)
        elif move == 'left' and col-1 >= 0:
            return (col-1, row)
        elif move == 'right' and col+1 < width:
            return (col+1, row)

        raise Exception

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
