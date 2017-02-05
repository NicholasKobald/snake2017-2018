import requests

snake_one = {
    'name': '1',
    'state':'alive',
    'coords':[[8, 8], [8,7], [8,6]]
}
snake_two = {
    'name': '2',
    'state': 'alive',
    'coords': [[1,1], [1,2], [1,3]]
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
#    0,9                                   9,9
