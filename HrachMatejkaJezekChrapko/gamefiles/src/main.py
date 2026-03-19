# Hlavní kod pro spuštění herní smyčky
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets.audio import play_menu_music
from game_loop import Game

if __name__ == "__main__":
    # Spustíme hudbu pro menu před vstupem do hlavní smyčky.
    play_menu_music()
    Game().run()
