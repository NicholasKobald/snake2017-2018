from gameObjects import *

def get_head_coords(snake):
    head_x, head_y = snake['coords'][0][0], snake['coords'][0][1]
    return (head_x, head_y)

def get_snake(snake_id, snakes):
    for snake in snakes:
        if snake['id'] == snake_id:
            return snake
