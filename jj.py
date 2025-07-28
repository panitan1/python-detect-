from ultralytics import YOLO

model = YOLO('gui\\best.pt')

results = model(r'Save_detection\2025\2025-07\20-07-2025\Night\00-28-52\_C2_Model1_0_0f7c79.jpg')

# แสดงภาพผลลัพธ์ของรูปแรก (ในที่นี้มีแค่ 1 รูป)
results[0].show()

# แสดงข้อมูลกล่องตรวจจับ
for result in results:
    print(result.boxes.data)
