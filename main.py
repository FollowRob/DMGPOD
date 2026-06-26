import pygame
import sys

import src.theme as t
from src.scene_manager import SceneManager
from src.scenes.main_menu import MainMenu
from src.scenes.music_menu import MusicMenu
from src.scenes.extras_menu import ExtrasMenu
from src.scenes.settings_menu import SettingsMenu
from src.scenes.games_menu import GamesMenu
from src.scenes.now_playing import NowPlaying
from src.scenes.stub_menu import StubMenu

FPS = 60


def main():
    pygame.init()
    screen = pygame.display.set_mode((t.SCREEN_W, t.SCREEN_H))
    pygame.display.set_caption("DMGPod")
    clock = pygame.time.Clock()

    fonts = t.load_fonts()
    manager = SceneManager()

    manager.register("main_menu",     MainMenu(manager, fonts))
    manager.register("music_menu",    MusicMenu(manager, fonts))
    manager.register("extras_menu",   ExtrasMenu(manager, fonts))
    manager.register("settings_menu", SettingsMenu(manager, fonts))
    manager.register("games_menu",    GamesMenu(manager, fonts))
    manager.register("now_playing",   NowPlaying(manager, fonts))
    manager.register("artists_menu",  StubMenu(manager, fonts, "Artists"))
    manager.register("albums_menu",   StubMenu(manager, fonts, "Albums"))
    manager.register("songs_menu",    StubMenu(manager, fonts, "Songs"))
    manager.register("playlists_menu", StubMenu(manager, fonts, "Playlists"))

    manager.switch("main_menu", push_history=False)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            manager.handle_event(event)

        manager.update()
        manager.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
