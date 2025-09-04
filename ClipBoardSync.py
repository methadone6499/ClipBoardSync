import pyperclip
import requests
import threading
import time
import base64
from io import BytesIO
from PIL import Image
from PIL import ImageGrab
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import win32clipboard

app = Flask(__name__)

load_dotenv()

PEER_IP = os.getenv("PC_IP")

last_clipboard = None
last_clipboard_img = None
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
        buf = BytesIO()
        img.convert("RGB").save(buf, "BMP")
        imgfr = buf.getvalue()[14:]
        buf.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, imgfr)
        win32clipboard.CloseClipboard()
    
    updating = False
    return jsonify({"status": "ok"})

def watch_clipboard():
    global last_clipboard, updating, last_clipboard_img
    while True:
        if not updating:
            current = pyperclip.paste()
            current_image = ImageGrab.grabclipboard()
            if (current_image != last_clipboard_img)  & (current_image is not None):
                print("sdfhsiod")
                last_clipboard = current
                last_clipboard_img = current_image
                buffer = BytesIO()
                current_image.save(buffer, format="PNG") # failing point because copying text would leave current_image as a None object
                img_bytes = buffer.getvalue()

                # Convert to base64 string
                img_b64 = base64.b64encode(img_bytes).decode("utf-8")
                try:
                    requests.post(f"http://{PEER_IP}/update",
                                  json={"type": "image", "data":  img_b64},
                                  timeout=2)
                except:
                    pass
                
            if (current != last_clipboard) & (current is not None):
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