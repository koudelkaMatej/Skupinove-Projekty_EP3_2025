import pygame
import random
import math
import os

_HERE    = os.path.dirname(os.path.abspath(__file__))
_GRAFIKA = os.path.normpath(os.path.join(_HERE, "..", "..", "assets", "images", "Grafika"))


# Proměnné pro hru


CENTER_SIZE      = 120
SHIELD_LENGTH    = 150
SHIELD_THICKNESS = 18
SHIELD_GAP       = 10

VIRUS_RADIUS      = 30
BASE_SPEED        = 4.0
SPEED_INCREMENT   = 0.25

BASE_SPAWN_FRAMES = 90
MIN_SPAWN_FRAMES  = 18



# Štít – zpracovává vstup, pozici a vykreslování štítu


class Shield:
    COLOR_IDLE   = (80, 180, 255)
    COLOR_BORDER = (255, 255, 255)

    def __init__(self, center_x, center_y, img=None):
        self.cx  = center_x
        self.cy  = center_y
        self.img = img          
        self.direction = "up"

    def handle_input(self, keys):
        if keys[pygame.K_w]:
            self.direction = "up"
        elif keys[pygame.K_s]:
            self.direction = "down"
        elif keys[pygame.K_a]:
            self.direction = "left"
        elif keys[pygame.K_d]:
            self.direction = "right"

    def get_rect(self):
        half_c = CENTER_SIZE // 2
        half_s = SHIELD_LENGTH // 2

        if self.direction == "up":
            return pygame.Rect(
                self.cx - half_s,
                self.cy - half_c - SHIELD_GAP - SHIELD_THICKNESS,
                SHIELD_LENGTH, SHIELD_THICKNESS
            )
        if self.direction == "down":
            return pygame.Rect(
                self.cx - half_s,
                self.cy + half_c + SHIELD_GAP,
                SHIELD_LENGTH, SHIELD_THICKNESS
            )
        if self.direction == "left":
            return pygame.Rect(
                self.cx - half_c - SHIELD_GAP - SHIELD_THICKNESS,
                self.cy - half_s,
                SHIELD_THICKNESS, SHIELD_LENGTH
            )
        return pygame.Rect(
            self.cx + half_c + SHIELD_GAP,
            self.cy - half_s,
            SHIELD_THICKNESS, SHIELD_LENGTH
        )

    def draw(self, screen):
        rect = self.get_rect()
        if self.img is not None:
            # Rotace podle směru (base image je horizontální)
            angle = {"up": 0, "down": 180, "left": 90, "right": -90}[self.direction]
            rotated = pygame.transform.rotate(self.img, angle)
            scaled  = pygame.transform.scale(rotated, (rect.width, rect.height))
            screen.blit(scaled, rect.topleft)
        else:
            pygame.draw.rect(screen, self.COLOR_IDLE,   rect, border_radius=6)
            pygame.draw.rect(screen, self.COLOR_BORDER, rect, 2, border_radius=6)


 
# Virus – zpracovává pozici, pohyb a vykreslování virů, které se objevují ze stran a míří ke středu


class Virus:
    COLOR      = (220, 50, 50)
    COLOR_DARK = (140, 20, 20)

    def __init__(self, screen_width, screen_height, speed, img=None):
        self.r   = VIRUS_RADIUS
        self.img = img
        cx = screen_width  // 2
        cy = screen_height // 2

        side = random.choice(("top", "bottom", "left", "right"))

        if side == "top":
            self.x, self.y = float(cx), float(-self.r)
            self.vx, self.vy = 0.0, speed
        elif side == "bottom":
            self.x, self.y = float(cx), float(screen_height + self.r)
            self.vx, self.vy = 0.0, -speed
        elif side == "left":
            self.x, self.y = float(-self.r), float(cy)
            self.vx, self.vy = speed, 0.0
        else:
            self.x, self.y = float(screen_width + self.r), float(cy)
            self.vx, self.vy = -speed, 0.0

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def get_rect(self):
        return pygame.Rect(
            int(self.x) - self.r, int(self.y) - self.r,
            self.r * 2, self.r * 2
        )

    def draw(self, screen):
        if self.img is not None:
            screen.blit(self.img, self.get_rect().topleft)
        else:
            ix, iy = int(self.x), int(self.y)
            pygame.draw.circle(screen, self.COLOR,      (ix, iy), self.r)
            pygame.draw.circle(screen, self.COLOR_DARK, (ix, iy), self.r, 3)
            for angle_deg in range(0, 360, 60):
                rad   = math.radians(angle_deg)
                tip_x = ix + int((self.r + 8) * math.cos(rad))
                tip_y = iy + int((self.r + 8) * math.sin(rad))
                pygame.draw.line(screen, self.COLOR_DARK, (ix, iy), (tip_x, tip_y), 2)



# Tlačítko pro menu a pause – zpracovává vykreslování a klikání na tlačítko


class _Button:
    def __init__(self, rect, label, font):
        self.rect  = rect
        self.label = label
        self.font  = font

    def draw(self, screen):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        color = (80, 130, 210) if hover else (50, 85, 160)
        pygame.draw.rect(screen, color,           self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=10)
        surf = self.font.render(self.label, True, (255, 255, 255))
        screen.blit(surf, surf.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )



# Herní stav – zpracovává logiku a vykreslování samotné hry, včetně správy štítu, virů, skóre a stavu hry (běží/končí)


class GameplayState:

    def __init__(self, screen_width, screen_height):
        self.sw = screen_width
        self.sh = screen_height
        self.cx = screen_width  // 2
        self.cy = screen_height // 2

        # načtení obrázků a vytvoření objektů pro štít a tlačítka
        def _load(name, size):
            path = os.path.join(_GRAFIKA, name)
            img  = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)

        self.img_center  = _load("slozka (1).png", (CENTER_SIZE, CENTER_SIZE))
        self.img_shield  = _load("stit (1).png",   (SHIELD_LENGTH, SHIELD_THICKNESS))
        self.img_virus1  = _load("Virus1.png",      (VIRUS_RADIUS * 2, VIRUS_RADIUS * 2))
        self.img_virus2  = _load("virus2.png",      (VIRUS_RADIUS * 2, VIRUS_RADIUS * 2))
        self._virus_imgs = [self.img_virus1, self.img_virus2]

        self.shield = Shield(self.cx, self.cy)
        self.center_rect = pygame.Rect(
            self.cx - CENTER_SIZE // 2,
            self.cy - CENTER_SIZE // 2,
            CENTER_SIZE, CENTER_SIZE
        )

        self.font_huge   = pygame.font.Font(None, 140)
        self.font_large  = pygame.font.Font(None, 80)
        self.font_medium = pygame.font.Font(None, 52)
        btn_font         = pygame.font.Font(None, 48)

        btn_w, btn_h = 320, 72
        gap     = 30
        total_w = btn_w * 2 + gap
        bx = self.cx - total_w // 2
        by = self.cy + 120

        self.btn_again = _Button(pygame.Rect(bx,               by, btn_w, btn_h), "PLAY AGAIN", btn_font)
        self.btn_menu  = _Button(pygame.Rect(bx + btn_w + gap, by, btn_w, btn_h), "MENU",       btn_font)

        self._reset()

    def _reset(self):
        self.viruses     = []
        self.score       = 0
        self.spawn_timer = 0
        self.game_over   = False
        self.shield.direction = "up"

    def reset(self):
        self._reset()

    def _spawn_interval(self):
        return max(MIN_SPAWN_FRAMES, BASE_SPAWN_FRAMES - self.score * 2)

    def _virus_speed(self):
        return BASE_SPEED + self.score * SPEED_INCREMENT

    def handle_event(self, event):
        if self.game_over:
            if self.btn_again.is_clicked(event):
                self._reset()
            elif self.btn_menu.is_clicked(event):
                self._reset()
                return "menu"
        return None

    def update(self, keys):
        if self.game_over:
            return

        self.shield.handle_input(keys)

        self.spawn_timer += 1
        if self.spawn_timer >= self._spawn_interval():
            self.spawn_timer = 0
            img = random.choice(self._virus_imgs)
            self.viruses.append(Virus(self.sw, self.sh, self._virus_speed(), img))

        shield_rect = self.shield.get_rect()
        alive = []
        for v in self.viruses:
            v.update()
            if v.get_rect().colliderect(shield_rect):
                self.score += 1
                continue
            if v.get_rect().colliderect(self.center_rect):
                self.game_over = True
                return
            alive.append(v)
        self.viruses = alive

    def draw(self, screen, bg=None):
        if bg is not None:
            screen.blit(bg, (0, 0))
        else:
            screen.fill((15, 15, 35))

        if self.game_over:
            self._draw_game_over(screen)
            return

        # Střed – složka
        screen.blit(self.img_center, self.center_rect.topleft)

        self.shield.draw(screen)

        for v in self.viruses:
            v.draw(screen)

        score_surf = self.font_medium.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_surf, (30, 30))

    def _draw_game_over(self, screen):
        overlay = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        screen.blit(overlay, (0, 0))

        go = self.font_huge.render("GAME OVER", True, (220, 50, 50))
        screen.blit(go, go.get_rect(center=(self.cx, self.cy - 180)))

        sc = self.font_large.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(sc, sc.get_rect(center=(self.cx, self.cy - 60)))

        self.btn_again.draw(screen)
        self.btn_menu.draw(screen)
