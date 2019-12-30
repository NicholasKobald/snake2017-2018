import sys
# necessary for rest of import statements below
sys.path.extend(['.', '../'])

flip_dict = dict(
    up='down',
    left='right',
    right='left',
    down='up'
)

DEBUG = True


def get_max_snake_length(snakes):
    return max(snake.length for _, snake in snakes.items())

def get_pos_from_move(cur_pos, move):
    raise NotImplementedError()
    col, row = cur_pos[0], cur_pos[1]
    if move == 'up':
        return col, row - 1
    elif move == 'down':
        return col, row + 1
    elif move == 'left':
        return col - 1, row
    elif move == 'right':
        return col + 1, row
    raise Exception

def get_new_bydest_dict(dest_coord_key_str, by_dest, cur_info, cur_snake_id):
    new_snake_info = dict(snake_id=cur_snake_id,
                          path_len=cur_info['path_len'],
                          coords=cur_info['coords'])
    # TODO settle ties by snake length
    by_dest[dest_coord_key_str].append(new_snake_info)
    return by_dest

def get_new_bysnake_dict(snake_id, by_snake, snake_coords, dest_coord, path_len, other_snake_info):
    tied_with = []
    for other_snake in other_snake_info:
        if other_snake['snake_id'] == snake_id: continue
        tied_with.append(other_snake['snake_id'])

        for dest_info in by_snake[other_snake['snake_id']]['dest_info']:
            # make 'tied_with' relation reflexive (as it should be)
            if dest_info['coords'] == dest_coord and \
                            snake_id not in dest_info['tied_with']:
                dest_info['tied_with'].append(snake_id)

    new_dest_info = dict(coords=dest_coord, path_len=path_len, tied_with=tied_with)
    if snake_id in by_snake:
        by_snake[snake_id]['dest_info'].append(new_dest_info)
    else:
        by_snake[snake_id] = dict(dest_info=[new_dest_info],
                                  coords=snake_coords)
    return by_snake

# iterates over coords_list to find closest snake(s) using BFS
def find_closest_snakes(board, coords_list):
    """Finds snakes closest to each of the given list of points.

    Params:
        board (Board).
        coords_list (list): the various destinations e.g. [[0,0], [1,5], [2,3]]

    Return:
        by_dest (dict): e.g. {
            1-2: [{
                snake_id: 'snake-007',
                path_len: 7,
                coords: [0,7]
            },
            ...
            ]
        }
        by_snake (dict): e.g. {
            snake_id: [{
                dest_info: {
                    coords: [1,1],
                    path_len: 7,
                    tied_with: ['snake-006']
                },
                coords: [0, 7]
            },
            ...
            ]
        }
    """
    by_dest, by_snake = dict(), dict()
    for dest_coord in coords_list:
        dest_coord_key_str = coords_to_key_str(dest_coord)
        by_dest[dest_coord_key_str] = []

        visited = [[False] * board.height for _ in range(board.width)]
        queue = [dict(coords=dest_coord, path_len=0)]
        working_min_path_len = float('inf')  # we stop our search once beyond this
        while len(queue) > 0:
            cur_info = queue.pop(0)
            cur_pos = cur_info['coords']
            cur_path_len = cur_info['path_len']

            # cancels need for path_len comparison when we find snake_head
            if cur_path_len > working_min_path_len:
                continue
            cur_col, cur_row = cur_pos['x'], cur_pos['y']

            # have we reached our destination ?
            if board.get_tile(cur_col, cur_row).is_head:
                working_min_path_len = cur_path_len
                cur_snake_id = board.get_tile(cur_col, cur_row).snake_id
                by_dest = get_new_bydest_dict(
                    dest_coord_key_str,
                    by_dest,
                    cur_info,
                    cur_snake_id
                )
                by_snake = get_new_bysnake_dict(
                    cur_snake_id,
                    by_snake,
                    cur_info['coords'],
                    dest_coord,
                    cur_path_len,
                    by_dest[dest_coord_key_str]
                )
                continue  # at working_min_path_len, anything from here is longer

            valid_moves = board.get_valid_moves(cur_col, cur_row)
            for move in ['up', 'down', 'right', 'left']:
                pos = board.get_pos_from_move(cur_pos, move)
                if pos is None or visited[pos[0]][pos[1]]:
                    continue
                # enqueue cell if unoccupied or containing snake head
                if move in valid_moves or board.get_tile(pos[0], pos[1]).is_head:
                    if cur_path_len + 1 <= working_min_path_len:
                        queue.append(dict(coords={"x": pos[0], "y": pos[1]}, path_len=(cur_path_len + 1)))
                        visited[pos[0]][pos[1]] = True

    return dict(by_dest=by_dest, by_snake=by_snake)

def coords_to_key_str(coords):
    """
    Returns:
        key_str (str): e.g. "1-2" for x=1, y=2.
    """
    col, row = coords['x'], coords['y']
    key_str = str(col) + ":" + str(row)
    return key_str

def key_str_to_coords(key_str):
    str_coords = key_str.split(':')
    assert len(str_coords) == 2
    coords = (int(str_coords[0]), int(str_coords[1]))
    return coords

def prefer_nearest_food(move_dict):
    moves_to_nearest_food, cur_nearest_food_dist = [], float('inf')
    for move, path_lengths in move_dict.items():
        for food_dist in path_lengths:
            if food_dist < cur_nearest_food_dist:
                cur_nearest_food_dist = food_dist
                moves_to_nearest_food = [move]
            elif food_dist == cur_nearest_food_dist:
                if move not in moves_to_nearest_food:
                    moves_to_nearest_food.append(move)
    return moves_to_nearest_food

def prefer_nearby_food_clusters(move_dict):
    moves_to_nearest_clusters, cur_nearest_cluster_dist = [], float('inf')
    for move, path_lengths in move_dict.items():
        ave_dist = int(round(sum(path_lengths) / (len(path_lengths))))
        if ave_dist < cur_nearest_cluster_dist:
            cur_nearest_cluster_dist = ave_dist
            moves_to_nearest_clusters = [move]
        elif ave_dist == cur_nearest_cluster_dist:
            moves_to_nearest_clusters.append(move)
    return moves_to_nearest_clusters

def prefer_biggest_food_clusters(move_dict):
    moves_to_biggest_cluster, cur_biggest_cluster_size = [], 0
    for move, path_lengths in move_dict.items():
        cur_cluster_size = len(path_lengths)
        if cur_biggest_cluster_size < cur_cluster_size:
            cur_biggest_cluster_size = cur_cluster_size
            moves_to_biggest_cluster = [move]
        elif cur_biggest_cluster_size == cur_cluster_size:
            moves_to_biggest_cluster.append(move)
    return moves_to_biggest_cluster

def confirm_closest(board, snake_id, comp_snake_ids):
    comp_snake_ids.append(snake_id)
    longest_snake_id = find_longest_snake(board, comp_snake_ids)
    return longest_snake_id == snake_id

def find_longest_snake(board, snake_ids):
    if len(snake_ids) < 1:
        return None
    cur_longest_snake = snake_ids[0]
    cur_longest_len = board.snakes[cur_longest_snake].length
    for other_snake_id in snake_ids:
        if other_snake_id == cur_longest_snake:
            continue
        other_snake_len = board.snakes[other_snake_id].length
        if other_snake_len > cur_longest_len:
            cur_longest_len = other_snake_len
            cur_longest_snake = other_snake_id
        elif other_snake_len == cur_longest_len:
            cur_longest_snake = None
    assert (cur_longest_snake is None or
            cur_longest_len == board.snakes[cur_longest_snake].length)
    return cur_longest_snake

def group_nearest_food_by_moves(valid_moves, snake_food_info):
    moves_towards_food = dict()
    food_info_list = snake_food_info['dest_info']
    for food_info in food_info_list:
        food_coords, path_len = food_info['coords'], food_info['path_len']
        for move in valid_moves:
            if move_approaches_target(move, snake_food_info['coords'], food_coords):
                if move in moves_towards_food:
                    moves_towards_food[move].append(path_len)
                else:
                    moves_towards_food[move] = [path_len]
    return moves_towards_food

# returns True if given move brings cur_pos closer to dest_pos (Euclidean dist)
def move_approaches_target(move, cur_pos, dest_pos):
    cur_col, cur_row = cur_pos['x'], cur_pos['y']
    dest_col, dest_row = dest_pos['x'], dest_pos['y']
    if move == 'right':
        return cur_col < dest_col
    elif move == 'left':
        return cur_col > dest_col
    elif move == 'down':
        return cur_row < dest_row
    elif move == 'up':
        return cur_row > dest_row
    print("* PROVIDED INVALID MOVE to move_approaches_target")
    return None

# NOTE: should probs use get_shortest_path_for_each() instead
# - this one is a tad faster but much dumber
#
# finds distance from (col, row) to each pair of coords in coord_list
# returns a dict where (key=dist, val=list of coordinates)
def get_displacement_for_each(col, row, coord_list):
    distances = dict()
    for item in coord_list:
        dist = abs(col - item[0]) + abs(row - item[1])
        # insert into dictionary
        # check if we already have another pair of coords for computed distances
        if dist in distances:
            distances[dist].append(item)
        else:
            distances[dist] = [item]
    return distances

def find_snakes_that_just_ate(food, prev_food_list, board):
    """
    Determines which snakes have just eaten food and will therefore grow next turn.
    Uses position of food from previous turn and current position of snake heads.

    Returns:
        snakes_just_ate (list): IDs of all snakes that ate in the previous turn
    """
    snakes_just_ate = []
    cur_food_list = convert_to_coords_list(food)
    for prev_food in prev_food_list:
        # ignore foods that are still there from last turn
        if prev_food in cur_food_list:
            continue

        tile = board.get_tile(prev_food[0], prev_food[1])
        if tile.is_snake():
            snakes_just_ate.append(tile.snake_id)
    return snakes_just_ate

def convert_to_coords_list(food_list):
    """
    e.g. food_list = [
        {"x": 0, "y": 0},
        ...
        {"x": 5, "y": 5}
    ] =>
    [
        [0,0],
        ...
        [5,5]
    ]
    """
    food_coords = []
    for food_item_dict in food_list:
        x, y = food_item_dict['x'], food_item_dict['y']
        food_coords.append([x, y])
    return food_coords

# quick bfs to count reachable from specific board
def count_reachable(board, head):
    visited = set()
    count = 0
    que = [head]
    while que:
        head, count = que.pop(), count + 1
        valid_moves = board.get_valid_moves(head[0], head[1])
        for move in valid_moves:
            tile = board.get_pos_from_move(head, move)
            if tile not in visited:
                visited.add(tile)
                que.append(tile)

    return count
