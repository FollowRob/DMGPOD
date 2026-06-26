from src.scenes.menu_scene import MenuScene


class GamesMenu(MenuScene):
    title = "Games"

    def items(self):
        return ["Launch RetroArch", "Recent Games"]

    def on_select(self, index, item):
        if item == "Launch RetroArch":
            self.manager.switch("retroarch_launcher")
