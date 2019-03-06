from app import shared
from app.food_fetcher import find_path_out
from app.objects import snake
import app.objects.board as Board
import tests.fixtures as fixtures

import unittest


class TestPathFinding(unittest.TestCase):
    def test_find_two_paths_out(self):
        game_data, valid_moves, safe_moves, _ = fixtures.get_data_with_two_ways_out()
        board_data = game_data['board']
        my_snake_id = game_data['you']['id']

        snakes = {
            s['id']: snake.Snake(s['id'], s['body'], s['health'], False)
            for s in board_data['snakes']
        }
        board = Board.Board(
            board_data['height'],
            board_data['width'],
            snakes,
            board_data['food'],
            my_snake_id,
        )

        x, y = snakes[my_snake_id].head
        max_length = shared.get_max_snake_length(snakes)

        moves_with_valid_paths_out = []
        for move in valid_moves:
            possible_head = board.get_pos_from_move((x, y), move)
            if find_path_out(board, possible_head, 1, max_length, set(), 0):
                moves_with_valid_paths_out.append(move)
        self.assertEqual(
            safe_moves,
            moves_with_valid_paths_out,
            "Failed to find exactly the moves with paths out.",
        )

    def test_find_one_path_out(self):
        game_data, valid_moves, safe_moves, _ = fixtures.get_data_with_one_way_out()
        board_data = game_data['board']
        my_snake_id = game_data['you']['id']

        snakes = {
            s['id']: snake.Snake(s['id'], s['body'], s['health'], False)
            for s in board_data['snakes']
        }
        board = Board.Board(
            board_data['height'],
            board_data['width'],
            snakes,
            board_data['food'],
            my_snake_id,
        )

        x, y = snakes[my_snake_id].head
        max_length = shared.get_max_snake_length(snakes)

        moves_with_valid_paths_out = []
        for move in valid_moves:
            possible_head = board.get_pos_from_move((x, y), move)
            if find_path_out(board, possible_head, 1, max_length, set(), 0):
                moves_with_valid_paths_out.append(move)
        self.assertEqual(
            safe_moves,
            moves_with_valid_paths_out,
            "Failed to find exactly the moves with paths out.",
        )
