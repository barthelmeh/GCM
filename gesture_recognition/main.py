import cv2
from hands import Landmarker, Hand
from cursor import Cursor
import time

def main():
    """
    Cursor will follow right hand pointer finger
    """

    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error opening video stream or file")
        exit(-1)

    landmarker = Landmarker('hand_landmarker.task', num_hands=2)
    cursor = Cursor()
    left, right = Hand(), Hand()

    break_timer = None

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        landmark_result = landmarker.get_landmarks(image)
        left.get_landmarks(landmark_result, 'Left')
        right.get_landmarks(landmark_result, 'Right')

        if right.landmarks:
            pos = right.get_centroid()
            cursor.move_to(pos)

        if left.landmarks:
            left.do_gesture(cursor)

        # Check if program should stop
        if right.landmarks and left.landmarks:
            if right.is_scrolling() and left.is_scrolling():
                if break_timer is None:
                    break_timer = time.time()
                else:
                    if time.time() - break_timer > 3:  # More than 3 seconds
                        break
            else:
                break_timer = None

        # image = draw_landmarks_on_image(image, landmark_result)
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # cv2.imshow('Result', image)
        #
        # pressed_key = cv2.waitKey(1)
        # if pressed_key & 0xFF == ord('q'):
        #     break

    video_capture.release()
    cv2.destroyAllWindows()
    print("Finished")


if __name__ == '__main__':
    main()
