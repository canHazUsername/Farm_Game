import pygame
import io


def load_scaled_background(bg_path, screen_size):
    # Completely bypass pygame's internal cache
    with open(bg_path, 'rb') as f:
        file_bytes = f.read()
    image_file = io.BytesIO(file_bytes)
    bg_surface = pygame.image.load(image_file).convert_alpha()

    bg_width, bg_height = bg_surface.get_size()
    screen_width, screen_height = screen_size

    scale_factor = screen_height / bg_height
    new_width = int(bg_width * scale_factor)
    new_height = screen_height

    scaled_bg = pygame.transform.smoothscale(bg_surface, (new_width, new_height))
    offset_x = (screen_width - new_width) // 2
    offset_y = 0

    return scaled_bg, (offset_x, offset_y)
