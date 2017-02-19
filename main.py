#
#
# N. Kobald - 2017-02-04
#

import os, json
import time

from flask import Flask, request
from deprecated import *
from shared import *
from duel import *
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
    move = minmax(board, data['snakes'], data['you'], data['food'], 0)
    print "move returned", move['move']
    return move['move']


#page to dump data
@app.route('/hello')
def hello():
    return "Hello World!"

def print_data(data):
    for key in data:
        print key, ":", data[key]

@app.route('/start', methods=['POST'])
def start():
    print "Got started pinged."
    data = request.get_json(force=True) #dict
    #print_data(data)
    response = dict(
        color='#369',
        name='master_ai',
        taunt='My. Treat.'
    )
    return json.dumps(response)

@app.route('/move', methods=['POST'])
def move():
    start = time.time()
    data = request.get_json(force=True) #dict
    print "Got pinged."
    direction = pick_move(data)
    response = {
        'move':direction,
        'taunt':'Lets raise the ROOOF'
    }
    end = time.time()
    print "Took", end - start, "seconds to compute move."
    return json.dumps(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
