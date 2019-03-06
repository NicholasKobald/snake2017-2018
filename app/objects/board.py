TILE_DEBUG = True


class Tile(object):

    def __init__(self, data=None):
        if data is None:
            self.data = dict(type='empty')
        else:
            self.data = data

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.is_food():
            return "f"
        elif self.is_head():
            return "h"
        elif self.is_snake():
            return "s"
        elif self.is_tail():
            return "t"
        elif self.is_safe():
            return "o"
        else:
            return "?"

    def naive_is_safe(self):
        return self.data['type'] != 'snake'

    def safe_in_the_future(self, num_turns_in_future, num_times_eaten, us_id, ate_last_turn=[]):
        if self.is_snake() and self.get_snake_id() == us_id:
            num_turns_until_safe = self.turns_till_safe(ate_last_turn=ate_last_turn) + num_times_eaten
        else:
            num_turns_until_safe = self.turns_till_safe(ate_last_turn=ate_last_turn)
        return num_turns_until_safe <= num_turns_in_future

    def is_safe(self, ate_last_turn):
        if self.is_tail():
            snake_id = self.get_snake_id()
            return snake_id not in ate_last_turn
        return not self.is_snake()

    def is_food(self):
        return self.data['type'] == 'food'

    def set_tile_type(self, tile_data):
        self.data = tile_data

    def get_tile_data(self):
        return self.data

    def is_snake(self):
        return self.data['type'] == 'snake'

    def get_snake_id(self):
        if self.is_snake():
            return self.data['snake_id']
        return None

    def is_head(self):
        return self.is_snake() and self.data['head']

    def is_tail(self):
        return self.is_snake() and self.data['tail']

    def turns_till_safe(self, ate_last_turn=[]):
        if 'til_empty' in self.data:
            if self.is_snake() and self.get_snake_id() in ate_last_turn:
                return self.data['til_empty']
            else:
                # because the tail is safe!
                return self.data['til_empty'] - 1
        else:
            return 0


class Board(object):

    def __init__(self, height, width, snakes, food, my_snake_id, ate_last_turn=[]):
        """
        Params:
            height (int): of board.
            width (int): of board.
            snakes (dict): IDs and locations of snakes.
            food (2D list): coords of food.
            my_snake_id (str): ID of our snake.
            ate_last_turn (list): list of snake IDs that ate food in the previous turn
                (which means they will grow by 1 tile in this turn, their tail staying where it was).

        """
        self.height = height
        self.width = width
        self.snakes = snakes
        self.my_snake_id = my_snake_id
        self.food = food
        self.ate_last_turn = ate_last_turn
        self.board = self.create_board_from_data()

    def __repr__(self):
        return __str__()

    def __str__(self):
        board_str = ""
        for row in self.board:
            for tile in row:
                board_str += str(tile) + " "
            board_str += "\n"
        return board_str

    def get_valid_moves_in_the_future(self, col, row, turns_passed, num_times_eaten):
        valid_moves = []
        us_id = self.my_snake_id

        if col < self.width - 1 and self.get_tile(col + 1, row).safe_in_the_future(turns_passed, num_times_eaten, us_id, self.ate_last_turn):
            valid_moves.append('right')

        if row < self.height - 1 and self.get_tile(col, row + 1).safe_in_the_future(turns_passed, num_times_eaten, us_id, self.ate_last_turn):
            valid_moves.append('down')

        if col > 0 and self.get_tile(col - 1, row).safe_in_the_future(turns_passed, num_times_eaten, us_id, self.ate_last_turn):
                valid_moves.append('left')

        if row > 0 and self.get_tile(col, row - 1).safe_in_the_future(turns_passed, num_times_eaten, us_id, self.ate_last_turn):
            valid_moves.append('up')

        return valid_moves

    # returns list of moves that will not result in instant death (wall or snake)
    def get_valid_moves(self, col, row):
        valid_moves = []
        if col < self.width - 1 and self.get_tile(col + 1, row).is_safe(self.ate_last_turn):
            valid_moves.append('right')
        if row < self.height - 1 and self.get_tile(col, row + 1).is_safe(self.ate_last_turn):
            valid_moves.append('down')
        if col > 0 and self.get_tile(col - 1, row).is_safe(self.ate_last_turn):
            valid_moves.append('left')
        if row > 0 and self.get_tile(col, row - 1).is_safe(self.ate_last_turn):
            valid_moves.append('up')

        return valid_moves

    def naive_get_valid_moves(self, col, row):
        valid_moves = []
        if col < self.width - 1 and self.get_tile(col + 1, row).naive_is_safe():
            valid_moves.append('right')
        if row < self.height - 1 and self.get_tile(col, row + 1).naive_is_safe():
            valid_moves.append('down')
        if col > 0 and self.get_tile(col - 1, row).naive_is_safe():
            valid_moves.append('left')
        if row > 0 and self.get_tile(col, row - 1).naive_is_safe():
            valid_moves.append('up')

        return valid_moves

    # for easier migrating to the 2018 api
    def _tuple_to_point(self, tup):
        return {'x': tup[0], 'y': tup[1]}

    def find_losing_head_collisions(self):
        """Determine which moves would cause death by head collision for specified snake.

        Returns:
            losing_head_collisions: list of dangerous moves e.g. ['up', 'left']
        """
        my_snake = self.snakes[self.my_snake_id]
        col, row = my_snake.head
        valid_moves = self.get_valid_moves(col, row)
        losing_head_collisions = []
        for move in valid_moves:
            valid_pos = self.get_pos_from_move((col, row), move)

            for adj in ['right', 'left', 'up', 'down']:
                adj_pos = self.get_pos_from_move((valid_pos[0], valid_pos[1]), adj)

                # skip if we are looking outside the board or if this is our head
                if adj_pos is None or (adj_pos[0] == col and adj_pos[1] == row):
                    continue

                adj_tile = self.get_tile(adj_pos[0], adj_pos[1])
                if adj_tile is None or not (adj_tile.is_head()):
                    # skip if we are outside the board or we're not at a snake's head
                    continue

                enemy_snake_id = adj_tile.get_snake_id()
                if enemy_snake_id is None:
                    continue

                enemy_snake = self.snakes[enemy_snake_id]

                enemy_snake_len = enemy_snake.length
                if enemy_snake.ate_last_turn:
                    enemy_snake_len += 1

                my_snake_len = my_snake.length
                if my_snake.ate_last_turn:
                    my_snake_len += 1
                # ensure not to insert duplicates
                if enemy_snake_len >= my_snake_len:
                    losing_head_collisions.append(move)

        return list(set(losing_head_collisions))

    def get_tile(self, col, row):
        return self.board[row][col]

    def not_valid_tile(self, row, col):
        # fixme
        if row > self.width - 1 or row < 0:
            return True
        if col > self.height - 1 or col < 0:
            return True

    def create_board_from_data(self):
        """
        NOTE: This should be the only function where the board grid is accessed directly.
        From everywhere else, only get_tile() should be used.

        Returns:
            board (2D list of Tile): 2D representation of the board using instances of Tile.
        """
        board = []
        height, width = self.height, self.width
        # creates board of empty Tile objects
        for i in range(height):
            row = []
            for j in range(width):
                # init empty board
                tile = Tile()
                row.append(tile)
            board.append(row)

        # encode snakes into board by setting Tile object type to 'snake'
        for s_id, snake in self.snakes.items():
            for index, coord in enumerate(snake.coords):
                x, y = coord['x'], coord['y']
                at_head, at_tail = (index == 0), (index == snake.length - 1)
                if board[y][x].is_snake():
                    continue
                else:
                    board[y][x].set_tile_type(dict(
                        type='snake',
                        snake_id=s_id,
                        head=at_head,
                        tail=at_tail,
                        til_empty=snake.length - index
                    ))
        for f in self.food:
            x, y = f['x'], f['y']
            board[y][x].set_tile_type(dict(type='food'))
        return board

    def get_pos_from_move(self, cur_pos, move):
        if isinstance(cur_pos, dict):
            col, row = cur_pos['x'], cur_pos['y']
        else:
            col, row = cur_pos[0], cur_pos[1]

        if move == 'up' and row - 1 >= 0:
            return col, row - 1
        elif move == 'down' and row + 1 < self.height:
            return col, row + 1
        elif move == 'left' and col - 1 >= 0:
            return col - 1, row
        elif move == 'right' and col + 1 < self.width:
            return col + 1, row
        # None indicates that move is out of bounds

    def print_til_empty(self):
        for i in range(self.height):
            row = ''
            for j in range(self.width):
                tile_data = self.get_tile(j, i).get_tile_data()
                if 'til_empty' not in tile_data:
                    row += '  |'
                else:
                    row += str(tile_data['til_empty']) + ' |'
            print(row)
            print('-' * self.width)

    def print_board(self):
        for i in range(self.height):
            row = ''
            for j in range(self.width):
                space_val = str(self.get_tile(j, i))
                if space_val == 'e':
                    row += '  |'
                else:
                    row += (str(self.get_tile(j, i))) + ' |'
            print(row)
            print('-' * self.width)
