# Autor: Ciboch, Černý, Hančikovský
# Popis: Jednoduchá hra Pexeso vytvořená v knihovně Pygame

import pygame
import random
import time
import sys

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

# MENU
def load_button(path, size):
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.smoothscale(image, size)
    return image

BUTTON_SIZE = (300, 120)

StartImg = load_button("StartButton.png", BUTTON_SIZE)
QuitImg = load_button("QuitButton.png", BUTTON_SIZE)

class Buttons:
    # Třída pro vytvoření klikatelného tlačítka
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.click = False

    def draw(self):
        action = False
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.click:
                action = True
                self.click = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.click = False

        win.blit(self.image, self.rect)
        return action

start_button = Buttons(150, 200, StartImg)
quit_button = Buttons(150, 320, QuitImg)

# MENU SMYČKA
game_state = "MENU"

while game_state == "MENU":
    win.fill(GRAY)

    if start_button.draw():
        game_state = "GAME"

    if quit_button.draw():
        pygame.quit()
        sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()

# PŘÍPRAVA HRY (PEXESO) - Od Roberta Hančikovskýho
tiles = list(range(1, (ROWS * COLS // 2) + 1)) * 2
random.shuffle(tiles)
tiles = [tiles[i * COLS:(i + 1) * COLS] for i in range(ROWS)]

revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]

font = pygame.font.SysFont("arial", 36)
first = None
matches = 0

# Funkce pro vykreslení herní plochy
def draw_board():
    win.fill(GRAY)
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if revealed[row][col]:
                pygame.draw.rect(win, GREEN, rect)
                num_text = font.render(str(tiles[row][col]), True, WHITE)
                win.blit(num_text, (col * TILE_SIZE + TILE_SIZE // 2 - 10, row * TILE_SIZE + TILE_SIZE // 2 - 20))
            else:
                pygame.draw.rect(win, BLUE, rect)
            pygame.draw.rect(win, WHITE, rect, 2)
    pygame.display.update()

def get_clicked_tile(pos):
    x, y = pos
    row, col = y // TILE_SIZE, x // TILE_SIZE
    return row, col

# Hlavní herní smyčka
running = True
while running: 
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            row, col = get_clicked_tile(pygame.mouse.get_pos())
            if not revealed[row][col]:
                revealed[row][col] = True
                if first is None:
                    first = (row, col)
                else:
                    r1, c1 = first
                    if tiles[row][col] != tiles[r1][c1]:
                        draw_board()
                        pygame.time.delay(800)
                        revealed[row][col] = False
                        revealed[r1][c1] = False
                    else:
                        matches += 1
                    first = None
    # Výhra - od Ondřeje Černýho
    if matches == (ROWS * COLS) // 2:
        win.fill(GRAY)
        win.blit(font.render("You Win!", True, WHITE), (WIDTH // 2 - 80, HEIGHT // 2 - 30))
        pygame.display.update()
        pygame.time.delay(2000)
        running = False

pygame.quit()