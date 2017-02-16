#
#
# N. Kobald - 2017-02-04

import os, json
from flask import Flask, request
from logic import *
from gen_fake_board import gen_board, gen_snake_list #testng

OUR_SNAKE_NAME = '1'

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World"

def pick_move(board, snake_list, us):
    #prolly change to ID at some point.
    our_snake = get_specific_snake(snake_list, us)

    height = len(board) #only tested on N x N  (not N x M)
    width = len(board[0])
    print "Playing on a", width, "by", height, "board."
    snake_list.remove(our_snake)
    game_info = dict(
        our_snake=our_snake,
        height=height,
        width=width,
        snake_list=snake_list
    )
    move = do_minmax(board, game_info)
    print "Move Picked:", move
    return move
#page to dump data
@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/start', methods=['POST'])
def start():
    print "Got started pinged."
    data = request.get_json(force=True) #dict
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
    
    response = {
        'move':'left',
        'taunt':'Lets raise the ROOOF'
    }

    return json.dumps(response)

if __name__ == '__main__':
    app.run(debug=True)
