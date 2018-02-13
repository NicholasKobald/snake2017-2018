import os
import json
import sys
from datetime import time

from flask import Flask
from flask import request

from food_fetcher import pick_move_to_food, find_snakes_that_just_ate, convert_to_coords_list
from objects import Board
from shared import create_snake_dict

OUR_SNAKE_NAME = '1'
PREV_DATA_BY_GAME_ID = dict()
DEBUG = True

taunts = ["10% LUCK, 20% SSSSLITHER", "I look like.. MOM'S SPAGHETTI"]

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello World"


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
    response = dict(
        color='#F00',
        name='Lucifer',
        taunt='temptaunt',
        head_type='dead',
        tail_type='curled'
    )
    return json.dumps(response)


@app.route('/move', methods=['POST'])
def move():
    global PREV_DATA_BY_GAME_ID
    print("\nPINGED\n  ********************")
    data = request.get_json(force=True)  # dict

    snake_dict = create_snake_dict(data['snakes'])
    board = Board(data['height'], data['width'], snake_dict, data['food']['data'])

    prev_food_list = PREV_DATA_BY_GAME_ID[data['id']]['prev_food_list']
    # insert info about which snakes ate last turn into data object
    if prev_food_list is not None:
        data['ate_last_turn'] = find_snakes_that_just_ate(data, prev_food_list, board)

    PREV_DATA_BY_GAME_ID[data['id']]['prev_food_list'] = convert_to_coords_list(data['food']['data'])

    move = pick_move(data, board, snake_dict)

    response = {
        'move': move,
        'taunt': 'Squaack'
    }
    return json.dumps(response)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
