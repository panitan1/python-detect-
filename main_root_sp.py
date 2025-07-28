import psutil
import GPUtil
import time
from IPython.display import clear_output

while True:
    clear_output(wait=True)  # เคลียร์หน้าจอก่อนแสดงใหม่
    print(f"CPU Usage: {psutil.cpu_percent()}%")
    print(f"RAM Usage: {psutil.virtual_memory().percent}%")
    
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        print(f"GPU Usage: {gpu.load*100}% | GPU Memory: {gpu.memoryUsed}/{gpu.memoryTotal} MB")
        print("========================================================================================")
    
    time.sleep(1)  # อัปเดตทุก 1 วินาที