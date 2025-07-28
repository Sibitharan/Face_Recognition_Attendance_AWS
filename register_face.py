import boto3
import os
import cv2
import uuid
from aws_helpers import upload_to_s3, index_face

def register_faces(folder='faces'):
    for filename in os.listdir(folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            student_name = os.path.splitext(filename)[0]
            image_path = os.path.join(folder, filename)

            s3_key = f"{student_name}_{uuid.uuid4()}.jpg"
            upload_to_s3(image_path, s3_key)
            index_face(s3_key, student_name)
            print(f"[✅] Registered face for: {student_name}")

if __name__ == "__main__":
    register_faces()
