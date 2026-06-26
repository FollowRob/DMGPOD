import io
import pygame
from src.scenes.base_scene import BaseScene
from src.input import get_button
import src.theme as t
import src.state as state

ITEM_H = 34
LIST_TOP_PAD = 8


def _max_visible(list_w):
    return (t.SCREEN_H - t.HEADER_H - LIST_TOP_PAD) // ITEM_H


def _scale_art(raw_bytes, size):
    try:
        img = pygame.image.load(io.BytesIO(raw_bytes))
        return pygame.transform.smoothscale(img, (size, size))
    except Exception:
        return None


class MenuScene(BaseScene):
    """Reusable iPod-style left-panel menu. Subclass and override title, items(), on_select(), draw_panel()."""

    title = "Menu"

    def __init__(self, manager, fonts):
        super().__init__(manager, fonts)
        self.selected = 0
        self.scroll = 0
        self._art_cache = {}

    def items(self):
        return []

    def on_select(self, index, item):
        pass

    def _should_show_panel(self, playing, track):
        return playing and track is not None

    def draw_panel(self, surface, playing, track):
        if playing and track:
            self._draw_mini_player(surface, track)

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

    def _clamp_scroll(self, list_w=None):
        mv = _max_visible(list_w or t.LIST_W)
        if self.selected < self.scroll:
            self.scroll = self.selected
        elif self.selected >= self.scroll + mv:
            self.scroll = self.selected - mv + 1

    def _get_art(self, track, size):
        if track is None:
            return None
        key = (track.path, size)
        if key not in self._art_cache:
            self._art_cache[key] = _scale_art(track.art_data, size) if track.art_data else None
        return self._art_cache[key]

    def draw(self, surface):
        surface.fill(t.BG)

        playing = state.player.is_playing
        track = state.queue[state.queue_index] if state.queue else None
        show_panel = self._should_show_panel(playing, track)

        list_w = t.LIST_W if show_panel else t.SCREEN_W
        mv = _max_visible(list_w)

        # Header
        pygame.draw.rect(surface, t.HEADER_BG, (0, 0, t.SCREEN_W, t.HEADER_H))
        title_surf = self.fonts["header"].render(self.title, True, t.TEXT)
        surface.blit(title_surf, (list_w // 2 - title_surf.get_width() // 2,
                                  t.HEADER_H // 2 - title_surf.get_height() // 2))
        pygame.draw.line(surface, t.DIVIDER, (0, t.HEADER_H), (t.SCREEN_W, t.HEADER_H))

        # Right panel
        if show_panel:
            pygame.draw.rect(surface, t.PANEL_BG, (t.PANEL_X, t.HEADER_H, t.PANEL_W, t.SCREEN_H - t.HEADER_H))
            pygame.draw.line(surface, t.DIVIDER, (t.PANEL_X, t.HEADER_H), (t.PANEL_X, t.SCREEN_H))
            self.draw_panel(surface, playing, track)

        # List
        items = self.items()
        list_top = t.HEADER_H + LIST_TOP_PAD
        visible = items[self.scroll: self.scroll + mv]

        for i, item in enumerate(visible):
            abs_i = self.scroll + i
            y = list_top + i * ITEM_H

            if abs_i == self.selected:
                pygame.draw.rect(surface, t.HIGHLIGHT, (0, y - 4, list_w, ITEM_H))

            color = t.TEXT if abs_i == self.selected else t.TEXT_DIM
            label = self.fonts["item"].render(item, True, color)
            surface.blit(label, (16, y + ITEM_H // 2 - label.get_height() // 2 - 4))

            # Chevron
            chev_x = list_w - 14
            chev_y = y + ITEM_H // 2 - 5
            pygame.draw.polygon(surface, color, [
                (chev_x, chev_y),
                (chev_x + 5, chev_y + 5),
                (chev_x, chev_y + 10),
            ])

        # Scroll indicator
        if len(items) > mv:
            track_h = t.SCREEN_H - t.HEADER_H - LIST_TOP_PAD
            thumb_h = max(12, track_h * mv // len(items))
            thumb_y = (t.HEADER_H + LIST_TOP_PAD +
                       (track_h - thumb_h) * self.scroll // max(1, len(items) - mv))
            pygame.draw.rect(surface, t.DIVIDER,
                             (list_w - 4, t.HEADER_H + LIST_TOP_PAD, 3, track_h))
            pygame.draw.rect(surface, t.TEXT_DIM, (list_w - 4, thumb_y, 3, thumb_h))

    def _draw_mini_player(self, surface, track):
        px = t.PANEL_X
        pw = t.PANEL_W

        # Album art
        art_size = pw - 16
        art_y = t.HEADER_H + 10
        art_rect = pygame.Rect(px + 8, art_y, art_size, art_size)
        pygame.draw.rect(surface, t.BG, art_rect)

        art = self._get_art(track, art_size)
        if art:
            surface.blit(art, art_rect.topleft)
        else:
            note = self.fonts["header"].render("♪", True, t.TEXT_DIM)
            surface.blit(note, (art_rect.centerx - note.get_width() // 2,
                                art_rect.centery - note.get_height() // 2))

        # Track info
        info_y = art_rect.bottom + 8
        info_x = px + 8
        info_w = pw - 16

        # Clip long text
        for text, font_key, color in [
            (track.title,  "small", t.TEXT),
            (track.artist, "small", t.TEXT_DIM),
        ]:
            s = self.fonts[font_key].render(text, True, color)
            clip = pygame.Rect(info_x, info_y, info_w, s.get_height())
            surface.set_clip(clip)
            surface.blit(s, (info_x, info_y))
            surface.set_clip(None)
            info_y += s.get_height() + 2

        # Progress bar
        bar_y = info_y + 4
        progress = state.player.progress
        pygame.draw.rect(surface, t.DIVIDER, (info_x, bar_y, info_w, 2))
        pygame.draw.rect(surface, t.HIGHLIGHT, (info_x, bar_y, int(info_w * progress), 2))

        # Play indicator dot
        dot_col = t.HIGHLIGHT if state.player.is_playing else t.TEXT_DIM
        pygame.draw.circle(surface, dot_col, (px + pw // 2, bar_y + 10), 3)
