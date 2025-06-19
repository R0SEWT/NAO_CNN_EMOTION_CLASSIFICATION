# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import cv2

# ──────────────────────────────────────────────────────────────
#  Utilidades básicas de webcam
# ──────────────────────────────────────────────────────────────
def list_webcams(max_cams=5):
    """Devuelve una lista con los índices de cámaras disponibles."""
    cams = []
    for i in range(max_cams):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cams.append(i)
            cap.release()
    return cams


def select_webcam(max_cams=5):
    """Muestra las cámaras detectadas y devuelve el índice elegido."""
    cams = list_webcams(max_cams)
    if not cams:
        print("No se detectaron cámaras.")
        return None

    print("Cámaras disponibles:", ", ".join("[{}]".format(c) for c in cams))
    try:  # raw_input para Py2, input para Py3
        sel = int(raw_input("Número de cámara (Enter = 0): ") or cams[0])
    except NameError:
        sel = int(input("Número de cámara (Enter = 0): ") or cams[0])

    return sel if sel in cams else None


def stream_webcam(cam_index=0, window_name="Webcam (q/Esc para salir)"):
    """Abre una ventana con el feed en tiempo real de la cámara elegida."""
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        print("No se pudo abrir la cámara {}".format(cam_index))
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF in (ord('q'), 27):  # 27 = Esc
            break

    cap.release()
    cv2.destroyAllWindows()


# Ejecución directa para test rápido
if __name__ == "__main__":
    cam = select_webcam()
    if cam is not None:
        stream_webcam(cam)
