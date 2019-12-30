import json
from app.objects.game_data_cache import GameDataCache

DATA_W_ONE_WAY_OUT = dict(
    data={
        'game': {'id': 'one-way-out'}, 'turn': 103, 'board': {'height': 11, 'width': 11, 'food': [{'x': 8, 'y': 1}, {'x': 0, 'y': 8}],
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

DATA_W_TWO_WAYS_OUT = dict(
    data={
        'game': {'id': 'two-ways-out'}, 'turn': 103, 'board': {'height': 11, 'width': 11, 'food': [{'x': 8, 'y': 1}, {'x': 0, 'y': 8}],
        'snakes': [
            {'id': 'other-3', 'name': 'other 3', 'health': 100,
            'body': [dict(x=5, y=3), dict(x=5, y=4), dict(x=5, y=5), dict(x=5, y=6), dict(x=6, y=6), dict(x=6, y=5), dict(x=7, y=5), dict(x=7, y=4)]},

            {'id': 'other-1', 'name': 'other 1', 'health': 100,
            'body': [dict(x=3, y=9), dict(x=2, y=9), dict(x=2, y=8), dict(x=1, y=8), dict(x=1, y=7), dict(x=0, y=7), dict(x=0, y=6), dict(x=1, y=6),]},

            {'id': 'snake-id-string', 'name': 'Sneky Snek', 'health': 100,
            'body': [dict(x=2, y=6), dict(x=3, y=6), dict(x=3, y=7), dict(x=4, y=7), dict(x=4, y=8), dict(x=5, y=8), dict(x=6, y=8), dict(x=6, y=9), dict(x=5, y=9), dict(x=4, y=9)]}
        ]},
        'you': {'id': 'snake-id-string', 'name': 'Sneky Snek', 'health': 100,
            'body': [dict(x=2, y=6), dict(x=3, y=6), dict(x=3, y=7), dict(x=4, y=7), dict(x=4, y=8), dict(x=5, y=8), dict(x=6, y=8), dict(x=6, y=9), dict(x=5, y=9), dict(x=4, y=9)]
        }
    },
    valid_moves=['left', 'down', 'up'],
    safe_moves=['left', 'up'],
    best_move='up',
)

DATA_HEAD_OR_WALL = dict(
    data={
        'game': {'id': 'head-or-wall'}, 'turn': 103, 'board': {'height': 11, 'width': 11,
        'food': [dict(x=10, y=0), dict(x=10, y=4), dict(x=7, y=3)],
        'snakes': [
            {'id': 'other-1', 'name': 'other 1', 'health': 100,
            'body': [dict(x=0, y=8), dict(x=1, y=8), dict(x=2, y=8), dict(x=3, y=8), dict(x=4, y=8), dict(x=5, y=8)]},

            {'id': 'snake-id-string', 'name': 'Sneky Snek', 'health': 100,
            'body': [dict(x=0, y=10), dict(x=1, y=10), dict(x=2, y=10), dict(x=3, y=10)]}
        ]},
        'you': {'id': 'snake-id-string', 'name': 'Sneky Snek', 'health': 70,
            'body': [dict(x=0, y=10), dict(x=1, y=10), dict(x=2, y=10), dict(x=3, y=10)]
        }
    },
    only_valid_move='up',
)

DATA_ONE_BIG_COMPONENT = dict(
    data={
        'game': {'id': 'one-big-component'}, 'turn': 103, 'board': {'height': 11, 'width': 11,
        'food': [dict(x=10, y=0), dict(x=10, y=4), dict(x=7, y=3)],
        'snakes': [
            {'id': 'other-1', 'name': 'other 1', 'health': 100,
            'body': [dict(x=8, y=7), dict(x=8, y=6), dict(x=8, y=5), dict(x=9, y=5), dict(x=9, y=6), dict(x=10, y=6), dict(x=10, y=5), dict(x=10, y=4), dict(x=10, y=3), dict(x=9, y=3), dict(x=9, y=4), dict(x=8, y=4), dict(x=7, y=4), dict(x=6, y=4), dict(x=6, y=5), dict(x=7, y=5), dict(x=7, y=6), dict(x=7, y=7), dict(x=7, y=8), dict(x=8, y=8), dict(x=9, y=8)]},

            {'id': 'snake-id-string', 'name': 'Sneky Snek', 'health': 100,
            'body': [dict(x=5, y=10), dict(x=5, y=9), dict(x=6, y=9), dict(x=6, y=8), dict(x=5, y=8), dict(x=5, y=7), dict(x=6, y=7), dict(x=6, y=6), dict(x=5, y=6), dict(x=5, y=5), dict(x=4, y=5), dict(x=3, y=5), dict(x=2, y=5), dict(x=1, y=5), dict(x=0, y=5), dict(x=0, y=6), dict(x=1, y=6), dict(x=1, y=7)]}
        ]},
        'you': {'id': 'snake-id-string', 'name': 'Sneky Snek', 'health': 70,
            'body': [dict(x=5, y=10), dict(x=5, y=9), dict(x=6, y=9), dict(x=6, y=8), dict(x=5, y=8), dict(x=5, y=7), dict(x=6, y=7), dict(x=6, y=6), dict(x=5, y=6), dict(x=5, y=5), dict(x=4, y=5), dict(x=3, y=5), dict(x=2, y=5), dict(x=1, y=5), dict(x=0, y=5), dict(x=0, y=6), dict(x=1, y=6), dict(x=1, y=5)]
        }
    },
    best_move='left',
    valid_moves=['left', 'right'],
)


def get_data_with_one_way_out():
    return (
        DATA_W_ONE_WAY_OUT['data'],
        DATA_W_ONE_WAY_OUT['valid_moves'],
        DATA_W_ONE_WAY_OUT['safe_moves'],
        DATA_W_ONE_WAY_OUT['best_move'],
    )

def get_data_with_two_ways_out():
    return (
        DATA_W_TWO_WAYS_OUT['data'],
        DATA_W_TWO_WAYS_OUT['valid_moves'],
        DATA_W_TWO_WAYS_OUT['safe_moves'],
        DATA_W_TWO_WAYS_OUT['best_move'],
    )

def get_data_with_one_valid_move():
    return (
        DATA_HEAD_OR_WALL['data'],
        DATA_HEAD_OR_WALL['only_valid_move'],
    )

def get_data_with_one_big_component():
    return (
        DATA_ONE_BIG_COMPONENT['data'],
        DATA_ONE_BIG_COMPONENT['best_move'],
        DATA_ONE_BIG_COMPONENT['valid_moves'],
    )

def get_empty_mock_game_data_cache():
    return GameDataCache(1)

def get_mock_game_data_cache(game_id, prev_foods):
    mock_game_data_cache = GameDataCache(1)
    mock_game_data_cache.new_game(game_id)
    mock_game_data_cache.update_food_list(game_id, prev_foods)
    return mock_game_data_cache