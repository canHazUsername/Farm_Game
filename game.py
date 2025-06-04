import pygame
import sys
from game.screen_manager import ScreenManager


DEFAULT_WIDTH, DEFAULT_HEIGHT = 1024, 768
FPS = 60

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
