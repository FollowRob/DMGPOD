import pygame
import src.state as state
import src.theme as t
from src.scenes.menu_scene import MenuScene


class ArtistAlbumsMenu(MenuScene):
    title = "Albums"

    def __init__(self, manager, fonts):
        super().__init__(manager, fonts)
        self.artist = None

    def on_enter(self):
        self.selected = 0
        self.scroll = 0
        if self.artist:
            self.title = self.artist

    def _artist_albums(self):
        if not self.artist:
            return []
        tracks = state.artists.get(self.artist, [])
        seen = {}
        for t in tracks:
            seen.setdefault(t.album, []).append(t)
        return sorted(seen.keys())

    def items(self):
        albums = self._artist_albums()
        return albums if albums else ["(no albums)"]

    def on_select(self, index, item):
        albums = self._artist_albums()
        if not albums:
            return
        album_tracks = [tr for tr in state.artists.get(self.artist, []) if tr.album == item]
        scene = self.manager._scenes["album_tracks"]
        scene.album = item
        scene.track_list = sorted(album_tracks, key=lambda tr: tr.track_num)
        self.manager.switch("album_tracks")

    def _should_show_panel(self, playing, track):
        return bool(self._artist_albums())

    def draw_panel(self, surface, playing, track):
        albums = self._artist_albums()
        if not albums:
            return
        album_name = albums[self.selected] if self.selected < len(albums) else None
        if not album_name:
            return

        all_tracks = state.artists.get(self.artist, [])
        art_track = next((tr for tr in all_tracks if tr.album == album_name and tr.art_data), None)

        px = t.PANEL_X
        pw = t.PANEL_W
        art_size = pw - 16
        art_rect = pygame.Rect(px + 8, t.HEADER_H + 10, art_size, art_size)

        art = self._get_art(art_track, art_size) if art_track else None
        if art:
            surface.blit(art, art_rect.topleft)
        else:
            pygame.draw.rect(surface, t.BG, art_rect, border_radius=4)
            note = self.fonts["header"].render("♪", True, t.TEXT_DIM)
            surface.blit(note, (art_rect.centerx - note.get_width() // 2,
                                art_rect.centery - note.get_height() // 2))

        label_y = art_rect.bottom + 8
        label = self.fonts["small"].render(album_name, True, t.TEXT)
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
