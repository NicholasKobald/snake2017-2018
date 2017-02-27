#
#
# N. Kobald - 2017-02-04
#

import os, json, sys
import time

from flask import Flask, request

from shared import *
from food_fetcher import *
from duel import *
from gameObjects import *
OUR_SNAKE_NAME = '1'
PREV_DATA_BY_GAME_ID = dict()
DEBUG = True

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World"


#Logic about which algorithm gets run,
#and some basic parsing
def pick_move(data, board, snake_dict, mode):
    if mode == 'food-fetcher':
        return pick_move_to_food(data, board, snake_dict)
    elif mode == 'min-max':
        move = minmax(board, snake_dict, data['you'], data['food'], 0)
        print "returning", move['move']
        return move['move']
    error_msg = 'No protocol set for mode=' + str(mode)
    raise Exception(error_msg)

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
    data = request.get_json(force=True) #dict
    PREV_DATA_BY_GAME_ID[data['game_id']] = dict(prev_food_list=None)

    response = dict(
        color='#000',
        name='master_ai',
        taunt='My. Treat.'
    )
    return json.dumps(response)

@app.route('/move', methods=['POST'])
def move():
    start = time.time()
    data = request.get_json(force=True) #dict
    print "\nPINGED\n********************"
    # create Board object
    snake_dict = create_snake_dict(data['snakes'])
    board = Board(data['height'], data['width'], snake_dict, data['food'])

    prev_food_list = PREV_DATA_BY_GAME_ID[data['game_id']]['prev_food_list']
    snakes_just_ate = []
    if prev_food_list != None:
        snakes_just_ate = find_snakes_that_just_ate(data, prev_food_list, board)
        for s in snakes_just_ate:
            if DEBUG: print "snakes_just_ate at:", snake_dict[s]['coords'][0]
    # insert info about which snakes ate last turn into data object
    data['ate_last_turn'] = snakes_just_ate

    PREV_DATA_BY_GAME_ID[data['game_id']]['prev_food_list'] = data['food'][:]

    # TODO pick a default
    if len(sys.argv) == 1:
        mode = 'default'
    else:
        mode = sys.argv[1]

    move = pick_move(data, board, snake_dict, mode)
    print "MOVE PICKED ======== " + str(move) + "\n"
    response = {
        'move':move,
        'taunt':'Lets raise the ROOOF'
    }
    end = time.time()
    print "Took", end - start, "seconds to compute move."
    return json.dumps(response)


if __name__ == '__main__':
    #use 5000 if we're local, or whatever port
    #heroku tells us to use.
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
