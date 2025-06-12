import cv2
import numpy as np
from keras.models import load_model
import os

# Evita errores por entorno gráfico al usar OpenCV en headless
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

# Cargar modelo y etiquetas
model = load_model("modelo_emocion.h5", compile=False)  # Evita problemas con versiones de Keras
emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

# Clasificador Haar de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detectar_emocion_desde_array(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) == 0:
        return "no_face"

    # Usamos solo la primera cara detectada
    (x, y, w, h) = faces[0]
    face = gray[y:y+h, x:x+w]
    face = cv2.resize(face, (64, 64)).astype('float32') / 255.0
    face = np.expand_dims(face, axis=(0, -1))

    preds = model.predict(face)
    return emotions[np.argmax(preds)]

# Función opcional para testear con webcam (solo en desarrollo local)
def detectar_emocion(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        return "no_cam"

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return "no_frame"

    return detectar_emocion_desde_array(frame)

if __name__ == "__main__":
    emocion = detectar_emocion()
    print("Emoción detectada:", emocion)
