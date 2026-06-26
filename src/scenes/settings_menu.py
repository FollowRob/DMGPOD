from src.scenes.menu_scene import MenuScene


class SettingsMenu(MenuScene):
    title = "Settings"

    def items(self):
        return ["Brightness", "Volume Limit", "EQ", "Shuffle", "Repeat", "Backlight Timer"]

    def on_select(self, index, item):
        pass  # Phase 8+
