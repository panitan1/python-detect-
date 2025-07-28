import cv2

# โหลดภาพ
image_path = 'Save_detection\\2025\\2025-07\\22-07-2025\\Night\\23-42-50\\_C2_Model1_0_b4ccdd.jpg'
image = cv2.imread(image_path)

# ตรวจสอบว่าภาพโหลดสำเร็จหรือไม่
if image is None:
    print("ไม่สามารถโหลดภาพได้ กรุณาตรวจสอบ path ไฟล์ค่ะ! 😓")
    exit()

# ใช้ Bilateral Filter เพื่อลด noise และรักษาขอบ
filtered = cv2.bilateralFilter(image, 9, 75, 75)

# เพิ่มความคมชัดด้วย Unsharp Masking
sharpened = cv2.addWeighted(image, 9, filtered, -0.5, 0)

# บันทึกภาพที่ sharpen แล้ว
output_path = 'output_sharpened.jpg'
cv2.imwrite(output_path, sharpened)
print(f"บันทึกภาพที่ชัดแล้วที่: {output_path} 🎉")

# แสดงภาพ
cv2.imshow('Original Image', image)
cv2.imshow('Sharpened Image', sharpened)

# รอการกดปุ่มและปิดหน้าต่าง
print("กด 'q' เพื่อออกจากหน้าต่างภาพนะคะ! 😊")
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()