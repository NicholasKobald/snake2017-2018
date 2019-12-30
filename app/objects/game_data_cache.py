from time import time


class GameDataCache():
    def __init__(self, max_concurrent_games):
        self.max_size = max_concurrent_games
        self.entries = dict()

    def new_game(self, game_id):
        if self.size() >= self.max_size:
            self._remove_entry()
        self.entries[str(game_id)] = dict(last_accessed=time())

    def get_food_list(self, game_id):
        if game_id not in self.entries:
            return None
        food_coords = self.entries[game_id]['food_coords']
        self.entries[game_id]['last_accessed'] = time()
        return food_coords

    def update_food_list(self, game_id, food_coords):
        """
        Returns:
            (bool): True iff value was successfully updated.
        """
        if game_id not in self.entries:
            return False
        self.entries[game_id]['food_coords'] = food_coords
        self.entries[game_id]['last_accessed'] = time()
        return True

    def size(self):
        return len(self.entries.keys())

    def remove_entry(self, game_id):
        """
        Returns:
            (bool): True iff a value was successfully removed.
        """
        if game_id not in self.entries:
            return False
        del self.entries[game_id]
        return game_id not in self.entries

    def _remove_entry(self):
        """Removes entry that was accessed least recently.
        Returns:
            (bool): True iff a value was successfully removed.
        """
        game_id_to_remove = None
        oldest_timestamp = time()
        for game_id, data in self.entries.items():
            if data['last_accessed'] < oldest_timestamp:
                game_id_to_remove = game_id

        if game_id_to_remove is None:
            print("ERROR: could not find an item to remove (probably bc of a bug).")
            return False

        return self.remove_entry(game_id_to_remove)
