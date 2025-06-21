# -*- coding: utf-8 -*-
"""
nao_actions.py – Conexión y gestos independientes de la fase
"""
from __future__ import print_function
from config import NAO_IP, PORT
import time

try:
    from naoqi import ALProxy
except ImportError:
    # PC testing sin NAOqi
    class _Dummy(object):
        def __getattr__(self, _):       # permite cualquier método sin fallar
            return lambda *a, **k: None
    ALProxy = lambda *a, **k: _Dummy()

tts    = ALProxy("ALTextToSpeech", NAO_IP, PORT)
motion = ALProxy("ALMotion",        NAO_IP, PORT)

# ───── Utilidades ──────────────────────────────────────────────────────
def wake_up():
    motion.wakeUp()

def rest():
    motion.rest()

def say(text):
    print("[NAO] →", text)
    tts.say(text)

def volver_base():
    names  = ["HeadYaw", "HeadPitch", "RShoulderPitch", "RElbowRoll",
              "LShoulderPitch", "LElbowRoll"]
    angles = [0, 0, 1.5, 0, 1.5, 0]
    times  = [1]*len(angles)
    motion.angleInterpolation(names, angles, times, True)

# ───── Gestos (fase-agnósticos) ────────────────────────────────────────
def gesto_saludo():
    names  = ["RShoulderPitch", "RElbowYaw", "RElbowRoll"]
    angles = [1.2, 1.4, 0.5]
    times  = [1, 1, 1]
    motion.angleInterpolation(names, angles, times, True)
    for _ in range(2):
        motion.angleInterpolation("RElbowRoll", 0.2, 0.3, True)
        motion.angleInterpolation("RElbowRoll", 0.5, 0.3, True)
    volver_base()

def gesto_brazo_derecho_arriba():
    names  = ["RShoulderPitch", "RElbowRoll"]
    angles = [0.3, 1.2]
    times  = [1, 1]
    motion.angleInterpolation(names, angles, times, True)

def gesto_sorpresa():
    names  = ["HeadPitch"]
    motion.angleInterpolation(names, 0.5, 0.5, True)

def gesto_confundido():
    motion.angleInterpolation("HeadYaw", 0.7, 0.5, True)
    motion.angleInterpolation("HeadYaw", -0.7, 0.5, True)
    motion.angleInterpolation("HeadYaw", 0.0, 0.3, True)
