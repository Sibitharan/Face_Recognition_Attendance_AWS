import boto3

rekognition = boto3.client('rekognition', region_name='ap-south-1')

collection_id = 'face_attendance_collection'

response = rekognition.create_collection(CollectionId=collection_id)
print(f"✅ Collection created: {response['CollectionArn']}")
