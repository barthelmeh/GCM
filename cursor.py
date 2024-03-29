from screeninfo import get_monitors
from pynput.mouse import Controller

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

    def moveToFinger(self, finger_pos):
        x_cord = self.screen_width - finger_pos.x * self.screen_width
        y_cord = finger_pos.y * self.screen_height

        if ((x_cord - self.prev_pos[0])**2 + (y_cord - self.prev_pos[1])**2) > self.movement_threshold:
            self.mouse.position = (x_cord, y_cord)
            self.prev_pos = self.mouse.position