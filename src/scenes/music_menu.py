from src.scenes.menu_scene import MenuScene


class MusicMenu(MenuScene):
    title = "Music"

    def items(self):
        return ["Artists", "Albums", "Songs", "Playlists", "Now Playing"]

    def on_select(self, index, item):
        destinations = {
            "Artists":     "artists_menu",
            "Albums":      "albums_menu",
            "Songs":       "songs_menu",
            "Playlists":   "playlists_menu",
            "Now Playing": "now_playing",
        }
        dest = destinations.get(item)
        if dest:
            self.manager.switch(dest)
