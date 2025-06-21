# -*- coding: utf-8 -*-
"""
perception.py – Captura y detección de emoción
"""
from __future__ import print_function
import base64, json, urllib2, time
from config import TESTING_ON_PC, PC_CAM_INDEX, API_EMOCION_URL, NAO_IP, PORT

try:
    from naoqi import ALProxy
except ImportError:
    ALProxy = None

# ───── Captura de imagen ───────────────────────────────────────────────
def _capture_nao():
    cam = ALProxy("ALVideoDevice", NAO_IP, PORT)
    name = cam.subscribeCamera("cam", 0, 2, 11, 5)  # 640×480 RGB
    time.sleep(0.1)
    img = cam.getImageRemote(name)
    cam.unsubscribe(name)
    if img is None:
        return None
    return base64.b64encode(bytearray(img[6]))

def _capture_pc():
    # pide al micro-servicio webcam_server.py /snapshot (opción A)
    url = "http://127.0.0.1:8000/snapshot"
    try:
        return urllib2.urlopen(url, timeout=3).read()
    except Exception as e:
        print("[PC] snapshot error:", e)
        return None

def capture_frame_b64():
    if TESTING_ON_PC:
        return _capture_pc()
    else:
        return _capture_nao()

# ───── Llamada a la API de emoción ─────────────────────────────────────
def detect_emotion(b64_img):
    req = urllib2.Request(API_EMOCION_URL,
                          json.dumps({"image_base64": b64_img}),
                          {"Content-Type": "application/json"})
    try:
        return urllib2.urlopen(req, timeout=5).read()
    except Exception as e:
        print("[API] error:", e)
        return "no_face"
