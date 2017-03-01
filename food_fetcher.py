from gameObjects import *
from shared import *

import random


DEBUG = True

def pick_move_to_food(data, board, snake_dict):
    my_snake_id = data['you']
    snake_coords = get_head_coords(snake_dict[my_snake_id])
    x, y = snake_coords[0], snake_coords[1]

    valid_moves = board.get_valid_moves(x, y, data['ate_last_turn'])

    losing_head_collisions = board.find_losing_head_collisions(x, y, my_snake_id, snake_dict, data['ate_last_turn'])

    # TODO add a better heuristic for choosing which dangerous move to make
    # --> e.g. consider whether other snake might move to other food instead
    for dangerous_move in losing_head_collisions:
        if len(valid_moves) <= 1:
            break
        valid_moves.remove(dangerous_move)

    moves_to_food = find_best_moves_to_food(data, board, valid_moves, snake_dict)
    
    candidate_move = moves_to_food[0]
    new_head = get_pos_from_move([x, y], candidate_move)
    section_size = count_reachable(board, new_head)
    if section_size < len(snake_dict[my_snake_id]['coords']) + board.width/2:
        best = -50000
        for move in valid_moves:
            new_head = get_pos_from_move([x, y], move)
            section_size = count_reachable(board, new_head)
            if section_size>best:
                best = section_size
                alt_move = move

        return alt_move
    return moves_to_food[0]

# returns a list ordered by BEST->2nd-BEST moves towards food
# favours moves that approach most of: nearest cluster, largest cluster, nearest food
def find_best_moves_to_food(data, board, valid_moves, snake_dict):
    my_snake_id = data['you']
    snake_coords = get_head_coords(snake_dict[my_snake_id])
    x, y = snake_coords[0], snake_coords[1]

    food_by_closest_snakes = find_closest_snakes(board, data['food'], snake_dict)
    moves_to_food = group_nearest_food_by_moves(x, y, my_snake_id, valid_moves, food_by_closest_snakes)

    moves_to_biggest_clusters = prefer_biggest_food_clusters(moves_to_food)
    moves_to_nearest_clusters = prefer_nearby_food_clusters(moves_to_food)
    moves_to_closest_food = prefer_nearest_food(moves_to_food)

    most_pop_moves, second_pop_moves = [], []
    highest_pop_count, second_pop_count = 0, 0
    for move in valid_moves:
        pop_count = 0
        if move in moves_to_biggest_clusters:
            pop_count += 1
        if move in moves_to_nearest_clusters:
            pop_count += 1
        if move in moves_to_closest_food:
            pop_count += 1

        if pop_count > highest_pop_count:
            # bump 1st down to 2nd place
            assert (highest_pop_count > second_pop_count or highest_pop_count == 0)
            second_pop_count = highest_pop_count
            second_pop_moves = most_pop_moves
            highest_pop_count = pop_count
            most_pop_moves = [move]
        elif pop_count == highest_pop_count:
            most_pop_moves.append(move)
        elif pop_count > second_pop_count:
            second_pop_count = pop_count
            second_pop_moves = [move]
        elif pop_count == second_pop_count:
            second_pop_moves.append(move)
    return (most_pop_moves + second_pop_moves)
