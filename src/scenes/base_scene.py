class BaseScene:
    def __init__(self, manager, fonts):
        self.manager = manager
        self.fonts = fonts

    def on_enter(self):
        pass

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass
