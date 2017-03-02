from gameObjects import *


flip_dict = dict(
    up='down',
    left='right',
    right='left',
    down='up'
)

DEBUG = True

def get_head_coords(snake):
    head_x, head_y = snake['coords'][0][0], snake['coords'][0][1]
    return (head_x, head_y)

def get_pos_from_move(cur_pos, move):
    col, row = cur_pos[0], cur_pos[1]
    if move == 'up':
        return (col, row-1)
    elif move == 'down':
        return (col, row+1)
    elif move == 'left':
        return (col-1, row)
    elif move == 'right':
        return (col+1, row)
    raise Exception

def get_new_byfood_dict(food_coord_key_str, by_food, cur_info, cur_snake_id):
    new_snake_info = dict(snake_id=cur_snake_id,
                          path_len=cur_info['path_len'],
                          coords=cur_info['coords'])
    # TODO settle ties by snake length
    by_food[food_coord_key_str].append(new_snake_info)
    return by_food

def get_new_bysnake_dict(snake_id, by_snake, snake_coords, food_coord, path_len, other_snake_info):
    tied_with = []
    for other_snake in other_snake_info:
        if other_snake['snake_id'] == snake_id: continue
        tied_with.append(other_snake['snake_id'])

        for food_info in by_snake[other_snake['snake_id']]['food_info']:
            # make 'tied_with' relation reflexive (as it should be)
            if food_info['coords'] == food_coord and \
                snake_id not in food_info['tied_with']:
                food_info['tied_with'].append(snake_id)

    new_food_info = dict(coords=food_coord, path_len=path_len, tied_with=tied_with)
    if snake_id in by_snake:
        by_snake[snake_id]['food_info'].append(new_food_info)
    else:
        by_snake[snake_id] = dict(food_info=[new_food_info],
                                      coords=snake_coords)
    return by_snake

# iterates over coords_list to find closest snake(s) using BFS
def find_closest_snakes(board, coords_list, snake_dict):
    by_food = dict() # key=coord_key_str, val=[{snake_id, path_len, coords}]
    by_snake = dict() # key=snake_id, val={food_info=[{[coords], path_len, [tied_with]}], coords}
    for food_coord in coords_list:
        food_coord_key_str = coords_to_key_str(food_coord)
        by_food[food_coord_key_str] = []

        visited = [ [False]*board.width for i in range(board.height) ]
        # TODO add 'first_move' key to indicate first move towards food_coords
        queue = [dict(coords=food_coord, path_len=0)]
        working_min_path_len = float('inf') # we stop our search once beyond this
        while len(queue) > 0:
            cur_info = queue.pop(0)
            cur_pos, cur_path_len = cur_info['coords'], cur_info['path_len']
            # cancels need for path_len comparison when we find snake_head
            if cur_path_len > working_min_path_len: continue
            cur_col, cur_row = cur_pos[0], cur_pos[1]

            # have we reached our dest?
            if board.get_tile(cur_col, cur_row).is_head():
                working_min_path_len = cur_path_len
                cur_snake_id = board.get_tile(cur_col, cur_row).get_snake_id()
                by_food = get_new_byfood_dict(food_coord_key_str,
                                              by_food,
                                              cur_info,
                                              cur_snake_id)
                by_snake = get_new_bysnake_dict(cur_snake_id,
                                                by_snake,
                                                cur_info['coords'],
                                                food_coord,
                                                cur_path_len,
                                                by_food[food_coord_key_str])
                continue # at working_min_path_len, anything from here is longer

            valid_moves = board.get_valid_moves(cur_col, cur_row)
            for move in ['up', 'down', 'right', 'left']:
                pos = board.get_pos_from_move(cur_pos, move)
                if pos == None or visited[pos[0]][pos[1]]: continue
                # enqueue cell if unoccupied or containing snake head
                if move in valid_moves or board.get_tile(pos[0], pos[1]).is_head():
                    if cur_path_len+1 <= working_min_path_len:
                        queue.append(dict(coords=pos, path_len=(cur_path_len+1)))
                        visited[pos[0]][pos[1]] = True
    return dict(by_food=by_food, by_snake=by_snake)

def coords_to_key_str(coords):
    col, row = coords[0], coords[1]
    key_str = str(col) + ":" + str(row)
    return key_str

def key_str_to_coords(key_str):
    str_coords = key_str.split(':')
    assert len(str_coords) == 2
    coords = (int(str_coords[0]), int(str_coords[1]))
    return coords

def prefer_nearest_food(move_dict):
    moves_to_nearest_food, cur_nearest_food_dist = [], float('inf')
    for move, path_lengths in move_dict.iteritems():
        for food_dist in path_lengths:
            if food_dist < cur_nearest_food_dist:
                cur_nearest_food_dist = food_dist
                if DEBUG: "min is now:", food_dist
                moves_to_nearest_food = [move]
            elif food_dist == cur_nearest_food_dist:
                if move not in moves_to_nearest_food:
                    moves_to_nearest_food.append(move)
            if DEBUG: "moves to nearest food:", moves_to_nearest_food
    return moves_to_nearest_food


def prefer_nearby_food_clusters(move_dict):
    moves_to_nearest_clusters, cur_nearest_cluster_dist = [], float('inf')
    for move, path_lengths in move_dict.iteritems():
        ave_dist = int(round(sum(path_lengths) / (len(path_lengths))))
        if ave_dist < cur_nearest_cluster_dist:
            cur_nearest_cluster_dist = ave_dist
            moves_to_nearest_clusters = [move]
        elif ave_dist == cur_nearest_cluster_dist:
            moves_to_nearest_clusters.append(move)
    return moves_to_nearest_clusters

def prefer_biggest_food_clusters(move_dict):
    moves_to_biggest_cluster, cur_biggest_cluster_size = [], 0
    for move, path_lengths in move_dict.iteritems():
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
    return (longest_snake_id == snake_id)

def find_longest_snake(board, snake_ids):
    if len(snake_ids) < 1: return None
    cur_longest_snake = snake_ids[0]
    cur_longest_len = board.get_snake_len_by_id(cur_longest_snake)
    for other_snake_id in snake_ids:
        if other_snake_id == cur_longest_snake: continue
        other_snake_len = board.get_snake_len_by_id(other_snake_id)
        if other_snake_len > cur_longest_len:
            cur_longest_len = other_snake_len
            cur_longest_snake = other_snake_id
        elif other_snake_len == cur_longest_len:
            cur_longest_snake = None
    assert (cur_longest_snake == None or \
            cur_longest_len == board.get_snake_len_by_id(cur_longest_snake))
    return cur_longest_snake

def group_nearest_food_by_moves(valid_moves, snake_food_info):
    moves_towards_food = dict()
    food_info_list = snake_food_info['food_info']
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
    cur_col, cur_row = cur_pos[0], cur_pos[1]
    dest_col, dest_row = dest_pos[0], dest_pos[1]
    if move == 'right':
        return (cur_col < dest_col)
    elif move == 'left':
        return (cur_col > dest_col)
    elif move == 'down':
        return (cur_row < dest_row)
    elif move == 'up':
        return (cur_row > dest_row)
    print "* PROVIDED INVALID MOVE to move_approaches_target"
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

def get_moves_from_id(snake_id, snake_list, board):
    snake = get_snake(snake_id, snake_list)
    head = get_head_coords(snake)
    moves = board.get_valid_moves(head[0], head[1])
    return moves

# returns IDs of all snakes that ate in the previous turn
def find_snakes_that_just_ate(data, prev_food_list, board):
    snakes_just_ate = []
    for prev_food in prev_food_list:
        # ignore foods that are still there from last turn
        if prev_food in data['food']:
            continue

        tile = board.safe_get_tile(prev_food[0], prev_food[1])
        if tile.is_snake():
            snakes_just_ate.append(tile.get_snake_id())
    return snakes_just_ate

def create_snake_dict(snake_list):
    snake_dict = dict()
    for snake in snake_list:
        snake_dict[snake['id']] = snake
        snake['eaten'] = 0
        snake['ate'] = [False] #init with prev game info.
        snake['old_tails'] = []
        snake['food_eaten'] = []
        del snake['id'] #nolonger needed.
    return snake_dict

def determine_distance_to_nearest_food(head, food_list):
    min_dist = float('inf')
    for food in food_list:
        x_diff = abs(head[0]-food[0])
        y_diff = abs(head[1]-food[1])
        min(min_dist, (x_diff+y_diff))

    return min_dist

#quick bfs to count reachable from specific board
def count_reachable(board, head):
    visited = [0] * board.width * board.height
    count, que = 0, [head]
    while que:
        head, count = que.pop(), count+1
        valid_moves = board.get_valid_moves(head[0], head[1])
        for move in valid_moves:
            tile = get_pos_from_move(head, move)
            if not visited[board.width * tile[0] + tile[1]]:
                visited[board.width * tile[0] + tile[1]] = True
                que.append(tile)

    return count

#must be called before 'is component safe'
def label_turns_until_safe(board, snake_dict):
    for snake in snake_dict:
        for i, c in enumerate(reversed(snake['coords'])):
            board.get_tile(c[0], c[1]).dist_down_snake(i)

#uses bfs to determine the coordinates of a component
def get_reachable(board, head):
    visited = [0] * board.width * board.height
    count, que = 0, [head]
    while que:
        head, count = que.pop(), count+1
        valid_moves = board.get_valid_moves(head[0], head[1])
        for move in valid_moves:
            tile = get_pos_from_move(head, move)
            if not visited[board.width * tile[0] + tile[1]]:
                visited[board.width * tile[0] + tile[1]] = True
                que.append(tile)

    return visited

def is_component_safe(board, head):
    my_component = get_reachable(board, head)
    count = my_component.count(True) #size of component
    visited = [False] * board.width * board.height
    visited[board.width * head[0] + head[1]] = True
    return find_path_out(board, head[0], head[1], visited, 0, component)

def find_path_out(board, x, y, visited, depth, component):
    if check_exit(board, x, y, component, depth):
        return True

    for move in board.get_valid_moves(x, y):
        to_x, to_y = get_pos_from_move(head, move)
        if not visited[board.width * to_x + to_y]:
            visited[board.width * to_x + to_y] = True
            find_path_out(board, to_x, to_y, visited, depth+1)

def check_exit(board, x, y, component, depth):
    s = set()
    for move in ['up', 'down', 'left', 'right']:
        s.add(board.get_pos_from_move([x, y], move))

    for x, y in s:
        if not component[board.width * x + y] \
            and board.get_tile(x, y).turns_till_safe() < depth:
            return True
