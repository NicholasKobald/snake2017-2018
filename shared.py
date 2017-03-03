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

# for each (col, row) in coords_list, finds snake(s) with shortest path to it
def find_closest_snakes(board, coords_list, snake_dict):
    dist_to = dict()
    for cur_snake_id, cur_snake in snake_dict.iteritems():
        # perform BFS to compute min path from (col, row) to every item in coords_list
        for coords in coords_list:
            queue = [dict(col=cur_snake['coords'][0][0], row=cur_snake['coords'][0][1], path_len=0)]
            # init entire board to False i.e. not visited
            visited = [ [False]*board.width for i in range(board.height) ]
            while len(queue) > 0:
                cur_pos = queue.pop(0)
                cur_col, cur_row = cur_pos['col'], cur_pos['row']
                cur_path_len = cur_pos['path_len']

                if visited[cur_col][cur_row]:
                    continue
                visited[cur_col][cur_row] = True

                # have we reached the destination?
                if cur_col == coords[0] and cur_row == coords[1]:
                    # TODO COMMENT
                    coord_key_str = coords_to_key_str(coords)
                    if coord_key_str in dist_to:
                        closest_snake_path_len = dist_to[coord_key_str][0]['path_len']
                        if cur_path_len < closest_snake_path_len:
                            dist_to[coord_key_str] = [dict(path_len=cur_path_len, snake_id=cur_snake_id)]
                        elif cur_path_len == closest_snake_path_len:
                            dist_to[coord_key_str].append(dict(path_len=cur_path_len, snake_id=cur_snake_id))

                    # create that list if necessary
                    else:
                        dist_to[coord_key_str] = [dict(path_len=cur_path_len, snake_id=cur_snake_id)]
                    break

                # o.w. continue searching
                valid_moves = board.get_valid_moves(cur_col, cur_row)
                for move in valid_moves:
                    new_pos = get_pos_from_move((cur_pos['col'], cur_pos['row']), move)
                    queue.append({'col': new_pos[0], 'row': new_pos[1], 'path_len': cur_path_len+1})
    return dist_to

def coords_to_key_str(coords):
    col, row = coords[0], coords[1]
    key_str = str(col) + ":" + str(row)
    return key_str

def key_str_to_coords(key_str):
    str_coords = key_str.split(':')
    assert len(str_coords) == 2
    coords = (int(str_coords[0]), int(str_coords[1]))
    return coords

def extract_closest_food_by_snake_id(food_dict_by_closest_snakes, snake_id):
    food = []
    # iterate over each food bit to see if specified snake is closest to it
    for food_coord_key_str, closest_snakes_list in food_dict_by_closest_snakes.iteritems():
        other_snakes = []
        temp_dict = None
        # check if snake_id is one of the closest snakes
        for closest_snake in closest_snakes_list:
            if snake_id == closest_snake['snake_id']:
                temp_dict = dict(coords=key_str_to_coords(food_coord_key_str), dist=closest_snake['path_len'])
            else:
                other_snakes.append(closest_snake['snake_id'])
        if temp_dict != None:
            temp_dict['tied_with'] = other_snakes
            food.append(temp_dict)
    return food

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

def group_nearest_food_by_moves(my_snake_col, my_snake_row, my_snake_id, valid_moves, food_dict_by_closest_snakes):
    closest_food_to_my_snake = extract_closest_food_by_snake_id(food_dict_by_closest_snakes, my_snake_id)
    moves_towards_food = dict()
    for closest_food_dict in closest_food_to_my_snake:
        coords_of_nearest = closest_food_dict['coords']
        col_of_nearest, row_of_nearest = coords_of_nearest[0], coords_of_nearest[1]
        path_len = closest_food_dict['dist']

        # TODO consider improving logic -- use BFS to find first move in shortest path
        for move in valid_moves:
            if move_approaches_target(move, (my_snake_col, my_snake_row), coords_of_nearest):
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


    for move in ['up', 'down', 'left', 'right']:
        to_x, to_y = get_pos_from_move(head, move)
        if not visited[board.width * to_x + to_y]:
            visited[board.width * to_x + to_y] = True
            find_path_out(board, to_x, to_y, visited, depth+1)

def check_exit(board, x, y, component, depth):
    s = set()
    for move in ['up', 'down', 'left', 'right']:
        m = board.get_pos_from_move([x, y], move)
        if m:
            s.add(m)

    for x, y in s:
        if not component[board.width * x + y] and board.get_tile(x, y).turns_till_safe() < depth:
            return True
