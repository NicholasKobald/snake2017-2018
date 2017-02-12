from logic import *


#maybe fuck the classes?
class GameBoard(object):

    def __init__(self, start_req):
        self.env = start_req

    def update(self, move_list, snake_list):
        """
        Takes a list of moves, and modifies the internal board rep
        to correspond to the board after those moves take place
        """
        pass

    def undo(self, move):
        pass
    def __str__(self):
        self.print_board()
        return ''

    def convert_to_internal_board(self, board):
        internal_rep = []
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
        print "Board rep:"
        for i in range(len(board)):
            row_repr = ''
            for j in range(len(board[0])):
                row_repr += board[i][j]
                if board[i][j]=='e':
                    row_repr+=' '

            print row_repr



class MoveSet():
    def __init__(self):
        self.move_set_list = []

    def get_moveset_list(self):
        return self.move_set_list
