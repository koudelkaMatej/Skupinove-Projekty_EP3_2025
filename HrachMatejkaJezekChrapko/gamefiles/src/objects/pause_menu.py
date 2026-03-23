import pygame
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from assets.colors import *
from objects.button import Button

# Pause menu zobrazené přes hru

class PauseMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        button_width = 200
        button_height = 60
        button_x = (screen_width - button_width) // 2
        center_y = screen_height // 2

        self.resume_button   = Button(button_x, center_y - 80, button_width, button_height, "RESUME",   DARK_GRAY, WHITE)
        self.settings_button = Button(button_x, center_y,      button_width, button_height, "SETTINGS", DARK_GRAY, WHITE)
        self.exit_button     = Button(button_x, center_y + 80, button_width, button_height, "EXIT",     DARK_GRAY, WHITE)

        self.buttons = [self.resume_button, self.settings_button, self.exit_button]
        self.font_title = pygame.font.Font(None, 72)

    def update(self, mouse_pos):
        for button in self.buttons:
            button.update(mouse_pos)

    def handle_click(self, event):
        if self.resume_button.is_clicked(event):
            return "resume"
        elif self.settings_button.is_clicked(event):
            return "settings"
        elif self.exit_button.is_clicked(event):
            return "exit"
        return None

    def draw(self, screen):
        # Poloprůhledný overlay přes hru
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        # Nadpis
        title_surf = self.font_title.render("PAUSED", True, TITLE)
        screen.blit(title_surf, title_surf.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 170)))

        for button in self.buttons:
            button.draw(screen)
