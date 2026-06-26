import pygame
import src.theme as t
import src.state as state
from src.scenes.menu_scene import MenuScene
from src.library.playlists import delete as delete_playlist
from src.toast import toast


class PlaylistDetailScene(MenuScene):
    """Options for a single playlist. Set .playlist before switching."""

    def __init__(self, manager, fonts):
        super().__init__(manager, fonts)
        self.playlist = None

    @property
    def title(self):
        return self.playlist["name"] if self.playlist else "Playlist"

    def items(self):
        return ["Play", "Edit", "Delete"]

    def on_select(self, index, item):
        if item == "Play":
            self._play()
        elif item == "Edit":
            self._edit()
        elif item == "Delete":
            self._delete()

    def _play(self):
        from src.scenes.songs_menu import _load_and_play
        if not self.playlist:
            return
        track_paths = set(self.playlist.get("tracks", []))
        queue = [tr for tr in state.tracks if tr.path in track_paths]
        if not queue:
            toast.show("No tracks found")
            return
        state.queue = queue
        state.queue_index = 0
        _load_and_play(0)
        self.manager.switch("now_playing")

    def _edit(self):
        builder = self.manager.get("playlist_builder")
        builder.playlist_name = self.playlist["name"]
        builder.existing_playlist = self.playlist
        self.manager.switch("playlist_builder")

    def _delete(self):
        name = self.playlist["name"]
        delete_playlist(self.playlist)
        self.playlist = None
        toast.show(f'Deleted "{name}"')
        self.manager.switch("playlists_menu", push_history=False)

    def draw_panel(self, surface, playing=None, track=None):
        if not self.playlist:
            return
        cx = t.PANEL_X + t.PANEL_W // 2
        cy = t.HEADER_H + (t.SCREEN_H - t.HEADER_H) // 2
        count = len(self.playlist.get("tracks", []))
        s = self.fonts["small"].render(f"{count} track{'s' if count != 1 else ''}", True, t.TEXT_DIM)
        surface.blit(s, (cx - s.get_width() // 2, cy - s.get_height() // 2))
