from src.scenes.menu_scene import MenuScene


class ExtrasMenu(MenuScene):
    title = "Extras"

    def items(self):
        return ["Bluetooth", "Sleep Timer", "About"]

    def on_select(self, index, item):
        pass  # Phase 8+
