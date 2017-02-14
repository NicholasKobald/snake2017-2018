def gen_snake_list():
    snek_one = dict(
        name='1',
        id='hashashash',
        health_points=100,
        coords=[[4,1], [3,1], [2,1]]
    )
    snek_two = dict(
        name='2',
        id='watever',
        health_points=95,
        coords=[[6,8], [7,8], [8,8]]
    )
    return [snek_one, snek_two]

def gen_board(width=10, height=10):
    print "In gen board."
    board_list = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append('e')
        board_list.append(row)

    #TODO generate boards randomly???
    #is it worth generating json to POST to normally?
    board_list[2][1] = 's1'
    board_list[3][1] = 's1'
    board_list[4][1] = 'h1'

    board_list[6][8] = 'h2'
    board_list[7][8] = 's2'
    board_list[8][8] = 's2'

    board_list[5][5] = 'f'
    board_list[6][6] = 'f'
    return board_list
