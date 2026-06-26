import src.state as state
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
        album_tracks = [t for t in state.artists.get(self.artist, []) if t.album == item]
        scene = self.manager._scenes["album_tracks"]
        scene.album = item
        scene.track_list = sorted(album_tracks, key=lambda t: t.track_num)
        self.manager.switch("album_tracks")
