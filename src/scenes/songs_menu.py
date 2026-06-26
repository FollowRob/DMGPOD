import pygame
import src.state as state
import src.theme as t
from src.scenes.menu_scene import MenuScene


class SongsMenu(MenuScene):
    title = "Songs"

    def items(self):
        if not state.tracks:
            return ["(no tracks)"]
        return [t.title for t in state.tracks]

    def on_select(self, index, item):
        if not state.tracks:
            return
        track = state.tracks[index]
        already_playing = (
            state.queue and
            state.queue_index < len(state.queue) and
            state.queue[state.queue_index].path == track.path
        )
        if not already_playing:
            state.queue = list(state.tracks)
            state.queue_index = index
            _load_and_play(index)
        self.manager.switch("now_playing")

    def _should_show_panel(self, playing, track):
        return bool(state.tracks)

    def draw_panel(self, surface, playing, track):
        if not state.tracks:
            return

        highlighted = state.tracks[self.selected] if self.selected < len(state.tracks) else None
        if not highlighted:
            return

        art_track = highlighted if highlighted.art_data else None
        px = t.PANEL_X
        pw = t.PANEL_W
        art_size = pw - 16
        art_rect = pygame.Rect(px + 8, t.HEADER_H + 10, art_size, art_size)

        art = self._get_art(art_track, art_size) if art_track else None
        if art:
            surface.blit(art, art_rect.topleft)
        else:
            t.draw_art_placeholder(surface, art_rect)

        label_y = art_rect.bottom + 8
        label = self.fonts["small"].render(highlighted.album, True, t.TEXT_DIM)
        clip = pygame.Rect(px + 8, label_y, pw - 16, label.get_height())
        surface.set_clip(clip)
        surface.blit(label, (px + 8, label_y))
        surface.set_clip(None)

        if playing and track:
            bar_y = t.SCREEN_H - 12
            bar_x = px + 8
            bar_w = pw - 16
            progress = state.player.progress
            pygame.draw.rect(surface, t.DIVIDER, (bar_x, bar_y, bar_w, 2))
            pygame.draw.rect(surface, t.HIGHLIGHT, (bar_x, bar_y, int(bar_w * progress), 2))


def _load_and_play(index):
    track = state.queue[index]
    state.player.load(track.path)
    state.player.play()
    state.player.on_track_end = _next_track


def _next_track():
    state.queue_index += 1
    if state.queue_index < len(state.queue):
        _load_and_play(state.queue_index)
