#importy knihoven

import pygame
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets.settings import KEYBINDS
from assets.colors import WHITE
from assets.audio import play_fight_music, play_menu_music, stop_music

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
        
       
        if self.x - self.radius < 0:
            self.x = self.radius
        elif self.x + self.radius > 1920:
            self.x = 1920 - self.radius

        
        if self.y - self.radius < 0:
            self.y = self.radius
        elif self.y + self.radius > 1080:
            self.y = 1080 - self.radius

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)