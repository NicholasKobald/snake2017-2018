import sys
sys.path.extend(['.', '../'])

from app import main
from app.food_fetcher import find_snakes_that_just_ate
from app.shared import create_snake_dict
import app.objects.board as Board
import tests.fixtures as fixtures

import unittest


class TestBasicSafety(unittest.TestCase):
    def test_prefer_head_collision_over_wall(self):
        game_data, only_valid_move = fixtures.get_data_with_one_valid_move()
        board_data = game_data['board']
        my_snake_id = game_data['you']['id']

        snake_dict = create_snake_dict(board_data['snakes'])
        board = Board.Board(
            board_data['height'],
            board_data['width'],
            snake_dict,
            board_data['food'],
            my_snake_id,
        )

        # assume that the one other snake ate
        game_data['ate_last_turn'] = [
            snake_id for snake_id in board_data['snakes'] if snake_id != game_data['you']['id']
        ]

        move = main.pick_move(board, snake_dict, my_snake_id)
        self.assertEqual(move, only_valid_move, "Failed to choose only valid move.")


    def test_avoids_dead_end(self):
        game_data, _, _, best_move = fixtures.get_data_with_one_way_out()
        board_data = game_data['board']
        my_snake_id = game_data['you']['id']

        snake_dict = create_snake_dict(board_data['snakes'])
        board = Board.Board(
            board_data['height'],
            board_data['width'],
            snake_dict,
            board_data['food'],
            my_snake_id,
        )

        move = main.pick_move(board, snake_dict, my_snake_id)
        self.assertEqual(move, best_move, "Failed to choose best move.")

    def test_prefers_move_away_from_snake(self):
        game_data, _, _, best_move = fixtures.get_data_with_two_ways_out()
        board_data = game_data['board']
        my_snake_id = game_data['you']['id']

        snake_dict = create_snake_dict(board_data['snakes'])
        board = Board.Board(
            board_data['height'],
            board_data['width'],
            snake_dict,
            board_data['food'],
            my_snake_id,
        )

        move = main.pick_move(board, snake_dict, my_snake_id)
        self.assertEqual(move, best_move, "Failed to choose best move.")

class TestAdvancedSafety(unittest.TestCase):
    def test_prefer_larger_component(self):
        game_data, best_move = fixtures.get_data_with_one_big_component()
        board_data = game_data['board']
        my_snake_id = game_data['you']['id']

        snake_dict = create_snake_dict(board_data['snakes'])
        board = Board.Board(
            board_data['height'],
            board_data['width'],
            snake_dict,
            board_data['food'],
            my_snake_id,
        )

        move = main.pick_move(board, snake_dict, my_snake_id)
        self.assertEqual(move, best_move, "Failed to choose move towards big component.")
