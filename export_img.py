# # from datetime import datetime

# # CM1_Model1_list = [
# #     {'timestamp': '2025-07-25 09:00:00'},
# #     {'timestamp': '2025-07-25 09:00:01'},
# #     {'timestamp': '2025-07-25 09:00:05'},
# # ]

# # CM2_Model1_list = [
# #     {'timestamp': '2025-07-25 09:00:02'},
# #     {'timestamp': '2025-07-25 09:00:09'},
# #     {'timestamp': '2025-07-25 09:00:04'},
# # ]

# # # เก็บ index ที่ควรลบ
# # delete_indexes = []

# # for i, (item1, item2) in enumerate(zip(CM1_Model1_list, CM2_Model1_list)):
# #     time_obj1 = datetime.strptime(item1['timestamp'], '%Y-%m-%d %H:%M:%S')
# #     time_obj2 = datetime.strptime(item2['timestamp'], '%Y-%m-%d %H:%M:%S')
# #     time_diff = abs((time_obj1 - time_obj2).total_seconds())
# #     print(f"Diff {i} = {time_diff} seconds")

# #     if time_diff <= 3:
# #         delete_indexes.append(i)

# # # ลบจากหลังมาหน้า
# # for i in reversed(delete_indexes):
# #     print(i)
# #     del CM1_Model1_list[i]
# #     del CM2_Model1_list[i]

# # print("หลังลบ:")
# # print("CM1:", CM1_Model1_list)
# # print("CM2:", CM2_Model1_list)

# pp = [123]
# oo = [444]
# result = pp + oo
# print(result)

# class APP_SY_Frame:
#     def __init__(self):
#         super().__init__()  # เรียก super class ถ้ามีการสืบทอด
#         self.sdfsdf = "pppp"  # ประกาศ instance variable

#     def show_message(self):
#         print(self.sdfsdf)  # เรียกใช้งาน instance variable

# # สร้าง object และเรียกใช้เมธอด
# if __name__ == "__main__":
#     app = APP_SY_Frame()
#     app.show_message()  # Output: pppp

# from datetime import datetime, timedelta
# import pytz

# tz = pytz.timezone('Asia/Bangkok')
# now = datetime.now(tz)
# CM1_Model1_list = {}
# if  CM1_Model1_list:
#     latest_item = CM1_Model1_list[-1]  # เอาตัวล่าสุดใน list
#     timestamp_str = latest_item['timestamp']  # สมมุติว่า timestamp เป็น string

#     # แปลง timestamp string เป็น datetime object
#     timestamp_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=tz)

#     # เช็คว่าผ่านไปเกิน 5 วินาทีหรือยัง
#     if (now - timestamp_time).total_seconds() > 5:
#         print("CM1 ข้อมูลล่าสุดเก่ากว่า 5 วินาที")
# เพิ่มตัวแปรเพื่อเก็บข้อมูลที่รอการจับคู่
# my_list = []

# if not my_list:
#     print("ลิสต์ว่าง")
# else:
#     print("ลิสต์มีค่า")

import customtkinter

def get_window_aspect_ratio(window):
    """
    ดึงความกว้างและความสูงของหน้าต่าง และคำนวณอัตราส่วน
    """
    # อัปเดต idletasks เพื่อให้แน่ใจว่าได้ค่าขนาดหน้าต่างที่ถูกต้อง
    # โดยเฉพาะอย่างยิ่งเมื่อหน้าต่างถูกปรับขนาด
    window.update_idletasks()
    
    width = window.winfo_width()
    height = window.winfo_height()

    if height == 0:  # ป้องกันการหารด้วยศูนย์
        return 0
    
    aspect_ratio = width / height
    return aspect_ratio

if __name__ == "__main__":
    app = customtkinter.CTk()
    app.title("Window Aspect Ratio")
    
    # ตั้งค่าขนาดเริ่มต้นของหน้าต่าง
    app.geometry("800x600")

    def print_aspect_ratio():
        ratio = get_window_aspect_ratio(app)
        print(f"Current Window Width: {app.winfo_width()} pixels")
        print(f"Current Window Height: {app.winfo_height()} pixels")
        print(f"Window Aspect Ratio: {ratio:.2f}")

    # สร้างปุ่มสำหรับแสดงอัตราส่วน
    button = customtkinter.CTkButton(app, text="Get Aspect Ratio", command=print_aspect_ratio)
    button.pack(pady=20)

    app.mainloop()