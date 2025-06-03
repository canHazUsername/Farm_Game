import pygame

class Button:
    def __init__(self, rect, label, font, callback, selected=False):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.font = font
        self.callback = callback
        self.selected = selected

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = (0, 255, 0, 191) if self.selected else (0, 0, 0, 191)

        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        surface.fill(color)
        screen.blit(surface, self.rect.topleft)

        if self.rect.collidepoint(mouse_pos):
            hover = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            hover.fill((255, 255, 255, 32))
            screen.blit(hover, self.rect.topleft)

        text_surf = self.font.render(self.label, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
