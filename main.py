#
#
# N. Kobald - 2017-02-04
#

import os, json
import time

from flask import Flask, request

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
    snake_dict = create_snake_dict(data['snakes'])
    board = Board(data['height'], data['width'], snake_dict, data['food'])
    print snake_dict
    move = minmax(board, snake_dict, data['you'], data['food'], 0)
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
    #use 5000 if we're local, or whatever port
    #heroku tells us to use. 
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
