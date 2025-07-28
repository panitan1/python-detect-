def Main_Save_path(self, frame, ID_camala, timestamp, track_id):
    re_list_index = []
    tz = pytz.timezone('Asia/Bangkok')
    now = datetime.now(tz)
    today = now.strftime("%d-%m-%Y")
    year = now.year
    month_str = now.strftime("%Y-%m")
    hour = now.hour

    # กำหนดช่วงเวลา
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

    unique_id = uuid.uuid4().hex[:6]

    # บันทึกข้อมูลลงลิสต์ตาม ID_camala
    if frame is not None and frame.size > 0:  # ตรวจสอบว่า frame ไม่ว่าง
        if ID_camala == "CM1_Model1":
            self.Time_CM1_MO1 = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            self.CM1_Model1 = frame
            self.Track_idC1M1 = track_id
            self.CM1_Model1_list.append({
                'image': self.CM1_Model1,
                'timestamp': self.Time_CM1_MO1,
                'inx': self.Track_idC1M1
            })

        elif ID_camala == "CM2_Model1":
            self.Time_CM2_MO1 = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            self.CM2_Model1 = frame
            self.Track_idC2M1 = track_id
            self.CM2_Model1_list.append({
                'image': self.CM2_Model1,
                'timestamp': self.Time_CM2_MO1,
                'inx': self.Track_idC2M1
            })

        elif ID_camala == "CM1_Model2":
            self.Time_CM1_MO2 = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            self.CM1_Model2 = frame
            self.Track_idC1M2 = track_id
            self.CM1_Model2_list.append({
                'image': self.CM1_Model2,
                'timestamp': self.Time_CM1_MO2,
                'inx': self.Track_idC1M2
            })

        elif ID_camala == "CM2_Model2":
            self.Time_CM2_MO2 = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            self.CM2_Model2 = frame
            self.Track_idC2M2 = track_id
            self.CM2_Model2_list.append({
                'image': self.CM2_Model2,
                'timestamp': self.Time_CM2_MO2,
                'inx': self.Track_idC2M2
            })

    # ตรวจสอบและบันทึกเมื่อมีข้อมูลจากทั้งสองกล้อง
    if self.CM1_Model1_list and self.CM2_Model1_list:
        for i, item1 in enumerate(self.CM1_Model1_list[:]):
            time_obj1 = datetime.strptime(item1['timestamp'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=tz)
            idx_ID1 = item1['inx']
            matched = False

            # ตรวจสอบคู่กับ CM2_Model1
            for j, item2 in enumerate(self.CM2_Model1_list[:]):
                time_obj2 = datetime.strptime(item2['timestamp'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=tz)
                idx_ID2 = item2['inx']
                time_diff = abs((time_obj1 - time_obj2).total_seconds())
                print(f"Checking pair: CM1_Model1[{i}] vs CM2_Model1[{j}], time_diff: {time_diff} seconds")

                if time_diff <= 3:
                    print(f"Saving paired images: CM1_Model1[{i}] and CM2_Model1[{j}]")
                    dateSQL = time_obj1.strftime('%Y-%m-%d')
                    timeSQL = time_obj1.strftime('%H:%M:%S')
                    timePATH = time_obj1.strftime('%H-%M-%S')
                    full_save_dir = f"{save_dir}/{timePATH}"
                    os.makedirs(full_save_dir, exist_ok=True)

                    # บันทึกภาพจาก CM1_Model1
                    C1_M1_Path_SQL = f"{full_save_dir}/_C1_Model1_{i}_{unique_id}.png"
                    try:
                        if cv2.imwrite(C1_M1_Path_SQL, item1['image']):
                            self.CM1_M1_M2_Path.append(C1_M1_Path_SQL)
                            print(f"Saved C1_Model1_{i}.png")
                    except Exception as e:
                        print(f"Error saving C1_Model1_{i}.png: {e}")

                    # บันทึกภาพจาก CM2_Model1
                    C2_M1_Path_SQL = f"{full_save_dir}/_C2_Model1_{j}_{unique_id}.png"
                    try:
                        if cv2.imwrite(C2_M1_Path_SQL, item2['image']):
                            self.CM2_M1_M2_Path.append(C2_M1_Path_SQL)
                            print(f"Saved C2_Model1_{j}.png")
                    except Exception as e:
                        print(f"Error saving C2_Model1_{j}.png: {e}")

                    # บันทึกภาพจาก CM1_Model2 (ถ้ามี track_id ตรงกัน)
                    for k, item_cm1_m2 in enumerate(self.CM1_Model2_list[:]):
                        if item_cm1_m2['inx'] == idx_ID1:
                            C1_M2_Path_SQL = f"{full_save_dir}/_C_one_Model2_{k}_{unique_id}.png"
                            try:
                                if cv2.imwrite(C1_M2_Path_SQL, item_cm1_m2['image']):
                                    self.CM1_M1_M2_Path.append(C1_M2_Path_SQL)
                                    print(f"Saved C1_Model2_{k}.png")
                                self.CM1_Model2_list.remove(item_cm1_m2)
                            except Exception as e:
                                print(f"Error saving C1_Model2_{k}.png: {e}")

                    # บันทึกภาพจาก CM2_Model2 (ถ้ามี track_id ตรงกัน)
                    for k, item_cm2_m2 in enumerate(self.CM2_Model2_list[:]):
                        if item_cm2_m2['inx'] == idx_ID2:
                            C2_M2_Path_SQL = f"{full_save_dir}/_C_two_Model2_{k}_{unique_id}.png"
                            try:
                                if cv2.imwrite(C2_M2_Path_SQL, item_cm2_m2['image']):
                                    self.CM2_M1_M2_Path.append(C2_M2_Path_SQL)
                                    print(f"Saved C2_Model2_{k}.png")
                                self.CM2_Model2_list.remove(item_cm2_m2)
                            except Exception as e:
                                print(f"Error saving C2_Model2_{k}.png: {e}")

                    # บันทึกข้อมูลลงฐานข้อมูล
                    try:
                        self.db.insert(self.period, dateSQL, timeSQL, self.CM1_M1_M2_Path, self.CM2_M1_M2_Path)
                        self.Notification_windown()
                    except Exception as e:
                        print(f"Error inserting into database: {e}")

                    # เก็บ index ที่บันทึกแล้ว
                    re_list_index.append((i, j))
                    matched = True
                    break  # ออกจากลูป CM2_Model1_list เมื่อเจอคู่

            if matched:
                continue

            # ตรวจสอบว่าภาพเดี่ยวเกิน 4 วินาทีหรือไม่
            time_diff_single = abs((time_obj1 - now).total_seconds())
            if time_diff_single >= 4:
                print(f"Saving single image from CM1_Model1[{i}]")
                dateSQL = time_obj1.strftime('%Y-%m-%d')
                timeSQL = time_obj1.strftime('%H:%M:%S')
                timePATH = time_obj1.strftime('%H-%M-%S')
                full_save_dir = f"{save_dir}/{timePATH}"
                os.makedirs(full_save_dir, exist_ok=True)

                C1_M1_Path_SQL = f"{full_save_dir}/_C1_Model1_{i}_{unique_id}.png"
                try:
                    if cv2.imwrite(C1_M1_Path_SQL, item1['image']):
                        self.CM1_M1_M2_Path_the_one.append(C1_M1_Path_SQL)
                        print(f"Saved C1_Model1_{i}.png")
                except Exception as e:
                    print(f"Error saving C1_Model1_{i}.png: {e}")

                for k, item_cm1_m2 in enumerate(self.CM1_Model2_list[:]):
                    if item_cm1_m2['inx'] == idx_ID1:
                        C1_M2_Path_SQL = f"{full_save_dir}/_C_one_Model2_{k}_{unique_id}.png"
                        try:
                            if cv2.imwrite(C1_M2_Path_SQL, item_cm1_m2['image']):
                                self.CM1_M1_M2_Path_the_one.append(C1_M2_Path_SQL)
                                print(f"Saved C1_Model2_{k}.png")
                            self.CM1_Model2_list.remove(item_cm1_m2)
                        except Exception as e:
                            print(f"Error saving C1_Model2_{k}.png: {e}")

                try:
                    self.db.insert(self.period, dateSQL, timeSQL, self.CM1_M1_M2_Path_the_one, None)
                    self.Notification_windown()
                except Exception as e:
                    print(f"Error inserting into database: {e}")

                self.CM1_M1_M2_Path_the_one = []
                self.CM1_Model1_list.remove(item1)

        # ลบรายการที่บันทึกแล้ว (คู่)
        for i, j in reversed(re_list_index):
            del self.CM1_Model1_list[i]
            del self.CM2_Model1_list[j]

        # รีเซ็ตตัวแปร
        self.CM1_M1_M2_Path = []
        self.CM2_M1_M2_Path = []

    # ตรวจสอบภาพเดี่ยวจาก CM2_Model1 ที่ยังไม่ถูกจับคู่
    for i, item in enumerate(self.CM2_Model1_list[:]):
        time_obj2 = datetime.strptime(item['timestamp'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=tz)
        time_diff = abs((time_obj2 - now).total_seconds())
        if time_diff >= 4:
            print(f"Saving single image from CM2_Model1[{i}]")
            dateSQL = time_obj2.strftime('%Y-%m-%d')
            timeSQL = time_obj2.strftime('%H:%M:%S')
            timePATH = time_obj2.strftime('%H-%M-%S')
            full_save_dir = f"{save_dir}/{timePATH}"
            os.makedirs(full_save_dir, exist_ok=True)

            C2_M1_Path_SQL = f"{full_save_dir}/_C2_Model1_{i}_{unique_id}.png"
            try:
                if cv2.imwrite(C2_M1_Path_SQL, item['image']):
                    self.CM2_M1_M2_Path_the_one.append(C2_M1_Path_SQL)
                    print(f"Saved C2_Model1_{i}.png")
            except Exception as e:
                print(f"Error saving C2_Model1_{i}.png: {e}")

            for j, item2 in enumerate(self.CM2_Model2_list[:]):
                if item2['inx'] == item['inx']:
                    C2_M2_Path_SQL = f"{full_save_dir}/_C_two_Model2_{j}_{unique_id}.png"
                    try:
                        if cv2.imwrite(C2_M2_Path_SQL, item2['image']):
                            self.CM2_M1_M2_Path_the_one.append(C2_M2_Path_SQL)
                            print(f"Saved C2_Model2_{j}.png")
                        self.CM2_Model2_list.remove(item2)
                    except Exception as e:
                        print(f"Error saving C2_Model2_{j}.png: {e}")

            try:
                self.db.insert(self.period, dateSQL, timeSQL, None, self.CM2_M1_M2_Path_the_one)
                self.Notification_windown()
            except Exception as e:
                print(f"Error inserting into database: {e}")

            self.CM2_M1_M2_Path_the_one = []
            self.CM2_Model1_list.remove(item)

    # รีเซ็ตตัวแปรกล้อง
    self.CM1_Model1 = None
    self.CM2_Model1 = None
    self.CM1_Model2 = None
    self.CM2_Model2 = None