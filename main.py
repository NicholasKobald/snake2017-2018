#
#
#
#
# N. Kobald - 2017-02-04
import os
from bottle import run, route, post

#for testing locally

#page to dump data
@route('/hello')
def hello():
    return "Hello World!"

@route('/start', method='POST')
def start():
    response = {
        'taunt':'Roar'
    }
    return response

@route('/move', method='POST')
def move():
    data = bottle.request.json
    return ''

run(host='localhost', port=8080, debug=True, reloader=True)
