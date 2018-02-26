from shared import *  # fixme


def pick_move_to_food(data, board, snake_dict):
    my_snake_id = data['you']['id']
    # get our head coordinates
    x, y = get_head_coords(snake_dict[my_snake_id])
    valid_moves = board.get_valid_moves(x, y, data.get('ate_last_turn', []))
    print("valid moves:", valid_moves)
    losing_head_collisions = board.find_losing_head_collisions(x, y, my_snake_id, snake_dict, data.get('ate_last_turn', []))

    prioritized_moves = prioritize_moves_by_food(data, board, valid_moves, snake_dict, my_snake_id)
    if prioritized_moves is None:
        snake_coords = get_head_coords(snake_dict[my_snake_id])
        prioritized_moves = prioritize_moves_backup(valid_moves, snake_coords, board.width,
                                                    board.height, board)

    size_and_move = []
    prioritized_unfatal_moves = [p for p in prioritized_moves if p not in losing_head_collisions]
    for move in prioritized_unfatal_moves:
        possible_head = board.get_pos_from_move((x, y), move)
        component_size = count_reachable(board, possible_head)
        size_and_move.append((move, component_size))

    if not size_and_move:  # all that exist are losing head collisions, I guess be optimistic?
        try:  # TODO: convince myself this can't happen unless it needs to
            return prioritized_moves[0]
        except IndexError:
            print("Returning 'left' (no valid options")
            return 'left'  # the answer is always left

    max_length = get_max_snake_length(snake_dict)
    for move in prioritized_unfatal_moves:
        possible_head = board.get_pos_from_move((x, y), move)
        if find_path_out(board, possible_head, 2, max_length, set(), 0):
            return move

    snake_len = len(snake_dict[my_snake_id]['coords'])
    if size_and_move[0][1] < snake_len:
        fallback = max(size_and_move, key=lambda v: v[1])
        print("Returning", fallback[0], "as a fallback")
        return fallback[0]

    try:
        return prioritized_unfatal_moves[0]
    except IndexError:
        # better not to crash if we're in multiple games
        print("Returning 'up' (no valid options)")
        return 'up'


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


def mark_dangerous_paths(board):
    pass


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
