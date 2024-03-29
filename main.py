import cv2
from hand_landmarks import Landmarker
from cursor import Cursor

def main():
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error opening video stream or file")
        exit(-1)

    landmarker = Landmarker('hand_landmarker.task')
    cursor = Cursor()

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        landmark_result = landmarker.get_landmarks(image)
        if len(landmark_result.hand_landmarks) > 0:
            # Cursor position maybe not pointer but average between pointer and thumb
            cursor.moveToFinger(landmark_result.hand_landmarks[0][8])

        # annotated_image = draw_landmarks_on_image(frame, landmark_result)
        # cv2.imshow('frame', annotated_image)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    video_capture.release()
    cv2.destroyAllWindows()
    print("Finished")


if __name__ == '__main__':
    main()
