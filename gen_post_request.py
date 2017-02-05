# generates sample boards to test snake AI
#
#
import os, sys, requests, random
#for now, empty board
def generate_board(x, y):
    """
    [
    [<boardT>, <boardT>, <boardT>],
    [<boardT>, <boardT>, <boardT>],
    ..
    .
    ]
    """
    board = []
    for i in range(x):
        row = []
        for j in range(y):
            row.append(gen_board_tile())
        board.append(row)
    return board

def gen_board_tile():
    return dict(state='empty')

def place_snakes(num_snakes, board):
    snake_length = 3;
    for i in range(num_snakes):
        for j in range(3):
            place_snake(board, i)

def place_snake(board, i):
    head_x = random.randint(0, len(board)-1)
    head_y = random.randint(0, len(board[0])-1)
    board[head_x][head_y] = dict(state='head', snake=str(i))

def generate_foodlist(num_snakes, board):
    pass

def create_final_request(board, snakes, foodlist):
    pass

def visualize_request(board):
    for row in board:
        print(row)
def temp_post_request(board):
    pass


def main():
    board = generate_board(4, 4)
    visualize_request(board)



if __name__ == '__main__':
    main()
