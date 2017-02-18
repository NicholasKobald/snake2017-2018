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
        return x, y+1
    if move == 'down':
        return x, y-1
    if move == 'left':
        return x-1, y
    if move == 'right':
        return x+1, y
    raise Exception
