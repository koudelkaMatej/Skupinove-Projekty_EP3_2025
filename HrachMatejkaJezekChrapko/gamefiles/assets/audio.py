# ZDE BUDOU AUDIO SOUBORY A NASTAVENÍ PRO HERNÍ AUDIO
import pygame
import os

# Zjistíme cestu ke složce assets, kde je tento soubor
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def hraj_hudbu():
    # Cesta k souboru: assets/hudba/menu.mp3
    cesta = os.path.join(BASE_DIR, "hudba", "menu.mp3")
    
    if os.path.exists(cesta):
        pygame.mixer.init()
        pygame.mixer.music.load(cesta)
        pygame.mixer.music.set_volume(0.3) # Hlasitost na 30 %
        pygame.mixer.music.play(-1)        # -1 bude hrát pořád dokola
        print("Hudba úspěšně spuštěna!")
    else:
        print(f"Chyba: Hudba nenalezena na cestě: {cesta}")