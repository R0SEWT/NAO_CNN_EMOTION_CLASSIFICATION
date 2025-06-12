🧠 Descripción del Proyecto

NAO Emocional Interactivo

Objetivo:
Permitir que el robot NAO detecte emociones humanas (como felicidad, tristeza o confusión) y reaccione de forma adecuada, usando gestos corporales y habla.
🧩 Componentes del Sistema
1. NAO (Python 2.7 con NAOqi)

    Captura una imagen con su cámara interna usando ALVideoDevice.

    Codifica la imagen en base64.

    Envía la imagen vía HTTP POST a un servidor Flask para clasificar la emoción.

    Recibe una emoción (happy, confused, no_face, etc.).

    Ejecuta un comportamiento preprogramado (hablar + mover brazos o cabeza) según la emoción detectada.

2. Servidor Flask (Python 3.9)

    Recibe la imagen en base64 desde NAO.

    Decodifica y procesa la imagen.

    Usa un modelo preentrenado (modelo_emocion.h5) para detectar emociones.

    Devuelve la emoción clasificada al NAO.

    Guarda un log local con la imagen clasificada y su etiqueta, con timestamp.

🎯 Flujo General

    NAO dice una frase y captura una imagen.

    La envía al servidor.

    El servidor responde con la emoción.

    NAO responde con un gesto y voz.

    La laptop guarda un log con la imagen.

🛠️ Tecnologías
Componente	Tecnología
Robot	NAOqi SDK (Python 2.7)
Backend	Flask (Python 3.9)
IA	Keras + TensorFlow (modelo .h5)
Comunicación	HTTP POST (json con base64)
Logs	Archivos .jpg con nombre timestamp_emocion.jpg