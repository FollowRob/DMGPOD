import pygame
import src.theme as t

DURATION_MS = 2500
FADE_MS = 400
TOAST_H = 28
TOAST_Y = t.HEADER_H + 8


class Toast:
    def __init__(self):
        self._message = ""
        self._start = None
        self._font = None

    def _ensure_font(self, fonts):
        if self._font is None:
            self._font = fonts["small"]

    def show(self, message):
        self._message = message
        self._start = pygame.time.get_ticks()

    def draw(self, surface, fonts):
        if self._start is None:
            return
        self._ensure_font(fonts)

        elapsed = pygame.time.get_ticks() - self._start
        if elapsed > DURATION_MS + FADE_MS:
            self._start = None
            return

        # Alpha: full during DURATION_MS, then fade out
        if elapsed > DURATION_MS:
            alpha = max(0, 255 - int(255 * (elapsed - DURATION_MS) / FADE_MS))
        else:
            alpha = 255

        text_surf = self._font.render(self._message, True, t.TEXT)
        pad_x, pad_y = 14, 6
        w = text_surf.get_width() + pad_x * 2
        h = TOAST_H
        x = t.SCREEN_W // 2 - w // 2

        bg = pygame.Surface((w, h), pygame.SRCALPHA)
        bg.fill((40, 40, 40, int(alpha * 0.92)))
        pygame.draw.rect(bg, (*t.HIGHLIGHT, alpha), bg.get_rect(), 1, border_radius=6)
        surface.blit(bg, (x, TOAST_Y))

        text_surf.set_alpha(alpha)
        surface.blit(text_surf, (x + pad_x, TOAST_Y + h // 2 - text_surf.get_height() // 2))


# Shared instance
toast = Toast()
