import pygame
import numpy as np


MIN_ZOOM = 0.5
MAX_ZOOM = 6.0
ZOOM_SPEED = 0.1
EDGE_SCROLL_SPEED = 10
EDGE_MARGIN = 50

class CameraController:
    def __init__(self):
        self.zoom = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.is_dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.is_dragging = True
            elif event.button == 4:
                self.zoom = min(self.zoom + ZOOM_SPEED, MAX_ZOOM)
            elif event.button == 5:
                self.zoom = max(self.zoom - ZOOM_SPEED, MIN_ZOOM)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False

        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            dx, dy = event.rel
            self.pan_x += dx
            self.pan_y += dy

    def update(self, screen_size):
        mx, my = pygame.mouse.get_pos()
        width, height = screen_size

        if mx <= EDGE_MARGIN:
            self.pan_x += EDGE_SCROLL_SPEED
        if mx >= width - EDGE_MARGIN:
            self.pan_x -= EDGE_SCROLL_SPEED
        if my <= EDGE_MARGIN:
            self.pan_y += EDGE_SCROLL_SPEED
        if my >= height - EDGE_MARGIN:
            self.pan_y -= EDGE_SCROLL_SPEED
