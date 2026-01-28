import pygame, sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets.settings import *
from assets.colors import *
from objects.player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Unnamed Dungeon")
        self.clock = pygame.time.Clock()
        self.state = "menu"
        self.player = Player()

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.state == "menu" and e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    self.state = "game"

    def update(self):
        if self.state == "game":
            self.player.update(pygame.key.get_pressed())

    def draw(self):
        if self.state == "menu":
            self.screen.fill(MENU_BG)
            font = pygame.font.Font(None, 72)
            title = font.render("Unnamed Dungeon", True, TITLE)
            self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
        else:
            self.screen.fill(BLACK)
            self.player.draw(self.screen)

        pygame.display.flip()
