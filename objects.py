from logic import *
from gen_fake_board import gen_board

#remove this likely? 
class GameBoard(object):

    def __init__(self, board, height, width):
        self.height = height
        self.width = width
        #commented out for testing
        #self.internal_rep = self.convert_to_internal_board(board)
        self.internal_rep = gen_board()

    def __str__(self):
        self.print_board()
        return ''
