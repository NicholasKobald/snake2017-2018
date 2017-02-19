from gameObjects import *

def get_head_coords(snake):
    head_x, head_y = snake['coords'][0][0], snake['coords'][0][1]
    return (head_x, head_y)

def get_snake(snake_id, snakes):
    for snake in snakes:
        if snake['id'] == snake_id:
            return snake

# finds distance of shortest path from (col, row) to each pair of coords in coord_list
# returns a dict where (key=dist, val=list of coordinates)
def get_shortest_path_for_each(col, row, board, coords_list):
    dist_to = dict()

    for coords in coords_list:
        queue = [dict(col=col, row=row, path_len=0)]
        visited = [ [False]*board.width for i in range(board.height) ]
        while len(queue) > 0:
            # pop from queue
            cur_pos = queue.pop(0)
            # print "cur pos is:", cur_pos, "type:", type(cur_pos)
            cur_col, cur_row = cur_pos['col'], cur_pos['row']
            cur_path_len = cur_pos['path_len']

            # print "visited: " + str(visited)
            if visited[cur_col][cur_row]:
                continue
            visited[cur_col][cur_row] = True

            # check if we've reached the destination
            if cur_col == coords[0] and cur_row == coords[1]:
                # now add to list of foods that are 'cur_path_len' moves away
                if cur_path_len in dist_to:
                    dist_to[cur_path_len].append(coords)
                else:
                    dist_to[cur_path_len] = [coords]
                break

            valid_moves = board.get_valid_moves(cur_col, cur_row)

            if "right" in valid_moves:
                queue.append({'col': cur_col+1, 'row': cur_row, 'path_len': cur_path_len+1})
            if "down" in valid_moves:
                queue.append({'col': cur_col, 'row': cur_row+1, 'path_len': cur_path_len+1})
            if "left" in valid_moves:
                queue.append({'col': cur_col-1, 'row': cur_row, 'path_len': cur_path_len+1})
            if "up" in valid_moves:
                queue.append({'col': cur_col, 'row': cur_row-1, 'path_len': cur_path_len+1})
    print "shortest_to: " + str(dist_to)
    return dist_to

# TODO consider generalizing function signature to any coord_dict_by_dist
def get_safe_move_to_nearest_food(col, row, valid_moves, food_dict_by_dist):
    near_first = sorted(food_dict_by_dist)

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
    print "distances: " + str(distances)
    return distances
