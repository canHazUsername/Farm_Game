import numpy as np
import random
import noise
import sys
import json
from scipy.spatial import Voronoi


# Terrain thresholds define biome zones
TERRAIN_THRESHOLDS = [0.3, 0.4, 0.55, 0.7]

# RGB colors for terrain types
TERRAIN_COLORS = [
    (0, 119, 190),   # Ocean
    (169, 169, 169), # Mountains
    (34, 139, 34),   # Forest
    (222, 184, 135), # Not Farmable Land
    (124, 252, 0)    # Farmable Land
]

# Global noise parameters
NOISE_SCALE = 0.05
NOISE_PARAMS_TEMPLATE = {
    'octaves': 3,
    'persistence': 0.5,
    'lacunarity': 2.0,
    'repeatx': 99999,
    'repeaty': 99999,
    'base': 0
}

VORONOI_SEED_COUNT = 60

def normalize(value, min_val=-1, max_val=1):
    return (value - min_val) / (max_val - min_val)

def generate_voronoi_points(count, cols, rows):
    points = np.random.rand(count, 2) * [cols, rows]
    return Voronoi(points)

def calculate_terrain(x, y, vor, noise_params):
    distances = np.linalg.norm(vor.points - np.array([x, y]), axis=1)
    region_idx = np.argmin(distances)
    voronoi_bias = region_idx / VORONOI_SEED_COUNT
    n = noise.pnoise2(x * NOISE_SCALE, y * NOISE_SCALE, **noise_params)
    n = normalize(n)
    return (n + voronoi_bias) / 2

def assign_terrain(value):
    for i, threshold in enumerate(TERRAIN_THRESHOLDS):
        if value < threshold:
            return i
    return len(TERRAIN_THRESHOLDS)

def generate_map(cols, rows, seed=None):
    if seed is None:
        seed = random.randint(0, 999999)

    random.seed(seed)
    np.random.seed(seed)

    noise_params = NOISE_PARAMS_TEMPLATE.copy()
    noise_params['base'] = seed

    vor = generate_voronoi_points(VORONOI_SEED_COUNT, cols, rows)
    terrain_map = []

    for col in range(cols):
        for row in range(rows):
            terrain_value = calculate_terrain(col, row, vor, noise_params)
            terrain_type = assign_terrain(terrain_value)
            terrain_map.append({'col': col, 'row': row, 'terrain': terrain_type})

    return (cols, rows, seed, terrain_map)

def save_map_to_file(map_data, filename):
    with open(filename, 'w') as f:
        json.dump(map_data, f, indent=2)
