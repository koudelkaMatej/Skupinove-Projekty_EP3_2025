# Autor: Ciboch, Černý, Hančikovský
# Popis: Jednoduchá hra Pexeso vytvořená v knihovně Pygame

import pygame
import random
import sys
import os
import sqlite3

# Připojení k databázi
conn = sqlite3.connect("memory.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

# Tabulka hráčů
# Tabulka hráčů
cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
)
""")

# Tabulka her
cursor.execute("""
CREATE TABLE IF NOT EXISTS games (
    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    score INTEGER,
    moves INTEGER,

    FOREIGN KEY(player_id) REFERENCES players(player_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS player_themes (
    player_id INTEGER,
    theme_id INTEGER,

    PRIMARY KEY(player_id, theme_id),

    FOREIGN KEY(player_id) REFERENCES players(player_id),
    FOREIGN KEY(theme_id) REFERENCES themes(theme_id)
)
""")

conn.commit()

pygame.init()

player_name = input("Zadej jméno hráče: ")

# HERNÍ NASTAVENÍ
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 4, 4
TILE_SIZE = WIDTH // COLS

# BARVY
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (100, 149, 237)
GREEN = (0, 200, 0)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Puzzle Game")

font = pygame.font.SysFont("arial", 36)

# NAČÍTÁNÍ OBRÁZKŮ
def load_button(relative_path, size):
    image = pygame.image.load(relative_path).convert_alpha()
    image = pygame.transform.smoothscale(image, size)
    return image

# MENU TLAČÍTKA
BUTTON_SIZE = (300, 120)

StartImg = load_button("StartButton.png", BUTTON_SIZE)
QuitImg = load_button("QuitButton.png", BUTTON_SIZE)

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False

    def draw(self):
        action = False
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                action = True
                self.clicked = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        win.blit(self.image, self.rect)
        return action

start_button = Button(150, 200, StartImg)
quit_button = Button(150, 340, QuitImg)

# MENU SMYČKA
game_state = "MENU"
clock = pygame.time.Clock()

while game_state == "MENU":
    clock.tick(60)
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
first = None
matches = 0
moves = 0

# Funkce pro vykreslení herní plochy
# Vykreslí herní plochu
def draw_board():
    win.fill(GRAY)
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if revealed[row][col]:
                pygame.draw.rect(win, GREEN, rect)
                text = font.render(str(tiles[row][col]), True, WHITE)
                win.blit(
                    text,
                    (col * TILE_SIZE + TILE_SIZE // 2 - 10,
                     row * TILE_SIZE + TILE_SIZE // 2 - 20)
                )
            else:
                pygame.draw.rect(win, BLUE, rect)

            pygame.draw.rect(win, WHITE, rect, 2)

    pygame.display.update()

# Vrátí pozici kliknutého políčka
def get_clicked_tile(pos):
    x, y = pos
    return y // TILE_SIZE, x // TILE_SIZE

# Uloží výsledek hráče do databáze
def save_score(name, score, moves):

    # Kontrola jestli hráč už existuje
    cursor.execute(
        "SELECT player_id FROM players WHERE name = ?",
        (name,)
    )

    player = cursor.fetchone()

    # Pokud neexistuje -> vytvoří se
    if player is None:
        cursor.execute(
            "INSERT INTO players(name) VALUES(?)",
            (name,)
        )

        conn.commit()

        player_id = cursor.lastrowid

    else:
        player_id = player[0]

    # Uložení hry
    cursor.execute(
        """
        INSERT INTO games(player_id, score, moves)
        VALUES(?, ?, ?)
        """,
        (player_id, score, moves)
    )

    conn.commit()
    
# HERNÍ SMYČKA
running = True
while running:
    clock.tick(60)
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            row, col = get_clicked_tile(pygame.mouse.get_pos())

            if row < ROWS and col < COLS and not revealed[row][col]:
                revealed[row][col] = True

                if first is None:
                    first = (row, col)
                else:
                    moves += 1
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
    score = max(0, 200 - moves * 5)

    if matches == (ROWS * COLS) // 2:
        win.fill(GRAY)
        score_text = font.render(f"Tahy: {moves}", True, WHITE)
        win.blit(score_text, (10, 10))
        win.blit(
            font.render("You Win!", True, WHITE),
            (WIDTH // 2 - 80, HEIGHT // 2 - 30)
        )
        pygame.display.update()
        save_score(player_name, score, moves)

        print(f"Hráč: {player_name}")
        print(f"Score: {score}")
        print(f"Tahy: {moves}")

        pygame.time.delay(3000)
        running = False

# Výpis leaderboardu
print("\n--- LEADERBOARD ---")

cursor.execute("""
SELECT players.name, games.score
FROM games
JOIN players
ON games.player_id = players.player_id
ORDER BY games.score DESC
LIMIT 5
""")

scores = cursor.fetchall()

for row in scores:
    print(row[0], "-", row[1])

conn.close()

pygame.quit()
