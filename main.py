# -*- coding: utf-8 -*-

from naoqi import ALProxy
import urllib2, time, base64, json, vision_definitions, io
from PIL import Image
import StringIO
# ──────────────────────────────────────────────────────────────
# Configuración
# ──────────────────────────────────────────────────────────────
API_EMOCION = "http://192.168.18.5:5000/emocion"
#NAO_IP = "192.168.108.90"
NAO_IP = "127.0.0.1"
#PORT = 9559
#PUERTO = 49940
PORT = 54923

TESTING_ON_PC = True   # ← cambia a False para usar la cámara del NAO
PC_CAM_INDEX  = 2       # Índice de tu webcam en Windows/Linux

# ──────────────────────────────────────────────────────────────
# Proxies NAO (solo se necesitan para audio/movimientos)
# ──────────────────────────────────────────────────────────────
tts = ALProxy("ALTextToSpeech", NAO_IP, PORT)
motion = ALProxy("ALMotion", NAO_IP, PORT)
camProxy = ALProxy("ALVideoDevice", NAO_IP, PORT)
# time.sleep(1)
# motion.stiffnessInterpolation("Body", 0.0, 0.0)
# motion.stiffnessInterpolation("Body", 1.0, 1.0)

# ────────────────────────────
# Cámara del NAO
# ────────────────────────────
def capturar_imagen_nao():
    resolution  = vision_definitions.kVGA
    colorSpace  = vision_definitions.kRGBColorSpace
    fps         = 10
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

# ───────────────────────────────────────────
# Cámara del PC – OpenCV con preview a/s
# ───────────────────────────────────────────
def capturar_imagen_pc(*_):
    try:
        return urllib2.urlopen("http://127.0.0.1:8000/snapshot", timeout=3).read()
    except Exception as e:
        print("[PC] No pudo obtener snapshot:", e)
        return None

# ────────────────────────────
# API Flask
# ────────────────────────────
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
    

def volver_a_base():
    names = ["HeadYaw", "HeadPitch", "RShoulderPitch", "RElbowRoll", "RWristYaw",
             "LShoulderPitch", "LElbowRoll", "LWristYaw"]
    angles = [0.0, 0.0, 1.5, 0.0, 0.0,
              1.5, 0.0, 0.0]
    times = [1.0] * len(angles)
    motion.angleInterpolation(names, angles, times, True)

def gesto_saludo():
    motion.stiffnessInterpolation("Body", 1.0, 1.0)
    names = ["RShoulderPitch", "RElbowYaw", "RElbowRoll", "RWristYaw"]
    angles = [1.3, 1.5, 0.5, 1.0]
    times = [1.0] * len(angles)
    motion.angleInterpolation(names, angles, times, True)
    # Simular movimiento de saludo
    for _ in range(2):
        motion.angleInterpolation("RWristYaw", 0.0, 0.5, True)
        motion.angleInterpolation("RWristYaw", 1.0, 0.5, True)
    volver_a_base()

def gesto_sorpresa():
    motion.stiffnessInterpolation("Body", 1.0, 1.0)
    names = ["RShoulderPitch", "RElbowRoll", "LShoulderPitch", "LElbowRoll"]
    angles = [0.5, 1.0, 0.5, -1.0]
    times = [1.0] * len(angles)
    motion.angleInterpolation(names, angles, times, True)
    time.sleep(1)
    volver_a_base()

def gesto_brazos_cruzados():
    motion.stiffnessInterpolation("Body", 1.0, 1.0)
    names = ["RShoulderPitch", "RElbowRoll", "LShoulderPitch", "LElbowRoll"]
    angles = [1.2, 1.2, 1.2, -1.2]
    times = [1.0] * len(angles)
    motion.angleInterpolation(names, angles, times, True)
    time.sleep(1)
    volver_a_base()

    

def gesto_brazo_derecho_arriba():
    motion.stiffnessInterpolation("Body", 1.0, 1.0)
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
    tts.say("How are you?")

def escena_piola():
    tts.say("Hmm... Let me take a good look at you.")
    
    # Escaneo dramatico con la cabeza
    motion.angleInterpolation("HeadYaw", 1.0, 0.7, True)
    motion.angleInterpolation("HeadYaw", -1.0, 0.7, True)
    motion.angleInterpolation("HeadYaw", 0.0, 0.5, True)

    tts.say("Interesting... very interesting.")

    # Brazos cruzados + leve movimiento de cabeza hacia abajo (juicio)
    gesto_brazos_cruzados()

    tts.say("I have seen many faces...")
    time.sleep(0.3)
    tts.say("But yours... it's definitely one of them.")
    



def reaccionar(emocion):

    # ("angry", "sad", "fear", "disgust"):
    if emocion == "happy":
        tts.say("You are happy")
        time.sleep(1)
        tts.say("Happy to see you!")
        time.sleep(1)
        tts.say("Im chilling with you hadshaskdhkaskjdashkdsbcx")
        gesto_saludo()
        time.sleep(0.3)

        gesto_brazo_derecho_arriba()


    elif emocion == "angry":
        tts.say("You seem angry")
        gesto_brazos_cruzados()

    elif emocion == "fear":
        tts.say("You look scared")
        gesto_sorpresa()

    elif emocion == "disgust":
        tts.say("I see you are disgusted")
        gesto_confundido()
    elif emocion == "neutral":
        tts.say("You look neutral")

    else:
        tts.say("I see you, but I don't know how you feel")
        tts.say("No se como te sientes asjdahsdjahsdj")
        tts.say("you dont have face hahahahahahhaha")
        motion.angleInterpolation("HeadYaw", 0.0, 0.5, True)
        escena_piola()


if __name__ == "__main__":
    motion.wakeUp()
    motion.angleInterpolation("HeadPitch", 0.1, 0.4, True)
    escena()
    time.sleep(0.5)

    # Elegir fuente de imagen según bandera
    if TESTING_ON_PC:
        img_base64 = capturar_imagen_pc(PC_CAM_INDEX)
    else:
        img_base64 = capturar_imagen_nao()

    if img_base64:
        emocion = enviar_imagen_y_recibir_emocion(img_base64)
    else:
        emocion = "no_face"

    print("Emocion detectada:", emocion)
    reaccionar(emocion)
    # motion.rest()