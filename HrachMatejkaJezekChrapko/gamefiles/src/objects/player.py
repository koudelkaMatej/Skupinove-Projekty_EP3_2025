#importy knihoven

import pygame
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets.settings import KEYBINDS
from assets.colors import WHITE

#nastavení hráče, jednoduchý pohyb WSAD

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