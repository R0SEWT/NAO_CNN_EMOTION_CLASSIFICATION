# NAO Emotion Detection System

Este proyecto implementa un sistema de detección emocional utilizando un robot NAO, visión por computadora y un modelo ligero de clasificación de emociones.

Está orientado a explorar aplicaciones de soporte psicoeducativo para niños con TEA (Trastorno del Espectro Autista), integrando componentes de Machine Learning y Robótica Social.

## 🚀 Descripción General

El flujo del sistema es:

1. El NAO captura una imagen desde su cámara frontal.
2. La imagen se codifica en base64 y se envía vía HTTP a una API Flask.
3. Un modelo de ML en la laptop analiza la emoción facial en la imagen.
4. La respuesta emocional se devuelve al NAO, que reacciona con voz y gestos expresivos.

## 🎯 Objetivo

Comparar el rendimiento de distintos métodos de reconocimiento emocional bajo diferentes condiciones de entrada (resolución, iluminación, posición de rostro), evaluando su utilidad para interacciones con niños autistas mediante un robot humanoide limitado en locomoción.

## 🧠 Tecnologías utilizadas

- Robot: NAO (versión con Python 2.7) (Flask)
- API backend: Flask (Python 3.10)
- Modelo: CNN ligero para FER (TDB)
- Librerías:
  - `pynaoqi`
  - `Pillow`
  - `Flask`, `NumPy`, `OpenCV`
- Comunicación: HTTP (sin sockets ni ROS)

## 📁 Estructura del repositorio

```
.
├── main.py                 # Script que corre en NAO (Py2.7)
├── run.sh                 # Script de ejecución
├── modelo\_emocion.h5      # Modelo Keras para clasificación emocional
├── apiflask/              # Carpeta con backend Flask en Py3 (modelo y API)
├── train\_model.ipynb      # Entrenamiento o prueba del modelo
├── readme.md              

````

## ⚙️ Requisitos

TODO: add requirements 2.7 y 3.10


## ▶️ Uso

TODO: Detallar uso

1. Ejecutar la API Flask en la laptop:

```bash
cd apiflask
python app.py
```

2. Ejecutar el script en el NAO (configurar IP del NAO):

```bash
./run.sh
```

## 🧪 Pruebas

Se probaron distintos escenarios controlados variando: (TDB)

* Iluminación ambiente
* Resolución de captura
* Angulación del rostro


Se observó la respuesta del modelo y del robot para cada caso.

(Metricas, diseno de exprimento)

## 📚 Enfoque académico

Se busca explorar cómo los sistemas de detección emocional pueden integrarse en contextos de robótica social como herramientas de soporte para niños con TEA, siguiendo enfoques vicarios.

## Observaciones

Nao puede prender los ojos y parlantes (util para emular cargas y mostrar alertas)
Asimismo detecta caras `ALVideoDevice`. Tmb detecta emociones usando voz con `ALMood`. Seria conveniente incluirlo en los exprimentos