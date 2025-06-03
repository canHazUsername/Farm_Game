from scipy.spatial import Voronoi
import numpy as np
import pygame
import noise
import random
import sys


# REFS:
#  https://www.redblobgames.com/x/2022-voronoi-maps-tutorial/
#  https://www.martinmcbride.org/post/2021/voronoi-diagrams-with-scipy/
#  http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/

# CONFIG
# Default window size (resizable)
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

# Map size in hex tiles
MAP_COLS = 50  # columns
MAP_ROWS = 50  # rows

# Voronoi seed count affects biome regions
VORONOI_SEED_COUNT = 60

# Noise parameters control terrain variation
NOISE_SCALE = 0.05
NOISE_PARAMS = {
    'octaves': 3,
    'persistence': 0.5,
    'lacunarity': 2.0,
    'repeatx': 99999,
    'repeaty': 99999,
    'base': 0
}

# Seed for consistent randomization
RANDOM_SEED = random.randint(0, 999999) if len(sys.argv) < 2 else int(sys.argv[1])
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
NOISE_PARAMS['base'] = RANDOM_SEED

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

# HEX & MAP MATH
def normalize(value, min_val=-1, max_val=1):
    return (value - min_val) / (max_val - min_val)

def generate_voronoi_points(count, cols, rows):
    points = np.random.rand(count, 2) * [cols, rows]
    return Voronoi(points)

def calculate_terrain(x, y, vor):
    distances = np.linalg.norm(vor.points - np.array([x, y]), axis=1)
    region_idx = np.argmin(distances)
    voronoi_bias = region_idx / VORONOI_SEED_COUNT
    n = noise.pnoise2(x * NOISE_SCALE, y * NOISE_SCALE, **NOISE_PARAMS)
    n = normalize(n)
    return (n + voronoi_bias) / 2

def assign_terrain(value):
    for i, threshold in enumerate(TERRAIN_THRESHOLDS):
        if value < threshold:
            return i
    return len(TERRAIN_THRESHOLDS)

def generate_map():
    vor = generate_voronoi_points(VORONOI_SEED_COUNT, MAP_COLS, MAP_ROWS)
    terrain_map = []
    for col in range(MAP_COLS):
        for row in range(MAP_ROWS):
            terrain_value = calculate_terrain(col, row, vor)
            terrain_type = assign_terrain(terrain_value)
            terrain_map.append((col, row, terrain_type))
    return terrain_map

def calculate_hex_size(window_width, window_height):
    map_pixel_width = (MAP_COLS - 1) * 1.5 + 2
    map_pixel_height = MAP_ROWS * np.sqrt(3)
    width_per_hex = window_width / map_pixel_width
    height_per_hex = window_height / map_pixel_height
    return min(width_per_hex, height_per_hex)

def hex_to_pixel(col, row, size):
    x = size * 3/2 * col
    y = size * np.sqrt(3) * (row + 0.5 * (col % 2))
    return (x, y)

def get_hex_vertices(center, size):
    vertices = []
    for i in range(6):
        angle = np.pi / 180 * (60 * i)
        dx = size * np.cos(angle)
        dy = size * np.sin(angle)
        vertices.append((center[0] + dx, center[1] + dy))
    return vertices

def draw_hex(surface, pos, color, size):
    points = get_hex_vertices(pos, size)
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, (0, 0, 0), points, 1)

# MAIN
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption(f"Hex Terrain Map (Seed {RANDOM_SEED})")
    
    terrain_map = generate_map()

    running = True
    while running:
        window_size = screen.get_size()
        hex_size = calculate_hex_size(*window_size)
        map_pixel_width = int((MAP_COLS - 1) * 1.5 * hex_size + 2 * hex_size)
        
        # Calculate true bounding box using vertices of both even and odd columns
        candidates = [
            hex_to_pixel(0, 0, hex_size),
            hex_to_pixel(1, 0, hex_size),
            hex_to_pixel(0, MAP_ROWS-1, hex_size),
            hex_to_pixel(1, MAP_ROWS-1, hex_size)
        ]

        all_vertices = []
        for center in candidates:
            all_vertices.extend(get_hex_vertices(center, hex_size))

        min_y = min([v[1] for v in all_vertices])
        max_y = max([v[1] for v in all_vertices])
        total_render_height = max_y - min_y
        
        offset_x = (window_size[0] - map_pixel_width) // 2
        offset_y = (window_size[1] - total_render_height) // 2 - min_y

        screen.fill((255, 255, 255))
        
        for col, row, terrain_type in terrain_map:
            px, py = hex_to_pixel(col, row, hex_size)
            px += offset_x
            py += offset_y
            draw_hex(screen, (int(px), int(py)), TERRAIN_COLORS[terrain_type], hex_size)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()

    pygame.quit()

if __name__ == "__main__":
    main()
