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

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World"


#Logic about which algorithm gets run,
#and some basic parsing
def pick_move(data, mode):
    if mode == 'food-fetcher':
        return pick_move_to_food(data)
    elif mode == 'min-max':
        snake_dict = create_snake_dict(data['snakes'])
        #print "--- ORIGINAL BOARD FROM WHICH ALL OTHERS FOLLOW --- "
        board = Board(data['height'], data['width'], snake_dict, data['food'])
        #board.print_board()
        #print "Num snakes:", len(snake_dict)
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
    print "Got started pinged."
    data = request.get_json(force=True) #dict
    #print_data(data)
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
    print_data(data)

    # TODO pick a default
    if len(sys.argv) == 1:
        mode = 'default'
    else:
        mode = sys.argv[1]

    print "Running in mode: ", mode
    move = pick_move(data, mode)
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
