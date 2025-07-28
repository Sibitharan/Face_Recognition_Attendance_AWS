import boto3
import csv

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('FaceAttendanceLogs')

def export_to_csv(filename='attendance_export.csv'):
    response = table.scan()
    items = response['Items']

    with open(filename, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['StudentID', 'Timestamp'])
        writer.writeheader()
        for item in items:
            writer.writerow(item)

    print(f"[📁] Attendance data exported to {filename}")

if __name__ == "__main__":
    export_to_csv()
