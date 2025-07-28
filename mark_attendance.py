import cv2
import boto3
import uuid
import datetime
from aws_helpers import upload_to_s3, search_face, log_attendance

def capture_and_mark():
    cam = cv2.VideoCapture(0)
    print("Press 'q' to capture and mark attendance...")

    while True:
        ret, frame = cam.read()
        cv2.imshow("Press 'q' to capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

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
