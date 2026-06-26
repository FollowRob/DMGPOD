import src.state as state
from src.scenes.menu_scene import MenuScene


class SongsMenu(MenuScene):
    title = "Songs"

    def items(self):
        if not state.tracks:
            return ["(no tracks)"]
        return [t.title for t in state.tracks]

    def on_select(self, index, item):
        if not state.tracks:
            return
        track = state.tracks[index]
        already_playing = (
            state.queue and
            state.queue_index < len(state.queue) and
            state.queue[state.queue_index].path == track.path
        )
        if not already_playing:
            state.queue = list(state.tracks)
            state.queue_index = index
            _load_and_play(index)
        self.manager.switch("now_playing")


def _load_and_play(index):
    track = state.queue[index]
    state.player.load(track.path)
    state.player.play()
    state.player.on_track_end = _next_track


def _next_track():
    state.queue_index += 1
    if state.queue_index < len(state.queue):
        _load_and_play(state.queue_index)
