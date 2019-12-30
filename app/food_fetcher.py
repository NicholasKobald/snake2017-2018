import sys
# necessary for rest of import statements below
sys.path.extend(['.', '../'])

from app.objects.board import Board
from app.objects.snake import Snake
from app.shared import find_snakes_that_just_ate
from app.shared import *  # fixme


def pick_move(board_height, board_width, snakes, food, my_snake_id, game_id, game_data_cache):
    """
    Params:
        board_height (int).
        board_width (int).
        snakes (list of dicts): with the following keys:
            'id' => str, 'body' => coords list, 'health' => int beteen 0,100.
        food (list of x,y coords): e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 1}].
        my_snake_id (str): our snake ID.
        game_id (str).
        game_data_cache (GameDataCache): manages.

    Returns:
        move (str): one of 'up', 'left', 'right', 'down'
    """
    snakes_dict = {
        s['id']: Snake(s['id'], s['body'], s['health'], False)
        for s in snakes
    }
    board = Board(board_height, board_width, snakes_dict, food, my_snake_id)

    prev_foods = game_data_cache.get_food_list(game_id)
    game_data_cache.update_food_list(game_id, food)
    if prev_foods is not None:
        ate_last_turn = find_snakes_that_just_ate(food, convert_to_coords_list(prev_foods), board)
    else:
        ate_last_turn = []

    for snake_id, snake in snakes_dict.items():
        if snake_id in ate_last_turn:
            snake.ate_last_turn = True

    move = pick_move_to_food(board, my_snake_id)
    return move

def pick_move_to_food(board, my_snake_id):
    cur_x, cur_y = board.snakes[my_snake_id].head
    my_snake_len = board.snakes[my_snake_id].length
    valid_moves = board.get_valid_moves(cur_x, cur_y)
    print("valid moves:", valid_moves)
    losing_head_collisions = board.find_losing_head_collisions()
    prioritized_moves, priority_val_per_move = prioritize_moves_by_food(board.food, board, valid_moves, my_snake_id)
    if prioritized_moves == []:
        prioritized_moves = prioritize_moves_backup(valid_moves, cur_x, cur_y, board)

    # all prioritized valid moves that aren't losing head collisions
    prioritized_unfatal_moves = [p for p in prioritized_moves if p not in losing_head_collisions]

    prioritized_potentially_fatal_moves = [p for p in prioritized_moves if p]
    potentially_fatal = False

    if not prioritized_unfatal_moves:
        potentially_fatal = True
        prioritized_unfatal_moves = prioritized_potentially_fatal_moves

    # if we have no valid moves
    if not prioritized_unfatal_moves:
        return 'left'

    if not potentially_fatal:
        dangerous_tiles = get_dangerous_tiles(board, my_snake_id)
        prioritized_moves_with_path_out = find_moves_with_path(
            prioritized_unfatal_moves,
            board,
            cur_x,
            cur_y,
            my_snake_len,   # so that we can fit
            dangerous_tiles,
        )
        print(f"Very safe moves: {prioritized_moves_with_path_out}")
    else:
        prioritized_moves_with_path_out = []

    if prioritized_moves_with_path_out == []:
        prioritized_moves_with_path_out = find_moves_with_path(
            prioritized_potentially_fatal_moves,
            board,
            cur_x,
            cur_y,
            my_snake_len,
            dict(),          # don't avoid any tiles
            anticipate_vacant_tiles=True,
        )
        print(f"Safe moves: {prioritized_moves_with_path_out}")

    num_paths_out_per_move = count_paths_out(board, prioritized_moves_with_path_out, cur_x, cur_y)
    if prioritized_moves_with_path_out:
        # if we are VERY hungry, move to food
        if should_eat(board.snakes, my_snake_id):
            for move in prioritized_moves_with_path_out:
                if priority_val_per_move.get(move, 0) >= 1:
                    return move

        # if we are getting hungry food, try to pick move to food
        # with number of paths above the average
        if board.snakes[my_snake_id].health < 70:
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

    moves = find_moves_with_path(
        prioritized_potentially_fatal_moves,
        board,
        cur_x,
        cur_y,
        my_snake_len,
        dict(),          # don't avoid any tiles
        anticipate_vacant_tiles=True,
    )
    if len(moves) > 0:
        return moves[0]

    # no path existed so, maybe a risky move is the right choice?
    if prioritized_potentially_fatal_moves:
        print("Selecting largest componenent because we found no path out")
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

def should_eat(snakes, my_snake_id):
    """
    Determines that we should eat if one of true holds:
    1) We have low health
    2) Some other snake is longer or within two units of our length
    """
    if snakes[my_snake_id].health < 30:
        return True

    for snake_id, other_snake in snakes.items():
        if snake_id == my_snake_id:
            continue
        if snakes[my_snake_id].length < other_snake.length + 2:
            return True
    return False

def count_paths_out(board, moves, cur_x, cur_y):
    """
    Returns:
        move_to_options (dict): key (str) is a move, val (int) is number of paths out.
            e.g. {'left': 3, 'up': 5}
    """
    # limit is a magic number! Wee!
    limit, move_to_options = 4, dict()
    for move in moves:
        possible_head = board.get_pos_from_move((cur_x, cur_y), move)
        num_paths = count_number_of_paths_out_from_move(board, possible_head, 2, limit + 2, set(), 0)
        move_to_options[move] = num_paths
    return move_to_options

def find_moves_with_path(prioritized_unfatal_moves, board, cur_x, cur_y, min_path_len, dangerous_tiles, anticipate_vacant_tiles=False):
    """Determines whether a "safe" path of the given minimum length exists.

    A path is considered safe if it does not include a tile that is close to another snake's head.
    The min proximity is how far away the path must be from other snake heads (throughotu the whole path).

    Params:
        prioritized_unfatal_moves (list): e.g. ['left', 'up'].
        board (Board).
        cur_x (int).
        cur_y (int).
        min_path_len (int): natural choices are our snake's length or the length of the longest snake.
        dangerous_tiles (dict): key is Tile instance, value is distance from the head of a threatening snake.
        anticipate_vacant_tiles (bool).
    """
    moves_with_paths, min_proximity = [], 1
    while moves_with_paths == [] and min_proximity < 3:
        for move in prioritized_unfatal_moves:
            possible_head = board.get_pos_from_move((cur_x, cur_y), move)
            tiles_to_avoid = {
                tile for tile, proximity_to_threat in dangerous_tiles.items()
                if proximity_to_threat <= min_proximity
            }
            path = find_longest_path(
                board,
                possible_head,
                tiles_to_avoid,
                visited=set(),
                num_times_eaten=0,
                path=[],
                anticipate_vacant_tiles=anticipate_vacant_tiles,
            )
            if len(path) >= min_path_len:
                moves_with_paths.append(move)
        min_proximity += 1
    return moves_with_paths

def count_number_of_paths_out_from_move(board, head, moves_elapsed, max_moves, visited, num_times_eaten):
    """
    Params:
        board (Board).
        head (tuple): head[0] is x-coord, head[1] is y-coord.
        moves_elapsed (int): length of current search path.
        max_moves (int): max length of search path.
        visited (set): coords of tiles we've already visited in our search.
        num_times_eaten (int): i.e. number of foods in our current search path.
    """
    visited.add(head)
    if board.get_tile(head[0], head[1]).is_food:
        num_times_eaten += 1

    if moves_elapsed >= max_moves:
        visited.remove(head)
        return 1

    valid_moves = board.get_valid_moves_in_the_future(head[0], head[1], moves_elapsed, num_times_eaten)
    moves_from_here = 0
    for move in valid_moves:
        new_pos = board.get_pos_from_move(head, move)
        moves_from_here += count_number_of_paths_out_from_move(
            board,
            new_pos,
            moves_elapsed + 1,
            max_moves,
            visited,
            num_times_eaten,
        )

    try:
        visited.remove(head)
    except:
        pass
    return moves_from_here

def find_longest_path(board, head, tiles_to_avoid, visited, num_times_eaten, path, anticipate_vacant_tiles=False):
    """Finds the longest path starting with the given head position.

    The algorithm is somewhat configurable; the caller may specify:
    - tiles to avoid altogether
    - whether or not to anticipate that tiles occupied by some snake will be vacant based on how close they are to
        the snake's tail.

    Params:
        board (Board).
        head (tuple): head[0] is x-coord, head[1] is y-coord.
        tiles_to_avoid (set): of Tile instances.
        visited (set): coords of tiles already in our path.
        num_times_eaten (int): i.e. number of foods in our current search path.
        path (list): coords of Tiles on path so far.
        anticipate_vacant_tiles (bool).

    Returns:
        longest_path (list): coords of path from first to last move.
    """
    visited.add(head)
    if board.get_tile(head[0], head[1]).is_food:
        num_times_eaten += 1

    longest_path = path[:]
    moves = board.get_valid_moves(head[0], head[1])
    if anticipate_vacant_tiles:
        future_valid_moves = board.get_valid_moves_in_the_future(head[0], head[1], len(path)+1, num_times_eaten)
        moves = list(set(moves + future_valid_moves)) # take set union

    for move in moves:
        new_pos = board.get_pos_from_move(head, move)
        tile = board.get_tile(new_pos[0], new_pos[1])
        if tile not in tiles_to_avoid and new_pos not in visited:
            path.append(head)
            tmp_longest_path = find_longest_path(
                board,
                new_pos,
                tiles_to_avoid,
                visited,
                num_times_eaten,
                path,
                anticipate_vacant_tiles=anticipate_vacant_tiles,
            )
            path.pop()
            if len(tmp_longest_path) > len(longest_path):
                longest_path = tmp_longest_path
    return longest_path

def get_dangerous_tiles(board, my_snake_id):
    """Find tiles that are near other snakes' heads.

    Params:
        board (Board).
        my_snake_id (str).

    Return:
        dangerous_tiles (dict): key is a Tile instance, value is the distance from other snake's head.
    """
    my_snake = board.snakes[my_snake_id]
    my_snake_len_next_turn = my_snake.length + 1 if my_snake.ate_last_turn else my_snake.length
    dangerous_tiles = dict()
    for s_id, snake in board.snakes.items():
        if s_id == my_snake_id:
            continue

        enemy_snake_len_next_turn = snake.length + 1 if snake.ate_last_turn else snake.length
        if enemy_snake_len_next_turn < my_snake_len_next_turn:
            # this other snake is not dangerous
            continue

        x, y = snake.head
        valid_moves = board.get_valid_moves(x, y)
        for move in valid_moves:
            head_x, head_y = board.get_pos_from_move((x, y), move)
            dangerous_tiles[board.get_tile(head_x, head_y)] = 1

            valid_followup_moves = board.get_valid_moves(head_x, head_y)
            for followup_move in valid_followup_moves:
                head_x2, head_y2 = board.get_pos_from_move((head_x, head_y), followup_move)
                tile = board.get_tile(head_x2, head_y2)
                # NOTE: we avoid updating a tile that is already marked dangerous since
                # the threatening snake might be one (instead of two) moves away
                if tile not in dangerous_tiles:
                    dangerous_tiles[tile] = 2
    return dangerous_tiles

def prioritize_moves_backup(valid_moves, cur_x, cur_y, board):
    """Prefers moves that approach centre of board."""
    preferred_moves, other_moves = [], []
    centre_x, centre_y = (board.width / 2) - 1, (board.height / 2) - 1
    max_dist_to_centre = abs(cur_x - centre_x) + abs(cur_y - centre_y)
    for move in valid_moves:
        pos = board.get_pos_from_move((cur_x, cur_y), move)
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

def prioritize_moves_by_food(food, board, valid_moves, my_snake_id):
    """
    Params:
        food (list of x,y coords): e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 1}].
        board (Board).
        valid_moves (list of str): e.g. ["up", "left"].
        my_snake_id (str).

    Returns:
        (2-tuple):
            (list): permuted valid_moves prioritized best->worst.
                favours moves that approach most of: nearest cluster, largest cluster, nearest food
            (dict): key (str) is move, value (int) is score [0,3] where higher is better
    """
    closest_food_and_snakes = find_closest_snakes(board, food)
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
