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

def create_snake_dict(snake_list):
    snake_dict = dict()
    for snake in snake_list:
        snake_dict[snake['id']] = snake
        snake['eaten'] = 0
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
            tile = get_tile_from_move(head, move)
            if not visited[board.width * tile[0] + tile[1]]:
                visited[board.width * tile[0] + tile[1]] = True
                que.append(tile)
    return count
