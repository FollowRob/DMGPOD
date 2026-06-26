import pygame
import src.state as state
import src.theme as t
from src.scenes.menu_scene import MenuScene


class AlbumsMenu(MenuScene):
    title = "Albums"

    def items(self):
        if not state.albums:
            return ["(no albums)"]
        return sorted(state.albums.keys())

    def on_select(self, index, item):
        if not state.albums:
            return
        scene = self.manager._scenes["album_tracks"]
        scene.album = item
        scene.track_list = sorted(state.albums.get(item, []), key=lambda t: t.track_num)
        self.manager.switch("album_tracks")

    def _should_show_panel(self, playing, track):
        return bool(self.items() and self.items()[0] != "(no albums)")

    def draw_panel(self, surface, playing, track):
        items = self.items()
        if not items or items[0] == "(no albums)":
            return

        album_name = items[self.selected] if self.selected < len(items) else None
        if not album_name:
            return

        tracks = state.albums.get(album_name, [])
        art_track = next((tr for tr in tracks if tr.art_data), None)

        px = t.PANEL_X
        pw = t.PANEL_W
        art_size = pw - 16
        art_rect = pygame.Rect(px + 8, t.HEADER_H + 10, art_size, art_size)

        art = self._get_art(art_track, art_size) if art_track else None
        if art:
            surface.blit(art, art_rect.topleft)
        else:
            t.draw_art_placeholder(surface, art_rect)

        # Album name
        label_y = art_rect.bottom + 8
        label = self.fonts["small"].render(album_name, True, t.TEXT)
        clip = pygame.Rect(px + 8, label_y, pw - 16, label.get_height())
        surface.set_clip(clip)
        surface.blit(label, (px + 8, label_y))
        surface.set_clip(None)

        # If also playing, show a small progress bar at the bottom
        if playing and track:
            bar_y = t.SCREEN_H - 12
            bar_x = px + 8
            bar_w = pw - 16
            progress = state.player.progress
            pygame.draw.rect(surface, t.DIVIDER, (bar_x, bar_y, bar_w, 2))
            pygame.draw.rect(surface, t.HIGHLIGHT, (bar_x, bar_y, int(bar_w * progress), 2))
