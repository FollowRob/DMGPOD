class SceneManager:
    def __init__(self):
        self._scenes = {}
        self._current = None
        self._history = []

    def register(self, name, scene):
        self._scenes[name] = scene

    def get(self, name):
        return self._scenes.get(name)

    def switch(self, name, push_history=True):
        if name not in self._scenes:
            return
        if self._current and push_history:
            self._history.append(self._current)
        self._current = self._scenes[name]
        self._current.on_enter()

    def back(self):
        if self._history:
            self._current = self._history.pop()
            self._current.on_enter()

    def handle_event(self, event):
        if self._current:
            self._current.handle_event(event)

    def update(self):
        if self._current:
            self._current.update()

    def draw(self, surface):
        if self._current:
            self._current.draw(surface)
