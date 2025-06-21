# webcam_server.py  (Python 3.x)
import base64, io, sys, cv2, time
from PIL import Image
from flask import Flask, Response, jsonify, render_template_string

app = Flask(__name__)
cap_index = 0
cap = cv2.VideoCapture(cap_index)
last_frame = None

HTML_PAGE = """
<!doctype html>
<title>Webcam</title>
<h2>Webcam – índice {{idx}}</h2>
<p>Presiona <b>c</b> en la ventana OpenCV para cambiar de cámara.</p>
<img src="/mjpg" width="640">
"""

# ────────────────── Helpers ──────────────────
def grab_frame():
    global last_frame
    if not cap.isOpened():
        return None
    ret, frame = cap.read()
    if not ret:
        return None
    last_frame = frame
    return frame

def jpg_bytes(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

# ────────────────── Routes ──────────────────
@app.route("/")
def index():
    return render_template_string(HTML_PAGE, idx=cap_index)

@app.route("/snapshot")
def snapshot():
    frame = grab_frame()
    if frame is None:
        return "No frame", 503
    return base64.b64encode(jpg_bytes(frame)), 200

@app.route("/mjpg")
def mjpg():
    def gen():
        while True:
            frame = grab_frame()
            if frame is None:
                time.sleep(0.1)
                continue
            jpg = jpg_bytes(frame)
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + jpg + b"\r\n")
    return Response(gen(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

# ────────────────── OpenCV preview (tecla c) ──────────────────
def preview_thread():
    global cap, cap_index
    while True:
        if not cap.isOpened():
            time.sleep(0.1)
            continue
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Webcam server – c cambia cam", frame)
        key = cv2.waitKey(1) & 0xFF
        if key in (ord('c'), ord('C')):
            cap_index = (cap_index + 1) % 5
            cap.release()
            cap = cv2.VideoCapture(cap_index)

# ────────────────── Main ──────────────────
if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print("[webcam_server] Ejecutando en http://127.0.0.1:{} …".format(port))
    import threading
    threading.Thread(target=preview_thread, daemon=True).start()
    app.run(host="0.0.0.0", port=port)
