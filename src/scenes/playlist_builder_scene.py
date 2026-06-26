import pygame
import src.theme as t
import src.state as state
from src.scenes.base_scene import BaseScene
from src.input import get_button
from src.library.playlists import save as save_playlist
from src.toast import toast

ITEM_H = 30
LIST_TOP = t.HEADER_H + 6
MAX_VISIBLE = (t.SCREEN_H - LIST_TOP - 24) // ITEM_H


class PlaylistBuilderScene(BaseScene):
    """Song picker. Set .playlist_name and optionally .existing_playlist before switching."""

    def __init__(self, manager, fonts):
        super().__init__(manager, fonts)
        self.playlist_name = ""
        self.existing_playlist = None   # set to edit an existing playlist
        self._selected = 0
        self._scroll = 0
        self._added = set()   # track paths

    def on_enter(self):
        self._selected = 0
        self._scroll = 0
        if self.existing_playlist:
            self._added = set(self.existing_playlist.get("tracks", []))
        else:
            self._added = set()

    def handle_event(self, event):
        btn = get_button(event)
        tracks = state.tracks
        if not tracks:
            if btn in ("b", "left"):
                self.manager.back()
            return

        if btn == "up":
            self._selected = (self._selected - 1) % len(tracks)
            self._clamp_scroll(len(tracks))
        elif btn == "down":
            self._selected = (self._selected + 1) % len(tracks)
            self._clamp_scroll(len(tracks))
        elif btn == "a":
            path = tracks[self._selected].path
            if path in self._added:
                self._added.discard(path)
            else:
                self._added.add(path)
        elif btn in ("b", "left"):
            self.manager.back()
        elif btn == "start":
            self._save_and_finish()

    def _clamp_scroll(self, total):
        if self._selected < self._scroll:
            self._scroll = self._selected
        elif self._selected >= self._scroll + MAX_VISIBLE:
            self._scroll = self._selected - MAX_VISIBLE + 1

    def _save_and_finish(self):
        if not self._added:
            toast.show("Add at least one track")
            return
        tracks = state.tracks
        ordered = [tr.path for tr in tracks if tr.path in self._added]
        playlist = dict(self.existing_playlist) if self.existing_playlist else {}
        playlist["name"] = self.playlist_name
        playlist["tracks"] = ordered
        save_playlist(playlist)
        self.existing_playlist = None
        toast.show(f'Saved "{self.playlist_name}"')
        self.manager.switch("playlists_menu", push_history=False)

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(t.BG)

        # Header
        pygame.draw.rect(surface, t.HEADER_BG, (0, 0, t.SCREEN_W, t.HEADER_H))
        title = self.fonts["header"].render(
            f'"{self.playlist_name}"  ({len(self._added)} tracks)', True, t.TEXT)
        surface.blit(title, (t.SCREEN_W // 2 - title.get_width() // 2,
                             t.HEADER_H // 2 - title.get_height() // 2))
        pygame.draw.line(surface, t.DIVIDER, (0, t.HEADER_H), (t.SCREEN_W, t.HEADER_H))

        tracks = state.tracks
        if not tracks:
            msg = self.fonts["small"].render("No tracks found", True, t.TEXT_DIM)
            surface.blit(msg, (t.SCREEN_W // 2 - msg.get_width() // 2, t.SCREEN_H // 2))
            return

        visible = tracks[self._scroll: self._scroll + MAX_VISIBLE]
        for i, track in enumerate(visible):
            abs_i = self._scroll + i
            y = LIST_TOP + i * ITEM_H
            in_list = track.path in self._added

            if abs_i == self._selected:
                t.draw_highlight(surface, (0, y, t.SCREEN_W, ITEM_H))

            col = t.TEXT_HI if abs_i == self._selected else t.TEXT

            # Checkbox
            box_x, box_y = 10, y + ITEM_H // 2 - 6
            pygame.draw.rect(surface, col, (box_x, box_y, 12, 12), 1, border_radius=2)
            if in_list:
                pygame.draw.rect(surface, t.TEXT_HI if abs_i == self._selected else t.HIGHLIGHT,
                                 (box_x + 2, box_y + 2, 8, 8), border_radius=1)

            label = self.fonts["small"].render(
                f"{track.title}  —  {track.artist}", True, col)
            surface.blit(label, (28, y + ITEM_H // 2 - label.get_height() // 2))

        # Scroll indicator
        if len(tracks) > MAX_VISIBLE:
            track_h = t.SCREEN_H - LIST_TOP - 24
            thumb_h = max(10, track_h * MAX_VISIBLE // len(tracks))
            thumb_y = LIST_TOP + (track_h - thumb_h) * self._scroll // max(1, len(tracks) - MAX_VISIBLE)
            pygame.draw.rect(surface, t.DIVIDER, (t.SCREEN_W - 4, LIST_TOP, 3, track_h))
            pygame.draw.rect(surface, t.TEXT_DIM, (t.SCREEN_W - 4, thumb_y, 3, thumb_h))

        # Bottom hint
        hint = self.fonts["small"].render("A: toggle  Start: save  B: back", True, t.TEXT_DIM)
        surface.blit(hint, (t.SCREEN_W // 2 - hint.get_width() // 2, t.SCREEN_H - 20))
