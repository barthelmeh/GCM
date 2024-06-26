from screeninfo import get_monitors
from pynput.mouse import Controller, Button
import numpy as np

class Cursor:

    def __init__(self):
        """
        Handles cursor events
        CURRENTLY ONLY SUPPORTS ONE MONITOR
        """
        self.monitor = get_monitors()[0]
        self.screen_height = self.monitor.height
        self.screen_width = self.monitor.width

        self.mouse = Controller()
        self.prev_pos = self.mouse.position
        self.movement_threshold = 35
        self.scroll_multiplier = 100

        self.mapping_range = (0.2, 0.8)

        self.left_clicking = False
        self.prev_scroll_position = None

    def normalize_coordinate(self, value, min_val, max_val):
        # Convert the camera positions that go from min to max, to screen positions within 0 to 1
        np.clip(value, min_val, max_val)
        return np.interp(value, [min_val, max_val], [0, 1])

    def translate_to_screen_coordinate(self, pos):
        x, y = pos
        x = self.normalize_coordinate(x, *self.mapping_range)
        y = self.normalize_coordinate(y, *self.mapping_range)

        x_cord = self.screen_width - x * self.screen_width
        y_cord = y * self.screen_height

        return x_cord, y_cord

    def move_to(self, pos):
        x_cord, y_cord = self.translate_to_screen_coordinate(pos)

        if ((x_cord - self.prev_pos[0])**2 + (y_cord - self.prev_pos[1])**2) > self.movement_threshold:
            self.mouse.position = (x_cord, y_cord)
            self.prev_pos = self.mouse.position
        return x_cord, y_cord

    def release_mouse_buttons(self):
        if self.left_clicking:
            self.mouse.release(Button.left)
            self.left_clicking = False

        self.prev_scroll_position = None

    def press_left_click(self):
        self.mouse.press(Button.left)
        self.left_clicking = True

    def press_right_click(self):
        self.mouse.click(Button.right)

    def scroll(self, pos: tuple[int, int]):
        if self.prev_scroll_position is None:
            self.prev_scroll_position = pos
        else:
            difference = pos[1] - self.prev_scroll_position[1]
            self.mouse.scroll(0, -difference * self.scroll_multiplier)
            self.prev_scroll_position = pos

    def double_click(self):
        self.mouse.click(Button.left, 2)

