#
#
#
#
# N. Kobald - 2017-02-04
import bottle, os

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')

@bottle.get('/')
def index():
    
    return {
        'color': '#00ffff',
    }


@bottle.post('/start')
def start():
    data = bottle.request.json

    return {
        'taunt': 'battlesnake-python!'
    }
