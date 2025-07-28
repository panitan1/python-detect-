import random
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from CTkMenuBar import *
from PIL import Image
import webbrowser
import numpy as np
import pytz
import cv2
import sys
import os
import threading
from ultralytics import YOLO 
from ultralytics.utils.plotting import Annotator
from datetime import datetime ,timedelta
import time
from ultralytics.utils import ThreadingLocked
from server_mysql.mysql_server import datasql 
import uuid
from win10toast_click import ToastNotifier
import gc


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

class APP_SY_Frame(ctk.CTkFrame):
    def __init__(self , master):
        super().__init__(master)
        self.master = master          
        self.show_loading_popup()
        # ctk.set_widget_scaling(0.8)
        
        self.save_lock = threading.Lock()
        self.save_lock2 = threading.Lock()
        self.lock = threading.Lock()
        self.Time_CM1_MO1 = None  # เพิ่มตัวแปรสำหรับเก็บเวลา
        self.Time_CM2_MO1 = None  # เพิ่มตัวแปรสำหรับเก็บเวลา
        self.Time_CM1_MO2 = None  # เพิ่มตัวแปรสำหรับเก็บเวลา
        self.Time_CM2_MO2 = None  # เพิ่มตัวแปรสำหรับเก็บเวลา
        self.CM1_Model1_list = []  # เก็บภาพรถจาก Cam01
        self.CM2_Model1_list = []  # เก็บภาพรถจาก Cam02
        self.CM1_Model2_list = []
        self.CM2_Model2_list = []
        self.CM1_M1_M2_Path = []
        self.CM2_M1_M2_Path = []
        self.period = None
        self.Line1 =  np.array([[816, 1079], [1515, 224]])
        self.Line2 = np.array([[1639, 986], [546, 333]])
        self.track_color = {}
        self.Check_Line = False
        self.Have_cam1_no_cam2 = False
        self.Have_cam2_no_cam1 = False
        self.MuNuAPP_main()
        self.Main_CV2()
        self.My_show_ui_My_cap1()
        self.My_show_ui_My_cap2()
        self.start_cam()
        
        
        
        self.Right_way_c1 = {}
        self.Right_way_c2 = {}
        self.Left_way_c1 = {}
        self.Left_way_c2 = {}
        
        
        
        self.db = datasql() 

    def MuNuAPP_main(self):
        self.munubar = CTkMenuBar(self)
        self.buttun01 = self.munubar.add_cascade("Munu")
        self.dropdown = CustomDropdownMenu(widget=self.buttun01)
        self.dropdown.add_option(option="Camela 1")
        self.dropdown.add_option(option="Camela 2")
        self.dropdown.add_separator() 
        self.dropdown.add_option(option="Folder " ,command= self.Folder)
        self.MuNuAPP_Profile_and_Dash()
    
    def Folder(self):
        path = "Save_detection"
        os.startfile(path)
    
    def MuNuAPP_Profile_and_Dash(self):
        self.buttun02 = self.munubar.add_cascade("Profile")
        self.dropdown2 = CustomDropdownMenu(widget=self.buttun02)
        self.dropdown2.add_option(option="Profile", command= lambda: webbrowser.open("http://localhost:5173/"))
        self.dropdown2.add_option(option="Dashboard" , command= lambda: webbrowser.open("http://localhost:5173/dashdata"))
        self.dropdown2.add_separator() 
        self.dropdown2.add_option(option="Logout" ,command=self.from_logout_)
        self.dropdown2.add_option(option="Exit" , command= self.destroyy)

  

    def Main_CV2(self):
        self.bkAPPmain = ctk.CTkFrame(self, fg_color="#686363"  )
        self.bkAPPmain.pack(fill="both", expand=True)
        
    def My_cap1(self):
        self.Ar_cm1_box = ctk.CTkFrame(self.bkAPPmain , fg_color="#000000")
        self.Ar_cm1_box.place(relx=0.003, rely=0.0018, relwidth=0.6, relheight=0.490)
        
        self.My_run_cam1_gui = ctk.CTkLabel(self.Ar_cm1_box ,text=f"")
        self.My_run_cam1_gui.pack(expand=True, fill="both")



    def My_cap2(self):
        self.Ar_cm2_box = ctk.CTkFrame(self.bkAPPmain , fg_color="#000000")
        self.Ar_cm2_box.place(relx=0.003, rely=0.5, relwidth=0.6, relheight=0.490)
        
        self.My_run_cam2_gui = ctk.CTkLabel(self.Ar_cm2_box ,text=f"")
        self.My_run_cam2_gui.pack(expand=True, fill="both")

    def My_show_ui_My_cap1(self):
        self.Main_Text_My_cap1 = ctk.CTkFrame(self.bkAPPmain , fg_color="#2C2C2C" )
        self.Main_Text_My_cap1.place(relx=0.604, rely=0.001, relwidth=0.393, relheight=0.07)
        
        self.TextMain_cap1 = ctk.CTkLabel(self.Main_Text_My_cap1 , text=f"กล้องหมายเลข 1")
        self.TextMain_cap1.pack(expand=True, fill="both")
 
        
    def Show_img_cap1(self):
        self.box1 = ctk.CTkFrame(self.bkAPPmain , fg_color="#000000")
        self.box1.place(relx=0.604, rely=0.08, relwidth=0.2, relheight=0.41)
        
        self.My_show_img1 = ctk.CTkLabel(self.box1, text="")
        self.My_show_img1.pack(expand=True, fill="both")
        
        
        self.box2 = ctk.CTkFrame(self.bkAPPmain , fg_color="#000000")
        self.box2.place(relx=0.808, rely=0.08, relwidth=0.19, relheight=0.41)
        
        self.My_show_img2 = ctk.CTkLabel(self.box2, text="")
        self.My_show_img2.pack(expand=True, fill="both")
    
    def My_show_ui_My_cap2(self):
        self.Main_Text_My_cap2 = ctk.CTkFrame(self.bkAPPmain , fg_color="#2C2C2C" )
        self.Main_Text_My_cap2.place(relx=0.604, rely=0.5, relwidth=0.393, relheight=0.07)
        
        self.TextMain_cap2 = ctk.CTkLabel(self.Main_Text_My_cap2, text=f"กล้องหมายเลข 2")
        self.TextMain_cap2.pack(expand=True, fill="both")
        
        
        
        
        self.Show_img_cap1()
        self.Show_img_cap2()
    
    
    def Show_img_cap2(self):
        self.box1_cap2 = ctk.CTkFrame(self.bkAPPmain , fg_color="#000000")
        self.box1_cap2.place(relx=0.604, rely=0.58, relwidth=0.2, relheight=0.41)
        
        self.My_show_img1_cap2 = ctk.CTkLabel(self.box1_cap2, text="")
        self.My_show_img1_cap2.pack(expand=True, fill="both")
        
        self.box2_cap2 = ctk.CTkFrame(self.bkAPPmain , fg_color="#000000")
        self.box2_cap2.place(relx=0.808, rely=0.58, relwidth=0.19, relheight=0.41)
        
        self.My_show_img2_cap2 = ctk.CTkLabel(self.box2_cap2, text="")
        self.My_show_img2_cap2.pack(expand=True, fill="both")
        
        
    def My_time_tz(self):
        tz = pytz.timezone('Asia/Bangkok')
        now = datetime.now(tz)
        # Time_Save_img = datetime.now(tz).strftime("%H-%M-%S")
        today = now.strftime("%d-%m-%Y")
        year = now.year
        month_str = now.strftime("%Y-%m")
        hour = now.hour

        if 6 <= hour <= 11:
            period = "Morning"
            self.period = "Morning"
        elif 12 <= hour <= 15:
            period = "Afternoon"
            self.period = "Afternoon"
        elif 16 <= hour <= 19:
            period = "Evening"
            self.period = "Evening"
        else:
            period = "Night"
            self.period = "Night"

        save_dir = f"Save_detection/{year}/{month_str}/{today}/{period}"
        os.makedirs(save_dir, exist_ok=True)
        return save_dir

    def show_loading_popup(self):
        CTkMessagebox(title="Info", message="กำลังโหลดข้อมูลกล้อง กรุณารอสักครู่",
                  icon="check")
        
        
    @ThreadingLocked() 
    def Process_Cam01(self):
        self.My_cap1()
        self.model = YOLO("yolov8x.pt").cuda()
        self.model_page = YOLO("gui\\best.pt").cuda()
        self.cam01 = cv2.VideoCapture(
            "rtsp://admin:L2012BB0@192.168.1.133:554/cam/realmonitor?channel=1&subtype=0",
            cv2.CAP_FFMPEG
        )
        self.cam01.set(cv2.CAP_PROP_HW_ACCELERATION, cv2.VIDEO_ACCELERATION_NONE)
        self.cam01.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        self.start_event.wait()
        self.running = True
        
        self.im_SAVE_Id_model1_cm1 = set()
        self.im_save_CHECK_Id_model1_cm1 = set()
        
        self.im_SAVE_Id_model2_cm1 = set()
        self.im_save_CHECK_Id_model2_cm1 = set()
        
        self.id_Time_check_c1_m1 = {}
        self.id_Time_check_c1_m2 = {}
        self.track_color = {}
        self.counter1 = {}
        
        self.crop_img_m1_m1_del = []
        self.crop_img_m1_m2_del = []
        
        self.direction_against001 = False
        
        
        self.Position_left_c1 = None
        self.Position_Right_c1 = None
        
     
        
        os.makedirs("vidioodetect1", exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        frame_width = int(self.cam01.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cam01.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(self.cam01.get(cv2.CAP_PROP_FPS)) or 30
    
        self.out1 = cv2.VideoWriter(f"vidioodetect1/output_detected_1.avi", fourcc, fps, (frame_width, frame_height))

        while self.running and self.save_lock:
            tz = pytz.timezone('Asia/Bangkok')
            Time_Save_img = datetime.now(tz).strftime("%H-%M-%S")

            
            ret, frame = self.cam01.read()
            if not ret:
                self.ERRORCAM_pp001 = "ไม่สามารถรับเชื่อมต่อกล้อง01ได้ {ret}"
                CTkMessagebox(title="Error", message=f"ไม่สามารถรับเชื่อมต่อกล้อง01ได้ \n {ret}", icon="cancel")
            
            frame_for_save = frame.copy()
            self.out1.write(frame_for_save)  # ✅ เขียน BGR ลงไฟล์

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            original_frame = frame.copy()
            original_frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2RGB)
            cv2.line(frame, self.Line1[0], self.Line1[1], (255, 0, 255), 3)
            annotator = Annotator(frame)
            annotated_frame = annotator.result()
            
            
            runYOLOm1 = self.model.track(frame, classes=[0], conf=0.5, persist=True)
            annotated_frame1 = runYOLOm1[0]
        
            if annotated_frame1.boxes is not None:
                
                current_time_ids = time.time()
                current_frame_ids = set()  # ชุดสำหรับเก็บ ID ในเฟรมปัจจุบัน
                for box in annotated_frame1.boxes:
                    class_if_model1 = int(box.cls.item())
                    Conf_if_model1 = box.conf.item()
                    xyxy_if_model1 = box.xyxy[0]
                    cx, cy, w, h = box.xywh[0].cpu().numpy().astype(int)
                    cv2.circle(frame, (cx, cy), 10, (5, 123, 255), -1)
                    
                    
                    if box.id is not None:
                        track_id = int(box.id.item())
                        current_frame_ids.add(track_id)  # เพิ่ม ID เข้าไปในชุดของเฟรมปัจจุบัน
                        self.id_Time_check_c1_m1[track_id] = current_time_ids
                        annotator.box_label(xyxy_if_model1, label=f"model1: {class_if_model1} -- {Conf_if_model1:.2f} -- {int(track_id)}")
                        
                        if track_id not in self.track_color:
                            self.track_color[track_id] = []
                        self.track_color[track_id].append((cx, cy))
                  
                        
                        if len(self.track_color[track_id]) > 15:
                                self.track_color[track_id].pop(0)
                                    
                        for j in range(1, len(self.track_color[track_id])):
                            if self.track_color[track_id][j-1] is None or self.track_color[track_id][j] is None:
                                continue
                            cv2.line(frame, self.track_color[track_id][j-1], self.track_color[track_id][j], (255, 0, 0), 2)

                    
                        
                        self.im_SAVE_Id_model1_cm1.add(track_id)
                        
                        if  (self.im_SAVE_Id_model1_cm1 != self.im_save_CHECK_Id_model1_cm1 and  self.is_Check_LINE1(cx, cy, self.Line1[0], self.Line1[1])):
                            if track_id in self.counter1:
                                prev_cx, prev_cy = self.counter1[track_id]
                                direction = "unknown"
                                if cx > prev_cx:
                                    self.Check_Line = True
                                    direction = "left to right"
                                    self.direction_against001 = False
        
                                    self.Left_way_c1[track_id] = {'Position' : "Left" , 'Time_Position' : Time_Save_img , 'CAM': 'CAM001'}
                                    self.Position_left_c1 = "C1_Left"
                                    print(self.Left_way_c1[track_id])
                                    
                                elif cx < prev_cx:
                                    direction = "right to left"
                                    self.Notification_windown_Counter()
                                    self.direction_against001 = True
                                    self.Right_way_c1[track_id] = {'Position' : "Right" , 'Time_Position' : Time_Save_img , 'CAM': 'CAM002'}
                                    self.Position_Right_c1 = "C1_Right"
                                    print(f"[C@1] ID {track_id}✅✅ crossed the line from {direction}")
                                

                            self.Have_cam1_no_cam2 = True
                            
                            self.im_save_CHECK_Id_model1_cm1.update(self.im_SAVE_Id_model1_cm1)
                            self.Tz = pytz.timezone('Asia/Bangkok')
                            self.Time_cm1_Model1 = datetime.now(self.Tz)
                            x1, y1, x2, y2 = map(int, xyxy_if_model1)

                            Crop_Img_c1_model_1 = original_frame[y1:y2, x1:x2]
                            self.crop_img_m1_m1_del.append((current_time_ids , Crop_Img_c1_model_1))
                            print("💚")
                            self.Main_Save_path(Crop_Img_c1_model_1, "CM1_Model1",self.Time_cm1_Model1 , self.Position_left_c1)
                            Crop_Img_c1_model_1 = cv2.cvtColor(Crop_Img_c1_model_1, cv2.COLOR_BGR2RGB)
                            img = Image.fromarray(Crop_Img_c1_model_1)
                            label_width = self.My_show_img1.winfo_width()
                            label_height = self.My_show_img1.winfo_height()
                            resizeimg = img.resize((label_width, label_height))
                            imgSHOWCtkm1_c1 = ctk.CTkImage(light_image=resizeimg, size=(label_width, label_height))
                            self.My_show_img1.configure(image=imgSHOWCtkm1_c1)
                            self.My_show_img1.image = imgSHOWCtkm1_c1
                            
                            # print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{Crop_Img_c1_model_1}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                            if Crop_Img_c1_model_1.size >= 1:
                                print(f"YOLO Model2 output💗💗💗💗")
                                runYOLOm2 = self.model_page(Crop_Img_c1_model_1, classes=[0])
                                annotated_frame2 = runYOLOm2[0]
                                
                                if annotated_frame2.boxes is not None:
                                    for box in annotated_frame2.boxes:
                                        class_if_model2 = int(box.cls.item())
                                        conf_if_model2 = box.conf.item()
                                        xyxy_if_model2 = box.xyxy[0]
                                        print(f"YOLO Model2 output💗💗💗💗 CM@2: {runYOLOm2[0].boxes}")
                                        annotator.box_label(xyxy_if_model2 , label=f"model2 : {class_if_model2} -- {conf_if_model2:.2f}")
                                        self.Tz = pytz.timezone('Asia/Bangkok')
                                        self.Time_cm1_Model2 = datetime.now(self.Tz)
                                        x1 ,y1 , x2 ,y2 = map(int , xyxy_if_model2)
                                        Crop_Img_c1_model_2 = Crop_Img_c1_model_1[y1:y2 , x1:x2]
                                        self.crop_img_m1_m2_del.append((current_time_ids , Crop_Img_c1_model_2))
                                        
                                        
                                        self.Main_Save_path(Crop_Img_c1_model_2 , "CM1_Model2" , self.Time_cm1_Model2 , )
                                        
                                        
                                        Crop_Img_c1_model_2 = cv2.cvtColor(Crop_Img_c1_model_2, cv2.COLOR_BGR2RGB)
                                        img = Image.fromarray(Crop_Img_c1_model_2)
                                        label_width = self.My_show_img2.winfo_width()
                                        label_height = self.My_show_img2.winfo_height()
                                        resizeimg = img.resize((label_width ,label_height))
                                        imgSHOWCtkm2_c1 = ctk.CTkImage(light_image= resizeimg , size= (label_width ,label_height ))
                                        self.My_show_img2.configure(image = imgSHOWCtkm2_c1)
                                        self.My_show_img2.image = imgSHOWCtkm2_c1
                                        self.crop_img_m1_m1_del = [(t , img) for t , img in self.crop_img_m1_m1_del if time.time() - t <=5]
                                        self.crop_img_m1_m2_del = [(t , img ) for t , img in self.crop_img_m1_m2_del if time.time() - t <=5]  
                                        
                                else:
                                    pass
                            else:
                                pass
                            
                            
                        self.counter1[track_id] = (cx , cy)


                missing_ids = self.im_SAVE_Id_model1_cm1 - current_frame_ids
                for lost_id in missing_ids:
                    if lost_id in self.id_Time_check_c1_m1:
                        time_since_last_seen = current_time_ids - self.id_Time_check_c1_m1[lost_id]
                        if time_since_last_seen > 10:
                            self.im_save_CHECK_Id_model1_cm1.discard(lost_id) 
                            self.im_SAVE_Id_model1_cm1.discard(lost_id)     
                            del self.id_Time_check_c1_m1[lost_id]             
                            # print(f"ตรวจสอบ ID {lost_id} | ล่าสุด: {self.id_Time_check_c1_m1[lost_id]} | ตอนนี้: {current_time_ids} | หายไปแล้ว {time_since_last_seen:.2f} วินาที")


                
                try: 
                    img1 = Image.fromarray(annotated_frame)
                    label_width = self.Ar_cm1_box.winfo_width()
                    label_height = self.Ar_cm1_box.winfo_height()
                    resiz_img = img1.resize((label_width, label_height))
                    imgTK = ctk.CTkImage(light_image=resiz_img, size=(label_width, label_height))
                
                    # อัปเดต GUI
                    self.My_run_cam1_gui.configure(image=imgTK)
                    self.My_run_cam1_gui.image = imgTK
                    
                    cv2.waitKey(1)
                except:
                    pass
        

    @ThreadingLocked()
    def Process_Cam02(self): 
        self.My_cap2()
        self.model22 = YOLO("yolov8x.pt").cuda()
        self.model_page22 = YOLO("gui\\best copy.pt").cuda()
        self.cam02 = cv2.VideoCapture(
            "rtsp://admin:L22C0475@192.168.1.134:554/cam/realmonitor?channel=1&subtype=0",
            cv2.CAP_FFMPEG
        )
        self.cam02.set(cv2.CAP_PROP_HW_ACCELERATION, cv2.VIDEO_ACCELERATION_NONE)
        self.cam02.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        self.start_event.wait()
        self.running = True
        
        self.im_SAVE_Id_model1_cm2 = set()
        self.im_save_CHECK_Id_model1_cm2 = set()
        
        self.im_SAVE_Id_model2_cm2 = set()
        self.im_save_CHECK_Id_model2_cm2 = set()
        
        self.id_Time_check_c2_m1 = {}
        self.id_Time_check_c2_m2 = {}
        self.track_color2 = {}
        
        self.counter2 = {}
        self.direction_against002  = False
        
        
        self.crop_img_m2_m1_del = []
        self.crop_img_m2_m2_del = []
        
        self.Position_left_c2 = None
        self.Position_Right_c2 = None
  
        
        os.makedirs("vidioodetect2", exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        frame_width = int(self.cam02.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cam02.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(self.cam02.get(cv2.CAP_PROP_FPS)) or 30
  
        self.out2 = cv2.VideoWriter(f"vidioodetect2/output_detected_2.avi", fourcc, fps, (frame_width, frame_height))
        
        
        while self.running and self.save_lock2:
            tz = pytz.timezone('Asia/Bangkok')
            Time_Save_img = datetime.now(tz).strftime("%H-%M-%S")
            ret, frame2 = self.cam02.read()
            if not ret:
                self.ERRORCAM_pp002 = "ไม่สามารถรับเชื่อมต่อกล้อง02ได้ {ret}"
                CTkMessagebox(title="Error", message=f"ไม่สามารถรับเชื่อมต่อกล้อง02ได้ \n {ret}", icon="cancel")
            
  
            frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            self.out2.write(frame2) 
            original_frame = frame2.copy()
            original_frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2RGB)
            cv2.line(frame2, self.Line2[0], self.Line2[1], (255, 0, 255), 3)
            annotator = Annotator(frame2)
            annotated_frame = annotator.result()
            
            runYOLOm1 = self.model22.track(frame2, classes=[0], conf=0.5, persist=True)
            annotated_frame1 = runYOLOm1[0]
            
            if annotated_frame1.boxes is not None:
                current_time_ids = time.time()
                current_frame_ids_C2_m1 = set()
                for box in annotated_frame1.boxes:
                    class_if_model1 = int(box.cls.item())
                    Conf_if_model1 = box.conf.item()
                    xyxy_if_model1 = box.xyxy[0]
                    cx, cy, w, h = box.xywh[0].cpu().numpy().astype(int)
                    cv2.circle(frame2, (cx, cy), 10, (5, 123, 255), -1)
                    
                    if box.id is not None:
                        track_id = int(box.id.item())
                        current_frame_ids_C2_m1.add(track_id)
                        self.id_Time_check_c2_m1[track_id] = current_time_ids
                        annotator.box_label(xyxy_if_model1, label=f"model1: {class_if_model1} -- {Conf_if_model1:.2f} -- {int(track_id)}")
                        self.im_SAVE_Id_model1_cm2.add(track_id)
                        
                        
                        if track_id not in self.track_color2:
                            self.track_color2[track_id] = []
                        self.track_color2[track_id].append((cx, cy))

                        if len(self.track_color2[track_id]) > 15:
                            self.track_color2[track_id].pop(0)
                            
                        for j in range(1, len(self.track_color2[track_id])):
                            if self.track_color2[track_id][j - 1] is None or self.track_color2[track_id][j] is None:
                                continue
                            cv2.line(frame2, self.track_color2[track_id][j - 1], self.track_color2[track_id][j], (255, 0, 0), 2)
                        
                        
                        
                        if (self.im_SAVE_Id_model1_cm2 != self.im_save_CHECK_Id_model1_cm2 and self.is_Check_LINE2(cx, cy, self.Line2[0], self.Line2[1])):
                            if track_id in self.counter2:
                                prev_cx, prev_cy = self.counter2[track_id]
                                direction = "unknown"
                                if cx > prev_cx:
                                    direction = "left to right"
                                    self.direction_against002 = False
                                    self.Left_way_c2[track_id] = {'Position' : "Left" , 'Time_Position' : Time_Save_img , 'CAM': 'CAM001'}
                                    self.Position_left_c2 = "C2_Left"
                                    print(self.Left_way_c2[track_id])
                                    
                                elif cx < prev_cx:
                                    direction = "right to left"
                                    
                                    self.Notification_windown_Counter()
                                    self.direction_against002 = True
                                    self.Right_way_c2[track_id] = {'Position' : "Right" , 'Time_Position' : Time_Save_img , 'CAM': 'CAM001'}
                                    self.Position_Right_c2 = "C2_Right"
                                    print(self.Right_way_c2[track_id])
                                    print(f"[C@2] ID {track_id}✅✅ crossed the line from {direction}")

                                
                            
                            self.Have_cam2_no_cam1 = True
                            self.im_save_CHECK_Id_model1_cm2.update(self.im_SAVE_Id_model1_cm2)
                            
                            
                            self.Tz = pytz.timezone('Asia/Bangkok')
                            self.Time_cm2_Model1 = datetime.now(self.Tz)
                            x1, y1, x2, y2 = map(int, xyxy_if_model1)
                            
                            Crop_Img_c2_model_1 = original_frame[y1:y2, x1:x2]
                            self.crop_img_m2_m1_del.append((current_time_ids , Crop_Img_c2_model_1 ))
                            
                            print("🩷")
                            self.Main_Save_path(Crop_Img_c2_model_1, "CM2_Model1", self.Time_cm2_Model1)
                            Crop_Img_c2_model_1 = cv2.cvtColor(Crop_Img_c2_model_1, cv2.COLOR_BGR2RGB)
                            img = Image.fromarray(Crop_Img_c2_model_1)
                            label_width = self.My_show_img1_cap2.winfo_width()
                            label_height = self.My_show_img1_cap2.winfo_height()
                            resizeimg = img.resize((label_width, label_height))
                            imgSHOWCtkm1_c2 = ctk.CTkImage(light_image=resizeimg, size=(label_width, label_height))
                            self.My_show_img1_cap2.configure(image=imgSHOWCtkm1_c2)
                            self.My_show_img1_cap2.image = imgSHOWCtkm1_c2
                            
                            if Crop_Img_c2_model_1.size >= 1:
                                print(f"YOLO Model2 output💗💗💗💗")
                                runYOLOm2 = self.model_page22(Crop_Img_c2_model_1, classes=[0])
                                annotated_frame2 = runYOLOm2[0]
                                
                                if annotated_frame2.boxes is not None:
                                    for box in annotated_frame2.boxes:
                                        class_if_model2 = int(box.cls.item())
                                        conf_if_model2 = box.conf.item()
                                        xyxy_if_model2 = box.xyxy[0]
                                        print(f"YOLO Model2 output💗💗💗💗 CM@2: {runYOLOm2[0].boxes}")
                                        
                                        annotator.box_label(xyxy_if_model2, label=f"model2: {class_if_model2} -- {conf_if_model2:.2f}")
                                        self.Tz = pytz.timezone('Asia/Bangkok')
                                        self.Time_cm2_Model2 = datetime.now(self.Tz)
                                        x1, y1, x2, y2 = map(int, xyxy_if_model2)
                                        Crop_Img_c2_model_2 = Crop_Img_c2_model_1[y1:y2, x1:x2]
                                        self.crop_img_m2_m2_del.append((current_time_ids , Crop_Img_c2_model_2 ))
                                        self.Main_Save_path(Crop_Img_c2_model_2, "CM2_Model2", self.Time_cm2_Model2)
                                        Crop_Img_c2_model_2 = cv2.cvtColor(Crop_Img_c2_model_2, cv2.COLOR_BGR2RGB)
                                        img = Image.fromarray(Crop_Img_c2_model_2)
                                        label_width = self.My_show_img2_cap2.winfo_width()
                                        label_height = self.My_show_img2_cap2.winfo_height()
                                        resizeimg = img.resize((label_width, label_height))
                                        imgSHOWCtkm2_c2 = ctk.CTkImage(light_image=resizeimg, size=(label_width, label_height))
                                        self.My_show_img2_cap2.configure(image=imgSHOWCtkm2_c2)
                                        self.My_show_img2_cap2.image = imgSHOWCtkm2_c2
                                        self.crop_img_m2_m2_del = [(t , img ) for t , img in self.crop_img_m2_m2_del if time.time() - t <=5]
                                        self.crop_img_m2_m1_del = [(t , img) for t , img in self.crop_img_m2_m1_del if time.time() - t <=5]
                                else:
                                    pass
                            else:
                                pass
                        self.counter2[track_id] = (cx , cy)
                    
                missing_ids = self.im_SAVE_Id_model1_cm2 - current_frame_ids_C2_m1
                for lost_id in missing_ids:
                    if lost_id in self.id_Time_check_c2_m1:
                        time_since_last_seen = current_time_ids - self.id_Time_check_c2_m1[lost_id]
                        if time_since_last_seen > 10:
                            self.im_save_CHECK_Id_model1_cm2.discard(lost_id)
                            self.im_SAVE_Id_model1_cm2.discard(lost_id)
                            del self.id_Time_check_c2_m1[lost_id]
                
                try:
                    img2 = Image.fromarray(annotated_frame)
                    label_width = self.My_run_cam2_gui.winfo_width()
                    label_height = self.My_run_cam2_gui.winfo_height()
                    resiz_img = img2.resize((label_width, label_height))
                    imgTK2 = ctk.CTkImage(light_image=resiz_img, size=(label_width, label_height))
                    
                    self.My_run_cam2_gui.configure(image=imgTK2)
                    self.My_run_cam2_gui.image = imgTK2
                    
                    cv2.waitKey(1)
                except:
                    pass
                                        
    def point_line_distance(self, cx, cy, line_start, line_end):
        x0, y0 = cx, cy
        x1, y1 = line_start
        x2, y2 = line_end

        numerator = abs((y2 - y1)*x0 - (x2 - x1)*y0 + x2*y1 - y2*x1)
        denominator = ((y2 - y1)**2 + (x2 - x1)**2)**0.5
        distance = numerator / denominator
        return distance
    
    
    def is_Check_LINE1(self, cx, cy, line_start, line_end, tolerance=39):
        distance = self.point_line_distance(cx, cy, line_start, line_end)
        return distance <= tolerance
    
    def is_Check_LINE2(self, cx, cy, line_start, line_end, tolerance=39):
        distance = self.point_line_distance(cx, cy, line_start, line_end)
        return distance <= tolerance



    def Main_Save_path(self, frame, ID_camala, timestamp ):
        path = self.My_time_tz()
        Left_Save = None
        Right_Save = None
        self.best_ALL_CAM_left = None
        self.sent_data_save_cam_lift = None
        self.SQL_direction_against = None
        unique_id = uuid.uuid4().hex[:6]
        # บันทึกข้อมูลลงลิสต์
        if ID_camala == "CM1_Model1":
            self.Time_CM1_MO1 = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            self.CM1_Model1 = frame
            self.CM1_Model1_list.append({
                'image': self.CM1_Model1,
                'timestamp': self.Time_CM1_MO1
            })

        if ID_camala == "CM2_Model1":
            self.Time_CM2_MO1 = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            self.CM2_Model1 = frame
            self.CM2_Model1_list.append({
                'image': self.CM2_Model1,
                'timestamp': self.Time_CM2_MO1
            })

        if ID_camala == "CM1_Model2":
            self.Time_CM1_MO2 = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            self.CM1_Model2 = frame
            self.CM1_Model2_list.append({
                'image': self.CM1_Model2,
                'timestamp': self.Time_CM1_MO2
            })

        if ID_camala == "CM2_Model2":
            self.Time_CM2_MO2 = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            self.CM2_Model2 = frame
            self.CM2_Model2_list.append({
                'image': self.CM2_Model2,
                'timestamp': self.Time_CM2_MO2
            })
            
        
        for dx1 ,time_c1_left in self.Left_way_c1.items():
            time_1c1_left_mod = time_c1_left['Time_Position']
            print(f"👽👽{time_1c1_left_mod}👽👽") 
            
            for dx2 ,  time_c2_left in self.Left_way_c2.items():
                time_2c2_left_mod = time_c2_left['Time_Position']
                print(f"👽👽{time_2c2_left_mod}👽👽")
                
                if time_c1_left['CAM'] == time_c2_left['CAM']:
                    time_1 = datetime.strptime(time_1c1_left_mod, "%H-%M-%S")
                    time_2 = datetime.strptime(time_2c2_left_mod, "%H-%M-%S")
                    diff_time = abs(time_2 - time_1).total_seconds()
                    print(diff_time)
                    
                    
                    if diff_time <= 5 :
                        print("🎃")
                        self.SQL_direction_against = False
                        self.best_ALL_CAM_left = (dx1 , dx2 ,time_c1_left , time_c2_left , diff_time )
                        if self.best_ALL_CAM_left:
                            print("🎃🎃")
                            dx1, dx2, time_data1, time_data2, diff_time = self.best_ALL_CAM_left
                            time1 = datetime.strptime(time_data1['Time_Position'], "%H-%M-%S")
                            time2 = datetime.strptime(time_data2['Time_Position'], "%H-%M-%S")
                            if time1 >= time2:
                                print("🎃🎃🎃")
                                self.sent_data_save_cam_lift = time_data2
                                Left_Save = True
                            else:
                                print("🎃🎃🎃")
                                self.sent_data_save_cam_lift = time_data1
                                Left_Save = True
                                
                        print("🫦🫦🫦🫦🫦🫦🫦🫦🫦🫦🫦")
                        print(diff_time)
                    
        
        for dx1 ,time_c1_right in self.Right_way_c1.items():
            time_1c1_right_mod = time_c1_right['Time_Position']
            # print(f"👽👽{time_1c1_right_mod}👽👽")
            
            for dx2 ,  time_c2_right in self.Right_way_c2.items():
                time_2c2_right_mod = time_c2_right['Time_Position']
                # print(f"👽👽{time_2c2_right_mod}👽👽")
                
                
                time_1 = datetime.strptime(time_1c1_right_mod, "%H-%M-%S")
                time_2 = datetime.strptime(time_2c2_right_mod, "%H-%M-%S")
                diff_time = abs(time_1 - time_2).total_seconds()
                if diff_time <= 5 :
                    self.SQL_direction_against = True
                    Right_Save = True
                    print("🫦🫦🫦🫦🫦🫦🫦🫦🫦🫦🫦")
        

            
        if Left_Save :
            time1= datetime.strptime(self.Time_CM1_MO1, '%Y-%m-%d %H:%M:%S')
            time2 = datetime.strptime(self.Time_CM2_MO1, '%Y-%m-%d %H:%M:%S')
            dateSQL = time1.strftime('%Y-%m-%d'); timeSQL = time1.strftime('%H:%M:%S')
            dateSQL = time2.strftime('%Y-%m-%d'); timeSQL = time2.strftime('%H:%M:%S')
            
            for i, item in enumerate(self.CM1_Model1_list):
                C1_M1_Path_SQL = f"{path}/{self.sent_data_save_cam_lift}/_C1_Model1_{i}_{unique_id}.jpg"
                if cv2.imwrite(C1_M1_Path_SQL, item['image']):
                    self.CM1_M1_M2_Path.append(C1_M1_Path_SQL)
                    print(f"Saved C1_Model1_{i}.jpg")

            for i, item in enumerate(self.CM2_Model1_list):
                C2_M1_Path_SQL = f"{path}/{self.sent_data_save_cam_lift}/_C2_Model1_{i}_{unique_id}.jpg"
                if cv2.imwrite(C2_M1_Path_SQL, item['image']):
                    self.CM2_M1_M2_Path.append(C2_M1_Path_SQL)
                    print(f"Saved C2_Model1_{i}.jpg")


            for i, item in enumerate(self.CM1_Model2_list):
                C1_M2_Path_SQL = f"{path}/{self.sent_data_save_cam_lift}/_C_one_Model2_{i}_{unique_id}.jpg"
                if cv2.imwrite(C1_M2_Path_SQL, item['image']):
                    self.CM1_M1_M2_Path.append(C1_M2_Path_SQL)
                    print(f"Saved C1_Model2_{i}.jpg")

            for i, item in enumerate(self.CM2_Model2_list):
                C2_M2_Path_SQL = f"{path}/{self.sent_data_save_cam_lift}/_C_two_Model2_{i}_{unique_id}.jpg"
                if cv2.imwrite(C2_M2_Path_SQL, item['image']):
                    self.CM2_M1_M2_Path.append(C2_M2_Path_SQL)
                    print(f"Saved C2_Model2_{i}_{unique_id}.jpg")
                    
            self.db.insert(self.period, dateSQL, timeSQL, self.CM1_M1_M2_Path, self.CM2_M1_M2_Path , self.SQL_direction_against)
            self.Notification_windown()
                
            # ล้างลิสต์
            self.CM1_Model1_list = []
            self.CM2_Model1_list = []
            self.CM1_Model2_list = []
            self.CM2_Model2_list = []
            self.Have_cam1_no_cam2 = False
            self.Have_cam2_no_cam1 = False
            self.direction_against001 = False
            self.direction_against002 = False
            self.SQL_direction_against = False
            Left_Save = None
            Right_Save = None
            self.My_show_img1_cap2.configure(image=None)
            self.My_show_img1_cap2.image = None

            self.My_show_img2_cap2.configure(image=None)
            self.My_show_img2_cap2.image = None
            
            

            
    def start_cam(self):
        self.start_event = threading.Event()
        threading.Thread(target= self.Process_Cam01 , daemon=True).start()
        threading.Thread(target= self.Process_Cam02 , daemon=True).start()
        self.start_event.set()
    
        
    def destroyy(self):
        msg = CTkMessagebox(title="ยืนยันการออก", message="คุณแน่ใจว่าต้องการออกจากโปรแกรม?", 
                            icon="question", option_1="ยกเลิก", option_2="ตกลง")
        if msg.get() == "ตกลง":
            gc.collect()
            self.running = False
            self.cam01.release()
            self.cam02.release()
            self.out1.release()
            self.out2.release()
            cv2.destroyAllWindows()
            self.quit()
            sys.exit()
    
    def from_logout_(self):
        
        msg = CTkMessagebox(title="ยืนยันการออก", message="คุณแน่ใจว่าต้องการออกจากระบบ?", 
                            icon="question", option_1="ยกเลิก", option_2="ตกลง")
        if msg.get() == "ตกลง":
            try:
                self.cam01.release()
                self.cam02.release()
                self.out1.release()
                self.out2.release()
                self.after(100 , self.quit)
                cv2.destroyAllWindows()
                self.master.LoginFFrame = LoginFrame(self.master) 
                self.master.LoginFFrame.pack(fill="both", expand=True)
            except:
                pass

    


    def Notification_windown(self):
        def on_click():
            webbrowser.open("http://localhost:8000/dachvoth")

        toaster = ToastNotifier()
        toaster.show_toast(
            "ตรวจพบการระเมิดรถจักยานยนต์บนทางเท้า",
            "คลิกเพื่อตรวจสอบ",
            duration=10,
            threaded=True,
            callback_on_click=on_click
        )
        
    def Notification_windown_Counter(self):
        def on_click():
            webbrowser.open("http://localhost:8000/dachvoth")

        toaster = ToastNotifier()
        toaster.show_toast(
            "ตรวจพบการระเมิดรถจักยานยนต์บนทางเท้า\nและการขับรถย้อนศร",
            "คลิกเพื่อตรวจสอบ",
            duration=10,
            threaded=True,
            callback_on_click=on_click
        )



class LoginFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.bind("<Configure>", self.Show_img_BkMain)
        self.Bk_laout_1()
    def Show_img_BkMain(self, event=None):
        self.width = self.winfo_width()
        self.height = self.winfo_height()

        # โหลดภาพและปรับขนาด
        img = Image.open("gui\\bkmain1.png")
        resized = img.resize((self.width, self.height))
        self.Show_BG_Sky = ctk.CTkImage(light_image=resized, size=(self.width, self.height))
        self.im_show_BG_Sky = ctk.CTkLabel(self, text="", image=self.Show_BG_Sky)
        self.im_show_BG_Sky.place(x=0, y=0, relwidth=1, relheight=1)
        self.bkmain1.lift()
        self.im_show_img_let1.lift()

    def Bk_laout_1(self):
        self.bkmain1 = ctk.CTkFrame(self, fg_color="#333333")
        self.bkmain1.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.85, anchor="center")

        self.bkmain2 = ctk.CTkFrame(self.bkmain1, fg_color="#040404")
        self.bkmain2.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        self.bkmain_input = ctk.CTkFrame(self.bkmain1, fg_color="#040404")
        self.bkmain_input.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)


        self.img_let1 = Image.open("gui\\img2.png")
        self.im_show_img_let1 = ctk.CTkLabel(self.bkmain2, text="")
        self.im_show_img_let1.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.bkmain2.bind("<Configure>", self.resize_img_in_bkmain2)
        self.bkmain_input.bind("<Configure>" , self.In_Put_index)

    def resize_img_in_bkmain2(self, event):
        print(f"Event widget: {event.widget}, Width: {event.width}, Height: {event.height}")
        width = event.width
        height = event.height
        resized_img = self.img_let1.resize((width, height))
        self.show_img_let1 = ctk.CTkImage(light_image=resized_img, size=(width, height))
        self.im_show_img_let1.configure(image=self.show_img_let1)
        self.im_show_img_let1.image = self.show_img_let1


    def In_Put_index(self, event=None):
        print(f"Event widget: {event.widget}, Width: {event.width}, Height: {event.height}xxxxxxxxxxx")
        if len(self.bkmain_input.winfo_children()) > 0:
            return  
        parent_width = self.bkmain_input.winfo_width() 
        parent_height = self.bkmain_input.winfo_height() 
        
        self.frame_login_back = ctk.CTkFrame(self.bkmain_input , fg_color="#040404")
        self.frame_login_back.place(relx=0.5, rely=0.3, anchor='n', relwidth=0.5, relheight=0.5)
        if parent_height >= 516 or parent_height >= 440:
            parent_width = 333
            parent_height = 33

        self.label = ctk.CTkLabel(self.frame_login_back, text="Welcome to Login" , width=parent_width , height=parent_height ,font=("Arial", 24, "bold"))
        self.label.pack(pady=40)

        self.entry_email = ctk.CTkEntry(self.frame_login_back, placeholder_text="Email...", width=parent_width, height=parent_height)
        self.entry_email.pack(pady=10)

        self.entry_password = ctk.CTkEntry(self.frame_login_back, placeholder_text="Password...", width=parent_width, height=parent_height, show="*")
        self.entry_password.pack(pady=10)

        self.button_login = ctk.CTkButton(self.frame_login_back, text="Login", command=self.master.Go_main_App_Sy)


        self.button_login.pack(pady=20)
    
    
    def Check_Login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()




class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("โปรแกรมตรวจจับมอไซบนทางเท้า")
        self.LoginFFrame = LoginFrame(self)
        self.LoginFFrame.pack(fill="both", expand=True)
        width = self.winfo_screenwidth() 
        height = self.winfo_screenheight()
        self.resizable(True, True)  # เปลี่ยนเป็น True เพื่อให้ยืดหยุ่น
        self.minsize(800, 600)
        self.geometry(f"1000x700")  # ขนาดเริ่มต้น
        self.screen_app_width = self.winfo_screenwidth()
        self.after(1000, lambda: self.state('zoomed'))
        self.protocol("WM_DELETE_WINDOW", self.surs)


    def Go_main_App_Sy(self):
        self.LoginFFrame.destroy()
        self.main_app_frame = APP_SY_Frame(self)
        self.main_app_frame.pack(fill="both", expand=True)
        
        
    def surs(self):
        msg = CTkMessagebox(title="ยืนยันการออก", message="คุณแน่ใจว่าต้องการออกจากโปรแกรม?", 
                            icon="warning", option_1="ยกเลิก", option_2="ตกลง")
        
        if msg.get() == "ตกลง":
            self.quit()
            
            
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
