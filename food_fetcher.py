from gameObjects import *
from shared import *

import random


DEBUG = True

def pick_move_to_food(data, board, snake_dict):
    # get our snake's head coords
    snake_id = data['you']
    snake_coords = get_head_coords(snake_dict[snake_id])
    x, y = snake_coords[0], snake_coords[1]

    # find safe moves first
    valid_moves = board.get_valid_moves(x, y, data['ate_last_turn'])
    losing_head_collisions = board.find_losing_head_collisions(x, y, snake_id, snake_dict, data['ate_last_turn'])

    for dangerous_move in losing_head_collisions:
        if len(valid_moves) > 1:
            valid_moves.remove(dangerous_move)
        else:
            break

    # find distances from snake head to each food bit
    food_dict_by_shortest_path = get_shortest_path_for_each(x, y, board, data['food'])

    # find move towards food
    move_towards_food = get_safe_move_to_nearest_food(x, y, valid_moves, food_dict_by_shortest_path)


    if move_towards_food == None:
        move_towards_food = random.choice(valid_moves)

    new_head = get_pos_from_move([x, y], move_towards_food)
    section_size = count_reachable(board, new_head)
    #WOAH TOO risky
    if section_size < len(snake_dict[snake_id]['coords']):
        best = -5000
        for move in valid_moves:
            new_head = get_pos_from_move([x, y], move)
            section_size = count_reachable(board, new_head)
            if section_size>best:
                best = section_size
                alt_move = move

        return alt_move

    return move_towards_food

def evaluate_safety(move, board, snake_dict):
    pass
