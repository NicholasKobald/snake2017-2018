from gameObjects import *

def get_snake_head(snake_id, snakes):
    for snake in snakes:
        if snake['id'] == snake_id:
            x, y = snake['coords'][0][0], snake['coords'][0][1]
            return (x,y)
