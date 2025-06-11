from flask import Flask
from detectar_emocion import detectar_emocion

app = Flask(__name__)

@app.route("/emocion")
def ruta_emocion():
    emocion = detectar_emocion()
    print("Emoción detectada:", emocion)
    # Puedes mapear varias emociones a simple happy/confused
    if emocion in ["happy", "surprise"]:
        return "happy"
    elif emocion in ["sad", "angry", "fear", "disgust"]:
        return "confused"
    else:
        return emocion

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
