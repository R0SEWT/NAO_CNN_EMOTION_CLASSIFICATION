# -*- coding: utf-8 -*-
"""
therapy_phases.py – Fase 1 → Fase 2 → Fase 3
"""
from __future__ import print_function
import time
from nao_actions import say, wake_up, rest, \
                        gesto_saludo, gesto_brazo_derecho_arriba, \
                        gesto_sorpresa, gesto_confundido
from perception import capture_frame_b64, detect_emotion

# ── Fase 1: Captar intención / atención ────────────────────────────────
def fase1_intencion(child):
    say("Hola " + child["nombre"] + "! " + child["sonido_atencion"])
    if child["cancion_favorita"]:
        say("♪ " + child["cancion_favorita"] + " ♪")
    time.sleep(2)

# ── Fase 2: Establecer contacto visual ─────────────────────────────────
def fase2_contacto_visual():
    say("¿Me puedes mirar?")
    time.sleep(3)
    # aquí podrías chequear detección rostro; retornamos True como demo
    return True

# ── Fase 3: Reciprocidad y objetivos ──────────────────────────────────
def fase3_recicprocidad(child):
    say("¡Genial! Ahora vamos a imitar un movimiento.")
    gesto_brazo_derecho_arriba()
    time.sleep(2)
    say("Muy bien, " + child["nombre"] + "!")
    b64 = capture_frame_b64()
    if not b64:
        say("No pude ver tu emoción.")
        return
    emocion = detect_emotion(b64)
    print("Emoción detectada:", emocion)
    if emocion == "happy":
        say("¡Te veo contento!")
        gesto_saludo()
    elif emocion == "angry":
        say("Pareces molesto.")
        gesto_confundido()
    elif emocion == "fear":
        say("¿Estás asustado?")
        gesto_sorpresa()
    else:
        say("Gracias por jugar conmigo.")

# ── Ejecutar sesión completa ───────────────────────────────────────────
def run_session(child_profile, pc_mode=False):
    wake_up()
    try:
        fase1_intencion(child_profile)
        if not fase2_contacto_visual():
            say("Intentemos de nuevo otro día.")
            return
        fase3_recicprocidad(child_profile)
    finally:
        rest()
