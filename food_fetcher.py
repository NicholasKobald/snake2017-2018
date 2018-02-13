from shared import *


def pick_move_to_food(data, board, snake_dict):
    my_snake_id = data['you']['id']

    # get our head coordinates
    x, y = get_head_coords(snake_dict[my_snake_id])
    valid_moves = board.get_valid_moves(x, y, data.get('ate_last_turn', []))

    # TODO add a better heuristic for choosing which dangerous move to make
    # --> e.g. consider whether other snake might move to other food instead
    # for dangerous_move in losing_head_collisions:
    #    if len(valid_moves) <= 1: break
    #    if dangerous_move in valid_moves: valid_moves.remove(dangerous_move)

    prioritized_moves = prioritize_moves_by_food(data, board, valid_moves, snake_dict, my_snake_id)
    if prioritized_moves is None:
        snake_coords = get_head_coords(snake_dict[my_snake_id])
        prioritized_moves = prioritize_moves_backup(valid_moves, snake_coords, board.width, board.height)

    size_and_move = []
    for move in prioritized_moves:
        possible_head = get_pos_from_move((x, y), move)
        component_size = count_reachable(board, possible_head)
        size_and_move.append((move, component_size))

    if size_and_move[0][1] < len(snake_dict[my_snake_id]['coords']):
        fallback = max(size_and_move, key=lambda v: v[1])
        print("Selected fallback!!")
        return fallback[0]

    return prioritized_moves[0]


def has_path_out(board, cur_pos, path_len, visited):
    valid_moves = board.get_valid_moves(cur_pos[0], cur_pos[1])
    if has_open_adj_tile(board, path_len, cur_pos):
        return True

    for move in valid_moves:
        new_pos = board.get_pos_from_move(cur_pos, move)
        if new_pos not in visited:
            visited.add(new_pos)
            return has_path_out(board, new_pos, path_len + 1, visited)
    return False


def has_open_adj_tile(board, path_len, cur_pos):
    adj_tiles = []
    for move in ['up', 'down', 'left', 'right']:
        pos = board.get_pos_from_move(cur_pos, move)
        if pos is not None:
            tile = board.get_tile(pos[0], pos[1])
            adj_tiles.append(tile)
    for tile in adj_tiles:
        l_bound = tile.turns_till_safe()
        if 0 < l_bound < path_len + 1:
            return True
    return False


# prefer moves that move us to the centre
def prioritize_moves_backup(valid_moves, snake_head_coords, board_width, board_height):
    preferred_moves, other_moves = [], []
    centre_x, centre_y = (board_width / 2) - 1, (board_height / 2) - 1
    max_dist_to_centre = abs(snake_head_coords[0] - centre_x) + abs(snake_head_coords[1] - centre_y)
    for move in valid_moves:
        pos = get_pos_from_move(snake_head_coords, move)
        dist_to_centre = abs(pos[0] - centre_x) + abs(pos[1] - centre_y)
        if dist_to_centre < max_dist_to_centre:
            preferred_moves.append(move)
        else:
            other_moves.append(move)
    prioritized_moves = preferred_moves + other_moves
    return prioritized_moves


def remove_moves_to_unsafe_components(moves, snake_coords, board, snake_len):
    unsafe_moves = []
    smallest_component_size = float('inf')
    largest_component_size = float('-inf')
    preferred_move = None
    for move in moves:
        new_head = get_pos_from_move(snake_coords, move)
        component_size = count_reachable(board, new_head)
        if component_size < snake_len:  # this is a dead end!
            if component_size > largest_component_size:
                largest_component_size = component_size
                preferred_move = move
            if component_size < smallest_component_size:
                smallest_component_size = component_size
                unsafe_moves.insert(0, move)
            else:
                unsafe_moves.append(move)
    if preferred_move is not None and preferred_move not in unsafe_moves:
        unsafe_moves.append(preferred_move)  # never removed

    # order of move removal corresponds to the order of move insertion
    for unsafe_move in unsafe_moves:
        if len(moves) == 1:
            break  # leave at least 1 move
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


def prioritize_moves_by_food(data, board, valid_moves, snake_dict, my_snake_id):
    """
    returns: 
        (1) permuted valid_moves prioritized best->worst
        (2) None if no foods are closest to us
     favours moves that approach most of: nearest cluster, largest cluster, nearest food
    """

    snake_coords = get_head_coords(snake_dict[my_snake_id])

    closest_food_and_snakes = find_closest_snakes(board, data['food']['data'])
    foods_by_snake = closest_food_and_snakes['by_snake']

    if my_snake_id not in foods_by_snake:
        return None

    food_info_dict = foods_by_snake[my_snake_id]
    food_info_dict['dest_info'] = remove_losing_ties_by_snake_len(
        board, my_snake_id,
        food_info_dict['dest_info'])

    moves_to_food = group_nearest_food_by_moves(valid_moves, food_info_dict)
    moves_to_biggest_clusters = prefer_biggest_food_clusters(moves_to_food)
    moves_to_nearest_clusters = prefer_nearby_food_clusters(moves_to_food)
    moves_to_closest_food = prefer_nearest_food(moves_to_food)
    return prioritize_valid_moves(valid_moves, moves_to_biggest_clusters,
                                  moves_to_nearest_clusters, moves_to_closest_food)


def prioritize_valid_moves(valid_moves, to_big_clusters, to_near_clusters, to_close_food):
    # create buckets for every 'tier' of move priority (where 0 is the highest priority)
    priority_buckets = [[], [], [], []]
    for move in valid_moves:
        pop_count = 0
        if move in to_big_clusters:
            pop_count += 1
        if move in to_near_clusters:
            pop_count += 1
        if move in to_close_food:
            pop_count += 1

        priority_index = (pop_count * (-1)) - 1
        priority_buckets[priority_index].append(move)

    # that's it, done.
    prioritized = sum(priority_buckets, [])
    return prioritized
