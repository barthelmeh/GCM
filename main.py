import cv2
from hand import Landmarker, GestureRecognition
from cursor import Cursor

def main():
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error opening video stream or file")
        exit(-1)

    landmarker = Landmarker('hand_landmarker.task')
    cursor = Cursor()
    gesture_recogniser = GestureRecognition()

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        landmark_result = landmarker.get_landmarks(image)
        if len(landmark_result.hand_landmarks) > 0:
            landmarks = landmark_result.hand_landmarks[0]
            # Cursor position maybe not pointer but average between pointer and thumb
            cursor_position = cursor.get_cursor_position(landmarks)
            cursor.move_to(cursor_position)

            # Get the gesture
            gesture = gesture_recogniser.get_gesture(landmarks)
            if gesture == 0:  # No gesture
                continue

            if gesture == 1:  # Pinching
                print("Pinching")

        # annotated_image = draw_landmarks_on_image(frame, landmark_result)
        # cv2.imshow('frame', annotated_image)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    video_capture.release()
    cv2.destroyAllWindows()
    print("Finished")


if __name__ == '__main__':
    main()
