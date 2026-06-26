import io
import pygame
from src.scenes.base_scene import BaseScene
from src.input import get_button
import src.theme as t
import src.state as state


def _fmt(seconds):
    s = int(seconds)
    return f"{s // 60}:{s % 60:02d}"


def _scale_art(raw_bytes, size):
    try:
        img = pygame.image.load(io.BytesIO(raw_bytes))
        return pygame.transform.smoothscale(img, (size, size))
    except Exception:
        return None


_SCROLL_SPEED = 30   # pixels per second
_SCROLL_PAUSE = 1500  # ms pause at each end


class NowPlaying(BaseScene):

    def __init__(self, manager, fonts):
        super().__init__(manager, fonts)
        self._art_cache = {}   # path -> surface or None
        self._scroll_x = 0.0
        self._scroll_dir = 1
        self._scroll_wait = 0
        self._last_title = None

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
        import pygame
        track = state.queue[state.queue_index] if state.queue else None
        title = track.title if track else ""
        if title != self._last_title:
            self._last_title = title
            self._scroll_x = 0.0
            self._scroll_dir = 1
            self._scroll_wait = _SCROLL_PAUSE

        dt = pygame.time.get_ticks()
        if not hasattr(self, "_last_tick"):
            self._last_tick = dt
        delta_ms = dt - self._last_tick
        self._last_tick = dt

        title_surf = self.fonts["header"].render(title, True, (255, 255, 255))
        info_x, info_w = self._info_bounds()
        overflow = title_surf.get_width() - info_w
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

    def _info_bounds(self):
        art_size = t.SCREEN_H - t.HEADER_H - 16
        info_x = 8 + art_size + 10
        info_w = t.SCREEN_W - info_x - 6
        return info_x, info_w

    def _get_art(self, track, size):
        if track is None:
            return None
        key = (track.path, size)
        if key not in self._art_cache:
            if track.art_data:
                self._art_cache[key] = _scale_art(track.art_data, size)
            else:
                self._art_cache[key] = None
        return self._art_cache[key]

    def draw(self, surface):
        surface.fill(t.BG)

        track = state.queue[state.queue_index] if state.queue else None
        playing = state.player.is_playing
        pos = state.player.position
        dur = state.player.duration
        progress = state.player.progress

        # Header
        pygame.draw.rect(surface, t.HEADER_BG, (0, 0, t.SCREEN_W, t.HEADER_H))
        title_surf = self.fonts["header"].render("Now Playing", True, t.TEXT)
        surface.blit(title_surf, (
            t.SCREEN_W // 2 - title_surf.get_width() // 2,
            t.HEADER_H // 2 - title_surf.get_height() // 2,
        ))
        pygame.draw.line(surface, t.DIVIDER, (0, t.HEADER_H), (t.SCREEN_W, t.HEADER_H))

        # Album art (left square)
        art_size = t.SCREEN_H - t.HEADER_H - 16
        art_rect = pygame.Rect(8, t.HEADER_H + 8, art_size, art_size)
        pygame.draw.rect(surface, t.PANEL_BG, art_rect)
        pygame.draw.rect(surface, t.DIVIDER, art_rect, 1)

        art_surf = self._get_art(track, art_size)
        if art_surf:
            surface.blit(art_surf, art_rect.topleft)
        else:
            note = self.fonts["header"].render("♪", True, t.TEXT_DIM)
            surface.blit(note, (
                art_rect.centerx - note.get_width() // 2,
                art_rect.centery - note.get_height() // 2,
            ))

        # Info panel
        info_x = art_rect.right + 10
        info_w = t.SCREEN_W - info_x - 6
        info_y = t.HEADER_H + 12

        title_str  = track.title  if track else "No Track"
        artist_str = track.artist if track else "Unknown Artist"
        album_str  = track.album  if track else "Unknown Album"

        title_surf = self.fonts["header"].render(title_str, True, t.TEXT)
        clip = pygame.Rect(info_x, info_y, info_w, title_surf.get_height())
        surface.set_clip(clip)
        surface.blit(title_surf, (info_x - int(self._scroll_x), info_y))
        surface.set_clip(None)

        surface.blit(self.fonts["small"].render(artist_str,  True, t.TEXT_DIM), (info_x, info_y + 18))
        surface.blit(self.fonts["small"].render(album_str,   True, t.TEXT_DIM), (info_x, info_y + 32))

        # Progress bar
        bar_y = info_y + 56
        pygame.draw.rect(surface, t.DIVIDER, (info_x, bar_y, info_w, 3))
        pygame.draw.rect(surface, t.HIGHLIGHT, (info_x, bar_y, int(info_w * progress), 3))

        # Time
        elapsed_s = self.fonts["small"].render(_fmt(pos), True, t.TEXT_DIM)
        total_s   = self.fonts["small"].render(_fmt(dur), True, t.TEXT_DIM)
        surface.blit(elapsed_s, (info_x, bar_y + 6))
        surface.blit(total_s, (info_x + info_w - total_s.get_width(), bar_y + 6))

        # Transport
        ctrl_y = bar_y + 30
        ctrl_cx = info_x + info_w // 2
        self._draw_transport(surface, ctrl_cx, ctrl_y, playing)

    def _draw_transport(self, surface, cx, cy, playing):
        col = t.TEXT_DIM
        # Prev ◀◀
        pygame.draw.polygon(surface, col, [(cx - 28, cy), (cx - 20, cy - 6), (cx - 20, cy + 6)])
        pygame.draw.rect(surface, col, (cx - 30, cy - 6, 3, 12))
        # Next ▶▶
        pygame.draw.polygon(surface, col, [(cx + 28, cy), (cx + 20, cy - 6), (cx + 20, cy + 6)])
        pygame.draw.rect(surface, col, (cx + 28, cy - 6, 3, 12))
        # Play / Pause
        if playing:
            pygame.draw.rect(surface, t.TEXT, (cx - 5, cy - 7, 4, 14))
            pygame.draw.rect(surface, t.TEXT, (cx + 1, cy - 7, 4, 14))
        else:
            pygame.draw.polygon(surface, t.TEXT, [(cx - 6, cy - 7), (cx + 8, cy), (cx - 6, cy + 7)])
