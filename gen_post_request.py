# generates sample boards to test snake AI
#
#
import os, sys, requests

def generate_board(x, y, **kwargs=None):
    pass

def place_snakes(num_snakes, board):
    pass

def generate_foodlist(num_snakes, board):
    pass

def create_final_request(board, snakes, foodlist):
    pass

my_dict = {
  "game_id": "11111",
  "turn": 1,
  "board": [
    [<BoardTile>, <BoardTile>, ...],
    [<BoardTile>, <BoardTile>, ...],
    ...
  ],
  "snakes":[<Snake>, <Snake>, ...],
  "food": [[1, 4], [3, 0], [5, 2]]
}
