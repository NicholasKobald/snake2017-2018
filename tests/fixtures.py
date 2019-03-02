import json

DATA_W_DEAD_END = dict(
    data={
        'game': {'id': 'game-id-string'}, 'turn': 103, 'board': {'height': 11, 'width': 11, 'food': [{'x': 8, 'y': 1}, {'x': 0, 'y': 8}],
        'snakes': [
            {'id': 'other-3', 'name': 'other 3', 'health': 100,
            'body': [dict(x=5, y=3), dict(x=5, y=4), dict(x=5, y=5), dict(x=5, y=6), dict(x=6, y=6), dict(x=6, y=5), dict(x=7, y=5), dict(x=7, y=4)]},

            {'id': 'other-2', 'name': 'other 2', 'health': 100,
            'body': [dict(x=3, y=3), dict(x=2, y=3), dict(x=2, y=4), dict(x=1, y=4), dict(x=0, y=4), dict(x=0, y=5), dict(x=1, y=5), dict(x=2, y=5), dict(x=3, y=5), dict(x=4, y=5)]},

            {'id': 'other-1', 'name': 'other 1', 'health': 100,
            'body': [dict(x=3, y=9), dict(x=2, y=9), dict(x=2, y=8), dict(x=1, y=8), dict(x=1, y=7), dict(x=0, y=7), dict(x=0, y=6), dict(x=1, y=6),]},

            {'id': 'snake-id-string', 'name': 'Sneky Snek', 'health': 100,
            'body': [dict(x=2, y=6), dict(x=3, y=6), dict(x=3, y=7), dict(x=4, y=7), dict(x=4, y=8), dict(x=5, y=8), dict(x=6, y=8), dict(x=6, y=9), dict(x=5, y=9), dict(x=4, y=9)]}
        ]},
        'you': {'id': 'snake-id-string', 'name': 'Sneky Snek', 'health': 100,
            'body': [dict(x=2, y=6), dict(x=3, y=6), dict(x=3, y=7), dict(x=4, y=7), dict(x=4, y=8), dict(x=5, y=8), dict(x=6, y=8), dict(x=6, y=9), dict(x=5, y=9), dict(x=4, y=9)]
        }
    },
    valid_moves=['left', 'down'],
    safe_moves=['left'],
    best_move='left',
)


def get_data_with_dead_end_position():
    return (
        DATA_W_DEAD_END['data'],
        DATA_W_DEAD_END['valid_moves'],
        DATA_W_DEAD_END['safe_moves'],
        DATA_W_DEAD_END['best_move'],
    )