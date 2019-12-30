import sys
sys.path.extend(['.', '../'])

from app.food_fetcher import pick_move
import tests.fixtures as fixtures

import unittest


class TestBasicSafety(unittest.TestCase):
    def test_prefer_head_collision_over_wall(self):
        data, only_valid_move = fixtures.get_data_with_one_valid_move()
        board_data = data['board']

        # assume that the one other snake ate
        if board_data['snakes'][0] == data['you']['id']:
            other_snake = board_data['snakes'][1]
        else:
            other_snake = board_data['snakes'][0]
        other_snake_head = other_snake['body'][0]
        prev_foods = [{"x": other_snake_head['x'], "y": other_snake_head['y']}]
        mock_game_data_cache = fixtures.get_mock_game_data_cache(data['game']['id'], prev_foods)

        move = pick_move(
            board_data['height'],
            board_data['width'],
            board_data['snakes'],
            board_data['food'],
            data['you']['id'],
            data['game']['id'],
            mock_game_data_cache,
        )
        self.assertEqual(move, only_valid_move, "Failed to choose only valid move.")


    def test_avoids_dead_end(self):
        data, _, _, best_move = fixtures.get_data_with_one_way_out()
        move = pick_move(
            data['board']['height'],
            data['board']['width'],
            data['board']['snakes'],
            data['board']['food'],
            data['you']['id'],
            data['game']['id'],
            fixtures.get_empty_mock_game_data_cache(),
        )

        self.assertEqual(move, best_move, "Failed to choose best move.")

    def test_prefers_move_away_from_snake(self):
        data, _, _, best_move = fixtures.get_data_with_two_ways_out()

        move = pick_move(
            data['board']['height'],
            data['board']['width'],
            data['board']['snakes'],
            data['board']['food'],
            data['you']['id'],
            data['game']['id'],
            fixtures.get_empty_mock_game_data_cache(),
        )

        self.assertEqual(move, best_move, "Failed to choose best move.")

class TestAdvancedSafety(unittest.TestCase):
    def test_prefer_larger_component(self):
        data, best_move, _ = fixtures.get_data_with_one_big_component()

        move = pick_move(
            data['board']['height'],
            data['board']['width'],
            data['board']['snakes'],
            data['board']['food'],
            data['you']['id'],
            data['game']['id'],
            fixtures.get_empty_mock_game_data_cache(),
        )

        self.assertEqual(move, best_move, "Failed to choose move towards big component.")
