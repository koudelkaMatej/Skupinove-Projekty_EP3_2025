import pygame
import os
from objects.button import Button
from assets.colors import *
from assets.fonts import *

_HERE = os.path.dirname(os.path.abspath(__file__))
GRAFIKA = os.path.normpath(os.path.join(_HERE, "..", "..", "assets", "images", "Grafika"))

#definice menu s tlačítky

class Menu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        bg_raw = pygame.image.load(os.path.join(GRAFIKA, "Background.png")).convert()
        self.background = pygame.transform.scale(bg_raw, (screen_width, screen_height))

        button_width = 350
        button_height = 82
        gap = 40
        total_w = 4 * button_width + 3 * gap
        bx = (screen_width - total_w) // 2
        by = screen_height - button_height - 80

        self.start_button    = Button(bx,                        by, button_width, button_height, "", DARK_GRAY, WHITE, image_path=os.path.join(GRAFIKA, "Startbutton.png"))
        self.settings_button = Button(bx + (button_width+gap),   by, button_width, button_height, "", DARK_GRAY, WHITE, image_path=os.path.join(GRAFIKA, "Settings.png"))
        self.web_button      = Button(bx + 2*(button_width+gap), by, button_width, button_height, "", DARK_GRAY, WHITE, image_path=os.path.join(GRAFIKA, "WEBbutton.png"))
        self.exit_button     = Button(bx + 3*(button_width+gap), by, button_width, button_height, "", DARK_GRAY, WHITE, image_path=os.path.join(GRAFIKA, "EXITbutton.png"))

        self.buttons = [self.start_button, self.settings_button, self.web_button, self.exit_button]

    #definice aktualizace menu

    def update(self, mouse_pos):
        for button in self.buttons:
            button.update(mouse_pos)

    #definice vykreslení menu

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        font = pygame.font.Font(None, 72)
        title = font.render("Unnamed Dungeon", True, TITLE)
        screen.blit(title, title.get_rect(center=(self.screen_width//2, 80)))
        
        for button in self.buttons:
            button.draw(screen)

    #definice reakce na kliknutí v menu

    def handle_click(self, event):
        if self.start_button.is_clicked(event):
            return "game"
        elif self.settings_button.is_clicked(event):
            return "settings"
        elif self.web_button.is_clicked(event):
            return "web"
        elif self.exit_button.is_clicked(event):
            return "exit"
        return None