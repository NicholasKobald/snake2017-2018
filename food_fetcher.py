from gameObjects import *
from shared import *

def pick_move_to_food(data):
    snake_dict = create_snake_dict(data['snakes'])
    board = Board(data['height'], data['width'], snake_dict, data['food'])

    # get our snake's head coords
    snake_id = data['you']
    snake_coords = get_head_coords(snake_dict[snake_id])
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
