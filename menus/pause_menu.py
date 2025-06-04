import pygame
import os
import time
from ui.menus.button import Button
from menus.load_game_browser import LoadGameBrowserMenu


class PauseMenu:
    def __init__(self, screen, game_screen):
        self.screen = screen
        self.game_screen = game_screen
        self.font = pygame.font.SysFont(None, 48)
        self.create_buttons()

    def create_buttons(self):
        self.buttons = []
        button_width, button_height = 300, 62
        screen_width, screen_height = self.screen.get_size()
        start_y, y_offset = 200, 80

        options = [
            ("Resume", self.resume_game),
            ("Save", self.game_screen.quick_save),
            ("Load", self.load_game),
            ("Options", self.options),
            ("Main Menu", self.back_to_main_menu),
            ("Quit", self.quit_game)
        ]

        for i, (label, callback) in enumerate(options):
            x = (screen_width - button_width) // 2
            y = start_y + i * y_offset
            rect = pygame.Rect(x, y, button_width, button_height)
            self.buttons.append(Button(rect, label, self.font, callback))

    def resume_game(self):
        self.game_screen.is_paused = False

    def load_game(self):
        self.game_screen.screen_manager.screens["load_game_browser"] = LoadGameBrowserMenu(
            self.screen, self.game_screen.screen_manager)
        self.game_screen.screen_manager.change_screen("load_game_browser")

    def options(self):
        print("Options selected")

    def back_to_main_menu(self):
        self.game_screen.screen_manager.change_screen("main_menu")

    def quit_game(self):
        pygame.quit()
        exit()

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def update(self):
        pass

    def draw(self):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 192))
        self.screen.blit(overlay, (0, 0))
        for button in self.buttons:
            button.draw(self.screen)

    def resize(self, new_screen):
        self.screen = new_screen
        self.create_buttons()
