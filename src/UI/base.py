from abc import ABC, abstractmethod

class Screen(ABC):
    title: str = ""

    @abstractmethod
    def show(self) -> None:
        ...

class MenuLoop:
    def __init__(self, root_screen: Screen):
        self._current = root_screen
        self._running = True

    def set_screen(self, screen: Screen):
        self._current = screen

    def stop(self):
        self._running = False

    def run(self):
        while self._running:
            self._current.show()
