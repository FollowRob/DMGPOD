import src.state as state
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
