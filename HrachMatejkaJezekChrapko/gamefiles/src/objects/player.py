import pygame
from constants.settings import KEYBINDS
from constants.colors import WHITE

class Player:
    def __init__(self):
        self.x = 500
        self.y = 350
        self.speed = 5
        self.radius = 15

    def update(self, keys):
        if keys[KEYBINDS["up"]]:
            self.y -= self.speed
        if keys[KEYBINDS["down"]]:
            self.y += self.speed
        if keys[KEYBINDS["left"]]:
            self.x -= self.speed
        if keys[KEYBINDS["right"]]:
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)
