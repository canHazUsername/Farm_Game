import os
from menus.main_menu import MainMenu
from menus.new_game import NewGameMenu
from menus.load_game import LoadGameMenu
from game.state import GameState
from game.render import RenderGameScreen


class ScreenManager:
    def __init__(self, screen):
        self.screen = screen
        self.screens = {}
        self.current_screen = None
        self.create_screens("main_menu")

    def create_screens(self, start_screen):
        self.screens["main_menu"] = MainMenu(self.screen, self)
        self.screens["new_game"] = NewGameMenu(self.screen, self)
        self.screens["load_game"] = LoadGameMenu(self.screen, self)
        self.current_screen = self.screens[start_screen]

    def load_game(self, filepath):
        state = GameState.load(filepath)
        self.screens["render"] = RenderGameScreen(self.screen, self, state, save_path=filepath)
        self.change_screen("render")

    def change_screen(self, screen_name):
        self.current_screen = self.screens[screen_name]

    def handle_event(self, event):
        self.current_screen.handle_event(event)

    def update(self):
        self.current_screen.update()

    def draw(self):
        self.current_screen.draw()

    def resize(self, new_screen):
        self.screen = new_screen
        for screen in self.screens.values():
            screen.resize(self.screen)
