import io
import pygame
from src.scenes.base_scene import BaseScene
from src.input import get_button
import src.theme as t
import src.state as state

PAD = 10
ART_SIZE = 110
INFO_X = PAD + ART_SIZE + PAD
INFO_W = t.SCREEN_W - INFO_X - PAD
BAR_H = 10
BAR_Y = t.SCREEN_H - 36

_SCROLL_SPEED = 30
_SCROLL_PAUSE = 1500


def _fmt(seconds):
    s = int(seconds)
    return f"{s // 60}:{s % 60:02d}"


def _fmt_remaining(seconds, duration):
    rem = max(0, duration - seconds)
    s = int(rem)
    return f"-{s // 60}:{s % 60:02d}"


def _scale_art(raw_bytes, size):
    try:
        img = pygame.image.load(io.BytesIO(raw_bytes))
        return pygame.transform.smoothscale(img, (size, size))
    except Exception:
        return None


class NowPlaying(BaseScene):

    def __init__(self, manager, fonts):
        super().__init__(manager, fonts)
        self._art_cache = {}
        self._scroll_x = 0.0
        self._scroll_dir = 1
        self._scroll_wait = 0
        self._last_title = None
        self._last_tick = None

    def on_enter(self):
        self._scroll_x = 0.0
        self._scroll_dir = 1
        self._scroll_wait = _SCROLL_PAUSE
        self._last_title = None

    def handle_event(self, event):
        btn = get_button(event)
        if btn == "b":
            self.manager.back()
        elif btn == "start":
            state.player.toggle()
        elif btn == "left":
            self._prev()
        elif btn == "right":
            self._next()

    def _next(self):
        from src.scenes.songs_menu import _load_and_play
        if state.queue and state.queue_index < len(state.queue) - 1:
            state.queue_index += 1
            _load_and_play(state.queue_index)

    def _prev(self):
        from src.scenes.songs_menu import _load_and_play
        if state.player.position > 3:
            state.player.seek(0)
        elif state.queue and state.queue_index > 0:
            state.queue_index -= 1
            _load_and_play(state.queue_index)
        else:
            state.player.seek(0)

    def update(self):
        track = state.queue[state.queue_index] if state.queue else None
        title = track.title if track else ""
        if title != self._last_title:
            self._last_title = title
            self._scroll_x = 0.0
            self._scroll_dir = 1
            self._scroll_wait = _SCROLL_PAUSE

        now = pygame.time.get_ticks()
        delta_ms = (now - self._last_tick) if self._last_tick else 0
        self._last_tick = now

        title_surf = self.fonts["header"].render(title, True, t.TEXT)
        overflow = title_surf.get_width() - INFO_W
        if overflow > 0:
            if self._scroll_wait > 0:
                self._scroll_wait -= delta_ms
            else:
                self._scroll_x += self._scroll_dir * _SCROLL_SPEED * delta_ms / 1000.0
                if self._scroll_x >= overflow:
                    self._scroll_x = overflow
                    self._scroll_dir = -1
                    self._scroll_wait = _SCROLL_PAUSE
                elif self._scroll_x <= 0:
                    self._scroll_x = 0.0
                    self._scroll_dir = 1
                    self._scroll_wait = _SCROLL_PAUSE
        else:
            self._scroll_x = 0.0

    def _get_art(self, track, size):
        if track is None:
            return None
        key = (track.path, size)
        if key not in self._art_cache:
            self._art_cache[key] = (
                _scale_art(track.art_data, size) if track.art_data else None
            )
        return self._art_cache[key]

    def draw(self, surface):
        surface.fill(t.BG)

        track = state.queue[state.queue_index] if state.queue else None
        pos = state.player.position
        dur = state.player.duration
        progress = state.player.progress

        # Header
        pygame.draw.rect(surface, t.HEADER_BG, (0, 0, t.SCREEN_W, t.HEADER_H))
        hdr = self.fonts["header"].render("Now Playing", True, t.TEXT)
        surface.blit(hdr, (t.SCREEN_W // 2 - hdr.get_width() // 2,
                           t.HEADER_H // 2 - hdr.get_height() // 2))

        # Play indicator triangle (left of header)
        tri_x, tri_y = 10, t.HEADER_H // 2
        pygame.draw.polygon(surface, t.HIGHLIGHT,
                            [(tri_x, tri_y - 5), (tri_x + 7, tri_y), (tri_x, tri_y + 5)])

        pygame.draw.line(surface, t.DIVIDER, (0, t.HEADER_H), (t.SCREEN_W, t.HEADER_H))

        # Track counter
        if state.queue:
            counter = f"{state.queue_index + 1} of {len(state.queue)}"
            c = self.fonts["small"].render(counter, True, t.TEXT_DIM)
            surface.blit(c, (PAD, t.HEADER_H + 6))

        # Album art
        art_y = t.HEADER_H + 22
        art_rect = pygame.Rect(PAD, art_y, ART_SIZE, ART_SIZE)
        art_surf = self._get_art(track, ART_SIZE)
        if art_surf:
            surface.blit(art_surf, art_rect.topleft)
        else:
            t.draw_art_placeholder(surface, art_rect)

        # Track info (right of art)
        title_str  = track.title  if track else "No Track"
        artist_str = track.artist if track else ""
        album_str  = track.album  if track else ""

        info_y = art_y + 8

        # Title (scrolling)
        title_surf = self.fonts["header"].render(title_str, True, t.TEXT)
        clip = pygame.Rect(INFO_X, info_y, INFO_W, title_surf.get_height())
        surface.set_clip(clip)
        surface.blit(title_surf, (INFO_X - int(self._scroll_x), info_y))
        surface.set_clip(None)
        info_y += title_surf.get_height() + 6

        # Artist
        a = self.fonts["item"].render(artist_str, True, t.TEXT)
        surface.set_clip(pygame.Rect(INFO_X, info_y, INFO_W, a.get_height()))
        surface.blit(a, (INFO_X, info_y))
        surface.set_clip(None)
        info_y += a.get_height() + 4

        # Album
        al = self.fonts["small"].render(album_str, True, t.TEXT_DIM)
        surface.set_clip(pygame.Rect(INFO_X, info_y, INFO_W, al.get_height()))
        surface.blit(al, (INFO_X, info_y))
        surface.set_clip(None)

        # Progress bar — full width, gradient fill
        bar_x = PAD
        bar_w = t.SCREEN_W - PAD * 2
        pygame.draw.rect(surface, t.DIVIDER, (bar_x, BAR_Y, bar_w, BAR_H), border_radius=3)
        fill_w = max(0, int(bar_w * progress))
        if fill_w:
            t.draw_highlight(surface, (bar_x, BAR_Y, fill_w, BAR_H))
            # Round the corners of the fill
            pygame.draw.rect(surface, t.DIVIDER,
                             (bar_x, BAR_Y, bar_w, BAR_H), 1, border_radius=3)

        # Times
        time_y = BAR_Y + BAR_H + 4
        elapsed = self.fonts["small"].render(_fmt(pos), True, t.TEXT_DIM)
        remain  = self.fonts["small"].render(_fmt_remaining(pos, dur), True, t.TEXT_DIM)
        surface.blit(elapsed, (bar_x, time_y))
        surface.blit(remain, (bar_x + bar_w - remain.get_width(), time_y))
