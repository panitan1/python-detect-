import json
import mysql.connector
import threading
<<<<<<< HEAD

class datasql:
    def __init__(self):
=======
from master_log.master_log import MasterLog

class datasql:
    def __init__(self):
        self.master_log_set = MasterLog()
>>>>>>> 7aa7b1c (Initial commit)
        self.lock = threading.Lock()  # 🔒 เพิ่ม Lock เพื่อให้ thread เขียนข้อมูลได้ปลอดภัย
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="data_detect",
            connection_timeout=5,
            pool_size=5
        )
<<<<<<< HEAD
        print("✅ Database connected:", self.mydb)
=======
        self.master_log_set.info(" Database connected")
        print(" Database connected:", self.mydb)
>>>>>>> 7aa7b1c (Initial commit)

    def insert(self, period, Dete_detect, Time_detect, cm1_dt, cm2_dt 	):
        with self.lock:  # 🔒 ป้องกันหลาย thread เขียนชนกัน
            try:
                cursor = self.mydb.cursor()
                query = "INSERT INTO detections (Period, Dete_detect, Time_detect, cm1_dt, cm2_dt ) VALUES (%s, %s, %s, %s, %s )"
                values = (period, Dete_detect, Time_detect, json.dumps(cm1_dt), json.dumps(cm2_dt) )
                cursor.execute(query, values)
                self.mydb.commit()
                print("✅ Data inserted successfully")

            except mysql.connector.Error as err:
<<<<<<< HEAD
=======
                self.master_log_set.error("Database error: {err}")
>>>>>>> 7aa7b1c (Initial commit)
                print(f"❌ Database error: {err}")

            finally:
                cursor.close()
