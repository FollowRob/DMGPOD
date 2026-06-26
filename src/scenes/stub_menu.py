from src.scenes.menu_scene import MenuScene


class StubMenu(MenuScene):
    """Placeholder for menus not yet implemented."""

    def __init__(self, manager, fonts, title="Coming Soon"):
        super().__init__(manager, fonts)
        self.title = title

    def items(self):
        return ["(empty — no library loaded)"]

    def on_select(self, index, item):
        pass
