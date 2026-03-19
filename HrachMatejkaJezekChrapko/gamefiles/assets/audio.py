# ZDE BUDOU AUDIO SOUBORY A NASTAVENÍ PRO HERNÍ AUDIO
import pygame
import os

# Zjistíme cestu ke složce assets, kde je tento soubor
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#default nastaveni
_DEFAULT_VOLUME = 0.3
_current_track = None

#vytvori mixer a nastavi hlasitost
def _init_mixer(volume: float = _DEFAULT_VOLUME):
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    pygame.mixer.music.set_volume(volume)

#hraje hudba pokud nic nehraje
def _play_track(filename: str, loops: int = -1):

    global _current_track

    if _current_track == filename and pygame.mixer.music.get_busy():
        return
#najde hudbu v assets
    cesta = os.path.join(BASE_DIR, "hudba", filename)

    if not os.path.exists(cesta):
        print(f"Chyba: Hudba nenalezena na cestě: {cesta}")
        return

    _init_mixer()
    try:
        pygame.mixer.music.load(cesta)
        pygame.mixer.music.play(loops)
        _current_track = filename
    except Exception as e:
        print(f"Chyba při přehrávání hudby {cesta}: {e}")


def play_menu_music():
    _play_track("menu.mp3")


def play_fight_music():
    _play_track("fight.mp3")

#mohu zneuzit na nastaveni tlacitka na zruseni hudby
def stop_music():
    global _current_track
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
    _current_track = None

#mohu zneuzit na nastaveni tlacitka na zastaveni hudby
def pause_music():
    global _current_track
    if pygame.mixer.get_init():
        pygame.mixer.music.pause()

