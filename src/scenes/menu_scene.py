import pygame
from src.scenes.base_scene import BaseScene
from src.input import get_button
import src.theme as t

ITEM_H = 34
LIST_TOP_PAD = 8
MAX_VISIBLE = (t.SCREEN_H - t.HEADER_H - LIST_TOP_PAD) // ITEM_H


class MenuScene(BaseScene):
    """Reusable iPod-style left-panel menu. Subclass and override title, items(), on_select(), draw_panel()."""

    title = "Menu"

    def __init__(self, manager, fonts):
        super().__init__(manager, fonts)
        self.selected = 0
        self.scroll = 0

    def items(self):
        return []

    def on_select(self, index, item):
        pass

    def draw_panel(self, surface):
        cx = t.PANEL_X + t.PANEL_W // 2
        cy = t.HEADER_H + (t.SCREEN_H - t.HEADER_H) // 2
        hint = self.fonts["small"].render(self.title, True, t.TEXT_DIM)
        surface.blit(hint, (cx - hint.get_width() // 2, cy - hint.get_height() // 2))

    def on_enter(self):
        self.selected = 0
        self.scroll = 0

    def handle_event(self, event):
        btn = get_button(event)
        items = self.items()
        if not items:
            return

        if btn == "up":
            self.selected = (self.selected - 1) % len(items)
            self._clamp_scroll()
        elif btn == "down":
            self.selected = (self.selected + 1) % len(items)
            self._clamp_scroll()
        elif btn in ("a", "right"):
            self.on_select(self.selected, items[self.selected])
        elif btn in ("b", "left"):
            self.manager.back()

    def _clamp_scroll(self):
        if self.selected < self.scroll:
            self.scroll = self.selected
        elif self.selected >= self.scroll + MAX_VISIBLE:
            self.scroll = self.selected - MAX_VISIBLE + 1

    def draw(self, surface):
        surface.fill(t.BG)

        # Header
        pygame.draw.rect(surface, t.HEADER_BG, (0, 0, t.SCREEN_W, t.HEADER_H))
        title_surf = self.fonts["header"].render(self.title, True, t.TEXT)
        surface.blit(title_surf, (t.LIST_W // 2 - title_surf.get_width() // 2,
                                  t.HEADER_H // 2 - title_surf.get_height() // 2))
        pygame.draw.line(surface, t.DIVIDER, (0, t.HEADER_H), (t.SCREEN_W, t.HEADER_H))

        # Right panel
        pygame.draw.rect(surface, t.PANEL_BG, (t.PANEL_X, t.HEADER_H, t.PANEL_W, t.SCREEN_H - t.HEADER_H))
        pygame.draw.line(surface, t.DIVIDER, (t.PANEL_X, t.HEADER_H), (t.PANEL_X, t.SCREEN_H))
        self.draw_panel(surface)

        # List
        items = self.items()
        list_top = t.HEADER_H + LIST_TOP_PAD
        visible = items[self.scroll: self.scroll + MAX_VISIBLE]

        for i, item in enumerate(visible):
            abs_i = self.scroll + i
            y = list_top + i * ITEM_H

            if abs_i == self.selected:
                pygame.draw.rect(surface, t.HIGHLIGHT, (0, y - 4, t.LIST_W, ITEM_H))

            color = t.TEXT if abs_i == self.selected else t.TEXT_DIM
            label = self.fonts["item"].render(item, True, color)
            surface.blit(label, (16, y + ITEM_H // 2 - label.get_height() // 2 - 4))

            # Chevron
            chev_x = t.LIST_W - 14
            chev_y = y + ITEM_H // 2 - 5
            pygame.draw.polygon(surface, color, [
                (chev_x, chev_y),
                (chev_x + 5, chev_y + 5),
                (chev_x, chev_y + 10),
            ])

        # Scroll indicator
        if len(items) > MAX_VISIBLE:
            track_h = t.SCREEN_H - t.HEADER_H - LIST_TOP_PAD
            thumb_h = max(12, track_h * MAX_VISIBLE // len(items))
            thumb_y = t.HEADER_H + LIST_TOP_PAD + (track_h - thumb_h) * self.scroll // max(1, len(items) - MAX_VISIBLE)
            pygame.draw.rect(surface, t.DIVIDER, (t.LIST_W - 4, t.HEADER_H + LIST_TOP_PAD, 3, track_h))
            pygame.draw.rect(surface, t.TEXT_DIM, (t.LIST_W - 4, thumb_y, 3, thumb_h))
