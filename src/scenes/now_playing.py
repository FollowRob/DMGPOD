import pygame
from src.scenes.base_scene import BaseScene
from src.input import get_button
import src.theme as t

PROGRESS_W = 130
PROGRESS_H = 3


class NowPlaying(BaseScene):

    def on_enter(self):
        self._tick = 0

    def handle_event(self, event):
        btn = get_button(event)
        if btn == "b":
            self.manager.back()
        elif btn == "left":
            pass  # previous track (Phase 4)
        elif btn == "right":
            pass  # next track (Phase 4)

    def update(self):
        self._tick += 1

    def draw(self, surface):
        surface.fill(t.BG)

        # Header
        pygame.draw.rect(surface, t.HEADER_BG, (0, 0, t.SCREEN_W, t.HEADER_H))
        title_surf = self.fonts["header"].render("Now Playing", True, t.TEXT)
        surface.blit(title_surf, (t.SCREEN_W // 2 - title_surf.get_width() // 2,
                                  t.HEADER_H // 2 - title_surf.get_height() // 2))
        pygame.draw.line(surface, t.DIVIDER, (0, t.HEADER_H), (t.SCREEN_W, t.HEADER_H))

        # Album art placeholder (left square)
        art_size = t.SCREEN_H - t.HEADER_H - 16
        art_rect = pygame.Rect(8, t.HEADER_H + 8, art_size, art_size)
        pygame.draw.rect(surface, t.PANEL_BG, art_rect)
        pygame.draw.rect(surface, t.DIVIDER, art_rect, 1)
        note = self.fonts["header"].render("♪", True, t.TEXT_DIM)
        surface.blit(note, (art_rect.centerx - note.get_width() // 2,
                            art_rect.centery - note.get_height() // 2))

        # Info panel — right of art
        info_x = art_rect.right + 10
        info_w = t.SCREEN_W - info_x - 6
        info_y = t.HEADER_H + 12

        track = self.fonts["header"].render("No Track", True, t.TEXT)
        artist = self.fonts["small"].render("Unknown Artist", True, t.TEXT_DIM)
        album = self.fonts["small"].render("Unknown Album", True, t.TEXT_DIM)

        surface.blit(track, (info_x, info_y))
        surface.blit(artist, (info_x, info_y + 18))
        surface.blit(album, (info_x, info_y + 32))

        # Progress bar
        bar_y = info_y + 56
        pygame.draw.rect(surface, t.DIVIDER, (info_x, bar_y, info_w, PROGRESS_H))
        progress = abs((self._tick % 240) / 240)
        pygame.draw.rect(surface, t.HIGHLIGHT, (info_x, bar_y, int(info_w * progress), PROGRESS_H))

        # Time labels
        elapsed = self.fonts["small"].render("0:00", True, t.TEXT_DIM)
        total = self.fonts["small"].render("0:00", True, t.TEXT_DIM)
        surface.blit(elapsed, (info_x, bar_y + 6))
        surface.blit(total, (info_x + info_w - total.get_width(), bar_y + 6))

        # Transport controls  ⏮ ▶ ⏭
        ctrl_y = bar_y + 26
        ctrl_cx = info_x + info_w // 2
        self._draw_transport(surface, ctrl_cx, ctrl_y, playing=False)

    def _draw_transport(self, surface, cx, cy, playing):
        col = t.TEXT_DIM
        # Prev  |◀◀
        pygame.draw.polygon(surface, col, [(cx - 28, cy), (cx - 20, cy - 6), (cx - 20, cy + 6)])
        pygame.draw.rect(surface, col, (cx - 30, cy - 6, 3, 12))
        # Next  ▶▶|
        pygame.draw.polygon(surface, col, [(cx + 28, cy), (cx + 20, cy - 6), (cx + 20, cy + 6)])
        pygame.draw.rect(surface, col, (cx + 28, cy - 6, 3, 12))
        # Play ▶ / Pause ‖
        if playing:
            pygame.draw.rect(surface, t.TEXT, (cx - 5, cy - 7, 4, 14))
            pygame.draw.rect(surface, t.TEXT, (cx + 1, cy - 7, 4, 14))
        else:
            pygame.draw.polygon(surface, t.TEXT, [(cx - 6, cy - 7), (cx + 8, cy), (cx - 6, cy + 7)])
