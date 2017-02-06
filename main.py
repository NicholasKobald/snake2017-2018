#
#
# N. Kobald - 2017-02-04

import os, json
from bottle import run, route, post, request
from helper import * #helper functions
from objects import * #helper classes
from logic import * #meat of the algorithm


OUR_SNAKE_NAME = '1'

def pick_move(data):
    snake_list = data['snakes']
    my_snake = get_specific_snake(snake_list, OUR_SNAKE_NAME)
    viable_moves = get_valid_moves(my_snake, data['board'])
    game = GameBoard(data['board'])
    print(game)

#page to dump data
@route('/hello')
def hello():
    return "Hello World!"

@route('/start', method='POST')
def start():
    print "In start"
    data = bottle.request.data
    parse_input(data)
    response = {
        'taunt':'Roar'
    }
    return response

@route('/move', method='POST')
def move():
    print "In Move."
    available_moves = ['n', 'e', 's', 'w']
    data = json.loads(request.body.read()) #dict
    pick_move(data)
    response = {
        'move':'up',
        'taunt':'Lets raise the ROOOF'
    }
    return response


def parse_input(board_info):
    print board_info

run(host='localhost', port=8080, debug=True, reloader=True)
