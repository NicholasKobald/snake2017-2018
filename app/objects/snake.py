class Snake():
    def __init__(self, snake_id, coords, health, ate_last_turn):
        """
        Params:
            snake_id (str).
            coords (list): e.g. [ {x=0, y=0}, {x=1, y=0} ]
            health (int): in range [0,100].
            ate_last_turn (bool).
        """
        self.id = snake_id
        self.coords = coords
        self.health = health
        self.ate_last_turn = ate_last_turn
        self.head = (coords[0]['x'], coords[0]['y'])
        self.length = len(coords)