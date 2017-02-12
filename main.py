#
#
# N. Kobald - 2017-02-04

import os, json
from bottle import run, route, post, request
from helper import * #helper functions
from objects import * #helper classes
from logic import * #meat of the algorithm

OUR_SNAKE_NAME = '1'

def pick_move(game_obj):
    game_obj.print_board()
    print "Done pick_move"
#page to dump data
@route('/hello')
def hello():
    return "Hello World!"

@route('/start', method='POST')
def start():
    print "In start"
    data = json.loads(request.body.read()) #dict
    response = dict(
        color='#369',
        name='Bennet',
        taunt='My. Treat.'
    )
    return json.dumps(response)

@route('/move', method='POST')
def move():
    print "In Move. V2."
    data = json.loads(request.body.read()) #dict

    height = len(data['board']) #only tested on N x N  (not N x M)
    width = len(data['board'][0])

    print "Playing on a", width, "by", height, "board."

    game = GameBoard(data['board'])
    print "game created"
    pick_move(game)

    response = {
        'move':'up',
        'taunt':'Lets raise the ROOOF'
    }
    return json.dumps(response)


def parse_input(board_info):
    print board_info

if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True, reloader=True)
