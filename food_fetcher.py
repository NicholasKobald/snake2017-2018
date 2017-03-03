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

    moves_prioritized_by_food = prioritize_moves_by_food(start_time, data, board, valid_moves, snake_dict)
    print "ALL FOOD TIME:", get_latency(start_time), "ms"

    print "moves before count_reachable:", moves_prioritized_by_food
    remove_unsafe_components(moves_prioritized_by_food, snake_coords, board,
                             len(snake_dict[my_snake_id]['coords']))
    print "moves after count_reachable:", moves_prioritized_by_food
    print "SAFE COMPONENT TIME:", get_latency(start_time), "ms"
    return moves_prioritized_by_food[0]

def remove_unsafe_components(moves, snake_coords, board, snake_len):
    unsafe_moves = []
    smallest_component_size = float('inf')
    largest_component_size = float('-inf')
    preferred_move = None
    for move in moves:
        new_head = get_pos_from_move(snake_coords, move)
        component_size = count_reachable(board, new_head)
        if component_size < snake_len: # this is a dead end!
            if component_size > largest_component_size:
                largest_component_size = component_size
                preferred_move = move
            if component_size < smallest_component_size:
                smallest_component_size = component_size
                unsafe_moves.insert(0, move)
            else:
                unsafe_moves.append(move)
    if preferred_move != None and preferred_move not in unsafe_moves:
        unsafe_moves.append(preferred_move) # never removed
    # notice: order of move removal corresponds to the order of move insertion
    for unsafe_move in unsafe_moves:
        if len(moves) == 1: break # leave at least 1 move
        moves.remove(unsafe_move)

def remove_losing_ties_by_snake_len(board, my_snake_id, food_info_list):
    to_remove = []
    for food_info in food_info_list:
        if confirm_closest(board, my_snake_id, food_info['tied_with']):
            continue
        else:
            to_remove.append(food_info)
    print "* checked ties for snake length"
    for elem in to_remove:
        food_info_list.remove(elem)
        print "* removed:", elem
    return food_info_list

# returns a list ordered by BEST->2nd-BEST moves towards food
# favours moves that approach most of: nearest cluster, largest cluster, nearest food
def prioritize_moves_by_food(start_time, data, board, valid_moves, snake_dict):
    my_snake_id = data['you']
    snake_coords = get_head_coords(snake_dict[my_snake_id])
    x, y = snake_coords[0], snake_coords[1]

    closest_food_and_snakes = find_closest_snakes(board, data['food'], snake_dict)
    print "SNAKES TO FOOD BFS TIME:", get_latency(start_time), "ms"
    snakes_by_food = closest_food_and_snakes['by_dest']
    foods_by_snake = closest_food_and_snakes['by_snake']

    if my_snake_id not in foods_by_snake:
        # TODO IMPLEMENT LOGIC FOR NO NEAR FOOD!!
        return valid_moves

    food_info_dict = foods_by_snake[my_snake_id]
    food_info_dict['dest_info'] = remove_losing_ties_by_snake_len(
                                        board, my_snake_id,
                                        food_info_dict['dest_info'])

    moves_to_food = group_nearest_food_by_moves(valid_moves, food_info_dict)
    print "GROUP FOOD BY MOVE TIME:", get_latency(start_time), "ms"

    moves_to_biggest_clusters = prefer_biggest_food_clusters(moves_to_food)
    print "BIG CLUSTER FOOD TIME:", get_latency(start_time), "ms"
    moves_to_nearest_clusters = prefer_nearby_food_clusters(moves_to_food)
    print "NEAR CLUSTER FOOD TIME:", get_latency(start_time), "ms"
    moves_to_closest_food = prefer_nearest_food(moves_to_food)
    print "NEAR BIT FOOD TIME:", get_latency(start_time), "ms"
    return prioritize_valid_moves(valid_moves, moves_to_biggest_clusters,
        moves_to_nearest_clusters, moves_to_closest_food)

def prioritize_valid_moves(valid_moves, to_big_clusters,
                           to_near_clusters, to_close_food):
    num_occurrences = [[], [], [], []]
    for move in valid_moves:
        pop_count = 0
        if move in to_big_clusters: pop_count += 1
        if move in to_near_clusters: pop_count += 1
        if move in to_close_food:     pop_count += 1
        priority_index = (pop_count * (-1)) - 1
        num_occurrences[priority_index].append(move)

    most_occur_first = []
    for moves in num_occurrences:
        most_occur_first += moves
    return most_occur_first
