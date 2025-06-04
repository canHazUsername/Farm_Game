import pygame
import os
import sys
import glob
from utils.background import load_scaled_background
from ui.menus.button import Button


class MainMenu:
    def __init__(self, screen, screen_manager):
        self.screen = screen
        self.screen_manager = screen_manager
        self.font = pygame.font.SysFont(None, 48)

        bg_path = os.path.join("assets", "main_menu", "MM_Background.png")
        self.bg_path = bg_path
        self.background, self.bg_offset = load_scaled_background(self.bg_path, screen.get_size())

        self.has_saves = self.check_for_saves()
        self.buttons = []
        self.create_buttons()

    def check_for_saves(self):
        save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sav")
        if not os.path.isdir(save_dir):
            return False
        return len(glob.glob(os.path.join(save_dir, "*.json"))) > 0

    def create_buttons(self):
        self.buttons.clear()
        button_width, button_height = 250, 62
        screen_width, screen_height = self.screen.get_size()
        start_y, y_offset = 250, 100

        labels = []
        if self.has_saves:
            labels.append(("Load Game", self.load_game))
        labels.extend([
            ("New Game", self.new_game),
            ("Options", self.options),
            ("Quit Game", self.quit_game),
        ])

        for i, (label, callback) in enumerate(labels):
            x = (screen_width - button_width) // 2
            y = start_y + i * y_offset
            rect = pygame.Rect(x, y, button_width, button_height)
            self.buttons.append(Button(rect, label, self.font, callback))

    def load_game(self):
        self.screen_manager.change_screen("load_game")

    def new_game(self):
        self.screen_manager.change_screen("new_game")

    def options(self):
        print("Options selected")

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, self.bg_offset)
        for button in self.buttons:
            button.draw(self.screen)

    def resize(self, new_screen):
        self.screen = new_screen
        self.background, self.bg_offset = load_scaled_background(self.bg_path, self.screen.get_size())
        self.create_buttons()
