import pygame, sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets.settings import *
from assets.colors import *
from objects.player import Player
from objects.menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Unnamed Dungeon")
        self.clock = pygame.time.Clock()
        self.state = "menu"
        self.player = Player()
        self.menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.state == "menu":
                self.menu.update(mouse_pos)
                result = self.menu.handle_click(e)
                if result == "game":
                    self.state = "game"
                elif result == "settings":
                    self.state = "settings"
                elif result == "exit":
                    pygame.quit()
                    sys.exit()

            if self.state == "game" and e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.state = "menu"

    def update(self):
        if self.state == "game":
            self.player.update(pygame.key.get_pressed())

    def draw(self):
        if self.state == "menu":
            self.menu.draw(self.screen)
        elif self.state == "settings":
            self.screen.fill(MENU_BG)
            font = pygame.font.Font(None, 48)
            text = font.render("Settings (Coming Soon)", True, TITLE)
            self.screen.blit(text, text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
        else:
            self.screen.fill(BLACK)
            self.player.draw(self.screen)

        pygame.display.flip()
