import pygame
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from assets.colors import *
from objects.button import Button

_HERE = os.path.dirname(os.path.abspath(__file__))
GRAFIKA = os.path.normpath(os.path.join(_HERE, "..", "..", "assets", "images", "Grafika"))

# Pause menu zobrazené přes hru

class PauseMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        button_width = 350
        button_height = 82
        gap = 40
        total_w = 3 * button_width + 2 * gap
        bx = (screen_width - total_w) // 2
        by = screen_height - button_height - 80

        self.resume_button   = Button(bx,                        by, button_width, button_height, "", DARK_GRAY, WHITE, image_path=os.path.join(GRAFIKA, "RESUMEbutton.png"))
        self.settings_button = Button(bx + (button_width+gap),   by, button_width, button_height, "", DARK_GRAY, WHITE, image_path=os.path.join(GRAFIKA, "Settings.png"))
        self.exit_button     = Button(bx + 2*(button_width+gap), by, button_width, button_height, "", DARK_GRAY, WHITE, image_path=os.path.join(GRAFIKA, "EXITbutton.png"))

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
        screen.blit(title_surf, title_surf.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 280)))

        for button in self.buttons:
            button.draw(screen)
