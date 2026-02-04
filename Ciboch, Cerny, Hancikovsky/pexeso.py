import pygame
import random
import time

pygame.init()

# herni settings
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 4, 4
TILE_SIZE = WIDTH // COLS

# barvy
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (100, 149, 237)
GREEN = (0, 200, 0)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Puzzle Game")

tiles = list(range(1, (ROWS * COLS // 2) + 1)) * 2
random.shuffle(tiles)
tiles = [tiles[i * COLS:(i + 1) * COLS] for i in range(ROWS)]

revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]

font = pygame.font.SysFont("arial", 36)
first = None
matches = 0
