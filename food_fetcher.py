from gameObjects import *
from shared import *

def pick_move_to_food(data):
    board = Board(data['height'], data['width'], data['snakes'], data['food'])

    # get our snake's head coords
    snake_id = data['you']
    snake_coords = get_head_coords(get_snake(snake_id, data['snakes']))
    x, y = snake_coords[0], snake_coords[1]

    # find safe moves first
    valid_moves = board.get_valid_moves(x, y)

    # find distances from snake head to each food bit
    food_dict_by_shortest_path = get_shortest_path_for_each(x, y, board, data['food'])

    # find move towards food
    move_towards_food = get_safe_move_to_nearest_food(x, y, valid_moves, food_dict_by_shortest_path)
    if move_towards_food == None:
        # TODO add more intelligent behavior (not just pick some valid move)
        move = valid_moves[0]
    else:
        move = move_towards_food
    return move
