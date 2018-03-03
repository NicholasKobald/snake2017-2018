from time import time

from shared import *  # fixme


def pick_move_to_food(data, board, snake_dict):
    my_snake_id = data['you']['id']
    ate_last_turn = data.get('ate_last_turn', [])
    # get our head coordinates
    x, y = get_head_coords(snake_dict[my_snake_id])
    valid_moves = board.get_valid_moves(x, y, ate_last_turn)
    print("valid moves:", valid_moves)
    losing_head_collisions = board.find_losing_head_collisions(x, y, my_snake_id, snake_dict, data.get('ate_last_turn', []))
    prioritized_moves = prioritize_moves_by_food(data, board, valid_moves, snake_dict, my_snake_id)
    if prioritized_moves is None:
        snake_coords = get_head_coords(snake_dict[my_snake_id])
        prioritized_moves = prioritize_moves_backup(valid_moves, snake_coords, board.width,
                                                    board.height, board)

    prioritized_unfatal_moves = [p for p in prioritized_moves if p not in losing_head_collisions]
    prioritized_potentially_fatal_moves = [p for p in prioritized_moves if p]
    potentially_fatal = False

    if not prioritized_unfatal_moves:
        potentially_fatal = True
        prioritized_unfatal_moves = prioritized_potentially_fatal_moves
    # if we have not valid moves
    if not prioritized_unfatal_moves:
        return 'left'

    max_length = get_max_snake_length(snake_dict)
    moves_with_valid_paths_out = []
    if not potentially_fatal:
        mark_dangerous_tiles(board, snake_dict, ate_last_turn, my_snake_id)

    limit = 4
    move_to_options = dict()

    conservative_start = time()
    if not potentially_fatal:
        threat_level = 3
        while not moves_with_valid_paths_out:
            threat_level = threat_level - 1
            for move in prioritized_unfatal_moves:
                possible_head = board.get_pos_from_move((x, y), move)
                if find_conservative_path_out(board, possible_head, 1, max_length, set(), 0, threat_level):
                    moves_with_valid_paths_out.append(move)

            if threat_level == 1:
                break


    conservative_end = time()
    print("Spent", (conservative_end - conservative_start), "seconds determining conservative paths")


    safe_paths = time()
    if not moves_with_valid_paths_out:
        for move in prioritized_unfatal_moves:
            possible_head = board.get_pos_from_move((x, y), move)
            if find_path_out(board, possible_head, 1, max_length, set(), 0):
                moves_with_valid_paths_out.append(move)

    safe_end = time()
    print("Spent", (safe_end - safe_paths), "seconds determining just safe paths")

    enumerate_paths_start = time()
    for move in moves_with_valid_paths_out:
        possible_head = board.get_pos_from_move((x, y), move)
        num_paths = count_number_of_paths_out_from_move(board, possible_head, 2, limit + 2, set(), 0)
        move_to_options[move] = num_paths
    enumerate_end = time()
    print("Spent", (enumerate_end - enumerate_paths_start) , "seconds enumerating the all-paths heuristic")


    if moves_with_valid_paths_out:
        move_to_options_with_path = {k: v for k, v in move_to_options.items() if k in moves_with_valid_paths_out}
        max_val = max(list(move_to_options_with_path.values()))
        first_choice_val = move_to_options_with_path[moves_with_valid_paths_out[0]]

        # if the improvement is less than some %, go with the food option
        food_bonus = (snake_dict[my_snake_id]['health'] * 1.0) / 100
        improvement = 1.0 - (first_choice_val * 1.0) / max_val
        if food_bonus < 0.3:
            improvement = improvement - 0.2
        elif food_bonus < 0.2:
            improvement = improvement - 0.4
        elif food_bonus < 0.1:
            improvement = improvement - 0.6
        elif food_bonus < 0.05:
            improvement = 0

        max_key = max(move_to_options_with_path, key=lambda k: move_to_options_with_path[k])
        if improvement < 0.70:
            return moves_with_valid_paths_out[0]
        else:
            return max_key

    for move in prioritized_potentially_fatal_moves:
        print("Potentially fatal move:", move)
        possible_head = board.get_pos_from_move((x, y), move)
        if find_path_out(board, possible_head, 1, max_length, set(), 0):
            return move # just do it

    # no path existed so, maybe a risky move is the right choice?
    if prioritized_potentially_fatal_moves:
        print("Selecting largest componenent cause no path out")
        move_to_size = dict()
        for move in prioritized_unfatal_moves:
            possible_head = board.get_pos_from_move((x, y), move)
            component_size = count_reachable(board, possible_head)
            move_to_size[move] = component_size
        max_key = max(move_to_size, key=lambda k: move_to_size[k])
        return max_key
    else:
        return 'right' # go right!
        # raise Exception("HELP US")


def find_path_out(board, head, moves_elapsed, max_snake_length, visited, num_times_eaten):
    # print('at depth:', moves_elapsed)
    visited.add(head)
    if board.get_tile(head[0], head[1]).is_food():
        num_times_eaten += 1

    if moves_elapsed == max_snake_length + 1:  # it's a brand new world
        return True

    valid_moves = board.get_valid_moves_in_the_future(head[0], head[1], moves_elapsed, num_times_eaten)
    if not valid_moves:
        return False

    for move in valid_moves:
        new_pos = board.get_pos_from_move(head, move)
        if new_pos not in visited and find_path_out(board, new_pos, moves_elapsed + 1, max_snake_length, visited, num_times_eaten):
            return True

    return False


def count_number_of_paths_out_from_move(board, head, moves_elapsed, limit, visited, num_times_eaten):
    # print('at depth:', moves_elapsed)
    visited.add(head)
    if board.get_tile(head[0], head[1]).is_food():
        num_times_eaten += 1

    if moves_elapsed == limit:  # it's a brand new world
        visited.remove(head)
        return 1

    valid_moves = board.get_valid_moves_in_the_future(head[0], head[1], moves_elapsed, num_times_eaten)

    total_moves_from_here = 0
    for move in valid_moves:
        new_pos = board.get_pos_from_move(head, move)
        total_moves_from_here += count_number_of_paths_out_from_move(board, new_pos, moves_elapsed + 1, limit, visited, num_times_eaten)

    try:
        visited.remove(head)
    except:
        pass
    return total_moves_from_here


def find_conservative_path_out(board, head, moves_elapsed, max_snake_length, visited, num_times_eaten, threat_level):
    # print('at depth:', moves_elapsed)
    visited.add(head)
    if board.get_tile(head[0], head[1]).is_food():
        num_times_eaten += 1

    if moves_elapsed == max_snake_length + 1:  # it's a brand new world
        return True

    valid_moves = board.get_valid_moves_in_the_future(head[0], head[1], moves_elapsed, num_times_eaten)
    if not valid_moves:
        return False

    for move in valid_moves:
        new_pos = board.get_pos_from_move(head, move)
        tile_data = board.get_tile(new_pos[0], new_pos[1]).data
        if 'threatened' not in tile_data or ('threatened' in tile_data and tile_data['threatened'] < threat_level):
            if new_pos not in visited and find_conservative_path_out(board, new_pos, moves_elapsed + 1, max_snake_length, visited, num_times_eaten, threat_level):
                return True

    return False


def mark_dangerous_tiles(board, snake_dict, ate_last_turn, our_snake_id):
    """Mark tiles around other snakes' heads as dangerous by mutating the board object.

    board[x][y] = Tile({
        ...
        'threatened_length': 10, # length of snake that is threatening us
        'threatened': 2,
        ...
    })

    Returns:
        killer_moves: list of moves e.g. ['left', 'right']
            moves that would kill another snake immediately (if they moved to the same tile that we do)
    """
    for s_id, snake in snake_dict.items():
        if s_id != our_snake_id:
            point = snake['coords'][0]
            x, y = point['x'], point['y']
            valid_moves = board.get_valid_moves(x, y, ate_last_turn)
            for move in valid_moves:
                head_x, head_y = board.get_pos_from_move((x, y), move)
                board.get_tile(head_x, head_y).data['threatened_length'] = snake['length'] # TODO this..
                board.get_tile(head_x, head_y).data['threatened'] = 1
                valid_followup_moves = board.get_valid_moves(head_x, head_y)
                for followup_move in valid_followup_moves:
                    head_x2, head_y2 = board.get_pos_from_move((head_x, head_y), followup_move)
                    if 'threatened' not in board.get_tile(head_x2, head_y2).data:
                        board.get_tile(head_x2, head_y2).data['threatened'] = 2

    us = snake_dict[our_snake_id]
    point = us['coords'][0]
    x, y = point['x'], point['y']
    killer_moves = []
    valid_moves = board.get_valid_moves(x, y, ate_last_turn)
    for move in valid_moves:
        head_x, head_y = board.get_pos_from_move((x, y), move)
        if 'threatened_length' in board.get_tile(head_x, head_y).data:
            if board.get_tile(head_x, head_y).data['threatened_length'] < us['length']:
                # if we can kill them, don't run away. be strong.
                killer_moves.append(move)
                del board.get_tile(head_x, head_y).data['threatened']

    return killer_moves


def print_marked_dangerous(board):

    for i in range(board.height):
        for j in range(board.width):
            print("X" if 'threatened' in board.get_tile(j, i).data else ".", end='')
        print()

    for i in range(board.height):
        for j in range(board.width):
            if 'threatened' in board.get_tile(j, i).data:
                print("x:", i, "y:", j)



# prefer moves that move us to the centre
def prioritize_moves_backup(valid_moves, snake_head_coords, board_width, board_height, board):
    preferred_moves, other_moves = [], []
    centre_x, centre_y = (board_width / 2) - 1, (board_height / 2) - 1
    max_dist_to_centre = abs(snake_head_coords[0] - centre_x) + abs(snake_head_coords[1] - centre_y)
    for move in valid_moves:
        pos = board.get_pos_from_move(snake_head_coords, move)
        dist_to_centre = abs(pos[0] - centre_x) + abs(pos[1] - centre_y)
        if dist_to_centre < max_dist_to_centre:
            preferred_moves.append(move)
        else:
            other_moves.append(move)
    prioritized_moves = preferred_moves + other_moves
    return prioritized_moves


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
    closest_food_and_snakes = find_closest_snakes(board, data['food']['data'])
    foods_by_snake = closest_food_and_snakes['by_snake']

    # we aren't the closest to anything
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
