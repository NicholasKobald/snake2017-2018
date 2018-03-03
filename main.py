import os
import json
from time import time 

from flask import Flask, request

from food_fetcher import pick_move_to_food, find_snakes_that_just_ate, convert_to_coords_list
from objects import Board
from shared import create_snake_dict

PREV_DATA_BY_GAME_ID = dict()

app = Flask(__name__)


@app.route('/')
def home():
    return "<b>Hello World</b>"


def pick_move(data, board, snake_dict):
    move = pick_move_to_food(data, board, snake_dict)
    return move


# page to dump data
@app.route('/hello')
def hello():
    return "Hello World!"


def print_data(data):
    print("DATA\n********************")
    for key in data:
        print(key, ":", data[key])


@app.route('/start', methods=['POST'])
def start():
    global PREV_DATA_BY_GAME_ID
    data = request.get_json(force=True)
    # game_id may be changed to id in the future, if they care about their documentation
    PREV_DATA_BY_GAME_ID[data['game_id']] = dict(prev_food_list=None)

    print("STARTING GAME WITH ID",  data['game_id'])

    response = dict(
        color='#0FF', 
        name='This is the guy!',
        taunt='temptaunt',
        head_type='dead',
        tail_type='curled'
    )
    return json.dumps(response)


@app.route('/end', methods=['POST'])
def end():
    data = request.get_json(force=True)  # dict
    # return json.dumps({'thanks': True})
    print("We finished a game")
    print(json.dumps(data, indent=2))
    print("** end data")
    game_finished = data['game_id']
    global PREV_DATA_BY_GAME_ID
    try:
        pass
        del PREV_DATA_BY_GAME_ID[game_finished]
    except Exception:
        print("Got told we finished a game we weren't in?")

    return json.dumps({'thanks': True})


@app.route('/move', methods=['POST'])
def move():
    global PREV_DATA_BY_GAME_ID
    print("\nPINGED\n  ********************")
    start = time()
    data = request.get_json(force=True)  # dict
    snake_dict = create_snake_dict(data['snakes'])
    board = Board(data['height'], data['width'], snake_dict, data['food']['data'], data['you']['id'])

    try:
        prev_food_list = PREV_DATA_BY_GAME_ID[data['id']]['prev_food_list']
    except KeyError:  # bit of a hack, but lets us restart the game server and resume the same game
        # without issues. Also good if we ever crash mid game
        print("Failed to retrieve prev turn data")
        prev_food_list = None

    # insert info about which snakes ate last turn into data object
    if prev_food_list is not None:
        data['ate_last_turn'] = find_snakes_that_just_ate(data, prev_food_list, board)

    try:
        PREV_DATA_BY_GAME_ID[data['id']]['prev_food_list'] = convert_to_coords_list(data['food']['data'])
    except KeyError:
        print("Failed to update prev food list for next turn")
        pass

    end = time()
    move = pick_move(data, board, snake_dict)
    print("Took", (end - start) * 100, "to compute move", move)
    response = {
        'move': move,
        'taunt': 'Nobody likes snakes. Even snakes dont like snakes'
    }
    return json.dumps(response)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
