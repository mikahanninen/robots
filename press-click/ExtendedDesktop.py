from RPA.Desktop import Desktop
from pynput_robocorp import keyboard
from RPA.Desktop.keywords import keyword
from RPA.Desktop.keywords.keyboard import to_key


class ExtendedDesktop(Desktop):
    def __init__(self, *args, **kwargs) -> None:
        Desktop.__init__(self, *args, **kwargs)
        self._keyboard = keyboard.Controller()

    @keyword
    def press_key(self, key: str):
        the_key = to_key(key, escaped=True)
        self._keyboard.press(the_key)

    @keyword
    def release_key(self, key: str):
        the_key = to_key(key, escaped=True)
        self._keyboard.release(the_key)
