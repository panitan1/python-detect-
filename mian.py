import cv2
import numpy as np
from ultralytics import YOLO
from datetime import datetime
import pytz
import os
import os
from server_mysql.mysql_server import  insert 

model_1 = YOLO('model/yolov8n.pt').cuda()  # YOLOv8 nano
model_2 = YOLO('model/best.pt').cuda()     # Custom trained model or another model

# Video paths
path1 = "vidio/x1.mp4"
path2 = "vidio/x1.mp4"


tz = pytz.timezone('Asia/Bangkok')
current_time = datetime.now(tz)
target_time = datetime.now(tz)


os.makedirs("Save_detection", exist_ok=True)

today = datetime.now(tz).strftime("%d-%m-%Y")

parts_day = datetime.now(tz).hour

if 6 <= parts_day <=11:
    period = "Morning"
    os.makedirs(f"Save_detection/{today}/Morning", exist_ok=True) 
    print("Morning")
elif 12 <= parts_day <= 15:
    period = "Afternoon"
    os.makedirs(f"Save_detection/{today}/Afternoon", exist_ok=True) 
    print("Afternoon")
elif 16 <= parts_day <= 19:
    period = "Evening"
    os.makedirs(f"Save_detection/{today}/Evening", exist_ok=True)
    print("Evening")
else:
    period = "Night"
    os.makedirs(f"Save_detection/{today}/Night", exist_ok=True)
    print("Night")

     
        
chack_save = 0

def Cm1():
    global current_time, target_time, chack_save , saved_ids , saved_ids2 ,tz
    cap1 = cv2.VideoCapture(path1)
    cap2 = cv2.VideoCapture(path2)
    print("เปิดวิดีโอ qwe2.mp4 และ qwe33.mp4")
    
    if not cap1.isOpened() or not cap2.isOpened():
        print("ไม่สามารถเปิดวิดีโอ qwe2.mp4 หรือ qwe33.mp4 ได้")
        return
    
    while True:
        ret1, frame1 = cap1.read() 
        ret2, frame2 = cap2.read()  
        
        if not ret1 or not ret2:
            print("สิ้นสุดวิดีโอ")
            break
        
        # กล้อง 1: Model 1 และ Model 2
        cm1mo1 = model_1.track(frame1, persist=False, tracker="botsort.yaml", classes=[3], conf=0.8)
        frame_cm1mo1 = cm1mo1[0].plot() 
        cm1mo2 = model_2.track(frame1, persist=False, tracker="botsort.yaml", classes=[0])
        frame_cm1mo2 = cm1mo2[0].plot() 
        
        results_idx_c1_m1 = cm1mo1[0]
        track_id_c1_m1 = results_idx_c1_m1.boxes.id
        track_bbox_c1_m1 = results_idx_c1_m1.boxes.xyxy
        
        # เก็บ cropped images ของทุกวัตถุในลิสต์
        corp_list_c1_m1 = []
        for box_c1_m1 in track_bbox_c1_m1:
            x1, y1, x2, y2 = box_c1_m1
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            corp_b1_c1_m1 = frame1[y1:y2, x1:x2]
            corp_list_c1_m1.append(corp_b1_c1_m1)
            
        cam1_mo1 = []
        if track_id_c1_m1 is not None:
            current_time = datetime.now(tz)
            for track_id_c1_m1_for in track_id_c1_m1:
                cam1_mo1.append(track_id_c1_m1_for)
                print(f"🤩CM@M1 = {current_time.second}")
                print(f"🤩🤩🤩{cam1_mo1}")
                print(f"🤩CM@M1🤩CM@M1🤩CM@M1  {track_id_c1_m1}")
        
        results_idx_c1_m2 = cm1mo2[0]
        track_id_c1_m2 = results_idx_c1_m2.boxes.id
        track_bbox_c1_m2 = results_idx_c1_m2.boxes.xyxy
        
        corp_list_c1_m2 = []
        for box_c1_m2 in track_bbox_c1_m2:
            x1, y1, x2, y2 = box_c1_m2
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            corp_b1_c1_m2 = frame1[y1:y2, x1:x2]
            corp_list_c1_m2.append(corp_b1_c1_m2)
        
        cam1_mo2 = []
        if track_id_c1_m2 is not None:
            target_time = datetime.now(tz)
            for track_id_c1_m2_for in track_id_c1_m2:
                cam1_mo2.append(track_id_c1_m2_for.item())
                print(f"🤩CM@M2 = {target_time.second}")
                print(f"🤩🤩🤩{cam1_mo2}")
                print(f"🤩CM@M1🤩CM@M1🤩CM@M1  {track_id_c1_m2}")
            
        sum_frame1 = cv2.addWeighted(frame_cm1mo1, 0.5, frame_cm1mo2, 0.5, 0)
        cv2.imshow("Camera 1 - Combined YOLOv8 & Best", sum_frame1)
        
        # กล้อง 2: Model 1 และ Model 2
        cm2mo1 = model_1.track(frame2, persist=False, classes=[3], tracker="botsort.yaml", conf=0.8)
        frame_cm2mo1 = cm2mo1[0].plot() 
        cm2mo2 = model_2.track(frame2, persist=False, classes=[0], tracker="botsort.yaml")
        frame_cm2mo2 = cm2mo2[0].plot()    
        
        results_idx_c2_m1 = cm2mo1[0]
        
        track_id_c2_m1 = results_idx_c2_m1.boxes.id
        cam2_mo1 = []
        if track_id_c2_m1 is not None:
            target_time = datetime.now(tz)
            for track_id_c2_m1_for in track_id_c2_m1:
                cam2_mo1.append(track_id_c2_m1_for)
                print(f"😎CM@M2 = {target_time.second}")
                print(f"cam2_mo1:::😎😎😎{cam2_mo1}")
                print(f"🤩CM@M1🤩CM@M1🤩CM@M1  {track_id_c2_m1}")
                
                
        track_bbox_c2_m1 = results_idx_c2_m1.boxes.xyxy
        corp_list_c2_m1 = []
        for box_c2_m1 in track_bbox_c2_m1:
            x1, y1, x2, y2 = box_c2_m1
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            corp_b1_c2_m1 = frame2[y1:y2, x1:x2]
            corp_list_c2_m1.append(corp_b1_c2_m1)
        
        
        
        results_idx_c2_m2 = cm2mo2[0]
        track_id_c2_m2 = results_idx_c2_m2.boxes.id
        
        cam2_mo2 = []
        if track_id_c2_m2 is not None:
            target_time = datetime.now(tz)
            for track_id_c2_m2_for in track_id_c2_m2:
                cam2_mo2.append(track_id_c2_m2_for.item())
                print(f"😎CM@M2 = {target_time.second}")
                print(f"😎😎😎{cam2_mo2}")
                print(f"🤩CM@M1🤩CM@M1🤩CM@M1  {track_id_c2_m2}")
                
                
        track_bbox_c2_m2 = results_idx_c2_m2.boxes.xyxy
        
        corp_list_c2_m2 = []
        for box_c2_m2 in track_bbox_c2_m2:
            x1, y1, x2, y2 = box_c2_m2
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            corp_b1_c2_m2 = frame2[y1:y2, x1:x2]
            corp_list_c2_m2.append(corp_b1_c2_m2)
        
                
        if current_time is not None and target_time is not None:
            # if target_time.second == current_time.second:
                if set(cam2_mo1) == set(cam2_mo1) and cam1_mo1 and cam2_mo1:
                    if chack_save == 0:
                        Save_in_tee = f"Save_detection/{today}/{period}/{target_time.strftime('Date_%d_%m_%Y_Time_%H.%M')}"
                        os.makedirs(Save_in_tee, exist_ok=True)
                        print(f"OKKK - บันทึกที่ {Save_in_tee}")
                        
                        list_path_img1 = []
                        list_path_img2 = []
                        for i, corp_img in enumerate(corp_list_c1_m1):
                            path_img = f"{Save_in_tee}/object_C1_{i}_{target_time.strftime('Date_%d_%m_%Y_Time_%H.%M')}.jpg"
                            cv2.imwrite(path_img , corp_img)
                            list_path_img1.append(path_img)
                     

                        for i, corp_img in enumerate(corp_list_c1_m2):
                            path_img = f"{Save_in_tee}/object_C2_{i}_{target_time.strftime('Date_%d_%m_%Y_Time_%H.%M')}.jpg"
                            cv2.imwrite(path_img , corp_img)
                            list_path_img1.append(path_img)
                     
                            
                        for i, corp_img in enumerate(corp_list_c2_m1):
                            path_img = f"{Save_in_tee}/object_C3_{i}_{target_time.strftime('Date_%d_%m_%Y_Time_%H.%M')}.jpg"
                            cv2.imwrite(path_img , corp_img)
                            list_path_img2.append(path_img)
                          
        
                        for i, corp_img in enumerate(corp_list_c2_m2):
                            path_img = f"{Save_in_tee}/object_C4_{i}_{target_time.strftime('Date_%d_%m_%Y_Time_%H.%M')}.jpg"
                            cv2.imwrite(path_img , corp_img)
                            list_path_img2.append(path_img)
                            

                        chack_save = 1
                        insert(period,target_time.today(),target_time.strftime("%H:%M:%S"),list_path_img1, list_path_img2 )
                    else:
                        
                        print("บันทึกไปแล้วนะลืมแล้วเหรอ")
                        
                elif not cam2_mo1 and not cam1_mo1:
                    chack_save = 0
                    print("🔄 Reset chack_save เพราะไม่มี ID อยู่ในเฟรม")
        
        sum_frame2 = cv2.addWeighted(frame_cm2mo1, 0.5, frame_cm2mo2, 0.5, 0)
        cv2.imshow("Camera 2 - Combined YOLOv8 & Best", sum_frame2)
        
        if cv2.waitKey(1) & 0xFF == 27:  
            break

    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

# เรียกฟังก์ชัน
Cm1()