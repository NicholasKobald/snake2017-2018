import sys

sys.path.extend(['.', '..'])

import main
import objects
import tests.fixtures as fixtures
import unittest

from food_fetcher import find_snakes_that_just_ate
from shared import create_snake_dict

class TestBasicSafety(unittest.TestCase):
    def test_avoids_dead_end(self):
        game_data, _, _, best_move = fixtures.get_data_with_one_way_out()
        board_data = game_data['board']

        snake_dict = create_snake_dict(board_data['snakes'])
        board = objects.Board(
            board_data['height'],
            board_data['width'],
            snake_dict,
            board_data['food'],
            game_data['you']['id'],
        )

        # should result in an empty list
        game_data['ate_last_turn'] = find_snakes_that_just_ate(board_data, [], board)

        move = main.pick_move(game_data, board, snake_dict)
        self.assertEqual(move, best_move, "Failed to choose best move.")

    def test_prefers_move_away_from_snake(self):
        game_data, _, _, best_move = fixtures.get_data_with_two_ways_out()
        board_data = game_data['board']

        snake_dict = create_snake_dict(board_data['snakes'])
        board = objects.Board(
            board_data['height'],
            board_data['width'],
            snake_dict,
            board_data['food'],
            game_data['you']['id'],
        )

        # should result in an empty list
        game_data['ate_last_turn'] = find_snakes_that_just_ate(board_data, [], board)

        move = main.pick_move(game_data, board, snake_dict)
        self.assertEqual(move, best_move, "Failed to choose best move.")
