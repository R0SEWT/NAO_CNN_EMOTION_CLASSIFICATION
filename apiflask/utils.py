import cv2


def select_webcam(show_cameras_not_available = False):
    if show_cameras_not_available:
        check_available_cameras()
    else:
        print("Selecciona la cámara que quieres usar:")
        for i in range(5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                print(f"[{i}] Cámara disponible")
                cap.release()

def check_available_cameras():
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"[{i}] Cámara disponible")
            cap.release()
        else:
            print(f"[{i}] No disponible")



select_webcam(show_cameras_not_available=True)