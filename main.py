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

import os, json, sys
from flask import Flask, request
from deprecated import *
from shared import *
from food_fetcher import *
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
    return json.dumps(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=(os.environ.get("PORT", "5001")))
