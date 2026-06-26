import pygame
import src.theme as t
from src.scenes.menu_scene import MenuScene
from src.library.playlists import load_all


class PlaylistsMenu(MenuScene):
    title = "Playlists"

    def on_enter(self):
        super().on_enter()
        self._playlists = load_all()

    def items(self):
        return ["New Playlist"] + [p["name"] for p in self._playlists]

    def on_select(self, index, item):
        if item == "New Playlist":
            entry = self.manager.get("name_entry")
            entry.playlist_name = ""

            def on_confirm(name):
                builder = self.manager.get("playlist_builder")
                builder.playlist_name = name
                self.manager.switch("playlist_builder")

            entry.on_confirm = on_confirm
            self.manager.switch("name_entry")
        else:
            playlist = self._playlists[index - 1]
            detail = self.manager.get("playlist_detail")
            detail.playlist = playlist
            self.manager.switch("playlist_detail")

    def draw_panel(self, surface):
        cx = t.PANEL_X + t.PANEL_W // 2
        cy = t.HEADER_H + (t.SCREEN_H - t.HEADER_H) // 2
        count = len(self._playlists)
        label = f"{count} playlist{'s' if count != 1 else ''}" if count else "No playlists yet"
        s = self.fonts["small"].render(label, True, t.TEXT_DIM)
        surface.blit(s, (cx - s.get_width() // 2, cy - s.get_height() // 2))
