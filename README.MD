# Comparative Emotion Detection System with NAO Robot – CNN vs Facial/Postural Keypoints

Este proyecto implementa un sistema de detección emocional con el robot humanoide NAO, utilizando tres enfoques distintos de visión por computadora: redes convolucionales (CNN), keypoints faciales y keypoints posturales.

El objetivo es comparar su precisión, velocidad y robustez para identificar emociones básicas en niños con TEA, integrándolos en una interacción real con el robot. El modelo con mejor desempeño se valida en el FabLab UPC en interacción directa con niños autistas.

## 🚀 Descripción General

El flujo del sistema es:

1. El NAO captura una imagen desde su cámara frontal.
2. La imagen se codifica en base64 y se envía vía HTTP a una API Flask.
3. Un modelo de ML en la laptop analiza la emoción facial en la imagen.
4. La respuesta emocional se devuelve al NAO, que reacciona con voz y gestos expresivos.

## 🎯 Objetivo

Comparar el rendimiento de tres técnicas de reconocimiento emocional —CNN, keypoints faciales y keypoints posturales— bajo distintos escenarios de entrada y condiciones reales, evaluando su utilidad para asistir a interacciones psicoeducativas con niños autistas mediante el robot NAO.

## 🧠 Tecnologías utilizadas

- **Robot**: NAO (versión con Python 2.7)
- **API backend**: Flask (Python 3.10)
- **Modelos**:
  - CNN (MobileNetV2 / VGG19)
  - Keypoints faciales (MediaPipe + MLP)
  - Keypoints posturales (MediaPipe Pose + MLP)
- **Librerías**:
  - `pynaoqi`
  - `Flask`, `NumPy`, `OpenCV`, `Pillow`
  - `MediaPipe`, `scikit-learn`, `PyTorch`
- **Comunicación**: HTTP simple (sin sockets ni ROS)

## 📁 Estructura del repositorio

```
├── models/ # Modelos para clasificación emocional
│   ├── cnn_model.py
│   ├── keypoints_face_model.py
│   └── keypoints_pose_model.py
├── data/
│   └── datasets_used.md
├── evaluation/
│   └── compare_metrics.ipynb
├── main.py                 # Script que corre en NAO (Py2.7)
├── run.sh                 # Script de ejecución     
├── apiflask/              # Carpeta con backend Flask en Py3 (uso demodelo y API)
├── pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327/
├── readme.md      
        
```

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

Se probaron tres técnicas de detección de emociones bajo diferentes condiciones controladas (iluminación, resolución, entrada recortada vs completa, color vs escala de grises).

Se midieron:

- Precisión y F1-score

- Velocidad de inferencia

- Robustez frente a condiciones no ideales

La técnica con mejor desempeño se implementó en el NAO y se validó en una sesión real con niños en el FabLab.
(Metricas, diseno de exprimento)

## 📚 Enfoque académico

Se busca explorar cómo los sistemas de detección emocional pueden integrarse en contextos de robótica social como herramientas de soporte para niños con TEA, siguiendo enfoques vicarios.

Este proyecto se enmarca como investigación aplicada de carácter comparativo, contribuyendo al análisis de técnicas de visión por computadora para contextos sociales asistidos. Se integra una validación práctica con niños autistas en el FabLab de la universidad, aportando evidencia preliminar sobre la viabilidad técnica y pedagógica del enfoque.

## 📊 Resultados comparativos (TBD)

Se incluirán tablas comparativas de rendimiento por técnica y escenario. Las pruebas abarcan desde entornos controlados hasta validaciones ecológicas con niños en el FabLab.
