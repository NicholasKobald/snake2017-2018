from shared import *  # fixme


def pick_move_to_food(data, board, snake_dict):
    my_snake_id = data['you']['id']
    ate_last_turn = data.get('ate_last_turn', [])
    # get our head coordinates
    cur_x, cur_y = get_head_coords(snake_dict[my_snake_id])
    valid_moves = board.get_valid_moves(cur_x, cur_y, ate_last_turn)
    print("valid moves:", valid_moves)
    losing_head_collisions = board.find_losing_head_collisions(cur_x, cur_y, my_snake_id, snake_dict, data.get('ate_last_turn', []))
    prioritized_moves, priority_val_per_move = prioritize_moves_by_food(data['board'], board, valid_moves, snake_dict, my_snake_id)
    if prioritized_moves == []:
        snake_coords = get_head_coords(snake_dict[my_snake_id])
        prioritized_moves = prioritize_moves_backup(
            valid_moves,
            snake_coords,
            board.width,
            board.height,
            board,
        )

    # all prioritized valid moves that aren't losing head collisions
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
    if not potentially_fatal:
        mark_dangerous_tiles(board, snake_dict, ate_last_turn, my_snake_id)

    prioritized_moves_with_path_out = []
    if not potentially_fatal:
        prioritized_moves_with_path_out = find_very_safe_moves(prioritized_unfatal_moves, board, cur_x, cur_y, max_length, ate_last_turn)
        print(f"Very safe moves: {prioritized_moves_with_path_out}")

    if not prioritized_moves_with_path_out:
        for move in prioritized_unfatal_moves:
            possible_head = board.get_pos_from_move((cur_x, cur_y), move)
            if find_path_out(board, possible_head, 1, max_length, set(), 0, ate_last_turn):
                prioritized_moves_with_path_out.append(move)
        print(f"Safe moves: {prioritized_moves_with_path_out}")

    num_paths_out_per_move = count_paths_out(board, prioritized_moves_with_path_out, cur_x, cur_y, ate_last_turn)
    if prioritized_moves_with_path_out:
        # if we are VERY hungry, move to food
        if should_eat(snake_dict, my_snake_id):
            for move in prioritized_moves_with_path_out:
                if priority_val_per_move.get(move, 0) >= 1:
                    return move

        # if we are getting hungry food, try to pick move to food
        # with number of paths above the average
        if snake_dict[my_snake_id]['health'] < 70:
            # get average number of paths
            ave_num_paths = sum(num_paths_out_per_move.values()) / len(num_paths_out_per_move.keys())
            for move in prioritized_moves_with_path_out:
                if num_paths_out_per_move[move] > ave_num_paths:
                    return move

        # if none are above average (or we're not hungry),
        # take move with most paths
        return max(
            num_paths_out_per_move,
            key=lambda k: num_paths_out_per_move[k],
        )

    for move in prioritized_potentially_fatal_moves:
        print("Potentially fatal move:", move)
        possible_head = board.get_pos_from_move((cur_x, cur_y), move)
        if find_path_out(board, possible_head, 1, max_length, set(), 0, ate_last_turn):
            return move # just do it

    # no path existed so, maybe a risky move is the right choice?
    if prioritized_potentially_fatal_moves:
        print("Selecting largest componenent cause no path out")
        move_to_size = dict()
        for move in prioritized_unfatal_moves:
            possible_head = board.get_pos_from_move((cur_x, cur_y), move)
            component_size = count_reachable(board, possible_head)
            move_to_size[move] = component_size
        max_key = max(move_to_size, key=lambda k: move_to_size[k])
        return max_key
    else:
        return 'right' # go right!
        # raise Exception("HELP US")

def should_eat(snake_dict, my_snake_id):
    if snake_dict[my_snake_id]['health'] < 30:
        return True

    cur_length = len(snake_dict[my_snake_id]['coords'])
    for snake_id, snake_data in snake_dict.items():
        if snake_id == my_snake_id:
            continue
        if cur_length < len(snake_data['coords']) - 2:
            return True
    return False


def count_paths_out(board, moves, cur_x, cur_y, ate_last_turn):
    """
    Returns:
        move_to_options (dict): key (str) is a move, val (int) is number of paths out.
            e.g. {'left': 3, 'up': 5}
    """
    limit, move_to_options = 4, dict()
    for move in moves:
        possible_head = board.get_pos_from_move((cur_x, cur_y), move)
        num_paths = count_number_of_paths_out_from_move(board, possible_head, 2, limit + 2, set(), 0, ate_last_turn)
        move_to_options[move] = num_paths
    return move_to_options

def find_very_safe_moves(prioritized_unfatal_moves, board, cur_x, cur_y, max_length, ate_last_turn=[]):
    threat_level, very_safe_moves = 3, []
    while not very_safe_moves:
        threat_level = threat_level - 1
        for move in prioritized_unfatal_moves:
            possible_head = board.get_pos_from_move((cur_x, cur_y), move)
            if find_conservative_path_out(board, possible_head, 1, max_length, set(), 0, threat_level, ate_last_turn):
                very_safe_moves.append(move)

        if threat_level == 1:
            break
    return very_safe_moves


def find_path_out(board, head, moves_elapsed, max_snake_length, visited, num_times_eaten, ate_last_turn):
    """
    Params:
        ate_last_turn (list): IDs of snakes that ate in the previous turn.

    """
    visited.add(head)
    if board.get_tile(head[0], head[1]).is_food():
        num_times_eaten += 1

    if moves_elapsed == max_snake_length + 1:  # it's a brand new world
        return True

    cur_valid_moves = board.get_valid_moves(head[0], head[1], ate_last_turn=ate_last_turn)
    future_valid_moves = board.get_valid_moves_in_the_future(head[0], head[1], moves_elapsed, num_times_eaten, ate_last_turn)
    # take set union
    valid_moves = list(set(cur_valid_moves + future_valid_moves))
    if not valid_moves:
        return False

    for move in valid_moves:
        new_pos = board.get_pos_from_move(head, move)
        if new_pos not in visited and find_path_out(
            board, new_pos, moves_elapsed + 1, max_snake_length, visited, num_times_eaten, ate_last_turn):
            return True

    return False


def count_number_of_paths_out_from_move(board, head, moves_elapsed, limit, visited, num_times_eaten, ate_last_turn=[]):
    # print('at depth:', moves_elapsed)
    visited.add(head)
    if board.get_tile(head[0], head[1]).is_food():
        num_times_eaten += 1

    if moves_elapsed == limit:  # it's a brand new world
        visited.remove(head)
        return 1

    valid_moves = board.get_valid_moves_in_the_future(head[0], head[1], moves_elapsed, num_times_eaten, ate_last_turn)

    total_moves_from_here = 0
    for move in valid_moves:
        new_pos = board.get_pos_from_move(head, move)
        total_moves_from_here += count_number_of_paths_out_from_move(board, new_pos, moves_elapsed + 1, limit, visited, num_times_eaten, ate_last_turn)

    try:
        visited.remove(head)
    except:
        pass
    return total_moves_from_here


def find_conservative_path_out(board, head, moves_elapsed, max_snake_length, visited, num_times_eaten, threat_level, ate_last_turn):
    # print('at depth:', moves_elapsed)
    visited.add(head)
    if board.get_tile(head[0], head[1]).is_food():
        num_times_eaten += 1

    if moves_elapsed == max_snake_length + 1:  # it's a brand new world
        return True

    valid_moves = board.get_valid_moves_in_the_future(head[0], head[1], moves_elapsed, num_times_eaten, ate_last_turn)
    if not valid_moves:
        return False

    for move in valid_moves:
        new_pos = board.get_pos_from_move(head, move)
        tile_data = board.get_tile(new_pos[0], new_pos[1]).data
        if 'threatened' not in tile_data or ('threatened' in tile_data and tile_data['threatened'] < threat_level):
            if new_pos not in visited and find_conservative_path_out(board, new_pos, moves_elapsed + 1, max_snake_length, visited, num_times_eaten, threat_level, ate_last_turn):
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
                board.get_tile(head_x, head_y).data['threatened_length'] = len(snake['coords']) # TODO this..
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
            if board.get_tile(head_x, head_y).data['threatened_length'] < len(us['coords']):
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


def prioritize_moves_by_food(board_data, board, valid_moves, snake_dict, my_snake_id):
    """
    returns:
        (list): permuted valid_moves prioritized best->worst.
            favours moves that approach most of: nearest cluster, largest cluster, nearest food
        (dict): key (str) is move, value (int) is score [0,3] where higher is better
    """
    closest_food_and_snakes = find_closest_snakes(board, board_data['food'])
    foods_by_snake = closest_food_and_snakes['by_snake']

    # we aren't the closest to anything
    if my_snake_id not in foods_by_snake:
        return [], dict()

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
    priority_val_per_move = dict()
    for move in valid_moves:
        pop_count = 0
        if move in to_big_clusters:
            pop_count += 1
        if move in to_near_clusters:
            pop_count += 1
        if move in to_close_food:
            pop_count += 1

        priority_val_per_move[move] = pop_count
        priority_index = (pop_count * (-1)) - 1
        priority_buckets[priority_index].append(move)

    # that's it, done.
    prioritized = sum(priority_buckets, [])
    return prioritized, priority_val_per_move
