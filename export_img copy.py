import cv2

cap = cv2.VideoCapture("rtsp://admin:L2012BB0@192.168.1.134:554/cam/realmonitor?channel=1&subtype=0")

if cap.isOpened():
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("frame_rtsp2.jpg", frame)
        print("✅ Image saved successfully.")
    else:
        print("❌ ไม่สามารถอ่านเฟรมจากกล้อง")
else:
    print("❌ ไม่สามารถเชื่อมต่อกับ RTSP stream")
