from PIL import Image, ImageGrab
import pynput
import os

class ImageClass:
    def __init__(self, coords:tuple=None):
        self.coords = coords
        self.image = None

        self.first_pos:tuple = None
        self.second_pos:tuple = None

    def normalized_coords(self, first_pos:tuple, second_pos:tuple) -> None:
        x1, y1 = first_pos
        x2, y2 = second_pos
        left = min(x1, x2)
        top = min(y1, y2)
        right = max(x1, x2)
        bottom = max(y1, y2)
        self.coords = (left, top, right, bottom)

    def set_coords(self, first_pos:tuple, second_pos:tuple) -> None:
        self.normalized_coords(first_pos, second_pos)

    def take_screenshot(self) -> Image:
        self.image = ImageGrab.grab(
            bbox=self.coords
        )

    def save_image(self, file):
        if not os.path.exists(file):
            with open(file, "w"):
                pass
        self.image.save(file, "PNG")

    def on_click(self, x, y, button, pressed):
        if pynput.mouse.Button.left == button.left:
            if pressed:
                self.first_pos = (x, y)
            else:
                self.second_pos = (x, y)
                return False

    def find(self):
        with pynput.mouse.Listener(
            on_click=self.on_click
        ) as mo_listener:
            mo_listener.join()
        self.normalized_coords(self.first_pos, self.second_pos)
