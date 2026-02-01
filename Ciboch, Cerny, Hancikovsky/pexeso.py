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