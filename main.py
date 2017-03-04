#
#
# N. Kobald - 2017-02-04
#

import os
import json
import time
import sys

from flask import Flask
from flask import request

from shared import *
from food_fetcher import *
from duel import *
from gameObjects import *


OUR_SNAKE_NAME = '1'
PREV_DATA_BY_GAME_ID = dict()
DEBUG = True

taunts = ["10% LUCK, 20% SSSSLITHER", "I look like.. MOM'S SPAGHETTI"]

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World"

#Logic about which algorithm gets run,
#and some basic parsing
def pick_move(start_time, data, board, snake_dict, mode):
    if mode == 'min-max':
        move = start_minmax(board, snake_dict, data['you'], data['food'])
        print "\n* MIN-MAX MOVE =====", move, "*"
        return move
    elif mode == 'food-fetcher':
        move, voronoi_move = pick_move_to_food(start_time, data, board, snake_dict)
        print "\n* FOOD-FETCHER MOVE =====", move, "*"
        return voronoi_move
    error_msg = 'No protocol set for mode=' +  mode
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
        color='#FFF',
        name='master_ai',
        taunt='My. Treat.'
    )
    return json.dumps(response)

@app.route('/move', methods=['POST'])
def move():
    start_time = time.time()
    data = request.get_json(force=True) #dict
    print "\nPINGED\n********************"
    # create Board object
    snake_dict = create_snake_dict(data['snakes'])
    board = Board(data['height'], data['width'], snake_dict, data['food'])

    prev_food_list = PREV_DATA_BY_GAME_ID[data['game_id']]['prev_food_list']
    snakes_just_ate = []
    if prev_food_list != None:
        snakes_just_ate = find_snakes_that_just_ate(data, prev_food_list, board)
    # insert info about which snakes ate last turn into data object
    data['ate_last_turn'] = snakes_just_ate

    PREV_DATA_BY_GAME_ID[data['game_id']]['prev_food_list'] = data['food'][:]

    # TODO pick a default
    if len(sys.argv) == 1:
        mode = 'food-fetcher'
    else:
        mode = sys.argv[1]

    move = pick_move(start_time, data, board, snake_dict, mode)
    response = {
        'move':move,
        'taunt':'Lets raise the ROOOF'
    }
    end_time = time.time()
    print "Took", end_time - start_time, "seconds to compute move."
    return json.dumps(response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
