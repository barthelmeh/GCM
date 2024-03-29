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

    def get_cursor_position(self, landmarks):
        # Average position between pointer finger and thumb
        pointer_x, pointer_y = landmarks[8].x, landmarks[8].y
        thumb_x, thumb_y = landmarks[4].x, landmarks[4].y

        return thumb_x + (pointer_x - thumb_x), thumb_y + (pointer_y - thumb_y)

    def move_to(self, pos):
        x_cord = self.screen_width - pos[0] * self.screen_width
        y_cord = pos[1] * self.screen_height

        if ((x_cord - self.prev_pos[0])**2 + (y_cord - self.prev_pos[1])**2) > self.movement_threshold:
            self.mouse.position = (x_cord, y_cord)
            self.prev_pos = self.mouse.position
