from logic import *
from gen_fake_board import gen_board

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

    def convert_to_internal_board(self, board):
        internal_rep = []
        print "In convert.--"
        for i in range(len(board)):
            row = []
            for j in range(len(board[0])):
                tile = board[i][j]
                if tile['state'] == 'empty':
                    row.append('e')
                elif tile['state']=='head':
                    row.append('h'+tile['snake'])
                elif tile['state']=='body':
                    row.append('s'+tile['snake'])
                elif tile['state']=='food':
                    row.append('f')
            internal_rep.append(row)
        return internal_rep

    def print_board(self):
        board = self.internal_rep
        print "----- PRINT BOARD ----\n"
        for i in range(len(board)):
            row_repr = '|'
            for j in range(len(board[0])):
                row_repr += board[i][j] + '|'
                if board[i][j]=='e' or board[i][j]=='f':
                    row_repr+=' '
            print row_repr
            print('-' * len(row_repr) )
        print "\n----- PRINT BOARD FIN ----"
