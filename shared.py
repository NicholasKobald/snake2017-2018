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

# finds distance of shortest path from (col, row) to each pair of coords in coord_list
# returns a dict where (key=dist, val=list of coordinates)
def get_shortest_path_for_each(col, row, board, coords_list):
    dist_to = dict()

    # perform BFS to compute min path from (col, row) to every item in coords_list
    for coords in coords_list:
        queue = [dict(col=col, row=row, path_len=0)]
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
                # now add to list of foods that are 'cur_path_len' moves away
                if cur_path_len in dist_to:
                    dist_to[cur_path_len].append(coords)
                # create that list if necessary
                else:
                    dist_to[cur_path_len] = [coords]
                break

            # o.w. continue searching
            valid_moves = board.get_valid_moves(cur_col, cur_row)
            for move in valid_moves:
                new_pos = get_pos_from_move((cur_pos['col'], cur_pos['row']), move)
                queue.append({'col': new_pos[0], 'row': new_pos[1], 'path_len': cur_path_len+1})
    return dist_to

# TODO consider generalizing function signature to any coord_dict_by_dist
def get_safe_move_to_nearest_food(col, row, valid_moves, food_dict_by_dist):
    near_first = sorted(food_dict_by_dist)
    if DEBUG:
        for dist in near_first:
            print "at dist:", dist, "food coords", food_dict_by_dist[dist]

    # TODO perhaps add logic to check if other snakes are nearer and stuff
    # get first coord corresponding to nearest food
    for dist in near_first:
        # 'food' is a list of length 2 containing the food's coordinates
        for food in food_dict_by_dist[dist]:
            col_of_nearest, row_of_nearest = food[0], food[1]
            if col < col_of_nearest:
                if "right" in valid_moves:
                    return "right"
            if col > col_of_nearest:
                if "left" in valid_moves:
                    return "left"
            if row < row_of_nearest:
                if "down" in valid_moves:
                    return "down"
            if row > row_of_nearest:
                if "up" in valid_moves:
                    return "up"
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
