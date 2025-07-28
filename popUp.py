# import numpy as np

# # จุดที่ต้องการตรวจสอบ
# # ตัวอย่างจุดใกล้เส้น
# cx, cy = 1306, 699


# # เส้นตรงผ่านสองจุด
# line1 = np.array([[460, 1076], [1226, 283]])

# # ดึงพิกัดสองจุดของเส้น
# x1, y1 = line1[0]
# x2, y2 = line1[1]

# # ความต่างของ x และ y
# A = x2 - x1
# B = y2 - y1

# # ความยาวเส้นตรง (ด้านเอียง)
# C = (A**2 + B**2)**0.5

#  คำนวณเศษในสูตรหาระยะห่างตั้งฉาก
# numerator = abs(A * (cy - y1) - B * (cx - x1))

# # ระยะห่างตั้งฉากจากจุดถึงเส้น
# distance = numerator / C

# print("ระยะห่างตั้งฉากจากจุดถึงเส้น:", distance)
# print("ระยะด้านเอียง =", C)

# # เช็กระยะห่างถ้าน้อยกว่าหรือเท่ากับ 15 พิมพ์ว่า "ชนแล้ว"
# threshold = 15
# if distance <= threshold:
#     print("ชนแล้ว!")
# else:
#     print("ยังไม่ชน")
class ImageProcessor:
    def __init__(self):
        # สมมติว่านี่คือตัวแปรที่เก็บข้อมูลรูปภาพที่ครอปแล้ว
        self.Crop_Img_c2_model_1 = "image_c2_model1.jpg"  # รูปจากโมเดล 1
        self.Crop_Img_c2_model_2 = None  # รูปจากโมเดล 2 (อาจจะไม่มี)
        
        self.Crop_Img_c2_model_1 = "image_c2_model1xxxxxxxxx.jpg"  # รูปจากโมเดล 1
        self.Crop_Img_c2_model_2 = None  # รูปจากโมเดล 2 (อาจจะไม่มี)

        # สร้าง dictionary เพื่อเก็บข้อมูลรูปภาพ
        self.Crop_Img_c2_c2_m1_m2 = {
            "c2_m1": self.Crop_Img_c2_model_1,  # เก็บรูปจากโมเดล 1
            "c2_m2": self.Crop_Img_c2_model_2 if self.Crop_Img_c2_model_2 is not None else None  # ตรวจสอบว่า model_2 มีรูปหรือไม่
        }

    def display_images(self):
        # แสดงข้อมูลใน dictionary
        print("ข้อมูลรูปภาพใน dictionary:")
        for key, value in self.Crop_Img_c2_c2_m1_m2.items():
            print(f"{key}: {value}")

# ทดสอบโค้ด
processor = ImageProcessor()
processor.display_images()