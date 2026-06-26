import src.state as state
from src.scenes.menu_scene import MenuScene


class ArtistsMenu(MenuScene):
    title = "Artists"

    def items(self):
        if not state.artists:
            return ["(no artists)"]
        return sorted(state.artists.keys())

    def on_select(self, index, item):
        if not state.artists:
            return
        scene = self.manager._scenes["artist_albums"]
        scene.artist = item
        self.manager.switch("artist_albums")
