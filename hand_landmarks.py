import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

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
