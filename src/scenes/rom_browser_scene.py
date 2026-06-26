import os
import pygame
import src.theme as t
import src.state as state
from src.scenes.base_scene import BaseScene
from src.input import get_button
from src.retro import scan_roms, launch, find_retroarch, find_core
from src.toast import toast

ROMS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "roms")
SYSTEM_LABELS = {"gb": "Game Boy", "gbc": "Game Boy Color", "gba": "Game Boy Advance"}

ITEM_H = 30
LIST_TOP = t.HEADER_H + 6
MAX_VISIBLE = (t.SCREEN_H - LIST_TOP - 4) // ITEM_H


class RomBrowserScene(BaseScene):

    def on_enter(self):
        self._roms_by_system = scan_roms(ROMS_DIR)
        self._flat = []   # list of (label, system, path, is_header)
        for system in ("gb", "gbc", "gba"):
            roms = self._roms_by_system.get(system, [])
            if roms:
                self._flat.append((SYSTEM_LABELS[system], system, None, True))
                for r in roms:
                    self._flat.append((r["name"], system, r["path"], False))
        self._selected = self._first_selectable(0, 1)
        self._scroll = 0
        self._launching = False

    def _first_selectable(self, start, direction=1):
        for i in range(len(self._flat)):
            idx = (start + i * direction) % len(self._flat)
            if not self._flat[idx][3]:
                return idx
        return 0

    def handle_event(self, event):
        btn = get_button(event)
        if not self._flat:
            if btn in ("b", "left"):
                self.manager.back()
            return

        if btn == "up":
            self._selected = self._first_selectable(self._selected - 1, -1)
            self._clamp_scroll()
        elif btn == "down":
            self._selected = self._first_selectable(self._selected + 1, 1)
            self._clamp_scroll()
        elif btn in ("a", "right"):
            self._launch_selected()
        elif btn in ("b", "left"):
            self.manager.back()

    def _clamp_scroll(self):
        if self._selected < self._scroll:
            self._scroll = self._selected
        elif self._selected >= self._scroll + MAX_VISIBLE:
            self._scroll = self._selected - MAX_VISIBLE + 1

    def _launch_selected(self):
        if not self._flat:
            return
        label, system, path, is_header = self._flat[self._selected]
        if is_header or not path:
            return

        ra = find_retroarch()
        if not ra:
            toast.show("RetroArch not found")
            return
        core = find_core(system)
        if not core:
            toast.show(f"No {system.upper()} core installed")
            return

        # Pause music, hide pygame window, launch, restore
        was_playing = state.player.is_playing
        state.player.pause()
        pygame.display.iconify()

        err = launch(path, system)

        pygame.display.set_mode((t.SCREEN_W, t.SCREEN_H))
        pygame.display.set_caption("DMGPod")
        if err:
            toast.show(err)
        else:
            if was_playing:
                state.player.resume()

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(t.BG)

        # Header
        pygame.draw.rect(surface, t.HEADER_BG, (0, 0, t.SCREEN_W, t.HEADER_H))
        h = self.fonts["header"].render("Games", True, t.TEXT)
        surface.blit(h, (t.SCREEN_W // 2 - h.get_width() // 2,
                         t.HEADER_H // 2 - h.get_height() // 2))
        pygame.draw.line(surface, t.DIVIDER, (0, t.HEADER_H), (t.SCREEN_W, t.HEADER_H))

        if not self._flat:
            msg = self.fonts["small"].render("No ROMs found in roms/", True, t.TEXT_DIM)
            surface.blit(msg, (t.SCREEN_W // 2 - msg.get_width() // 2, t.SCREEN_H // 2))
            return

        visible = self._flat[self._scroll: self._scroll + MAX_VISIBLE]
        for i, (label, system, path, is_header) in enumerate(visible):
            abs_i = self._scroll + i
            y = LIST_TOP + i * ITEM_H

            if is_header:
                s = self.fonts["small"].render(label.upper(), True, t.HIGHLIGHT)
                surface.blit(s, (12, y + ITEM_H // 2 - s.get_height() // 2))
                pygame.draw.line(surface, t.DIVIDER,
                                 (12, y + ITEM_H - 1), (t.SCREEN_W - 12, y + ITEM_H - 1))
            else:
                if abs_i == self._selected:
                    t.draw_highlight(surface, (0, y, t.SCREEN_W, ITEM_H))
                col = t.TEXT_HI if abs_i == self._selected else t.TEXT
                s = self.fonts["item"].render(label, True, col)
                surface.blit(s, (24, y + ITEM_H // 2 - s.get_height() // 2))

                # Chevron
                cx = t.SCREEN_W - 14
                cy = y + ITEM_H // 2
                pygame.draw.polygon(surface, col, [
                    (cx, cy - 5), (cx + 5, cy), (cx, cy + 5)
                ])

        # Scroll indicator
        if len(self._flat) > MAX_VISIBLE:
            track_h = t.SCREEN_H - LIST_TOP
            thumb_h = max(10, track_h * MAX_VISIBLE // len(self._flat))
            thumb_y = LIST_TOP + (track_h - thumb_h) * self._scroll // max(1, len(self._flat) - MAX_VISIBLE)
            pygame.draw.rect(surface, t.DIVIDER, (t.SCREEN_W - 4, LIST_TOP, 3, track_h))
            pygame.draw.rect(surface, t.TEXT_DIM, (t.SCREEN_W - 4, thumb_y, 3, thumb_h))
