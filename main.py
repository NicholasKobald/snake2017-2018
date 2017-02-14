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

    #going to look into best way to differentiate snakes
    #using ID's seems like the best best,
    #for now I'm naming snakes 1, 2, 3.. etc
    #since its allows me to print out boards in a way thats legible.

    board = gen_board() #testing
    snake_list = gen_snake_list() #testing
    pick_move(board, snake_list, '1')

    response = {
        'move':'up',
        'taunt':'Lets raise the ROOOF'
    }

    return json.dumps(response)

if __name__ == '__main__':
    app.run(debug=True)
