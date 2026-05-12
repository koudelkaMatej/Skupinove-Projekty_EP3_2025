import pygame
import os
import threading
import webbrowser

try:
    import requests
    _REQUESTS_OK = True
except ImportError:
    _REQUESTS_OK = False

_HERE    = os.path.dirname(os.path.abspath(__file__))
_GRAFIKA = os.path.normpath(os.path.join(_HERE, "..", "..", "assets", "images", "Grafika"))

SERVER_URL = "http://localhost:5000"

# Barvy -- stejne jako v menu
_GOLD     = (255, 215,   0)
_WHITE    = (255, 255, 255)
_GRAY     = (160, 160, 180)
_RED      = (220,  50,  50)
_GREEN    = ( 50, 200,  80)
_ACTIVE   = (255, 215,   0)   # zlata hranice aktivniho pole
_BORDER   = ( 90,  90, 110)
_BTN      = ( 50,  85, 160)
_BTN_HOV  = ( 80, 130, 210)
_INPUT_BG = (  0,   0,   0, 140)   # RGBA


class LoginScreen:

    def __init__(self, screen_width, screen_height):
        self.sw = screen_width
        self.sh = screen_height
        cx = screen_width  // 2
        cy = screen_height // 2

        # --- Pozadi: Background.png rozmazany (scale down/up trick) ---
        bg_raw  = pygame.image.load(os.path.join(_GRAFIKA, "Background.png")).convert()
        bg_full = pygame.transform.scale(bg_raw, (screen_width, screen_height))
        small   = pygame.transform.smoothscale(bg_full, (screen_width // 8, screen_height // 8))
        self._bg = pygame.transform.smoothscale(small, (screen_width, screen_height))

        # Tmava vrstva pres blur
        self._overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self._overlay.fill((0, 0, 0, 140))

        # --- Font (deltarune -- stejny jako menu) ---
        _fp = os.path.join(_GRAFIKA, "deltarune.ttf")
        self.font_title = pygame.font.Font(_fp, 80)
        self.font_label = pygame.font.Font(_fp, 28)
        self.font_input = pygame.font.Font(_fp, 32)
        self.font_btn   = pygame.font.Font(_fp, 34)
        self.font_msg   = pygame.font.Font(_fp, 24)
        self.font_hint  = pygame.font.Font(_fp, 20)

        # --- Panel (polo-pruhledny) ---
        pw, ph = 700, 530
        self.panel      = pygame.Rect(cx - pw // 2, cy - ph // 2, pw, ph)
        self._panel_s   = pygame.Surface((pw, ph), pygame.SRCALPHA)
        self._panel_s.fill((8, 8, 18, 220))

        # --- Inputy ---
        iw, ih = 560, 52
        ix = cx - iw // 2
        self.rect_user = pygame.Rect(ix, cy - 95, iw, ih)
        self.rect_pass = pygame.Rect(ix, cy +  5, iw, ih)

        # --- Tlacitka ---
        bw, bh = 230, 58
        self.rect_login = pygame.Rect(cx - bw - 16, cy + 105, bw, bh)
        self.rect_reg   = pygame.Rect(cx + 16,      cy + 105, bw, bh)

        self.username     = ""
        self.password     = ""
        self.active_field = "username"
        self.message       = ""
        self.message_color = _RED
        self._token        = None
        self._loading      = False

    # ---------------------------------------------------------------- events

    def handle_event(self, event):
        """Vraci token po uspesnem prihlaseni, jinak None."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect_user.collidepoint(event.pos):
                self.active_field = "username"
            elif self.rect_pass.collidepoint(event.pos):
                self.active_field = "password"
            elif self.rect_login.collidepoint(event.pos):
                self._do_login()
            elif self.rect_reg.collidepoint(event.pos):
                webbrowser.open(f"{SERVER_URL}/register")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.active_field = "password" if self.active_field == "username" else "username"
            elif event.key == pygame.K_RETURN:
                self._do_login()
            elif event.key == pygame.K_BACKSPACE:
                if self.active_field == "username":
                    self.username = self.username[:-1]
                else:
                    self.password = self.password[:-1]
            else:
                ch = event.unicode
                if ch and ch.isprintable():
                    if self.active_field == "username" and len(self.username) < 30:
                        self.username += ch
                    elif self.active_field == "password" and len(self.password) < 50:
                        self.password += ch

        if self._token:
            token        = self._token
            self._token  = None
            return token
        return None

    # --------------------------------------------------------------- login

    def _do_login(self):
        if self._loading:
            return
        if not self.username or not self.password:
            self.message       = "Zadej jmeno i heslo."
            self.message_color = _RED
            return
        if not _REQUESTS_OK:
            self.message       = "Chybi knihovna requests.  pip install requests"
            self.message_color = _RED
            return
        self._loading      = True
        self.message       = "Prihlasovani..."
        self.message_color = _GRAY
        threading.Thread(target=self._login_thread, daemon=True).start()

    def _login_thread(self):
        try:
            resp = requests.post(
                f"{SERVER_URL}/api/login",
                json={"username": self.username, "password": self.password},
                timeout=5,
            )
            data = resp.json()
            if data.get("success"):
                self.message       = f"Vitej, {self.username}!"
                self.message_color = _GREEN
                self._token        = data["token"]
            else:
                self.message       = data.get("error", "Nespravne jmeno nebo heslo.")
                self.message_color = _RED
        except Exception:
            self.message       = "Server neni dostupny. Spust Flask server."
            self.message_color = _RED
        finally:
            self._loading = False

    # ---------------------------------------------------------------- draw

    def draw(self, screen):
        # 1) Rozmazane pozadi
        screen.blit(self._bg, (0, 0))

        # 2) Tmava vrstva
        screen.blit(self._overlay, (0, 0))

        cx = self.sw // 2
        cy = self.sh // 2

        # 3) Polo-pruhledny panel
        screen.blit(self._panel_s, self.panel.topleft)
        pygame.draw.rect(screen, _BORDER, self.panel, 1, border_radius=4)

        # 4) Titulek (zlaty -- jako menu)
        t = self.font_title.render("ShieldBash", True, _GOLD)
        screen.blit(t, t.get_rect(center=(cx, self.panel.top + 72)))

        # Subtitulek
        sub = self.font_hint.render("-- Login --", True, (160, 160, 160))
        screen.blit(sub, sub.get_rect(center=(cx, self.panel.top + 128)))

        # 5) Username
        self._draw_input(screen, "Username:", self.rect_user,
                         self.username, self.active_field == "username")

        # 6) Password
        self._draw_input(screen, "Password:", self.rect_pass,
                         "*" * len(self.password), self.active_field == "password")

        # 7) Tlacitka
        mp = pygame.mouse.get_pos()
        self._draw_btn(screen, self.rect_login, "Login",    mp)
        self._draw_btn(screen, self.rect_reg,   "Register", mp)

        # 8) Zprava (chyba / uspech)
        if self.message:
            msg = self.font_msg.render(self.message, True, self.message_color)
            screen.blit(msg, msg.get_rect(center=(cx, self.panel.bottom - 38)))

        # 9) Napoveda
        hint = self.font_hint.render("Tab = switch field   Enter = login", True, (70, 70, 90))
        screen.blit(hint, hint.get_rect(center=(cx, self.panel.bottom + 26)))

    # -------------------------------------------------------- helpers

    def _draw_input(self, screen, label, rect, value, active):
        lbl = self.font_label.render(label, True, _GOLD if active else (180, 180, 180))
        screen.blit(lbl, (rect.left, rect.top - 30))

        # Input box (polo-pruhledny)
        box = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        box.fill((0, 0, 0, 150))
        screen.blit(box, rect.topleft)
        border_col = _ACTIVE if active else _BORDER
        pygame.draw.rect(screen, border_col, rect, 2, border_radius=6)

        txt = self.font_input.render(value, True, _WHITE)
        screen.blit(txt, (rect.left + 12, rect.centery - txt.get_height() // 2))

    def _draw_btn(self, screen, rect, label, mp):
        col = _BTN_HOV if rect.collidepoint(mp) else _BTN
        pygame.draw.rect(screen, col,    rect, border_radius=8)
        pygame.draw.rect(screen, _GOLD if rect.collidepoint(mp) else _BORDER,
                         rect, 2, border_radius=8)
        s = self.font_btn.render(label, True, _WHITE)
        screen.blit(s, s.get_rect(center=rect.center))
