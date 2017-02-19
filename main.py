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

    # return list of all possible moves
    return board.get_valid_moves(x, y)


#page to dump data
@app.route('/hello')
def hello():
    return "Hello World!"

def print_data(data):
    for key in data:
        print key, ";", data[key]

@app.route('/start', methods=['POST'])
def start():
    print "Got started pinged."
    data = request.get_json(force=True) #dict
    #print_data(data)
    response = dict(
        color='#369',
        name='Bennet',
        taunt='My. Treat.'
    )
    return json.dumps(response)

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json(force=True) #dict
    print "Got pinged."
    print_data(data)
    all_directions = pick_move(data)
    print all_directions
    direction = all_directions[0]
    response = {
        'move':direction,
        'taunt':'Lets raise the ROOOF'
    }
    return json.dumps(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
