import pygame
import sys
from menus.main_menu import MainMenu
from menus.new_game import NewGameMenu


DEFAULT_WIDTH = 1024
DEFAULT_HEIGHT = 768
FPS = 60

class ScreenManager:
    def __init__(self, screen):
        self.screen = screen
        self.screens = {}
        self.current_screen = None
        self.create_screens("main_menu")

    def create_screens(self, start_screen):
        self.screens["main_menu"] = MainMenu(self.screen, self)
        self.screens["new_game"] = NewGameMenu(self.screen, self)
        self.current_screen = self.screens[start_screen]

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


def main():
    pygame.init()
    pygame.display.set_caption("Quiet Acres")
    screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    screen_manager = ScreenManager(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                screen_manager.resize(screen)
            else:
                screen_manager.handle_event(event)

        screen_manager.update()
        screen_manager.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
