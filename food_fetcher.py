from gameObjects import *
from shared import *

import random
import time

DEBUG = True

get_latency = lambda start_time: int(round((time.time()-start_time) * 1000))

def pick_move_to_food(start_time, data, board, snake_dict):
    my_snake_id = data['you']
    snake_coords = get_head_coords(snake_dict[my_snake_id])
    x, y = snake_coords[0], snake_coords[1]

    valid_moves = board.get_valid_moves(x, y, data['ate_last_turn'])
    print "VALID MOVES TIME:", get_latency(start_time), "ms"

    losing_head_collisions = board.find_losing_head_collisions(x, y, my_snake_id, snake_dict, data['ate_last_turn'])
    print "HEAD COLLISIONS TIME:", get_latency(start_time), "ms"

    # TODO add a better heuristic for choosing which dangerous move to make
    # --> e.g. consider whether other snake might move to other food instead
    for dangerous_move in losing_head_collisions:
        if len(valid_moves) <= 1:
            break
        valid_moves.remove(dangerous_move)

    moves_to_food = find_best_moves_to_food(start_time, data, board, valid_moves, snake_dict)
    print "ALL FOOD TIME:", get_latency(start_time), "ms"

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

        print "SAFE COMPONENT TIME:", get_latency(start_time), "ms"
        return alt_move
    return moves_to_food[0]

# returns a list ordered by BEST->2nd-BEST moves towards food
# favours moves that approach most of: nearest cluster, largest cluster, nearest food
def find_best_moves_to_food(start_time, data, board, valid_moves, snake_dict):
    my_snake_id = data['you']
    snake_coords = get_head_coords(snake_dict[my_snake_id])
    x, y = snake_coords[0], snake_coords[1]

    closest_food_and_snakes = find_closest_snakes(board, data['food'], snake_dict)
    print "SNAKES TO FOOD BFS TIME:", get_latency(start_time), "ms"
    snakes_by_food = closest_food_and_snakes['by_food']
    foods_by_snake = closest_food_and_snakes['by_snake']

    if my_snake_id not in foods_by_snake:
        # TODO IMPLEMENT LOGIC FOR NO NEAR FOOD!!
        return valid_moves

    food_info_list = foods_by_snake[my_snake_id]
    moves_to_food = group_nearest_food_by_moves(valid_moves, food_info_list)
    print "GROUP FOOD BY MOVE TIME:", get_latency(start_time), "ms"

    moves_to_biggest_clusters = prefer_biggest_food_clusters(moves_to_food)
    print "BIG CLUSTER FOOD TIME:", get_latency(start_time), "ms"
    moves_to_nearest_clusters = prefer_nearby_food_clusters(moves_to_food)
    print "NEAR CLUSTER FOOD TIME:", get_latency(start_time), "ms"
    moves_to_closest_food = prefer_nearest_food(moves_to_food)
    print "NEAR BIT FOOD TIME:", get_latency(start_time), "ms"

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
