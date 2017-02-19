from gameObjects import *

def get_head_coords(snake):
    head_x, head_y = snake['coords'][0][0], snake['coords'][0][1]
    return (head_x, head_y)

def get_snake(snake_id, snakes):
    for snake in snakes:
        if snake['id'] == snake_id:
            return snake


def get_tile_from_move(head, move):
    x, y = head[0], head[1]
    if move == 'up':
        return x, y-1
    if move == 'down':
        return x, y+1
    if move == 'left':
        return x-1, y
    if move == 'right':
        return x+1, y

    raise Exception

def get_moves_from_id(snake_id, snake_list, board):
    snake = get_snake(snake_id, snake_list)
    head = get_head_coords(snake)
    moves = board.get_valid_moves(head[0], head[1])
    return moves

def determine_distance_to_nearest_food(head, food_list):
    min_dist = float('inf')
    for food in food_list:
        x_diff = abs(head[0]-food[0])
        y_diff = abs(head[1]-food[1])
        min(min_dist, (x_diff+y_diff))

    return min_dist
