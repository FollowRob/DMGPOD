import pygame
import src.state as state
from src.toast import toast
from src.scenes.songs_menu import _load_and_play

# Keyboard cart simulation
# Keys 1-9 → music cart (playlist slot)
# Key 0    → games cart
# Key e    → eject

MUSIC_KEYS = {
    pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3,
    pygame.K_4: 4, pygame.K_5: 5, pygame.K_6: 6,
    pygame.K_7: 7, pygame.K_8: 8, pygame.K_9: 9,
}


def handle_event(event, manager):
    if event.type != pygame.KEYDOWN:
        return

    if event.key in MUSIC_KEYS:
        _insert_music(MUSIC_KEYS[event.key], manager)
    elif event.key == pygame.K_0:
        _insert_games(manager)
    elif event.key == pygame.K_e:
        _eject(manager)


def _insert_music(slot, manager):
    state.cart_inserted = "music"
    state.cart_playlist_id = slot

    if not state.tracks:
        toast.show(f"Cart {slot}: no tracks found")
        return

    # For now: all tracks as the queue (Phase 5 — playlists come later)
    state.queue = list(state.tracks)
    state.queue_index = 0
    _load_and_play(0)

    track = state.queue[0]
    toast.show(f"♫  {track.title}")
    manager.switch("now_playing")


def _insert_games(manager):
    state.cart_inserted = "games"
    state.games_unlocked = True

    # Tell main menu to show Games
    main_menu = manager._scenes.get("main_menu")
    if main_menu:
        main_menu.games_unlocked = True

    toast.show("Games Unlocked")


def _eject(manager):
    prev = state.cart_inserted
    state.cart_inserted = None
    state.cart_playlist_id = None

    if prev == "games":
        state.games_unlocked = False
        main_menu = manager._scenes.get("main_menu")
        if main_menu:
            main_menu.games_unlocked = False
        toast.show("Cart ejected")
    elif prev == "music":
        toast.show("Cart ejected — playback continues")
    else:
        toast.show("No cart inserted")
