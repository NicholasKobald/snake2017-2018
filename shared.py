from gameObjects import *

def get_head_coords(snake):
    head_x, head_y = snake['coords'][0][0], snake['coords'][0][1]
    return (head_x, head_y)

def get_snake(snake_id, snakes):
    for snake in snakes:
        if snake['id'] == snake_id:
            return snake

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
