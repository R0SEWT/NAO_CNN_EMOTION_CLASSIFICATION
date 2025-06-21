# -*- coding: utf-8 -*-
from flask import Flask, request
import base64
import numpy as np
import cv2
import datetime
import os

from detectar_emocion import detectar_emocion_desde_array

app = Flask(__name__)
LOG_DIR = "apiflask/logs_img"

# Asegura que exista la carpeta de logs
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

@app.route("/emocion", methods=["POST"])
def emocion():
    data = request.get_json()
    if not data or "image_base64" not in data:
        return "no_image"

    try:
        # Decodificar imagen
        img_bytes = base64.b64decode(data["image_base64"])
        np_arr = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Clasificar emoción
        emocion = detectar_emocion_desde_array(img)

        # Guardar log
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{LOG_DIR}/{timestamp}_{emocion}.jpg"
        cv2.imwrite(filename, img)
        print(f"[{timestamp}] Emoción: {emocion} -> guardada en {filename}")

        # Normalizar emoción para NAO
        if emocion in ("happy"):
            return "happy"
        elif emocion in ("angry", "sad", "fear", "disgust"):
            return emocion
        elif emocion in ("surprise", "neutral"):
            return "neutral"
        return "no_face"

    except Exception as e:
        print("Error procesando imagen:", e)
        return "error"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
