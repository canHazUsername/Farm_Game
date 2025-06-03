import json

class GameState:
    def __init__(self, cols, rows, seed, terrain_map):
        self.cols = cols
        self.rows = rows
        self.seed = seed
        self.terrain_map = terrain_map  # list of dicts: {col, row, terrain}

    @classmethod
    def generate(cls, cols, rows, seed, terrain_map):
        return cls(cols, rows, seed, terrain_map)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        return cls(
            cols=data['cols'],
            rows=data['rows'],
            seed=data['seed'],
            terrain_map=data['map']
        )

    def save(self, filename):
        data = {
            'cols': self.cols,
            'rows': self.rows,
            'seed': self.seed,
            'map': self.terrain_map
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
