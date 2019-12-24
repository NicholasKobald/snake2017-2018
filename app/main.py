from flask import Flask, request
from time import time
import json
import os

import sys
# necessary for rest of import statements below
sys.path.extend(['.', '../'])

from app.food_fetcher import pick_move_to_food, convert_to_coords_list
from app.objects.snake import Snake
from app.objects.board import Board
from app.shared import find_snakes_that_just_ate

PREV_GAME_DATA = dict()

app = Flask(__name__)


@app.route('/')
def home():
    return "<b>Hello World</b>"

def pick_move(board, my_snake_id):
    """
    Params:
        board (Board): represents game state.
        my_snake_id (str): our snake ID.

    Returns:
        move (str): one of 'up', 'left', 'right', 'down'
    """
    move = pick_move_to_food(board, my_snake_id)
    return move

@app.route('/ping')
def ping():
    return "Successfully pinged"

@app.route('/start', methods=['POST'])
def start():
    global PREV_GAME_DATA
    data = request.get_json(force=True)
    PREV_GAME_DATA[data['game']['id']] = dict()

    print("STARTING GAME WITH ID",  data['game']['id'])

    # TODO update this to 2019 standard
    response = dict(
        color='#069',
        name='Bitcoin',
        taunt="Hope I don't crash!",
        head_type='pixel',
        tail_type='pixel',
        head_url="data:image/png;base64,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",
    )
    return json.dumps(response)

@app.route('/end', methods=['POST'])
def end():
    data = request.get_json(force=True)  # dict
    print("We finished a game")
    print(json.dumps(data, indent=2))
    print("** end data")
    game_finished = data['game']['id']
    global PREV_GAME_DATA
    try:
        del PREV_GAME_DATA[game_finished]
    except Exception:
        print("Got told we finished a game we weren't in?")
    return json.dumps({'thanks': True})

@app.route('/move', methods=['POST'])
def move():
    """Returns chosen move, given request with body describing the board state.

    Prepares board and snake data structures, from given game data.
    See battlesnake documentation for details about body structure.

    Returns:
        (json): e.g. {"move": "up"}
    """
    global PREV_GAME_DATA
    data = request.get_json(force=True)
    board_data = data['board']
    board_height, board_width, food = board_data['height'], board_data['width'], board_data['food']
    game_id = data['game']['id']
    my_snake_id = data['you']['id']

    print("\nPINGED\n  ********************")
    start = time()

    prev_foods = PREV_GAME_DATA.get(game_id, {}).get('prev_foods', [])
    if prev_foods != []:
        ate_last_turn = find_snakes_that_just_ate(board_data, prev_foods, board)
    else:
        ate_last_turn = []

    snakes = {
        s['id']: Snake(s['id'], s['body'], s['health'], s['id'] in ate_last_turn)
        for s in board_data['snakes']
    }
    board = Board(
        board_height,
        board_width,
        snakes,
        food,
        my_snake_id,
        ate_last_turn,
    )

    if game_id in PREV_GAME_DATA:
        PREV_GAME_DATA[game_id]['prev_foods'] = convert_to_coords_list(board_data['food'])

    end = time()
    print("Took", (end - start), "to build the board and setup game data")

    move_alone = time()
    move = pick_move(board, my_snake_id)
    print("Computing the move took", (move_alone - start), "time")

    end = time()
    print("TOTAL time:", (end - start), "to compute move", move)
    return json.dumps(dict(move=move))


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
