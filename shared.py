from gameObjects import *

def get_head_coords(snake):
    head_x, head_y = snake['coords'][0][0], snake['coords'][0][1]
    return (head_x, head_y)

def get_snake(snake_id, snakes):
    for snake in snakes:
        if snake['id'] == snake_id:
            return snake

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
