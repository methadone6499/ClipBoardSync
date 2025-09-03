import pyperclip
import requests
import threading
import time
import base64
from io import BytesIO
from PIL import Image
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

PEER_IP = os.getenv("PC_IP")

last_clipboard = None
#ensures there's no race condition
updating = False

@app.route("/update", methods=["POST"])
def update_clipboard():
    global last_clipboard, updating
    data = request.json
    updating = True

    if data["type"] == "text":
        pyperclip.copy(data["data"])
        last_clipboard = data["data"]

    elif data["type"] == "image":
        img_data = base64.b64decode(data["data"])
        img = Image.open(BytesIO(img_data))
        img.show()
        buf = BytesIO
        img.save(buf, format="PNG")
        pyperclip.copy("[[IMAGE]]")
        last_clipboard = "[[IMAGE]]"
    
    updating = False
    return jsonify({"status": "ok"})

def watch_clipboard():
    global last_clipboard, updating
    while True:
        if not updating:
            current = pyperclip.paste()
            if current != last_clipboard:
                last_clipboard = current
                try:
                    requests.post(f"http://{PEER_IP}/update",
                                  json={"type": "text", "data":  current},
                                  timeout=2)
                except:
                    pass
        
        time.sleep(0.5)

def start():
    print(PEER_IP)
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)).start()
    threading.Thread(target=watch_clipboard,  daemon=True).start()

if __name__ == "__main__":
    print(PEER_IP)
    print("dhfsodifsd")
    start()