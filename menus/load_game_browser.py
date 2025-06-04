import pygame
import os
import glob
from utils.background import load_scaled_background
from ui.menus.button import Button


class LoadGameBrowserMenu:
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

        files = glob.glob(os.path.join(self.saves_dir, "*.json"))
        files.sort(key=os.path.getmtime, reverse=True)

        button_width, button_height = 700, 50
        screen_width, screen_height = self.screen.get_size()
        start_y, y_offset = 150, 60

        if not files:
            rect = pygame.Rect((screen_width - button_width) // 2, start_y, button_width, button_height)
            self.buttons.append(Button(rect, "No saves found", self.font, lambda: None))
        else:
            for i, filepath in enumerate(files):
                filename = os.path.basename(filepath)
                x = (screen_width - button_width) // 2
                y = start_y + i * y_offset
                rect = pygame.Rect(x, y, button_width, button_height)
                self.buttons.append(Button(rect, filename, self.font, lambda f=filepath: self.load_save(f)))

        back_rect = pygame.Rect(20, 20, 150, 50)
        self.buttons.append(Button(back_rect, "Back", self.font, self.back_to_load_menu))

    def load_save(self, filepath):
        self.screen_manager.load_game(filepath)

    def back_to_load_menu(self):
        self.screen_manager.change_screen("load_game")

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
