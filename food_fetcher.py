from gameObjects import *
from shared import *


DEBUG = True

def pick_move_to_food(data, board, snake_dict):
    # get our snake's head coords
    my_snake_id = data['you']
    snake_coords = get_head_coords(snake_dict[my_snake_id])
    x, y = snake_coords[0], snake_coords[1]

    # find safe moves first
    valid_moves = board.get_valid_moves(x, y, data['ate_last_turn'])
    if DEBUG: print "valid moves:", valid_moves
    losing_head_collisions = board.find_losing_head_collisions(x, y, my_snake_id, snake_dict, data['ate_last_turn'])
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
    food_by_closest_snakes = find_closest_snakes(board, data['food'], snake_dict)
    if DEBUG: print "food distances:", food_by_closest_snakes

    # find move towards food
    moves_towards_food = group_nearest_food_by_moves(x, y, my_snake_id, valid_moves, food_by_closest_snakes)
    if DEBUG: print "moves_towards_food", moves_towards_food
    moves_towards_food_clusters = prefer_food_clusters(moves_towards_food)
    if DEBUG: print "moves towards clusters", moves_towards_food_clusters

    # TODO improve move picking logic
    if moves_towards_food_clusters == []:
        if len(move_towards_food) == 0:
            # TODO add more intelligent behavior (not just pick some valid move)
            move = valid_moves[0]
        else:
            move = move_towards_food[move_towards_food.keys()[0]]
    else:
        move = moves_towards_food_clusters[0]
    return move
