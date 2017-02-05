#
#
#
#

def get_specific_snake(snake_list, snake_name):
    for snake in snake_list:
        if snake['name'] == snake_name:
            return snake['name']

def get_valid_moves(snake, board):
    print "In get valid moves" 
