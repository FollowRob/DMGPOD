import pygame
import src.state as state
import src.theme as t
from src.scenes.base_scene import BaseScene
from src.input import get_button

VERSION = "0.1.0"
PHASE = "Phase 5 — Mac Prototype"


class AboutScene(BaseScene):

    def handle_event(self, event):
        if get_button(event) in ("b", "left"):
            self.manager.back()

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(t.BG)

        # Header
        pygame.draw.rect(surface, t.HEADER_BG, (0, 0, t.SCREEN_W, t.HEADER_H))
        title = self.fonts["header"].render("About", True, t.TEXT)
        surface.blit(title, (t.SCREEN_W // 2 - title.get_width() // 2,
                             t.HEADER_H // 2 - title.get_height() // 2))
        pygame.draw.line(surface, t.DIVIDER, (0, t.HEADER_H), (t.SCREEN_W, t.HEADER_H))

        rows = [
            ("DMGPod",          VERSION),
            ("Build",           PHASE),
            ("",                ""),
            ("Tracks",          str(len(state.tracks))),
            ("Artists",         str(len(state.artists))),
            ("Albums",          str(len(state.albums))),
            ("",                ""),
            ("Display",         "320×240 ILI9341"),
            ("Target",          "Raspberry Pi Zero 2W"),
        ]

        pad_x = 16
        y = t.HEADER_H + 16
        row_h = 20

        for label, value in rows:
            if not label and not value:
                pygame.draw.line(surface, t.DIVIDER,
                                 (pad_x, y + row_h // 2),
                                 (t.SCREEN_W - pad_x, y + row_h // 2))
                y += row_h
                continue

            lbl_surf = self.fonts["small"].render(label, True, t.TEXT_DIM)
            val_surf = self.fonts["small"].render(value, True, t.TEXT)
            surface.blit(lbl_surf, (pad_x, y))
            surface.blit(val_surf, (t.SCREEN_W - pad_x - val_surf.get_width(), y))
            y += row_h
