import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from cursor import Cursor
from filters import OneEuroFilter


class Landmarker:
    def __init__(self, model_path: str, num_hands=1, min_detection_confidence=0.6):
        self.model_path = model_path
        base_options = python.BaseOptions(model_asset_path=self.model_path)
        options = vision.HandLandmarkerOptions(base_options=base_options,
                                               num_hands=num_hands,
                                               min_hand_detection_confidence=min_detection_confidence)
        self.detector = vision.HandLandmarker.create_from_options(options)

    def get_landmarks(self, frame):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        return self.detector.detect(mp_image)


class Hand:
    def __init__(self):
        self.landmarks = None
        self.filter = OneEuroFilter()

    def get_landmarks(self, result: vision.HandLandmarkerResult, hand='Right'):
        """
        Sets the landmarks for the given hand.
        Hand can be either 'Right' or 'Left'
        """
        for c, hand_store in enumerate(result.handedness):
            hand_category = hand_store[0]
            if hand_category.display_name == hand:
                self.landmarks = result.hand_landmarks[c]

    def get_centroid(self):
        # Average position of all landmarks
        avg_x, avg_y = 0, 0
        n = len(self.landmarks)
        for landmark in self.landmarks:
            avg_x += landmark.x
            avg_y += landmark.y

        return self.filter(np.array([avg_x / n, avg_y / n]))

    def do_gesture(self, mouse: Cursor):
        """
            Checks for given gestures and performs the actions on the mouse object
        """
        if self.landmarks is None:
            mouse.release_mouse_buttons()
            return

        if self.is_scrolling():
            mouse.scroll(self.get_centroid())

        elif self.is_left_clicking():
            mouse.press_left_click()

        elif self.is_right_clicking():
            mouse.press_right_click()

        elif self.is_double_clicking():
            mouse.double_click()

        else:
            mouse.release_mouse_buttons()

    def is_left_clicking(self):
        pinching_threshold = 0.008
        pointer_x, pointer_y = self.landmarks[8].x, self.landmarks[8].y
        thumb_x, thumb_y = self.landmarks[4].x, self.landmarks[4].y

        return ((pointer_x - thumb_x) ** 2 + (pointer_y - thumb_y) ** 2) < pinching_threshold

    def is_right_clicking(self):
        pinching_threshold = 0.008
        middle_x, middle_y = self.landmarks[12].x, self.landmarks[12].y
        thumb_x, thumb_y = self.landmarks[4].x, self.landmarks[4].y

        return ((middle_x - thumb_x) ** 2 + (middle_y - thumb_y) ** 2) < pinching_threshold

    def is_double_clicking(self):
        pinching_threshold = 0.008
        pinky_x, pinky_y = self.landmarks[20].x, self.landmarks[20].y
        thumb_x, thumb_y = self.landmarks[4].x, self.landmarks[4].y

        return ((pinky_x - thumb_x) ** 2 + (pinky_y - thumb_y) ** 2) < pinching_threshold

    def is_scrolling(self):
        pinching_threshold = 0.008
        thumb_x, thumb_y = self.landmarks[4].x, self.landmarks[4].y

        # Get coordinates for the tips of all fingers
        finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
        distances = []

        for tip in finger_tips:
            finger_x, finger_y = self.landmarks[tip].x, self.landmarks[tip].y
            distance = (finger_x - thumb_x) ** 2 + (finger_y - thumb_y) ** 2
            distances.append(distance)

        return all(distance < pinching_threshold for distance in distances)
