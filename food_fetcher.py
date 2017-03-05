from gameObjects import *
from shared import *
from voronoi import label_board_voronoi

import random
import time

DEBUG = True

get_latency = lambda start_time: int(round((time.time()-start_time) * 1000))

def pick_move_to_food(start_time, data, board, snake_dict):
    my_snake_id = data['you']
    our_snake_coords_len = len(snake_dict[my_snake_id]['coords'])

    snake_coords = get_head_coords(snake_dict[my_snake_id])
    x, y = snake_coords[0], snake_coords[1]

    valid_moves = board.get_valid_moves(x, y, data['ate_last_turn'])
    #print "VALID MOVES TIME:", get_latency(start_time), "ms"

    losing_head_collisions = board.find_losing_head_collisions(x, y, my_snake_id, snake_dict, data['ate_last_turn'])
    #print "HEAD COLLISIONS TIME:", get_latency(start_time), "ms"

    # TODO add a better heuristic for choosing which dangerous move to make
    # --> e.g. consider whether other snake might move to other food instead
    for dangerous_move in losing_head_collisions:
        if len(valid_moves) <= 1: break
        if dangerous_move in valid_moves: valid_moves.remove(dangerous_move)

    prioritized_moves = prioritize_moves_by_food(start_time, data, board, valid_moves, snake_dict)
    #print "ALL FOOD TIME:", get_latency(start_time), "ms"

    if prioritized_moves == None:
        prioritized_moves = prioritize_moves_backup(valid_moves, snake_coords,
                                                board.width, board.height)

    if not count_reachable_fixed(board, snake_dict[my_snake_id]['coords'][0], our_snake_coords_len):
        print "IN COMPONENT:TRIED TO MAXIMIZE TIME"
        surivival_move = find_first_move_in_path_out(board, (x,y), prioritized_moves)
        if surivival_move == None:
            return prioritized_moves[0]
        else:
            return surivival_move
        #return get_maximizing_component_size_move(board, snake_dict, snake_dict[my_snake_id])
    voronoi_data = label_board_voronoi(board, snake_dict)
    voronoi_move_info = dict() # e.g. key=move, value=component_size
    for move in prioritized_moves:
        voronoi_move_info[move] = voronoi_data[my_snake_id][move]

    cutoff = compute_cutoff(our_snake_coords_len, data['turn'], snake_dict[my_snake_id]['health_points'])
    #board.print_voronoi_board()
    #board.print_voronoi_board_moves()
    #return weight_voronoi_versus_food(board,
    #    prioritized_moves,
    #    voronoi_move_info,
    #    snake_dict[my_snake_id]['coords'][0],
    #    our_snake_coords_len
    #)

    dangerous_moves = []
    cur_min_component_size = float('inf')
    turn_coef = max(1, float(data['turn'])/100)
    turn_coef = min(3, turn_coef)
    # remove all dangerous moves intelligently
    hp_important = 100 - snake_dict[my_snake_id]['health_points']
    our_cutoff = our_snake_coords_len
    alt_move = None
    voronoi_max = float('-inf')

    candidate_move = prioritized_moves[0]

    if voronoi_move_info[candidate_move] > our_cutoff:
        return candidate_move

    for move in prioritized_moves:
        cur_val = voronoi_move_info[move]
        if cur_val > voronoi_max:
            voronoi_max = cur_val
            alt_move = move

    return alt_move



    """
    print "turn_coef is", turn_coef
    for move in prioritized_moves:
        component_size = voronoi_move_info[move]
        if component_size < our_snake_coords_len:
            if component_size < cur_min_component_size:
                print "voronoi influenced shit!"
                cur_min_component_size = component_size
                dangerous_moves.insert(0, move)
            else:
                dangerous_moves.append(move)
    for d_move in dangerous_moves:
        if len(prioritized_moves) == 1: break
        prioritized_moves.remove(d_move)

    print "RETURNING NOW", prioritized_moves[0]
    return prioritized_moves[0]
    #print "SAFE COMPONENT TIME:", get_latency(start_time), "ms"
    """

    # find first move towards exit
    #for move in prioritized_moves:
    #    if find_path_out(prioritized_moves) != None:
    #        return surivival_move


#returns one move. THE MOVE.
def weight_voronoi_versus_food(board, prioritized_moves, voronoi_data, head, my_len):
    best_food_move = prioritized_moves[0]
    size_of_best = voronoi_data[best_food_move]
    if len(prioritized_moves) == 1:
        print "RRETURNED FF MOVE."
        return prioritized_moves[0]

    best_diff = float('-inf')
    candidate_replacement = None
    for move in prioritized_moves[1:]:
        x, y= get_pos_from_move(head, move)
        tile = board.get_tile(x, y)
        if tile.is_food():
            size_of_option = voronoi_data[move]
            diff = size_of_option - size_of_best
            if diff < my_len:
                return move


    print "returned FF choice"
    return prioritized_moves[0]



def compute_cutoff(turn, snake_len, hp):
    hp_val = 5
    if hp < 10:
        hp_coef = 5
    elif hp<50:
        hp_coef = 2
    elif hp<=100:
        hp_coef = 1

    return (snake_len) + 2*hp_coef


def find_first_move_in_path_out(board, cur_pos, prioritized_moves):
    for move in prioritized_moves:
        new_pos = board.get_pos_from_move(cur_pos, move)
        visited = set()
        visited.add(cur_pos)
        visited.add(new_pos)
        if has_path_out(board, new_pos, 1, visited):
            return move
        visited.remove(cur_pos)
        visited.remove(new_pos)
    return None

def has_path_out(board, cur_pos, path_len, visited):
    valid_moves = board.get_valid_moves(cur_pos[0], cur_pos[1])
    if has_open_adj_tile(board, path_len, cur_pos):
        return True

    for move in valid_moves:
        cur_path_len = path_len
        new_pos = board.get_pos_from_move(cur_pos, move)
        if new_pos not in visited:
            visited.add(new_pos)
            return has_path_out(board, new_pos, path_len+1, visited)
    return False

def has_open_adj_tile(board, path_len, cur_pos):
    adj_tiles = []
    for move in ['up', 'down', 'left', 'right']:
        pos = board.get_pos_from_move(cur_pos, move)
        if pos != None:
            tile = board.get_tile(pos[0], pos[1])
            adj_tiles.append(tile)
    for tile in adj_tiles:
        l_bound = tile.turns_till_safe()
        if l_bound > 0 and l_bound < path_len + 1: return True
    return False


# prefer moves that near us to the centre
def prioritize_moves_backup(valid_moves, snake_coords, board_width, board_height):
    preferred_moves, other_moves = [], []
    centre_x, centre_y = (board_width/2)-1, (board_height/2)-1
    max_dist_to_centre = abs(snake_coords[0]-centre_x) + abs(snake_coords[1]-centre_y)
    for move in valid_moves:
        pos = get_pos_from_move(snake_coords, move)
        dist_to_centre = abs(pos[0]-centre_x) + abs(pos[1]-centre_y)
        if dist_to_centre < max_dist_to_centre:
            preferred_moves.append(move)
        else:
            other_moves.append(move)
    prioritized_moves = preferred_moves + other_moves
    return prioritized_moves

def get_maximizing_component_size_move(board, snake_dict, our_snake):
    head = our_snake['coords'][0]
    valid_moves = board.get_valid_moves(head[0], head[1])
    best = 0
    our_move = None
    for move in valid_moves:
        new_head = get_pos_from_move(head, move)
        val = count_reachable(board, new_head)
        if val>best:
            our_move = move
            best = val

    return our_move




def remove_moves_to_unsafe_components(moves, snake_coords, board, snake_len):
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
        if unsafe_move in moves: moves.remove(unsafe_move)

def remove_losing_ties_by_snake_len(board, my_snake_id, food_info_list):
    to_remove = []
    for food_info in food_info_list:
        if confirm_closest(board, my_snake_id, food_info['tied_with']):
            continue
        else:
            to_remove.append(food_info)
    for elem in to_remove:
        if elem in food_info_list: food_info_list.remove(elem)
    return food_info_list

# returns: (1) permuted valid_moves prioritized best->worst
#          (2) None if no foods are closest to us
# favours moves that approach most of: nearest cluster, largest cluster, nearest food
def prioritize_moves_by_food(start_time, data, board, valid_moves, snake_dict):
    my_snake_id = data['you']
    snake_coords = get_head_coords(snake_dict[my_snake_id])
    x, y = snake_coords[0], snake_coords[1]

    closest_food_and_snakes = find_closest_snakes(board, data['food'], snake_dict)
    #print "SNAKES TO FOOD BFS TIME:", get_latency(start_time), "ms"
    snakes_by_food = closest_food_and_snakes['by_dest']
    foods_by_snake = closest_food_and_snakes['by_snake']

    if my_snake_id not in foods_by_snake:
        return None

    food_info_dict = foods_by_snake[my_snake_id]
    food_info_dict['dest_info'] = remove_losing_ties_by_snake_len(
                                        board, my_snake_id,
                                        food_info_dict['dest_info'])

    moves_to_food = group_nearest_food_by_moves(valid_moves, food_info_dict)
    #print "GROUP FOOD BY MOVE TIME:", get_latency(start_time), "ms"

    moves_to_biggest_clusters = prefer_biggest_food_clusters(moves_to_food)
    #print "BIG CLUSTER FOOD TIME:", get_latency(start_time), "ms"
    moves_to_nearest_clusters = prefer_nearby_food_clusters(moves_to_food)
    #print "NEAR CLUSTER FOOD TIME:", get_latency(start_time), "ms"
    moves_to_closest_food = prefer_nearest_food(moves_to_food)
    #print "NEAR BIT FOOD TIME:", get_latency(start_time), "ms"
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
