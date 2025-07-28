import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print("🎉 Connected to server!")
    sio.emit("message", "สวัสดีจากไคลเอนต์!")  # ส่งข้อความไปเซิร์ฟเวอร์

@sio.on("message")
def receive_message(data):
    print(f"📩 Message from server: {data}")
    
@sio.on("chat")
def receive_chat(data):
    print(f"💬 แชท: {data}")

sio.connect("http://localhost:3333" , transports=['websocket'])
sio.wait()
while True:
    time.sleep(3)
    sio.emit("chat" , "ทดสอบวินาทีส่ง")