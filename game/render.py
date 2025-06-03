import pygame
import numpy as np
from game.state import GameState


TERRAIN_COLORS = [
    (0, 119, 190),   
    (169, 169, 169), 
    (34, 139, 34),   
    (222, 184, 135), 
    (124, 252, 0)    
]

BORDER_COLOR = (80, 80, 80)
BACKGROUND_COLOR = (40, 40, 40)

def calculate_hex_size(cols, rows, window_width, window_height):
    map_pixel_width = (cols - 1) * 1.5 + 2
    map_pixel_height = rows * np.sqrt(3)
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
    pygame.draw.polygon(surface, BORDER_COLOR, points, 1)

class RenderGameScreen:
    def __init__(self, screen, screen_manager, game_state: GameState):
        self.screen = screen
        self.screen_manager = screen_manager
        self.game_state = game_state

        self.cols = game_state.cols
        self.rows = game_state.rows
        self.terrain_map = game_state.terrain_map

        self.hex_size = None
        self.offset_x = 0
        self.offset_y = 0
        self.recalculate_layout()

    def recalculate_layout(self):
        window_width, window_height = self.screen.get_size()
        self.hex_size = calculate_hex_size(self.cols, self.rows, window_width, window_height)
        map_pixel_width = int((self.cols - 1) * 1.5 * self.hex_size + 2 * self.hex_size)

        candidates = [
            hex_to_pixel(0, 0, self.hex_size),
            hex_to_pixel(1, 0, self.hex_size),
            hex_to_pixel(0, self.rows-1, self.hex_size),
            hex_to_pixel(1, self.rows-1, self.hex_size)
        ]

        all_vertices = []
        for center in candidates:
            all_vertices.extend(get_hex_vertices(center, self.hex_size))

        min_y = min(v[1] for v in all_vertices)
        max_y = max(v[1] for v in all_vertices)
        total_render_height = max_y - min_y

        self.offset_x = (window_width - map_pixel_width) // 2
        self.offset_y = (window_height - total_render_height) // 2 - min_y

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.screen_manager.change_screen("main_menu")

    def update(self):
        pass

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        for tile in self.terrain_map:
            col = tile['col']
            row = tile['row']
            terrain = tile['terrain']

            px, py = hex_to_pixel(col, row, self.hex_size)
            px += self.offset_x
            py += self.offset_y
            draw_hex(self.screen, (int(px), int(py)), TERRAIN_COLORS[terrain], self.hex_size)

    def resize(self, new_screen):
        self.screen = new_screen
        self.recalculate_layout()
