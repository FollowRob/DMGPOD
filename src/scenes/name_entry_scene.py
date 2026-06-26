import pygame
import src.theme as t
from src.scenes.base_scene import BaseScene
from src.input import get_button

CHARS = list("abcdefghijklmnopqrstuvwxyz0123456789 ")
MAX_LEN = 20
BLINK_MS = 500


class NameEntryScene(BaseScene):
    """Single-line name entry. Set .on_confirm(name) callback before switching."""

    def __init__(self, manager, fonts):
        super().__init__(manager, fonts)
        self.on_confirm = None
        self._text = []
        self._char_idx = 0
        self._last_blink = 0
        self._blink_on = True
        self.prompt = "Name your playlist"

    def on_enter(self):
        self._text = []
        self._char_idx = 0
        self._last_blink = pygame.time.get_ticks()
        self._blink_on = True

    def handle_event(self, event):
        btn = get_button(event)
        if btn == "left":
            self._char_idx = (self._char_idx - 1) % len(CHARS)
        elif btn == "right":
            self._char_idx = (self._char_idx + 1) % len(CHARS)
        elif btn == "a":
            if len(self._text) < MAX_LEN:
                self._text.append(CHARS[self._char_idx])
        elif btn == "b":
            if self._text:
                self._text.pop()
            else:
                self.manager.back()
        elif btn == "start":
            name = "".join(self._text).strip()
            if name and self.on_confirm:
                self.on_confirm(name)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self._last_blink > BLINK_MS:
            self._blink_on = not self._blink_on
            self._last_blink = now

    def draw(self, surface):
        surface.fill(t.BG)

        # Header
        pygame.draw.rect(surface, t.HEADER_BG, (0, 0, t.SCREEN_W, t.HEADER_H))
        h = self.fonts["header"].render("New Playlist", True, t.TEXT)
        surface.blit(h, (t.SCREEN_W // 2 - h.get_width() // 2,
                         t.HEADER_H // 2 - h.get_height() // 2))
        pygame.draw.line(surface, t.DIVIDER, (0, t.HEADER_H), (t.SCREEN_W, t.HEADER_H))

        # Prompt
        prompt = self.fonts["small"].render(self.prompt, True, t.TEXT_DIM)
        surface.blit(prompt, (t.SCREEN_W // 2 - prompt.get_width() // 2, t.HEADER_H + 18))

        # Typed text + cursor
        typed = "".join(self._text)
        cursor = "|" if self._blink_on else " "
        display = typed + cursor
        text_surf = self.fonts["header"].render(display, True, t.TEXT)
        text_y = t.HEADER_H + 44
        surface.blit(text_surf, (t.SCREEN_W // 2 - text_surf.get_width() // 2, text_y))

        # Underline
        line_y = text_y + text_surf.get_height() + 4
        pygame.draw.line(surface, t.HIGHLIGHT,
                         (40, line_y), (t.SCREEN_W - 40, line_y), 1)

        # Character wheel — show 5 chars centred on current
        wheel_y = t.SCREEN_H // 2 + 10
        offsets = [-2, -1, 0, 1, 2]
        spacing = 28
        cx = t.SCREEN_W // 2
        for o in offsets:
            idx = (self._char_idx + o) % len(CHARS)
            ch = CHARS[idx]
            label = " " if ch == " " else ch.upper()
            if o == 0:
                s = self.fonts["header"].render(label, True, t.TEXT)
                pygame.draw.rect(surface, t.HIGHLIGHT,
                                 (cx - 14, wheel_y - 2, 28, s.get_height() + 4),
                                 border_radius=4)
            else:
                fade = max(60, 160 - abs(o) * 60)
                s = self.fonts["item"].render(label, True, (fade, fade, fade))
            surface.blit(s, (cx + o * spacing - s.get_width() // 2, wheel_y))

        # Hints
        hints = [
            ("←→", "change"),
            ("A", "select"),
            ("B", "delete"),
            ("Start", "confirm"),
        ]
        hint_y = t.SCREEN_H - 28
        hint_x = 12
        for key, desc in hints:
            k = self.fonts["small"].render(key, True, t.HIGHLIGHT)
            d = self.fonts["small"].render(" " + desc + "  ", True, t.TEXT_DIM)
            surface.blit(k, (hint_x, hint_y))
            hint_x += k.get_width()
            surface.blit(d, (hint_x, hint_y))
            hint_x += d.get_width()
