import pygame
import os
from utils.background import load_scaled_background
from ui.menus.button import Button


class NewGameMenu:
    def __init__(self, screen, screen_manager):
        self.screen = screen
        self.screen_manager = screen_manager
        self.font = pygame.font.SysFont(None, 48)

        bg_path = os.path.join("assets", "main_menu", "MM_Background.png")
        self.bg_path = bg_path
        self.background, self.bg_offset = load_scaled_background(self.bg_path, screen.get_size())

        self.map_sizes = [30, 50, 100]
        self.selected_size = 30

        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        self.buttons.clear()
        button_width, button_height = 250, 62
        screen_width, screen_height = self.screen.get_size()
        start_y, y_offset = 200, 100

        # Map size buttons
        for i, size in enumerate(self.map_sizes):
            x = (screen_width - button_width) // 2
            y = start_y + i * y_offset
            rect = pygame.Rect(x, y, button_width, button_height)
            self.buttons.append(Button(rect, f"{size}x{size}", self.font, lambda s=size: self.select_size(s), selected=(self.selected_size == size)))

        # Start Game button
        y = start_y + len(self.map_sizes) * y_offset
        start_rect = pygame.Rect((screen_width - button_width) // 2, y, button_width, button_height)
        self.buttons.append(Button(start_rect, "Start Game", self.font, self.start_game))

        # Back button
        back_rect = pygame.Rect(20, 20, 150, 50)
        self.buttons.append(Button(back_rect, "Back", self.font, self.back_to_main))

    def select_size(self, size):
        self.selected_size = size
        self.create_buttons()  # update button highlights

    def start_game(self):
        print(f"Starting game with map size {self.selected_size}x{self.selected_size}")
        # In future: self.screen_manager.change_screen("actual_game", self.selected_size)

    def back_to_main(self):
        self.screen_manager.change_screen("main_menu")

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.background, self.bg_offset)
        for button in self.buttons:
            button.draw(self.screen)

    def resize(self, new_screen):
        self.screen = new_screen
        self.background, self.bg_offset = load_scaled_background(self.bg_path, self.screen.get_size())
        self.create_buttons()
