import pygame
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from assets.colors import *

_HERE = os.path.dirname(os.path.abspath(__file__))
_GRAFIKA = os.path.normpath(os.path.join(_HERE, "..", "..", "assets", "images", "Grafika"))
from assets.audio import (
    get_master_volume, get_music_volume, get_effects_volume,
    set_master_volume, set_music_volume, set_effects_volume
)
from objects.button import Button

# Slider pro nastavení hlasitosti

class Slider:
    def __init__(self, x, y, width, label, get_fn, set_fn):
        self.x = x
        self.y = y
        self.width = width
        self.track_height = 8
        self.label = label
        self.get_fn = get_fn
        self.set_fn = set_fn
        self.handle_radius = 14
        self.dragging = False

        self.track_rect = pygame.Rect(x, y, width, self.track_height)
        self.font_label = pygame.font.Font(None, 36)
        self.font_value = pygame.font.Font(None, 32)

    @property
    def value(self):
        return self.get_fn()

    def _handle_x(self):
        return int(self.x + self.value * self.width)

    def _handle_rect(self):
        hx = self._handle_x()
        hy = self.y + self.track_height // 2
        return pygame.Rect(
            hx - self.handle_radius, hy - self.handle_radius,
            self.handle_radius * 2, self.handle_radius * 2
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._handle_rect().collidepoint(event.pos):
                self.dragging = True
            elif self.track_rect.inflate(0, 20).collidepoint(event.pos):
                # klik přímo na track taky posune slider
                rel_x = event.pos[0] - self.x
                val = max(0.0, min(1.0, rel_x / self.width))
                self.set_fn(val)
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            rel_x = event.pos[0] - self.x
            val = max(0.0, min(1.0, rel_x / self.width))
            self.set_fn(val)

    def draw(self, screen):
        # Popis slideru nad ním
        label_surf = self.font_label.render(self.label, True, WHITE)
        screen.blit(label_surf, (self.x, self.y - 32))

        # Track pozadí
        pygame.draw.rect(screen, DARK_GRAY, self.track_rect, border_radius=4)

        # Vyplněná část tracku (zlatá)
        filled_w = int(self.value * self.width)
        if filled_w > 0:
            filled_rect = pygame.Rect(self.x, self.y, filled_w, self.track_height)
            pygame.draw.rect(screen, TITLE, filled_rect, border_radius=4)

        # Handle - bílý okraj, zlatý vnitřek
        hx = self._handle_x()
        hy = self.y + self.track_height // 2
        pygame.draw.circle(screen, WHITE, (hx, hy), self.handle_radius)
        pygame.draw.circle(screen, TITLE, (hx, hy), self.handle_radius - 3)

        # Procenta napravo od slideru
        pct = int(self.value * 100)
        val_surf = self.font_value.render(f"{pct}%", True, TITLE)
        screen.blit(val_surf, (self.x + self.width + 18, self.y - 4))


# Settings obrazovka se 3 slidery a tlačítkem návratu

class SettingsScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        slider_width = 500
        slider_x = (screen_width - slider_width) // 2

        self.sliders = [
            Slider(slider_x, 360, slider_width, "MASTER VOLUME",  get_master_volume,  set_master_volume),
            Slider(slider_x, 490, slider_width, "MUSIC VOLUME",   get_music_volume,   set_music_volume),
            Slider(slider_x, 620, slider_width, "EFFECTS VOLUME", get_effects_volume, set_effects_volume),
        ]

        # X tlačítko v pravém horním rohu
        btn_size = 54
        margin = 28
        self.return_button = Button(
            screen_width - btn_size - margin, margin,
            btn_size, btn_size,
            "X", DARK_GRAY, WHITE, font_size=40
        )

        self.font_title = pygame.font.Font(None, 72)

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        self.return_button.update(mouse_pos)

        for slider in self.sliders:
            slider.handle_event(event)

        if self.return_button.is_clicked(event):
            return "menu"
        return None

    def draw(self, screen):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        # Nadpis
        title_surf = self.font_title.render("SETTINGS", True, TITLE)
        screen.blit(title_surf, title_surf.get_rect(center=(self.screen_width // 2, 80)))

        # Slidery
        for slider in self.sliders:
            slider.draw(screen)

        # X tlačítko
        self.return_button.draw(screen)
