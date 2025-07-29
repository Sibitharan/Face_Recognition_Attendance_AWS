# 🎓 Face Recognition Attendance System using AWS

This project is a cloud-based attendance system that uses **facial recognition** to mark attendance securely and automatically. Designed as a final year cloud computing project using **AWS Rekognition**, **S3**, **DynamoDB**, and **Python (OpenCV)**.

---

## ✅ Features

- 📸 Capture face images using webcam (OpenCV)
- 🧠 Recognize faces using **AWS Rekognition**
- ☁️ Store images in **S3 bucket**
- 🗂️ Log attendance in **DynamoDB** with timestamp
- 🔒 Uses **IAM Roles** for secure AWS access

---

## 🛠️ Technologies Used

- **Python 3**
- **OpenCV**
- **AWS Rekognition**
- **AWS S3**
- **AWS DynamoDB**
- **IAM Roles**
- **Boto3 (AWS SDK)**

---

## 🧾 Project Structure

```
Face_Recognition_Attendance_AWS/
├── faces/                 # Folder to store sample face images
├── register_face.py       # Upload and index faces into Rekognition
├── mark_attendance.py     # Capture photo, recognize, mark attendance
├── aws_helpers.py         # AWS functions (upload, index, search, log)
├── requirements.txt       # Required Python libraries
└── README.md              # Project documentation (this file)
```

---

## ▶️ How to Run

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Register Faces (store in Rekognition)
Put face images in `faces/` folder, named like `john.jpg`, then run:
```bash
python register_face.py
```

### 3. Mark Attendance (via webcam)
```bash
python mark_attendance.py
```

---

## 🏗️ AWS Setup Required

- ✅ S3 Bucket: `sibitharan-attendance-bucket`
- ✅ Rekognition Collection: `face_attendance_collection`
- ✅ DynamoDB Table: `FaceAttendanceLogs` with `StudentID`, `Timestamp`
- ✅ IAM Role with full access to Rekognition, S3, DynamoDB

---



## 👨‍💻 Author

**Sibitharan S**  
BSc Computer Science – KG College of Arts and Science  
GitHub: [@Sibitharan](https://github.com/Sibitharan)

---



