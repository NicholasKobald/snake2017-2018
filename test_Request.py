import requests, time

BASE_URL = 'http://localhost:8080'

def make_start_request():
    pass

def make_move_request():
    pass

snake_one = {
    'name': '1',
    'state':'alive',
    'coords':[[8, 8], [8,7], [8,6]],
    'score':0
}
snake_two = {
    'name': '2',
    'state': 'alive',
    'coords': [[1,1], [1,2], [1,3]],
    'score':0
}

#tiles for snake two head/body
th = {'state':'head', 'snake':'2'}
st = {'state':'body', 'snake':'2'}

#tiles for snake one head/body
so = {'state':'body', 'snake':'1'}
oh = {'state':'head', 'snake':'1'}
#emptytile
et = {'state':'empty'}
#food title
ft = {'state':'food'}
#10 by 10
##0,0                                   9, 0
board = [
    [et, et, et, et, et, et, et, et, et, et],
    [et, th, et, et, et, et, et, et, et, et],
    [et, st, et, et, et, et, et, et, et, et],
    [et, st, et, et, et, et, et, et, et, et],
    [et, et, et, et, et, et, et, et, et, et],
    [et, et, et, et, et, et, et, et, et, et],
    [et, et, et, et, et, et, et, et, so, et],
    [et, et, et, et, et, et, et, et, so, et],
    [et, et, et, et, et, et, et, et, oh, et],
    [et, et, et, et, et, et, et, et, et, et],
]

request_data = dict(
    board=board,
    turn=1,
    snakes=[snake_one, snake_two],
    food=[]
)

#call to snake api
requests.post(BASE_URL + '/move', data=request_data)

exit() 

#    0,9                                   9,9
