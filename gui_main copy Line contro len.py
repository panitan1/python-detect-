import math
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
from server_mysql.mysql_server import datasql 
import uuid
from win10toast_click import ToastNotifier
import gc
from master_log.master_log import MasterLog


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

class APP_SY_Frame(ctk.CTkFrame):
    def __init__(self , master):
        super().__init__(master)
        self.master = master          
        self.show_loading_popup()
        # ctk.set_widget_scaling(0.8)
        
        self.save_lock = threading.Lock()

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
        self.CM1_M1_M2_Path_the_one = []
        self.CM2_M1_M2_Path_the_one = []


        self.period = None
        self.Line1 =  np.array([[394, 1282], [1772, 195]])
        self.Line2 = np.array([[1831, 932], [449, 312]])
        self.track_color = {}
        self.Check_Line = False

        self.MuNuAPP_main()
        self.Main_CV2()
        self.My_show_ui_My_cap1()
        self.My_show_ui_My_cap2()
        self.start_cam()
        
        
        self.CM2_Model1_and_Model2_list = {}
        self.CM1_Model1_and_Model2_list = {}
        self.Supper_check_c1_List = []
        self.Supper_check_c2_List = []

        self.Check_Cam1_ = True
        self.Check_Cam2_ = True
        self.sent_save1 = False
        self.contro_Save1 = False
        self.contro_Save2 = False
        self.Time_cm1_Model1 = None
        self.Time_cm2_Model1 = None
        self.Time_cam2_oj = None
        self.Time_cam1_oj = None
        
        
        self.My_checkOut_cm1 = {} 
        self.My_checkOut_cm2 = {} 
        self.db = datasql()
        self.master_log_set = MasterLog()

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
        
        
    
        
        

    def Process_Cam01(self):
        self.My_cap1()
        self.model = YOLO("yolov8m.pt").cuda()
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

        
        self.crop_img_m1_m1_del = []
        self.crop_img_m1_m2_del = []


        
        os.makedirs("vidioodetect1", exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        frame_width = int(self.cam01.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cam01.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(self.cam01.get(cv2.CAP_PROP_FPS)) or 30
    
        self.out1 = cv2.VideoWriter(f"vidioodetect1/output_detected_1.avi", fourcc, fps, (frame_width, frame_height))
        self.master_log_set.info("connect to Camera 1") 
        while self.running and self.save_lock:

            ret, frame = self.cam01.read()
            if not ret:
                self.ERRORCAM_pp001 = "กล้องหมายเลข 1 ไม่ทำงาน กรุณาตรวจสอบการเชื่อมต่อ {ret}"
                CTkMessagebox(title="Error", message=f"กล้องหมายเลข 1 ไม่ทำงาน กรุณาตรวจสอบการเชื่อมต่อ \n {ret}", icon="cancel")
                self.Check_Cam1_ = False
                self.master_log_set.error("Failed to connect to Camera 1")
               
            frame_for_save = frame.copy()
            self.out1.write(frame_for_save)  # ✅ เขียน BGR ลงไฟล์

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            original_frame = frame.copy()
            original_frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2RGB)
            cv2.line(frame, self.Line1[0], self.Line1[1], (255, 0, 255), 3)
            annotator = Annotator(frame)
            annotated_frame = annotator.result()
            
            
            runYOLOm1 = self.model.track(frame, classes=[0], conf=0.5, persist=True, tracker="gui\\botsort.yaml")
            annotated_frame1 = runYOLOm1[0]
            self.Tz = pytz.timezone('Asia/Bangkok')
            self.Time_cm1_Model1 = datetime.now(self.Tz)
            self.Main_Save_path(None, "Supper_check_c1", self.Time_cm1_Model1, None)
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
                        annotator.box_label(xyxy_if_model1, 
                                            label=f"motorcycle_c1: {class_if_model1} -- {Conf_if_model1:.2f} -- {int(track_id)}")
                        
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
                        
                        if  self.im_SAVE_Id_model1_cm1 != self.im_save_CHECK_Id_model1_cm1 and  self.is_Check_LINE1(cx, cy):
                            self.Time_cam1_oj = self.Time_cm1_Model1
                            self.master_log_set.info("Motorcycle detected on Camera 1")
                            self.im_save_CHECK_Id_model1_cm1.update(self.im_SAVE_Id_model1_cm1)

                            x1, y1, x2, y2 = map(int, xyxy_if_model1)

                            self.Crop_Img_c1_model_1 = original_frame[y1:y2, x1:x2]
                            
    
                            
                            print("💚")
                            
                            self.Main_Save_path(self.Crop_Img_c1_model_1, "CM1_Model1",self.Time_cam1_oj , track_id)
                            
                            self.Crop_Img_c1_model_1_GUI = cv2.cvtColor(self.Crop_Img_c1_model_1, cv2.COLOR_BGR2RGB)
                            img = Image.fromarray(self.Crop_Img_c1_model_1_GUI)
                            label_width = self.My_show_img1.winfo_width()
                            label_height = self.My_show_img1.winfo_height()
                            resizeimg = img.resize((label_width, label_height))
                            imgSHOWCtkm1_c1 = ctk.CTkImage(light_image=resizeimg, size=(label_width, label_height))
                            self.My_show_img1.configure(image=imgSHOWCtkm1_c1)
                            self.My_show_img1.image = imgSHOWCtkm1_c1
                            self.after(5000, self.clear_image_after_delay)

                            # print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{Crop_Img_c1_model_1}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                            if self.Crop_Img_c1_model_1.size >= 1:
                                print(f"YOLO Model2 output💗💗💗💗")
                                runYOLOm2 = self.model_page(self.Crop_Img_c1_model_1, classes=[0])
                                annotated_frame2 = runYOLOm2[0]
                                
                                if annotated_frame2.boxes is not None:
                                    for box in annotated_frame2.boxes:
                                        self.master_log_set.info("License plate detected by Camera 1")
                                        class_if_model2 = int(box.cls.item())
                                        conf_if_model2 = box.conf.item()
                                        xyxy_if_model2 = box.xyxy[0]
                                        print(f"YOLO Model2 output💗💗💗💗 CM@2: {runYOLOm2[0].boxes}")
                                        annotator.box_label(xyxy_if_model2 , label=f"model2 : {class_if_model2} -- {conf_if_model2:.2f}")
                                        
                                        x1 ,y1 , x2 ,y2 = map(int , xyxy_if_model2)
                                        self.Crop_Img_c1_model_2 = self.Crop_Img_c1_model_1[y1:y2 , x1:x2]

                                        self.Main_Save_path(self.Crop_Img_c1_model_2 , "CM1_Model2" , self.Time_cam1_oj , track_id)
                                        
                                        self.Crop_Img_c1_model_2 = cv2.cvtColor(self.Crop_Img_c1_model_2, cv2.COLOR_BGR2RGB)
                                        img = Image.fromarray(self.Crop_Img_c1_model_2)
                                        label_width = self.My_show_img2.winfo_width()
                                        label_height = self.My_show_img2.winfo_height()
                                        resizeimg = img.resize((label_width ,label_height))
                                        imgSHOWCtkm2_c1 = ctk.CTkImage(light_image= resizeimg , size= (label_width ,label_height ))
                                        self.My_show_img2.configure(image = imgSHOWCtkm2_c1)
                                        self.My_show_img2.image = imgSHOWCtkm2_c1
                    
                                        self.after(5000, self.clear_image_after_delay)
                                        self.Crop_Img_c1_model_2 = None
                                        self.Crop_Img_c1_model_1 = None
                                    
                            # if self.Time_cam1_oj is not None and self.Time_cm2_Model1 is not None:
                                    



                missing_ids = self.im_SAVE_Id_model1_cm1 - current_frame_ids
                for lost_id in missing_ids:
                    if lost_id in self.id_Time_check_c1_m1:
                        time_since_last_seen = current_time_ids - self.id_Time_check_c1_m1[lost_id]
                        if time_since_last_seen > 10:
                            print(f"Test: ล้างข้อมูล ก่อน : {self.im_save_CHECK_Id_model1_cm1} ")
                            print(f"Test: ล้างข้อมูล ก่อน : {self.im_SAVE_Id_model1_cm1} ")
                            print(f"Test: ล้างข้อมูล ก่อน : {self.id_Time_check_c1_m1} ")
                            self.im_save_CHECK_Id_model1_cm1.discard(lost_id) 
                            self.im_SAVE_Id_model1_cm1.discard(lost_id)     
                            del self.id_Time_check_c1_m1[lost_id]             
                            print(f"Test: ล้างข้อมูล หลัง : {self.im_save_CHECK_Id_model1_cm1} ")
                            print(f"Test: ล้างข้อมูล หลัง : {self.im_SAVE_Id_model1_cm1} ")
                            print(f"Test: ล้างข้อมูล หลัง : {self.id_Time_check_c1_m1} ")


                
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
        


    def Process_Cam02(self): 
        self.My_cap2()
        self.model22 = YOLO("yolov8m.pt").cuda()
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



  
        
        os.makedirs("vidioodetect2", exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        frame_width = int(self.cam02.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cam02.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(self.cam02.get(cv2.CAP_PROP_FPS)) or 30
  
        self.out2 = cv2.VideoWriter(f"vidioodetect2/output_detected_2.avi", fourcc, fps, (frame_width, frame_height))
        
        self.master_log_set.info("connect to Camera 2")  
        while self.running and self.save_lock:
 
            ret, frame2 = self.cam02.read()
            if not ret:
                self.ERRORCAM_pp002 = "กล้องหมายเลข 2 ไม่ทำงาน กรุณาตรวจสอบการเชื่อมต่อ {ret}"
                CTkMessagebox(title="Error", message=f"กล้องหมายเลข 2 ไม่ทำงาน กรุณาตรวจสอบการเชื่อมต่อ \n {ret}", icon="cancel")
                self.Check_Cam2_ = False
                self.master_log_set.error("Failed to connect to Camera 2")
            
            frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            self.out2.write(frame2) 
            original_frame = frame2.copy()
            original_frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2RGB)
            cv2.line(frame2, self.Line2[0], self.Line2[1], (255, 0, 255), 3)
            annotator = Annotator(frame2)
            annotated_frame = annotator.result()
            
            runYOLOm1 = self.model22.track(frame2, classes=[0], conf=0.5, persist=True  , tracker="gui\\botsort.yaml")
            annotated_frame1 = runYOLOm1[0]
            self.Tz = pytz.timezone('Asia/Bangkok')
            self.Time_cm2_Model1 = datetime.now(self.Tz)
            self.Main_Save_path(None, "Supper_check_c2", self.Time_cm2_Model1, None)
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
                        
                        
                        
                        if self.im_SAVE_Id_model1_cm2 != self.im_save_CHECK_Id_model1_cm2 and self.is_Check_LINE2(cx, cy):
                            self.Time_cam2_oj = self.Time_cm2_Model1
                            self.master_log_set.info("Motorcycle detected on Camera 2")

                            self.im_save_CHECK_Id_model1_cm2.update(self.im_SAVE_Id_model1_cm2)
                            
                            
                            
                            
                            x1, y1, x2, y2 = map(int, xyxy_if_model1)
                            
                            self.Crop_Img_c2_model_1 = original_frame[y1:y2, x1:x2]
    
                            
                            print("🩷")
                        
                            self.Main_Save_path(self.Crop_Img_c2_model_1, "CM2_Model1", self.Time_cam2_oj, track_id)
                            
                            self.Crop_Img_c2_model_1_show_GUI = cv2.cvtColor(self.Crop_Img_c2_model_1, cv2.COLOR_BGR2RGB)
                            img = Image.fromarray(self.Crop_Img_c2_model_1_show_GUI)
                            label_width = self.My_show_img1_cap2.winfo_width()
                            label_height = self.My_show_img1_cap2.winfo_height()
                            resizeimg = img.resize((label_width, label_height))
                            imgSHOWCtkm1_c2 = ctk.CTkImage(light_image=resizeimg, size=(label_width, label_height))
                            self.My_show_img1_cap2.configure(image=imgSHOWCtkm1_c2)
                            self.My_show_img1_cap2.image = imgSHOWCtkm1_c2
    

                            self.after(5000, self.clear_image_after_delay)
                            if self.Crop_Img_c2_model_1.size >= 1:
                                
                                print(f"YOLO Model2 output💗💗💗💗")
                                runYOLOm2 = self.model_page22(self.Crop_Img_c2_model_1, classes=[0])
                                annotated_frame2 = runYOLOm2[0]
                                
                                if annotated_frame2.boxes is not None:
                                    for box in annotated_frame2.boxes:
                                        class_if_model2 = int(box.cls.item())
                                        conf_if_model2 = box.conf.item()
                                        xyxy_if_model2 = box.xyxy[0]
                                        print(f"YOLO Model2 output💗💗💗💗 CM@2: {runYOLOm2[0].boxes}")
                                        self.master_log_set.info("License plate detected by Camera 2")
                                        annotator.box_label(xyxy_if_model2, label=f"motorcycle_c2: {class_if_model2} -- {conf_if_model2:.2f}")
                                        self.Tz = pytz.timezone('Asia/Bangkok')
                                        self.Time_cm2_Model2 = datetime.now(self.Tz)
                                        x1, y1, x2, y2 = map(int, xyxy_if_model2)
                                        self.Crop_Img_c2_model_2 = self.Crop_Img_c2_model_1[y1:y2, x1:x2]
                                        
                                        
                                        
                                        self.Main_Save_path(self.Crop_Img_c2_model_2 , "CM2_Model2", self.Time_cam2_oj, track_id)
                                        self.Crop_Img_c2_model_2 = cv2.cvtColor(self.Crop_Img_c2_model_2, cv2.COLOR_BGR2RGB)
                                        img = Image.fromarray(self.Crop_Img_c2_model_2)
                                        label_width = self.My_show_img2_cap2.winfo_width()
                                        label_height = self.My_show_img2_cap2.winfo_height()
                                        resizeimg = img.resize((label_width, label_height))
                                        imgSHOWCtkm2_c2 = ctk.CTkImage(light_image=resizeimg, size=(label_width, label_height))
                                        self.My_show_img2_cap2.configure(image=imgSHOWCtkm2_c2)
                                        self.My_show_img2_cap2.image = imgSHOWCtkm2_c2

                                        self.after(5000, self.clear_image_after_delay)
                                        self.Crop_Img_c2_model_1 = None
                                        self.Crop_Img_c2_model_2 = None
                            
                            # if self.Time_cam2_oj is not None and self.Time_cm1_Model1 is not None:                
                                
      
                    
                missing_ids = self.im_SAVE_Id_model1_cm2 - current_frame_ids_C2_m1
                for lost_id in missing_ids:
                    if lost_id in self.id_Time_check_c2_m1:
                        time_since_last_seen = current_time_ids - self.id_Time_check_c2_m1[lost_id]
                        if time_since_last_seen > 10:
                            print(f"Test: ล้างข้อมูล ก่อน : {self.im_save_CHECK_Id_model1_cm2} ")
                            print(f"Test: ล้างข้อมูล ก่อน : {self.im_SAVE_Id_model1_cm2} ")
                            print(f"Test: ล้างข้อมูล ก่อน : {self.id_Time_check_c2_m1} ")
                            self.im_save_CHECK_Id_model1_cm2.discard(lost_id)
                            self.im_SAVE_Id_model1_cm2.discard(lost_id)
                            del self.id_Time_check_c2_m1[lost_id]
                            print(f"Test: ล้างข้อมูล หลัง : {self.im_save_CHECK_Id_model1_cm2} ")
                            print(f"Test: ล้างข้อมูล หลัง : {self.im_SAVE_Id_model1_cm2} ")
                            print(f"Test: ล้างข้อมูล หลัง : {self.id_Time_check_c2_m1} ")
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
    
    def clear_image_after_delay(self):
        self.My_show_img1_cap2.configure(image="", text="")
        self.My_show_img1_cap2.image = None
        self.My_show_img1_cap2.update()
        self.My_show_img1.configure(image="", text="")
        self.My_show_img1.image = None
        

        self.My_show_img2_cap2.configure(image="", text="")
        self.My_show_img2_cap2.image = None
        self.My_show_img2_cap2.update()
        self.My_show_img2.configure(image = "", text="")
        self.My_show_img2.image = None
        # ล้างภาพจาก CTkLabel
        self.My_show_img1.configure(image="")
        self.My_show_img1.image = None
        # ล้างตัวแปรภาพ
        self.imgSHOWCtkm1_c1 = None
        self.imgSHOWCtkm1_c2 = None
        
        self.Crop_Img_c1_model_1 = None

        print("🧹 ล้างภาพเรียบร้อยหลังจาก 5 วินาที")


                                        

    
    def is_Check_LINE1(self, cx, cy):
        x1, y1 = self.Line1[0]
        x2, y2 = self.Line1[1]

        A = x2 - x1 
        B = y2 - y1
        C = A**2 + B**2
        C_root = math.sqrt(C)
        numerator = abs(A * (cy - y1) - B * (cx - x1))
        distance = numerator / C_root
        threshold = 75
        if distance <= threshold:
            return True
        else:
            return False
            
    def is_Check_LINE2(self, cx, cy):
        x1, y1 = self.Line2[0]
        x2, y2 = self.Line2[1]

        A = x2 - x1 
        B = y2 - y1
        C = A**2 + B**2
        C_root = math.sqrt(C)
        numerator = abs(A * (cy - y1) - B * (cx - x1))
        distance = numerator / C_root
        threshold = 75
        if distance <= threshold:
            return True
        else:
            return False
    

    def show_loading_popup(self):
        CTkMessagebox(title="Info", message="กำลังโหลดข้อมูลกล้อง กรุณารอสักครู่",icon="check")


    def Main_Save_path(self, frame, ID_camala, timestamp, track_id):
        
        re_list_index = []
        re_list_index_model2_c1 = []
        re_list_index_model2_c2 = []
        re_supprt_index1 = []
        re_supprt_index2 = []
        re_supprt_index1_model2 = []
        re_supprt_index2_model2 = []
        two_save = False
        supper_SAVE = False
        tz = pytz.timezone('Asia/Bangkok')
        now = datetime.now(tz)
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

        self.best_ALL_CAM_left = None
        self.sent_data_save_cam_lift = None
        self.SQL_direction_against = None
        unique_id = uuid.uuid4().hex[:6]

        # เก็บข้อมูลการตรวจจับลงในลิสต์ที่เหมาะสม
        if ID_camala == "CM1_Model1":
            self.Time_CM1_MO1 = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            self.CM1_Model1 = frame
            self.Track_idC1M1 = track_id
            self.CM1_Model1_list.append({
                'image': self.CM1_Model1,
                'timestamp': self.Time_CM1_MO1,
                'inx': self.Track_idC1M1
            })

        if ID_camala == "CM2_Model1":
            self.Time_CM2_MO1 = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            self.CM2_Model1 = frame
            self.Track_idC2M1 = track_id
            self.CM2_Model1_list.append({
                'image': self.CM2_Model1,
                'timestamp': self.Time_CM2_MO1,
                'inx': self.Track_idC2M1
            })
        
        if ID_camala == "CM1_Model2":
            self.Time_CM1_MO2 = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            self.CM1_Model2 = frame
            self.Track_idC1M2 = track_id
            self.CM1_Model2_list.append({
                'image': self.CM1_Model2,
                'timestamp': self.Time_CM1_MO2,
                'inx': self.Track_idC1M2
            })

        if ID_camala == "CM2_Model2":
            self.Time_CM2_MO2 = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            self.CM2_Model2 = frame
            self.Track_idC2M2 = track_id
            self.CM2_Model2_list.append({
                'image': self.CM2_Model2,
                'timestamp': self.Time_CM2_MO2,
                'inx': self.Track_idC2M2
            })
        
        if ID_camala == "Supper_check_c1":
            self.Supper_check_c1 = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            self.Supper_check_c1_List = [{
                'timestamp': self.Supper_check_c1,
            }]
        if ID_camala == "Supper_check_c2":
            self.Supper_check_c2 = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            self.Supper_check_c2_List = [{
                'timestamp': self.Supper_check_c2,
            }]

        if self.CM1_Model1_list or self.CM2_Model1_list:
            for i, (item1, item2) in enumerate(zip(self.CM1_Model1_list, self.CM2_Model1_list)):
                if two_save:
                    break
                time_str1 = item1['timestamp']
                time_str2 = item2['timestamp']
                idx_ID1 = item1['inx']
                idx_ID2 = item2['inx']

                time_obj1 = datetime.strptime(time_str1, '%Y-%m-%d %H:%M:%S')
                time_obj2 = datetime.strptime(time_str2, '%Y-%m-%d %H:%M:%S')

                time_diff = abs((time_obj1 - time_obj2).total_seconds())
                print(f"{time_obj1}")
                print(f"{time_obj2}")
                print(f"ส่วนต่างเวลา: {time_diff} วินาที")
                if time_obj1 < time_obj2:
                    time1= datetime.strptime(self.Time_CM1_MO1, '%Y-%m-%d %H:%M:%S')
                    dateSQL = time1.strftime('%Y-%m-%d') 
                    timeSQL = time1.strftime('%H:%M:%S')
                    timePATH = time1.strftime('%H-%M-%S')
                    print("CM1_Model1 มาก่อน CM2_Model1")
                elif time_obj1 > time_obj2:
                    time2 = datetime.strptime(self.Time_CM2_MO1, '%Y-%m-%d %H:%M:%S')
                    dateSQL = time2.strftime('%Y-%m-%d')
                    timeSQL = time2.strftime('%H:%M:%S')
                    timePATH = time2.strftime('%H-%M-%S')
                    print("CM2_Model1 มาก่อน CM1_Model1")
                else:
                    time1= datetime.strptime(self.Time_CM1_MO1, '%Y-%m-%d %H:%M:%S')
                    dateSQL = time1.strftime('%Y-%m-%d') 
                    timeSQL = time1.strftime('%H:%M:%S')
                    timePATH = time1.strftime('%H-%M-%S')
                if time_diff <= 5:
                    self.master_log_set.info("Matched detection from Camera 1 and Camera 2")
                    re_list_index.append(i)
                    time1 = datetime.strptime(self.Time_CM1_MO1, '%Y-%m-%d %H:%M:%S')
                    dateSQL = time1.strftime('%Y-%m-%d')
                    timeSQL = time1.strftime('%H:%M:%S')
                    timePATH = time1.strftime('%H-%M-%S')
                    full_save_dir = f"{save_dir}/{timePATH}"
                    os.makedirs(full_save_dir, exist_ok=True)

                    for i, item in enumerate(self.CM1_Model1_list):
                        C1_M1_Path_SQL = f"{full_save_dir}/_C1_Model1_{i}_{unique_id}.png"
                        if cv2.imwrite(C1_M1_Path_SQL, item['image']):
                            self.CM1_M1_M2_Path.append(C1_M1_Path_SQL)
                            print(f"บันทึก C1_Model1_{i}.png")

                    for i, item in enumerate(self.CM2_Model1_list):
                        C2_M1_Path_SQL = f"{full_save_dir}/_C2_Model1_{i}_{unique_id}.png"
                        if cv2.imwrite(C2_M1_Path_SQL, item['image']):
                            self.CM2_M1_M2_Path.append(C2_M1_Path_SQL)
                            print(f"บันทึก C2_Model1_{i}.png")

                    for i, item in enumerate(self.CM1_Model2_list):
                        timeCM1_p = item['inx']
                        if timeCM1_p == idx_ID1:
                            C1_M2_Path_SQL = f"{full_save_dir}/_C_one_Model2_{i}_{unique_id}.png"
                            if cv2.imwrite(C1_M2_Path_SQL, item['image']):
                                self.CM1_M1_M2_Path.append(C1_M2_Path_SQL)
                                print(f"บันทึก C1_Model2_{i}.png")
                            re_list_index_model2_c1.append(i)
      

                    for i, item in enumerate(self.CM2_Model2_list):
                        timeCM2_p = item['inx']
                        if timeCM2_p == idx_ID2:
                            C2_M2_Path_SQL = f"{full_save_dir}/_C_two_Model2_{i}_{unique_id}.png"
                            if cv2.imwrite(C2_M2_Path_SQL, item['image']):
                                self.CM2_M1_M2_Path.append(C2_M2_Path_SQL)
                                print(f"บันทึก C2_Model2_{i}_{unique_id}.png")
                            re_list_index_model2_c2.append(i)
                    

                    
                        
                
                    self.master_log_set.info("Matched detection from Camera 1 and Camera 2. Data saved successfully")
                    self.db.insert(self.period, dateSQL, timeSQL, self.CM1_M1_M2_Path, self.CM2_M1_M2_Path)
                    self.Notification_windown()
                    self.CM1_Model1 = None
                    self.CM2_Model1 = None
                    self.CM1_Model2 = None
                    self.CM2_Model2 = None
                    self.CM2_M1_M2_Path = []
                    self.CM1_M1_M2_Path = []
                    two_save = True
                    for i in reversed(re_list_index):
                        if i < len(self.CM1_Model1_list):
                            del self.CM1_Model1_list[i]
                        if i < len(self.CM2_Model1_list):
                            del self.CM2_Model1_list[i]
                    for i in reversed(re_list_index_model2_c1):
                        if i < len(self.CM1_Model1_list):
                            del self.CM1_Model1_list[i]
                        if i < len(self.CM1_Model2_list):
                            del self.CM1_Model2_list[i]
                    for i in reversed(re_list_index_model2_c2):
                        if i < len(self.CM2_Model2_list):
                            del self.CM2_Model2_list[i]
                        if i < len(self.CM2_Model2_list):
                            del self.CM2_Model2_list[i]

        # บันทึกข้อมูลกล้อง 1 อิสระถ้าเกิน 4 วินาที
        if self.CM1_Model1_list:
            for i, item1 in enumerate(self.CM1_Model1_list):
                if supper_SAVE:
                    break
                re_supprt_index1.append(i)
                idx_ID1 = item1['inx']
                timeput = item1['timestamp']
                Time_only_Cam1 = tz.localize(datetime.strptime(timeput, "%Y-%m-%d %H:%M:%S"))
                for sp_item1 in self.Supper_check_c2_List:
                    sp_item1_now = sp_item1['timestamp']
                    sp_item1_now_str = tz.localize(datetime.strptime(sp_item1_now, "%Y-%m-%d %H:%M:%S"))
                    time_diff = abs((sp_item1_now_str - Time_only_Cam1).total_seconds())
                    if time_diff > 4 :
                        self.master_log_set.info("Matched detection from Camera 1 only.")
                        print(f"ส่วนต่างเวลากล้อง 1: {time_diff} วินาที")
                        print(f"ค่าของง self.CM1_Model1_list {self.CM1_Model1_list}")
                        print("บันทึกข้อมูลกล้อง 1 อิสระ")
                        timePATH = Time_only_Cam1.strftime('%H-%M-%S')
                        dateSQL = Time_only_Cam1.strftime('%Y-%m-%d')
                        timeSQL = Time_only_Cam1.strftime('%H:%M:%S')
                        full_save_dir = f"{save_dir}/{timePATH}"
                        os.makedirs(full_save_dir, exist_ok=True)
                        C1_M1_Path_SQL = f"{full_save_dir}/_C1_Model1_{i}_{unique_id}.png"
                        if cv2.imwrite(C1_M1_Path_SQL, item1['image']):
                            self.CM1_M1_M2_Path_the_one.append(C1_M1_Path_SQL)
                            print(f"บันทึก C1_Model1_{i}.png")

                        for j, item in enumerate(self.CM1_Model2_list):
                            if item['inx'] == idx_ID1:
                                C1_M2_Path_SQL = f"{full_save_dir}/_C_one_Model2_{j}_{unique_id}.png"
                                if cv2.imwrite(C1_M2_Path_SQL, item['image']):
                                    self.CM1_M1_M2_Path_the_one.append(C1_M2_Path_SQL)
                                    print(f"บันทึก C1_Model2_{j}.png")
                                re_supprt_index1_model2.append(j)


                        self.master_log_set.info(" detection from Camera 1 only. Data saved successfully")
                        self.db.insert(self.period, dateSQL, timeSQL, self.CM1_M1_M2_Path_the_one, None)
                        self.Notification_windown()
                        self.CM1_M1_M2_Path_the_one = []
                        self.contro_Save1 = False
                        print(f"ค่าของง self.CM1_Model1_list ลบแล้ว {self.CM1_Model1_list}")
                        self.Time_cam1_oj = None
                        if self.CM1_Model1_list:
                            for i in reversed(re_supprt_index1):
                                if i < len(self.CM1_Model1_list):
                                    del self.CM1_Model1_list[i]
                            for i in reversed(re_supprt_index1_model2):
                                if i < len(self.CM1_Model1_list):
                                    del self.CM1_Model2_list[i]
                supper_SAVE = True  
                break  
                            
        # บันทึกข้อมูลกล้อง 2 อิสระถ้าเกิน 4 วินาที
        if self.CM2_Model1_list:
            for i, item1 in enumerate(self.CM2_Model1_list):
                if supper_SAVE:
                    break
                re_supprt_index2.append(i)
                idx_ID2 = item1['inx']
                timeput = item1['timestamp']
                Time_only_Cam2 = tz.localize(datetime.strptime(timeput, "%Y-%m-%d %H:%M:%S"))
                
                for sp_item1 in self.Supper_check_c1_List:
                    sp_item1_now  = sp_item1['timestamp']
                    sp_item1_now_str = tz.localize(datetime.strptime(sp_item1_now, "%Y-%m-%d %H:%M:%S"))
                
                    time_diff = abs((sp_item1_now_str - Time_only_Cam2).total_seconds())
                    print(f"ส่วนต่างเวลากล้อง 2: {time_diff} วินาที")
                    print(f"ค่าของง self.CM2_Model1_list  {self.CM2_Model1_list}")
                    print("บันทึกข้อมูลกล้อง 2 อิสระ")
                    if time_diff > 4:
                        self.master_log_set.info("Matched detection from Camera 2 only.")    
                        timePATH = Time_only_Cam2.strftime('%H-%M-%S')
                        dateSQL = Time_only_Cam2.strftime('%Y-%m-%d')
                        timeSQL = Time_only_Cam2.strftime('%H:%M:%S')
                        full_save_dir = f"{save_dir}/{timePATH}"
                        os.makedirs(full_save_dir, exist_ok=True)

                        C2_M1_Path_SQL = f"{full_save_dir}/_C2_Model1_{i}_{unique_id}.png"
                        if cv2.imwrite(C2_M1_Path_SQL, item1['image']):
                            self.CM2_M1_M2_Path_the_one.append(C2_M1_Path_SQL)
                            print(f"บันทึก C2_Model1_{i}.png")

                        for j, item in enumerate(self.CM2_Model2_list):
                            if item['inx'] == idx_ID2:
                                C2_M2_Path_SQL = f"{full_save_dir}/_C_two_Model2_{j}_{unique_id}.png"
                                if cv2.imwrite(C2_M2_Path_SQL, item['image']):
                                    self.CM2_M1_M2_Path_the_one.append(C2_M2_Path_SQL)
                                    print(f"บันทึก C2_Model2_{j}.png")
                                re_supprt_index2_model2.append(j)

                        self.master_log_set.info(" detection from Camera 2 only. Data saved successfully")
                        self.db.insert(self.period, dateSQL, timeSQL, None, self.CM2_M1_M2_Path_the_one)
                        self.Notification_windown()
                        self.CM2_M1_M2_Path_the_one = []
              
                        self.contro_Save2 = False
                        print(f"ค่าของง self.CM2_Model1_list ลบแล้ว{self.CM2_Model1_list}")
                        self.Time_cam2_oj = None
                        if self.CM2_Model1_list:
                            for i in reversed(re_supprt_index2):
                                if i < len(self.CM2_Model1_list):
                                    del self.CM2_Model1_list[i]
                            for i in reversed(re_supprt_index2_model2):
                                if i < len(self.CM2_Model2_list):
                                    del self.CM2_Model2_list[i]
                    supper_SAVE = True
                    break  
                
    def start_cam(self):
        self.start_event = threading.Event()
        threading.Thread(target= self.Process_Cam01 , daemon=True).start()
        threading.Thread(target= self.Process_Cam02 , daemon=True).start()
        self.start_event.set()
    
        
    def destroyy(self):
        msg = CTkMessagebox(title="ยืนยันการออก", message="คุณแน่ใจว่าต้องการออกจากโปรแกรม?", 
                            icon="question", option_1="ยกเลิก", option_2="ตกลง")
        if msg.get() == "ตกลง":
            self.master_log_set.info("User closed the program")
            self.running = False
            self.cam01.release()
            self.cam02.release()
            self.out1.release()
            self.out2.release()
            cv2.destroyAllWindows()
            # ล้าง lists และ dictionaries
            self.CM1_Model1_list.clear()
            self.CM2_Model1_list.clear()
            self.CM1_Model2_list.clear()
            self.CM2_Model2_list.clear()
            self.CM1_M1_M2_Path.clear()
            self.CM2_M1_M2_Path.clear()

            self.im_SAVE_Id_model1_cm1.clear()
            self.im_save_CHECK_Id_model1_cm1.clear()
            self.im_SAVE_Id_model2_cm1.clear()
            self.im_save_CHECK_Id_model2_cm1.clear()
            self.im_SAVE_Id_model1_cm2.clear()
            self.im_save_CHECK_Id_model1_cm2.clear()
            self.im_SAVE_Id_model2_cm2.clear()
            self.im_save_CHECK_Id_model2_cm2.clear()
            self.id_Time_check_c1_m1.clear()
            self.id_Time_check_c1_m2.clear()
            self.id_Time_check_c2_m1.clear()
            self.id_Time_check_c2_m2.clear()
            self.track_color.clear()
            self.track_color2.clear()

            self.crop_img_m1_m1_del.clear()
            self.crop_img_m1_m2_del.clear()
            gc.collect()
            self.quit()
            sys.exit()
    
    def from_logout_(self):
        msg = CTkMessagebox(title="ยืนยันการออก", message="คุณแน่ใจว่าต้องการออกจากระบบ?", 
                            icon="question", option_1="ยกเลิก", option_2="ตกลง")
        if msg.get() == "ตกลง":
            try:
                self.master_log_set.info("User logout the program")
                self.running = False
                self.cam01.release()
                self.cam02.release()
                self.out1.release()
                self.out2.release()
                cv2.destroyAllWindows()
                # ล้าง lists และ dictionaries
                self.CM1_Model1_list.clear()
                self.CM2_Model1_list.clear()
                self.CM1_Model2_list.clear()
                self.CM2_Model2_list.clear()
                self.CM1_M1_M2_Path.clear()
                self.CM2_M1_M2_Path.clear()

                self.im_SAVE_Id_model1_cm1.clear()
                self.im_save_CHECK_Id_model1_cm1.clear()
                self.im_SAVE_Id_model2_cm1.clear()
                self.im_save_CHECK_Id_model2_cm1.clear()
                self.im_SAVE_Id_model1_cm2.clear()
                self.im_save_CHECK_Id_model1_cm2.clear()
                self.im_SAVE_Id_model2_cm2.clear()
                self.im_save_CHECK_Id_model2_cm2.clear()
                self.id_Time_check_c1_m1.clear()
                self.id_Time_check_c1_m2.clear()
                self.id_Time_check_c2_m1.clear()
                self.id_Time_check_c2_m2.clear()
                self.track_color.clear()
                self.track_color2.clear()
                self.crop_img_m1_m1_del.clear()
                self.crop_img_m1_m2_del.clear()
                gc.collect()
                self.after(100, self.quit)
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
        self.MasterLog_app = MasterLog()
        self.MasterLog_app.info("Application started")
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
    
