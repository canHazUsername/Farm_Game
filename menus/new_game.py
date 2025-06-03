import pygame
import os
import time
from utils.background import load_scaled_background
from ui.menus.button import Button
from map_gen import map_generator
from game.state import GameState
from game.render import RenderGameScreen


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

        for i, size in enumerate(self.map_sizes):
            x = (screen_width - button_width) // 2
            y = start_y + i * y_offset
            rect = pygame.Rect(x, y, button_width, button_height)
            self.buttons.append(Button(
                rect, 
                f"{size}x{size}", 
                self.font, 
                lambda s=size: self.select_size(s),
                selected=(self.selected_size == size)
            ))

        y = start_y + len(self.map_sizes) * y_offset
        start_rect = pygame.Rect((screen_width - button_width) // 2, y, button_width, button_height)
        self.buttons.append(Button(start_rect, "Start Game", self.font, self.start_game))

        back_rect = pygame.Rect(20, 20, 150, 50)
        self.buttons.append(Button(back_rect, "Back", self.font, self.back_to_main))

    def select_size(self, size):
        self.selected_size = size
        self.create_buttons()

    def start_game(self):
        # Generate map
        cols, rows = self.selected_size, self.selected_size
        cols, rows, seed, terrain_map = map_generator.generate_map(cols, rows)

        # Build game state object
        state = GameState(cols, rows, seed, terrain_map)

        # Save to file
        save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sav")
        os.makedirs(save_dir, exist_ok=True)
        filename = f"map_{cols}x{rows}_{seed}_{int(time.time())}.json"
        filepath = os.path.join(save_dir, filename)
        state.save(filepath)
        print(f"Map saved to {filepath}")

        # Pass state directly to renderer
        self.screen_manager.screens["render"] = RenderGameScreen(self.screen, self.screen_manager, state)
        self.screen_manager.change_screen("render")

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
