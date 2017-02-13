#
#
# N. Kobald - 2017-02-04

import os, json
from flask import Flask, request
from helper import * #helper functions
from objects import * #helper classes
from logic import * #meat of the algorithm

OUR_SNAKE_NAME = '1'

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World"

def pick_move(game_obj):
    game_obj.print_board()
    move = do_minmax(game_obj, snake_list)
    print "Done pick_move"

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

    height = len(data['board']) #only tested on N x N  (not N x M)
    width = len(data['board'][0])

    print "Playing on a", width, "by", height, "board."

    game = GameBoard(data['board'], height, width
    
    #going to look into best way to differentiate snakes
    #using ID's seems like the best best,
    #for now I'm naming snakes 1, 2, 3.. etc
    #since its allows me to print out boards in a way thats legible.

    pick_move(game, data['snakes'], '1')

    response = {
        'move':'up',
        'taunt':'Lets raise the ROOOF'
    }

    return json.dumps(response)

if __name__ == '__main__':
    app.run(debug=True)
