import pygame
import src.state as state
import src.theme as t
from src.scenes.menu_scene import MenuScene
from src.scenes.songs_menu import _load_and_play


class AlbumTracksMenu(MenuScene):
    title = "Tracks"

    def __init__(self, manager, fonts):
        super().__init__(manager, fonts)
        self.album = None
        self.track_list = []

    def on_enter(self):
        self.selected = 0
        self.scroll = 0
        if self.album:
            self.title = self.album

    def items(self):
        return [t.title for t in self.track_list] if self.track_list else ["(no tracks)"]

    def on_select(self, index, item):
        if not self.track_list:
            return
        track = self.track_list[index]
        already_playing = (
            state.queue and
            state.queue_index < len(state.queue) and
            state.queue[state.queue_index].path == track.path
        )
        if not already_playing:
            state.queue = list(self.track_list)
            state.queue_index = index
            _load_and_play(index)
        self.manager.switch("now_playing")

    def _should_show_panel(self, playing, track):
        return bool(self.track_list)

    def draw_panel(self, surface, playing, track):
        if not self.track_list:
            return

        art_track = next((tr for tr in self.track_list if tr.art_data), None)
        px = t.PANEL_X
        pw = t.PANEL_W
        art_size = pw - 16
        art_rect = pygame.Rect(px + 8, t.HEADER_H + 10, art_size, art_size)

        art = self._get_art(art_track, art_size) if art_track else None
        if art:
            surface.blit(art, art_rect.topleft)
        else:
            t.draw_art_placeholder(surface, art_rect)

        if playing and track:
            bar_y = t.SCREEN_H - 12
            bar_x = px + 8
            bar_w = pw - 16
            progress = state.player.progress
            pygame.draw.rect(surface, t.DIVIDER, (bar_x, bar_y, bar_w, 2))
            pygame.draw.rect(surface, t.HIGHLIGHT, (bar_x, bar_y, int(bar_w * progress), 2))
