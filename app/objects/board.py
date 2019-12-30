TILE_DEBUG = True


class Tile(object):

    def __init__(self, x, y, board, is_food=False, snake_id=None, is_head=False, is_tail=False, til_empty=0):
        self.col = x
        self.row = y
        self.board = board
        self.is_food = is_food
        self.snake_id = snake_id
        self.is_head = is_head
        self.is_tail = is_tail
        self.til_empty = til_empty
        self.is_empty = not is_food and snake_id == None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.is_food:
            return "f"
        elif self.is_head:
            return "h"
        elif self.is_tail:
            return "t"
        elif self.is_snake():
            return "s"
        elif self.is_safe():
            return " "
        else:
            return "?"

    def safe_in_the_future(self, num_turns_in_future, num_times_eaten, us_id):
        if self.is_snake() and self.snake_id == us_id:
            num_turns_until_safe = self.turns_til_safe() + num_times_eaten
        else:
            num_turns_until_safe = self.turns_til_safe()
        return num_turns_until_safe <= num_turns_in_future

    def is_safe(self):
        if self.is_tail:
            return self.board.snakes[self.snake_id].ate_last_turn
        else:
            return not self.is_snake()

    def is_snake(self):
        return self.snake_id is not None

    def turns_til_safe(self):
        if not self.is_snake():
            return 0

        s = self.board.snakes.get(self.snake_id)
        if s is not None and s.ate_last_turn:
            return self.til_empty
        else:
            return self.til_empty - 1


class Board(object):

    def __init__(self, height, width, snakes, food, my_snake_id):
        """
        Params:
            height (int): of board.
            width (int): of board.
            snakes (dict): IDs and locations of snakes.
            food (2D list): coords of food.
            my_snake_id (str): ID of our snake.
        """
        self.height = height
        self.width = width
        self.snakes = snakes
        self.my_snake_id = my_snake_id
        self.food = food
        self.board = self.populate_board()

    def __repr__(self):
        return __str__()

    def __str__(self):
        """
        e.g.
        Key:
        - other-3: 1
        - other-2: 2
        - other-1: 3
        - snake-id-string: 4
        0  1  2  3  4  5  6  7  8  9  10
        |  |  |  |  |  |  |  |  |  |  |  | 0
        |  |  |  |  |  |  |  |  |f |  |  | 1
        |  |  |  |  |  |  |  |  |  |  |  | 2
        |  |  |2 |h |  |h |  |  |  |  |  | 3
        |2 |2 |2 |  |  |1 |  |t |  |  |  | 4
        |2 |2 |2 |2 |t |1 |1 |1 |  |  |  | 5
        |3 |t |h |4 |  |1 |1 |  |  |  |  | 6
        |3 |3 |  |4 |4 |  |  |  |  |  |  | 7
        |f |3 |3 |  |4 |4 |4 |  |  |  |  | 8
        |  |  |3 |h |t |4 |4 |  |  |  |  | 9
        |  |  |  |  |  |  |  |  |  |  |  | 10
        """
        # arbitrarily map ints [0, number of snakes] to the snakes to make board str more readable
        snake_nums = {snake_id: i+1 for i, snake_id in enumerate(self.snakes.keys())}
        board_str = "Key: \n- " + "\n- ".join([f"{snake_id}: {num}" for snake_id, num in snake_nums.items()]) + "\n"
        board_str += "".join([f" {col_num} " for col_num in range(self.width)]) + "\n"
        for row_num, row in enumerate(self.board):
            for tile in row:
                if tile.is_snake() and not tile.is_head and not tile.is_tail:
                    board_str += "|" + str(snake_nums[tile.snake_id]) + " "
                else:
                    board_str += "|" + str(tile) + " "
            board_str += f"| {row_num}\n"
        return board_str

    def get_valid_moves_in_the_future(self, col, row, turns_passed, num_times_eaten):
        valid_moves = []
        us_id = self.my_snake_id

        if col < self.width - 1 and self.get_tile(col + 1, row).safe_in_the_future(turns_passed, num_times_eaten, us_id):
            valid_moves.append('right')

        if row < self.height - 1 and self.get_tile(col, row + 1).safe_in_the_future(turns_passed, num_times_eaten, us_id):
            valid_moves.append('down')

        if col > 0 and self.get_tile(col - 1, row).safe_in_the_future(turns_passed, num_times_eaten, us_id):
                valid_moves.append('left')

        if row > 0 and self.get_tile(col, row - 1).safe_in_the_future(turns_passed, num_times_eaten, us_id):
            valid_moves.append('up')

        return valid_moves

    def get_valid_moves(self, col, row):
        """Returns list of moves that will not result in instant death (wall or other snake)."""
        valid_moves = []
        if col < self.width - 1 and self.get_tile(col + 1, row).is_safe():
            valid_moves.append('right')
        if row < self.height - 1 and self.get_tile(col, row + 1).is_safe():
            valid_moves.append('down')
        if col > 0 and self.get_tile(col - 1, row).is_safe():
            valid_moves.append('left')
        if row > 0 and self.get_tile(col, row - 1).is_safe():
            valid_moves.append('up')
        return valid_moves

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
                if adj_tile is None or not adj_tile.is_head:
                    # skip if we are outside the board or we're not at a snake's head
                    continue

                enemy_snake_id = adj_tile.snake_id
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

    def populate_board(self):
        """
        NOTE: This should be the only function where the board grid is accessed directly.
        From everywhere else, only get_tile() should be used.

        Returns:
            board (2D list of Tile): 2D representation of the board using instances of Tile.
        """
        board = [[None for cols in range(self.width)] for rows in range(self.height)]
        # encode snakes into board
        for s_id, snake in self.snakes.items():
            for index, coord in enumerate(snake.coords):
                x, y = coord['x'], coord['y']
                at_head, at_tail = (index == 0), (index == snake.length - 1)

                # NOTE: we don't want to modify the current tile if we've already init'd it;
                # this happens in the first 1-2 moves of the game, when the snake is stacked on itself.
                # We should not set it as tail=True if it also contains other body parts.
                if board[y][x] is not None and board[y][x].is_snake():
                    continue
                else:
                    board[y][x] = Tile(
                        x, y, self,
                        snake_id=s_id,
                        is_head=at_head,
                        is_tail=at_tail,
                        til_empty=snake.length - index,
                    )

        for f in self.food:
            x, y = f['x'], f['y']
            board[y][x] = Tile(x, y, self, is_food=True)

        for y in range(self.height):
            for x in range(self.width):
                if board[y][x] is None:
                    board[y][x] = Tile(x, y, self)
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
        return None
