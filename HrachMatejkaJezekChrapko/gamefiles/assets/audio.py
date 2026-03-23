# ZDE BUDOU AUDIO SOUBORY A NASTAVENÍ PRO HERNÍ AUDIO
import pygame
import os

# Zjistíme cestu ke složce assets, kde je tento soubor
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#default nastaveni
_master_volume = 0.3
_music_volume = 1.0
_effects_volume = 1.0
_current_track = None

def _apply_music_volume():
    if pygame.mixer.get_init():
        pygame.mixer.music.set_volume(_master_volume * _music_volume)

#vytvori mixer a nastavi hlasitost
def _init_mixer():
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    _apply_music_volume()

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

# Volume settery a gettery pro settings screen
def set_master_volume(val: float):
    global _master_volume
    _master_volume = max(0.0, min(1.0, val))
    _apply_music_volume()

def set_music_volume(val: float):
    global _music_volume
    _music_volume = max(0.0, min(1.0, val))
    _apply_music_volume()

def set_effects_volume(val: float):
    global _effects_volume
    _effects_volume = max(0.0, min(1.0, val))
    # Použije se až budou zvukové efekty implementovány

def get_master_volume() -> float:
    return _master_volume

def get_music_volume() -> float:
    return _music_volume

def get_effects_volume() -> float:
    return _effects_volume
