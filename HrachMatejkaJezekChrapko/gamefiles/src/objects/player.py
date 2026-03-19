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

# --- OMEZENÍ POHYBU (Hranice obrazovky) ---
        
        # Šířka okna je 1000
        if self.x - self.radius < 0:
            self.x = self.radius
        elif self.x + self.radius > 1000:
            self.x = 1000 - self.radius

        # Výška okna je 800
        if self.y - self.radius < 0:
            self.y = self.radius
        elif self.y + self.radius > 800:
            self.y = 800 - self.radius

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)