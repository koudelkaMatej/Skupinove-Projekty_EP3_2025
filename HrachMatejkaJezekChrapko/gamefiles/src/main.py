# Hlavní kod pro spuštění herní smyčky
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets.audio import hraj_hudbu
from game_loop import Game

if __name__ == "__main__":
    hraj_hudbu() 
    Game().run()
