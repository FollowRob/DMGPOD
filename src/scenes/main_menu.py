import pygame
from src.scenes.menu_scene import MenuScene
from src.input import get_button
import src.theme as t


class MainMenu(MenuScene):
    title = "DMGPod"

    def __init__(self, manager, fonts):
        super().__init__(manager, fonts)
        self.games_unlocked = False

    def items(self):
        base = ["Music"]
        if self.games_unlocked:
            base.append("Games")
        base += ["Extras", "Settings"]
        return base

    def on_enter(self):
        self.selected = 0
        self.scroll = 0

    def handle_event(self, event):
        btn = get_button(event)
        items = self.items()
        if btn == "up":
            self.selected = (self.selected - 1) % len(items)
            self._clamp_scroll()
        elif btn == "down":
            self.selected = (self.selected + 1) % len(items)
            self._clamp_scroll()
        elif btn in ("a", "right"):
            self.on_select(self.selected, items[self.selected])

    def on_select(self, index, item):
        destinations = {
            "Music":           "music_menu",
            "Games":           "games_menu",
            "Extras":          "extras_menu",
            "Settings":        "settings_menu",
        }
        dest = destinations.get(item)
        if dest:
            self.manager.switch(dest)

    def draw_panel(self, surface, playing=None, track=None):
        cx = t.PANEL_X + t.PANEL_W // 2
        cy = t.HEADER_H + (t.SCREEN_H - t.HEADER_H) // 2
        # Simple Game Boy pixel-art style icon placeholder
        col = t.TEXT_DIM
        rect = pygame.Rect(cx - 20, cy - 14, 40, 28)
        pygame.draw.rect(surface, col, rect, 2, border_radius=4)
        pygame.draw.rect(surface, col, (cx - 8, cy + 14, 16, 6), 2)
        pygame.draw.rect(surface, col, (cx - 12, cy + 18, 24, 4), 2)
        label = self.fonts["small"].render("DMGPod", True, t.TEXT_DIM)
        surface.blit(label, (cx - label.get_width() // 2, cy - 32))
