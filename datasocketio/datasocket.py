import time
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("connect")
def handle_connect():
    print("✅ Client connected")
    socketio.emit("message", "Hello from server!")  # ส่งข้อความไปให้ไคลเอนต์

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
