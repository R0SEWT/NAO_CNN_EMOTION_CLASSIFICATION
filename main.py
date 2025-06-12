# main.py (Python 2.7)

from naoqi import ALProxy
import urllib2
import time
import base64
import json
import vision_definitions
from PIL import Image
import StringIO

NAO_IP = "macloli-Air.Local"
PORT = 9559
API_EMOCION = "http://<IP_DE_TU_LAPTOP>:5000/emocion"  # cambia esto

tts = ALProxy("ALTextToSpeech", NAO_IP, PORT)
motion = ALProxy("ALMotion", NAO_IP, PORT)
camProxy = ALProxy("ALVideoDevice", NAO_IP, PORT)

motion.stiffnessInterpolation("Body", 1.0, 1.0)

def capturar_imagen():
    resolution = vision_definitions.kVGA
    colorSpace = vision_definitions.kRGBColorSpace
    fps = 10
    client_name = "nao_emotion_client"

    videoClient = camProxy.subscribeCamera(client_name, 0, resolution, colorSpace, fps)
    time.sleep(0.2)
    naoImage = camProxy.getImageRemote(videoClient)
    camProxy.unsubscribe(videoClient)

    if naoImage is None:
        return None

    width, height, array = naoImage[0], naoImage[1], naoImage[6]
    img = Image.frombytes("RGB", (width, height), array)

    buffer = StringIO.StringIO()
    img.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue())

def enviar_imagen_y_recibir_emocion(encoded_img):
    req = urllib2.Request(API_EMOCION)
    req.add_header('Content-Type', 'application/json')
    data = json.dumps({"image_base64": encoded_img})
    try:
        response = urllib2.urlopen(req, data, timeout=10)
        return response.read()
    except Exception as e:
        print("Error al enviar imagen:", e)
        return "no_face"

def gesto_brazo_derecho_arriba():
    names = ["RShoulderPitch", "RElbowRoll", "RWristYaw"]
    angles = [0.5, 1.0, 1.0]
    times = [1.0] * len(angles)
    motion.angleInterpolation(names, angles, times, True)

def gesto_confundido():
    names = ["HeadYaw", "HeadPitch"]
    angles = [[0.5, -0.5, 0.5], [0.3, 0.3, 0.3]]
    times = [[1.0, 2.0, 3.0], [1.0, 2.0, 3.0]]
    motion.angleInterpolation(names, angles, times, True)

def escena():
    tts.say("Como te sientes")

def reaccionar(emocion):
    if emocion == "happy":
        tts.say("Me alegra que estes feliz")
        gesto_brazo_derecho_arriba()
    elif emocion == "confused":
        tts.say("Parece que no entendiste bien")
        gesto_confundido()
        time.sleep(1)
        escena()
    else:
        tts.say("No te veo bien")

if __name__ == "__main__":
    motion.wakeUp()
    escena()
    time.sleep(1)
    img_base64 = capturar_imagen()
    if img_base64:
        emocion = enviar_imagen_y_recibir_emocion(img_base64)
    else:
        emocion = "no_face"

    print("Emocion detectada:", emocion)
    reaccionar(emocion)
