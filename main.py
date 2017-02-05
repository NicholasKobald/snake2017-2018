#
#
#
#
# N. Kobald - 2017-02-04
import os
from bottle import run, route, post, request
#for testing locally

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
    data = request.body.read()

    response = {
        'move':'up',
        'taunt':'Lets raise the ROOOF'
    }
    return response


def parse_input(board_info):
    print board_info

run(host='localhost', port=8080, debug=True, reloader=True)
