import pygame
import os

#definice tlačítek pro menu

class Button:
    def __init__(self, x, y, width, height, text, color, text_color, font_size=36, image_path=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.hovered = False

        self.image = None
        if image_path and os.path.exists(image_path):
            raw = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(raw, (width, height))

#definice vykreslení tlačítka

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
            if self.hovered:
                hover_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
                hover_surf.fill((255, 255, 255, 40))
                screen.blit(hover_surf, self.rect)
        else:
            color = tuple(min(c + 30, 255) for c in self.color) if self.hovered else self.color
            pygame.draw.rect(screen, color, self.rect)
            pygame.draw.rect(screen, self.text_color, self.rect, 2)
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)

#definice efektu tlačítka

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

#definice kliknutí na tlačítko

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False