# -*- coding: utf-8 -*-
"""
config.py – Parámetros globales y perfil del niño
"""

# ───── Conexión robot / API ─────────────────────────────────────────────
NAO_IP          = "127.0.0.1"     # IP del NAO o simulador
PORT            = 9559            # Puerto NAOqi
API_EMOCION_URL = "http://127.0.0.1:5000/emocion"  # API Flask emoción

# ───── Modo PC o Robot ─────────────────────────────────────────────────
TESTING_ON_PC   = True            # False = cámara NAO real
PC_CAM_INDEX    = 0               # (se ignora si usas snapshot server)

# ───── Perfil del niño (ejemplo) ───────────────────────────────────────
CHILD = {
    "nombre"             : "Juan",
    "grado_tea"          : 1,      # solo grado 1 funcional
    "edad"               : 6,
    "sensibilidad"       : "hipersensible",  # 'hiposensible'
    "sonido_atencion"    : "Ah-ah",          # palabra que capta atención
    "cancion_favorita"   : "La lechuza",
    "tiene_hiperfoco"    : True,
}
