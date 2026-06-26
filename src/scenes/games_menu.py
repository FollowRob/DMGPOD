from src.scenes.menu_scene import MenuScene


class GamesMenu(MenuScene):
    title = "Games"

    def items(self):
        return ["Browse ROMs"]

    def on_select(self, index, item):
        if item == "Browse ROMs":
            self.manager.switch("rom_browser")
