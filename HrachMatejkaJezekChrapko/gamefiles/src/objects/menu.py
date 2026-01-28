import pygame
from objects.button import Button
from assets.colors import *

#definice menu s tlačítky

class Menu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        button_width = 200
        button_height = 60
        button_x = (screen_width - button_width) // 2
        
        self.start_button = Button(button_x, 250, button_width, button_height, "START", DARK_GRAY, WHITE)
        self.settings_button = Button(button_x, 330, button_width, button_height, "SETTINGS", DARK_GRAY, WHITE)
        self.exit_button = Button(button_x, 410, button_width, button_height, "EXIT", DARK_GRAY, WHITE)
        
        self.buttons = [self.start_button, self.settings_button, self.exit_button]

    #definice aktualizace menu

    def update(self, mouse_pos):
        for button in self.buttons:
            button.update(mouse_pos)

    #definice vykreslení menu

    def draw(self, screen):
        screen.fill(MENU_BG)
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
        elif self.exit_button.is_clicked(event):
            return "exit"
        return None