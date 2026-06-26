import src.state as state
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
