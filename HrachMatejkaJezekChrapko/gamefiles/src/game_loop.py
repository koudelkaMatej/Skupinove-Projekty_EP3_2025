#importy knihoven

import pygame, sys
import os
import subprocess
import webbrowser
import threading
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets.settings import *
from assets.colors import *
from assets.audio import play_menu_music, play_fight_music, play_game_over_music
from objects.gameplay import GameplayState
from objects.menu import Menu
from objects.settings_screen import SettingsScreen
from objects.pause_menu import PauseMenu
from objects.login_screen import LoginScreen

try:
    import requests as _requests
    _REQUESTS_OK = True
except ImportError:
    _REQUESTS_OK = False

_HERE = os.path.dirname(os.path.abspath(__file__))
_GRAFIKA = os.path.normpath(os.path.join(_HERE, "..", "assets", "images", "Grafika"))

#celkové nastavení herní smyčky

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("ShieldBash")
        self.clock = pygame.time.Clock()
        self.state = "login"
        self.gameplay = GameplayState(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.settings_screen = SettingsScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.pause_menu = PauseMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.login_screen = LoginScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
        self._settings_origin = "menu"
        self._web_process = None
        self.auth_token = None

        bg_raw = pygame.image.load(os.path.join(_GRAFIKA, "BG_game.png")).convert()
        self.bg_game = pygame.transform.scale(bg_raw, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Cesta k Flask serveru (Website/Run.py je o složku výš než gamefiles)
        self._web_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "Website", "Run.py"
        )

        self._game_over_music_played = False
        self._score_submitted = False

        # Spustit Flask server hned pri startu hry
        self._start_web_server()

        # Startovní hudba pro menu.
        play_menu_music()

    def _start_web_server(self):
        """Spusti Flask server na pozadi (jednou pri startu hry)."""
        if self._web_process is None or self._web_process.poll() is not None:
            self._web_process = subprocess.Popen(
                [sys.executable, self._web_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

    def _open_web(self):
        """Tlacitko Web v menu — jen otevri prohlizec, server uz bezi."""
        webbrowser.open("http://localhost:5000")

    def _quit(self):
        if self._web_process and self._web_process.poll() is None:
            self._web_process.terminate()
        pygame.quit()
        sys.exit()

    def _submit_score(self, score):
        if not _REQUESTS_OK or not self.auth_token:
            return
        def _thread():
            try:
                _requests.post(
                    "http://localhost:5000/api/score",
                    json={"token": self.auth_token, "score": score},
                    timeout=5,
                )
            except Exception:
                pass
        threading.Thread(target=_thread, daemon=True).start()

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

            if self.state == "login":
                token = self.login_screen.handle_event(e)
                if token:
                    self.auth_token = token
                    self.state = "menu"

                #nastavení tlačítek menu.
#pokud jsem v menu tak hraje hudba menu a sleduju kliky ktere udelaju stav z menu game
            if self.state == "menu":
                self.menu.update(mouse_pos)
                result = self.menu.handle_click(e)
                if result == "game":
                    self.state = "game"
                    self._game_over_music_played = False
                    self._score_submitted = False
                    self.gameplay.reset()
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

            if self.state == "game":
                result = self.gameplay.handle_event(e)
                if result == "menu":
                    self.state = "menu"
                    play_menu_music()

    def update(self):
        if self.state == "game":
            self.gameplay.update(pygame.key.get_pressed())
            if self.gameplay.game_over:
                if not self._game_over_music_played:
                    play_game_over_music()
                    self._game_over_music_played = True
                if not self._score_submitted:
                    self._score_submitted = True
                    self._submit_score(self.gameplay.score)

#definice settings okna

    def draw(self):
        if self.state == "login":
            self.login_screen.draw(self.screen)
        elif self.state == "menu":
            self.menu.draw(self.screen)
        elif self.state == "settings":
            if self._settings_origin == "menu":
                self.menu.draw(self.screen)
            else:
                self.screen.blit(self.bg_game, (0, 0))
            self.settings_screen.draw(self.screen)
        elif self.state == "pause":
            self.screen.blit(self.bg_game, (0, 0))
            self.pause_menu.draw(self.screen)
        else:
            self.gameplay.draw(self.screen, self.bg_game)

        pygame.display.flip()
