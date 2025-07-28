import boto3
import uuid

bucket_name = 'sibitharan-attendance-bucket'
collection_id = 'face_attendance_collection'
table_name = 'FaceAttendanceLogs'
region = 'ap-south-1'

rekognition = boto3.client('rekognition', region_name=region)
s3 = boto3.client('s3', region_name=region)
dynamodb = boto3.resource('dynamodb', region_name=region)

def upload_to_s3(file_path, s3_key):
    with open(file_path, 'rb') as f:
        s3.upload_fileobj(f, bucket_name, s3_key)

def index_face(s3_key, external_id):
    response = rekognition.index_faces(
        CollectionId=collection_id,
        Image={'S3Object': {'Bucket': bucket_name, 'Name': s3_key}},
        ExternalImageId=external_id,
        DetectionAttributes=['DEFAULT']
    )
    return response

def search_face(s3_key):
    response = rekognition.search_faces_by_image(
        CollectionId=collection_id,
        Image={'S3Object': {'Bucket': bucket_name, 'Name': s3_key}},
        MaxFaces=1,
        FaceMatchThreshold=90
    )
    face_matches = response.get('FaceMatches', [])
    if face_matches:
        return face_matches[0]['Face']['ExternalImageId']
    return None

def log_attendance(student_name, timestamp):
    table = dynamodb.Table(table_name)
    table.put_item(Item={
        'StudentID': student_name,
        'Timestamp': timestamp
    })
