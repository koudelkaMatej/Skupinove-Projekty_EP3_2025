#importy knihoven

import pygame, sys
import os
import subprocess
import webbrowser
import threading
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets.settings import *
from assets.colors import *
from assets.audio import play_menu_music, play_fight_music
from objects.player import Player
from objects.menu import Menu
from objects.settings_screen import SettingsScreen
from objects.pause_menu import PauseMenu

#celkové nastavení herní smyčky

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Unnamed Dungeon")
        self.clock = pygame.time.Clock()
        self.state = "menu"
        self.player = Player()
        self.menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.settings_screen = SettingsScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.pause_menu = PauseMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self._settings_origin = "menu"
        self._web_process = None

        # Cesta k Flask serveru (Website/Run.py je o složku výš než gamefiles)
        self._web_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "Website", "Run.py"
        )

        # Startovní hudba pro menu.
        play_menu_music()

    def _open_web(self):
        # Pokud server ještě neběží, spusť ho
        if self._web_process is None or self._web_process.poll() is not None:
            self._web_process = subprocess.Popen(
                [sys.executable, self._web_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        # Otevři prohlížeč po 1.5s aby Flask stihl nastartovat
        threading.Timer(1.5, webbrowser.open, args=["http://localhost:5000"]).start()

    def _quit(self):
        if self._web_process and self._web_process.poll() is None:
            self._web_process.terminate()
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        #e = klik pokud kliknu na x tak se zavre
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self._quit()

                #nastavení tlačítek menu.
#pokud jsem v menu tak hraje hudba menu a sleduju kliky ktere udelaju stav z menu game
            if self.state == "menu":
                self.menu.update(mouse_pos)
                result = self.menu.handle_click(e)
                if result == "game":
                    self.state = "game"
                    play_fight_music()
                elif result == "settings":
                    self._settings_origin = "menu"
                    self.state = "settings"
                elif result == "web":
                    self._open_web()
                elif result == "exit":
                    self._quit()

            if self.state == "pause":
                self.pause_menu.update(mouse_pos)
                result = self.pause_menu.handle_click(e)
                if result == "resume":
                    self.state = "game"
                elif result == "settings":
                    self._settings_origin = "pause"
                    self.state = "settings"
                elif result == "exit":
                    self.state = "menu"
                    play_menu_music()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    self.state = "game"

            if self.state == "settings":
                result = self.settings_screen.handle_event(e)
                if result == "menu":
                    self.state = self._settings_origin
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    self.state = self._settings_origin

#kdy zmacku esc ve hre, zobrazí se pause menu
            if self.state == "game" and e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.state = "pause"

    def update(self):
        if self.state == "game":
            self.player.update(pygame.key.get_pressed())

#definice settings okna

    def draw(self):
        if self.state == "menu":
            self.menu.draw(self.screen)
        elif self.state == "settings":
            self.settings_screen.draw(self.screen)
        elif self.state == "pause":
            # nejdříve vykreslí hru, pak pause overlay přes ni
            self.screen.fill(BLACK)
            self.player.draw(self.screen)
            self.pause_menu.draw(self.screen)
        else:
            self.screen.fill(BLACK)
            self.player.draw(self.screen)

        pygame.display.flip()
