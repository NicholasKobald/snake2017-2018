#
#
# N. Kobald - 2017-02-04
#
#TODO rearrange code into duel.py, shared.py, gladiator.py
#TODO implement TILE class
#TODO implement get_board_from_data
#TODO maybe a BOARD class that is made up of
#tile classes, abstract the board away a bit?
#might be overkill...
# Implement like this, or look into Cython immediately?

import os, json
from flask import Flask, request
from deprecated import *
from shared import *
from gameObjects import *
OUR_SNAKE_NAME = '1'

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World"


#Logic about which algorithm gets run,
#and some basic parsing
def pick_move(data):
    board = Board(data['height'], data['width'], data['snakes'], data['food'])

    # get our snake's head coords
    snake_id = data['you']
    snake_coords = get_head_coords(get_snake(snake_id, data['snakes']))
    x, y = snake_coords[0], snake_coords[1]

    # find safe moves first
    valid_moves = board.get_valid_moves(x, y)

    # find distances from snake head to each food bit
    #food_dict_by_dist = get_displacement_for_each(x, y, data['food'])
    food_dict_by_shortest_path = get_shortest_path_for_each(x, y, board, data['food'])

    # find move towards food
    #move_towards_food_1 = get_safe_move_to_nearest_food(x, y, valid_moves, food_dict_by_dist)
    move_towards_food = get_safe_move_to_nearest_food(x, y, valid_moves, food_dict_by_shortest_path)
    # print "displ: ", move_towards_food_1, " BFS: ", move_towards_food
    if move_towards_food == None:
        # TODO add more intelligent behavior (not just pick some valid move)
        move = valid_moves[0]
    else:
        move = move_towards_food
    # return move that approaches nearest food
    return move


#page to dump data
@app.route('/hello')
def hello():
    return "Hello World!"

def print_data(data):
    print "DATA\n********************"
    for key in data:
        print key, ":", data[key]

@app.route('/start', methods=['POST'])
def start():
    print "Got started pinged."
    data = request.get_json(force=True) #dict
    #print_data(data)
    response = dict(
        color='#FFF',
        name='Bennet',
        taunt='My. Treat.'
    )
    return json.dumps(response)

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json(force=True) #dict
    print "\nPINGED\n********************"
    print_data(data)

    move = pick_move(data)
    print "MOVE PICKED ======== " + str(move) + "\n"
    response = {
        'move':pick_move(data),
        'taunt':'Lets raise the ROOOF'
    }
    return json.dumps(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=(os.environ.get("PORT", "5001"))

