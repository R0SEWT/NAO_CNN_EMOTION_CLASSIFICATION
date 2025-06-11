from naoqi import ALProxy
import urllib2
import time
import base64
import json


# Cambia por la IP de tu PC con el servidor Flask
API_EMOCION = "http://172.25.88.231:5000/emocion"
NAO_IP = "192.168.108.36"


tts = ALProxy("ALTextToSpeech", NAO_IP, 9559)

motion = ALProxy("ALMotion", NAO_IP, 9559)
motion.stiffnessInterpolation("Body", 0.0, 1.0)
motion.stiffnessInterpolation("Body", 1.0, 1.0)  # Activa todos los motores



def capturar_imagen():
    camProxy = ALProxy("ALVideoDevice", NAO_IP, 9559)
    resolution = 2  # 640x480
    colorSpace = 11  # RGB
    fps = 10

    nameId = camProxy.subscribe("nao_emotion_cam", resolution, colorSpace, fps)
    naoImage = camProxy.getImageRemote(nameId)
    camProxy.unsubscribe(nameId)

    if naoImage is None:
        return None

    width = naoImage[0]
    height = naoImage[1]
    array = naoImage[6]

    # Convertir a base64
    img_data = bytearray(array)
    return base64.b64encode(img_data)


def obtener_emocion():
    try:
        res = urllib2.urlopen(API_EMOCION, timeout=5)
        return res.read()
    except:
        return "no_face"

def gesto_brazo_derecho_arriba():
    names = ["RShoulderPitch", "RElbowRoll", "RWristYaw"]
    angles = [0.5, 1.0, 1.0]
    times = [1.0] * len(angles)
    isAbsolute = True
    motion.angleInterpolation(names, angles, times, isAbsolute)

def gesto_confundido():
    names = ["HeadYaw", "HeadPitch"]
    angles = [[0.5, -0.5, 0.5], [0.3, 0.3, 0.3]]
    times = [[1.0, 2.0, 3.0], [1.0, 2.0, 3.0]]
    isAbsolute = True
    motion.angleInterpolation(names, angles, times, isAbsolute)

def escena():
    tts.say("question")
    #tts.say("Si alguien esta triste, puedes preguntarle si se encuentra bien.")


def enviar_imagen_y_recibir_emocion(encoded_img):
    req = urllib2.Request(API_EMOCION)
    req.add_header('Content-Type', 'application/json')
    data = json.dumps({ "image_base64": encoded_img })
    try:
        response = urllib2.urlopen(req, data)
        return response.read()
    except Exception as e:
        print("Error al enviar imagen:", e)
        return "no_face"



def reaccionar(emocion):
    if emocion == "happy":
        #tts.say("Excelente! Me alegra que lo hayas entendido.")
        tts.say("happy")
        gesto_brazo_derecho_arriba()
    elif emocion == "confused":
        tts.say("Confused")
        #tts.say("Mmm, no fue tan claro. Te lo explico otra vez.")
        gesto_confundido()
        time.sleep(1)
        escena()  # Repetir la escena
    else:
        # tts.say("No pude verte bien. Puedes acercarte un poco?")
        tts.say("Where are you?")

if __name__ == "__main__":
    motion.wakeUp()
    escena()
    time.sleep(1)
    emocion = obtener_emocion()
    print("Emocion detectada:", emocion)
    reaccionar(emocion)



# tts = ALProxy("ALTextToSpeech", NAO_IP, 9559)
# motion = ALProxy("ALMotion", NAO_IP, 9559)

# def obtener_emocion():
#     try:
#         res = urllib2.urlopen(API_EMOCION, timeout=5)
#         return res.read()
#     except:
#         return "no_face"

# def gesto_brazo_derecho_arriba():
#     names = ["RShoulderPitch", "RElbowRoll", "RWristYaw"]
#     angles = [0.5, 1.0, 1.0]
#     times = [1.0] * len(angles)
#     isAbsolute = True
#     motion.angleInterpolation(names, angles, times, isAbsolute)

# def gesto_confundido():
#     names = ["HeadYaw", "HeadPitch"]
#     angles = [[0.5, -0.5, 0.5], [0.3, 0.3, 0.3]]
#     times = [[1.0, 2.0, 3.0], [1.0, 2.0, 3.0]]
#     isAbsolute = True
#     motion.angleInterpolation(names, angles, times, isAbsolute)

# def escena():
#     tts.say("Si alguien esta triste, puedes preguntarle si se encuentra bien.")

# def reaccionar(emocion):
#     if emocion == "happy":
#         tts.say("Excelente! Me alegra que lo hayas entendido.")
#         gesto_brazo_derecho_arriba()
#     elif emocion == "confused":
#         tts.say("Mmm, no fue tan claro. Te lo explico otra vez.")
#         gesto_confundido()
#         time.sleep(1)
#         escena()  # Repetir la escena
#     else:
#         tts.say("No pude verte bien. Puedes acercarte un poco?")

# if __name__ == "__main__":
#     motion.wakeUp()
#     escena()
#     time.sleep(1)
#     emocion = obtener_emocion()
#     print("Emocion detectada:", emocion)
#     reaccionar(emocion)

