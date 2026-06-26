import pygame
import sys
import os

import src.theme as t
import src.state as state
from src.library.scanner import scan, build_index
from src.scene_manager import SceneManager
from src.toast import toast
import src.cart as cart
import src.volume_overlay as vol
from src.scenes.main_menu import MainMenu
from src.scenes.music_menu import MusicMenu
from src.scenes.extras_menu import ExtrasMenu
from src.scenes.settings_menu import SettingsMenu
from src.scenes.games_menu import GamesMenu
from src.scenes.now_playing import NowPlaying
from src.scenes.songs_menu import SongsMenu
from src.scenes.artists_menu import ArtistsMenu
from src.scenes.albums_menu import AlbumsMenu
from src.scenes.artist_albums_menu import ArtistAlbumsMenu
from src.scenes.album_tracks_menu import AlbumTracksMenu
from src.scenes.boot_splash import BootSplash
from src.scenes.about_scene import AboutScene
from src.scenes.stub_menu import StubMenu

FPS = 60
MUSIC_DIR = os.path.join(os.path.dirname(__file__), "music")


def main():
    pygame.init()
    screen = pygame.display.set_mode((t.SCREEN_W, t.SCREEN_H))
    pygame.display.set_caption("DMGPod")
    clock = pygame.time.Clock()

    fonts = t.load_fonts()

    state.tracks = scan(MUSIC_DIR)
    state.artists, state.albums = build_index(state.tracks)

    manager = SceneManager()
    manager.register("boot_splash",    BootSplash(manager, fonts))
    manager.register("main_menu",      MainMenu(manager, fonts))
    manager.register("music_menu",     MusicMenu(manager, fonts))
    manager.register("extras_menu",    ExtrasMenu(manager, fonts))
    manager.register("settings_menu",  SettingsMenu(manager, fonts))
    manager.register("games_menu",     GamesMenu(manager, fonts))
    manager.register("now_playing",    NowPlaying(manager, fonts))
    manager.register("songs_menu",     SongsMenu(manager, fonts))
    manager.register("artists_menu",   ArtistsMenu(manager, fonts))
    manager.register("albums_menu",    AlbumsMenu(manager, fonts))
    manager.register("artist_albums",  ArtistAlbumsMenu(manager, fonts))
    manager.register("album_tracks",   AlbumTracksMenu(manager, fonts))
    manager.register("playlists_menu", StubMenu(manager, fonts, "Playlists"))
    manager.register("about",          AboutScene(manager, fonts))

    manager.switch("boot_splash", push_history=False)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state.player.stop()
                pygame.quit()
                sys.exit()
            cart.handle_event(event, manager)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFTBRACKET:
                    vol.bump(-0.05)
                elif event.key == pygame.K_RIGHTBRACKET:
                    vol.bump(0.05)
            manager.handle_event(event)

        manager.update()
        manager.draw(screen)
        t.draw_battery(screen, fonts)
        toast.draw(screen, fonts)
        vol.draw(screen, fonts)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
