import pygame

#definice tlačítek pro menu

class Button:
    def __init__(self, x, y, width, height, text, color, text_color, font_size=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.hovered = False

#definice vykreslení tlačítka

    def draw(self, screen):
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