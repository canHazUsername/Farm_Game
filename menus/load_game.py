import pygame
import os
import glob
import time
from utils.background import load_scaled_background
from ui.menus.button import Button
from game.state import GameState
from game.render import RenderGameScreen


class LoadGameMenu:
    def __init__(self, screen, screen_manager):
        self.screen = screen
        self.screen_manager = screen_manager
        self.font = pygame.font.SysFont(None, 48)

        bg_path = os.path.join("assets", "main_menu", "MM_Background.png")
        self.bg_path = bg_path
        self.background, self.bg_offset = load_scaled_background(self.bg_path, screen.get_size())

        self.saves_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sav")
        os.makedirs(self.saves_dir, exist_ok=True)

        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        self.buttons.clear()

        button_width, button_height = 300, 62
        screen_width, screen_height = self.screen.get_size()
        start_y, y_offset = 250, 100

        options = [
            ("Continue", self.continue_game),
            ("Load Game", self.load_game_browser),
            ("Back", self.back_to_main)
        ]

        for i, (label, callback) in enumerate(options):
            x = (screen_width - button_width) // 2
            y = start_y + i * y_offset
            rect = pygame.Rect(x, y, button_width, button_height)
            self.buttons.append(Button(rect, label, self.font, callback))

    def get_most_recent_save(self):
        files = glob.glob(os.path.join(self.saves_dir, "*.json"))
        if not files:
            return None

        files.sort(key=os.path.getmtime, reverse=True)
        return files[0]

    def continue_game(self):
        recent_file = self.get_most_recent_save()
        if not recent_file:
            print("No saves found.")
            return

        state = GameState.load(recent_file)
        self.screen_manager.screens["render"] = RenderGameScreen(self.screen, self.screen_manager, state)
        self.screen_manager.change_screen("render")

    def load_game_browser(self):
        # Dynamically register browser screen
        from menus.load_game_browser import LoadGameBrowserMenu
        self.screen_manager.screens["load_game_browser"] = LoadGameBrowserMenu(self.screen, self.screen_manager)
        self.screen_manager.change_screen("load_game_browser")

    def back_to_main(self):
        self.screen_manager.change_screen("main_menu")

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
