import cv2
import numpy as np
from keras.models import load_model
import os

os.environ['QT_QPA_PLATFORM'] = 'offscreen'

# Cargar modelo y etiquetas
model = load_model("modelo_emocion.h5", compile=False) #sin compilación para evitar problemas de compatibilidad

emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

# Clasificador de rostros Haar
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detectar_emocion(camera_index=2):
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return "no_cam"
    
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return "no frame"

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        # cv2.imshow("Frame", frame)
        # cv2.waitKey(2000)
        # cv2.destroyAllWindows()
        return "no_face"

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (64, 64))
        face = face.astype('float32') / 255.0
        face = np.expand_dims(face, axis=0)
        face = np.expand_dims(face, axis=-1)
        
        # #debug
        # cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # cv2.imshow("Cara detectada", frame)
        # cv2.waitKey(2000)
        # cv2.destroyAllWindows()


        preds = model.predict(face)
        return emotions[np.argmax(preds)]

    return "no_face"


if __name__ == "__main__":
    emocion = detectar_emocion()
    print("Emoción detectada:", emocion)

