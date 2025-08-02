import cv2
import boto3
import uuid
import datetime
from aws_helpers import upload_to_s3, search_face, log_attendance

import time
import dlib
from imutils import face_utils

# Load dlib's face detector and eye landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Download required

def is_blinking(eye):
    # Calculate eye aspect ratio (EAR) to detect blinking
    A = ((eye[1][1] - eye[5][1]) ** 2 + (eye[1][0] - eye[5][0]) ** 2) ** 0.5
    B = ((eye[2][1] - eye[4][1]) ** 2 + (eye[2][0] - eye[4][0]) ** 2) ** 0.5
    C = ((eye[0][1] - eye[3][1]) ** 2 + (eye[0][0] - eye[3][0]) ** 2) ** 0.5
    ear = (A + B) / (2.0 * C)
    return ear < 0.21  # Threshold for blink

def detect_blink(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        shape = predictor(gray, face)
        shape_np = face_utils.shape_to_np(shape)
        left_eye = shape_np[36:42]
        right_eye = shape_np[42:48]

        if is_blinking(left_eye) or is_blinking(right_eye):
            return True
    return False

def capture_and_mark():
    cam = cv2.VideoCapture(0)
    print("Blink your eyes to verify liveness...")

    blink_confirmed = False
    start_time = time.time()

    while True:
        ret, frame = cam.read()
        cv2.imshow("Liveness Check (Blink)", frame)

        if detect_blink(frame):
            print("✅ Blink detected! Capturing face...")
            blink_confirmed = True
            break

        if time.time() - start_time > 10:  # Timeout after 10 seconds
            print("❌ Liveness not detected. Try again.")
            cam.release()
            cv2.destroyAllWindows()
            return

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("⛔ Cancelled by user.")
            cam.release()
            cv2.destroyAllWindows()
            return

    if blink_confirmed:
        img_name = f"temp_capture_{uuid.uuid4()}.jpg"
        cv2.imwrite(img_name, frame)
        cam.release()
        cv2.destroyAllWindows()

        s3_key = f"attendance_capture/{img_name}"
        upload_to_s3(img_name, s3_key)
        student_name = search_face(s3_key)

        if student_name:
            timestamp = datetime.datetime.now().isoformat()
            log_attendance(student_name, timestamp)
            print(f"[🟢] Attendance marked for: {student_name}")
        else:
            print("[🔴] Face not recognized!")

if __name__ == "__main__":
    capture_and_mark()
