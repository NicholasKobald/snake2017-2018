from gameObjects import *
from shared import *


DEBUG = True

def pick_move_to_food(data, board, snake_dict):
    # get our snake's head coords
    snake_id = data['you']
    snake_coords = get_head_coords(snake_dict[snake_id])
    x, y = snake_coords[0], snake_coords[1]

    # find safe moves first
    valid_moves = board.get_valid_moves(x, y, data['ate_last_turn'])
    if DEBUG: print "valid moves:", valid_moves
    losing_head_collisions = board.find_losing_head_collisions(x, y, snake_id, snake_dict, data['ate_last_turn'])
    if DEBUG: print "dangerous head collisions:", losing_head_collisions

    # TODO add a better heuristic for choosing which dangerous move to make
    # --> e.g. if the other snake might move towards other food instead
    for dangerous_move in losing_head_collisions:
        if len(valid_moves) > 1:
            assert dangerous_move in valid_moves
            valid_moves.remove(dangerous_move)
            assert dangerous_move not in valid_moves
        else:
            break

    # find distances from snake head to each food bit
    food_dict_by_shortest_path = get_shortest_path_for_each(x, y, board, data['food'])
    if DEBUG: print "food distances:", food_dict_by_shortest_path

    # find move towards food
    move_towards_food = get_safe_move_to_nearest_food(x, y, valid_moves, food_dict_by_shortest_path)
    if move_towards_food == None:
        # TODO add more intelligent behavior (not just pick some valid move)
        move = valid_moves[0]
    else:
        move = move_towards_food
    return move
