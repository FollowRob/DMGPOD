import pygame
import src.theme as t
from src.scenes.base_scene import BaseScene

FADE_IN_MS  = 800
HOLD_MS     = 1400
FADE_OUT_MS = 600
TOTAL_MS    = FADE_IN_MS + HOLD_MS + FADE_OUT_MS


class BootSplash(BaseScene):

    def on_enter(self):
        self._start = pygame.time.get_ticks()
        self._done = False
        font_large = pygame.font.SysFont("helveticaneue", 22, bold=True)
        self._logo = font_large.render("DMGPod", True, (220, 220, 220))

    def handle_event(self, event):
        pass

    def update(self):
        if self._done:
            return
        elapsed = pygame.time.get_ticks() - self._start
        if elapsed >= TOTAL_MS:
            self._done = True
            self.manager.switch("main_menu", push_history=False)

    def draw(self, surface):
        elapsed = pygame.time.get_ticks() - self._start
        surface.fill((0, 0, 0))

        cx = t.SCREEN_W // 2
        cy = t.SCREEN_H // 2 - 10

        self._draw_dmg(surface, cx, cy - 52)

        surface.blit(self._logo, (cx - self._logo.get_width() // 2, cy + 10))

        if elapsed < FADE_IN_MS:
            black_alpha = 255 - int(255 * elapsed / FADE_IN_MS)
        elif elapsed < FADE_IN_MS + HOLD_MS:
            black_alpha = 0
        else:
            fade_elapsed = elapsed - FADE_IN_MS - HOLD_MS
            black_alpha = min(255, int(255 * fade_elapsed / FADE_OUT_MS))

        if black_alpha > 0:
            overlay = pygame.Surface((t.SCREEN_W, t.SCREEN_H))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(black_alpha)
            surface.blit(overlay, (0, 0))

    def _draw_dmg(self, surface, cx, top):
        col = (200, 200, 200)
        bw, bh = 44, 60
        bx = cx - bw // 2

        # Body
        pygame.draw.rect(surface, col, (bx, top, bw, bh), 2, border_radius=7)
        # Screen bezel
        pygame.draw.rect(surface, col, (bx + 6, top + 6, bw - 12, 22), 2, border_radius=2)
        # Speaker dots
        for r in range(2):
            for c in range(3):
                pygame.draw.circle(surface, col, (bx + 8 + c * 5, top + 38 + r * 5), 1)
        # D-pad
        dpx, dpy = bx + 11, top + 48
        pygame.draw.rect(surface, col, (dpx - 5, dpy - 2, 10, 4))
        pygame.draw.rect(surface, col, (dpx - 2, dpy - 5, 4, 10))
        # A/B buttons
        pygame.draw.circle(surface, col, (bx + bw - 10, top + 46), 3, 2)
        pygame.draw.circle(surface, col, (bx + bw - 17, top + 50), 3, 2)
        # Cart slot
        pygame.draw.rect(surface, col, (cx - 9, top + bh - 2, 18, 5), 2)
