# 📂 Datasets utilizados

Este documento describe los datasets utilizados en el proyecto *Comparative Emotion Detection System with NAO Robot*, así como las justificaciones técnicas y éticas de su uso.

---

## 1. FER2013

- **Fuente**: [FER2013 Kaggle Challenge](https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge)
- **Contenido**: ~35,000 imágenes en escala de grises, 48x48 px, etiquetadas en 7 emociones básicas.
- **Uso en este proyecto**:
  - Entrenamiento base para CNNs.
  - Extracción de keypoints faciales (MediaPipe) para entrenamiento de clasificadores.
- **Ventajas**: accesible, bien estructurado, común en benchmarks.
- **Limitaciones**: no incluye cuerpos completos ni variedad étnica infantil clara.

---

## 2. RAF-DB (TDB)

- **Fuente**: [Real-world Affective Faces Database](http://www.whdeng.cn/RAF/model1.html)
- **Contenido**: ~30,000 imágenes en color con etiquetas emocionales.
- **Uso en este proyecto**:
  - Complemento para entrenamiento/fine-tuning de CNNs si se desea más calidad visual.
- **Ventajas**: mejor calidad, más expresiones sutiles.
- **Limitaciones**: adultos mayormente, requiere permiso de uso académico.

---

## 3. Capturas propias (keypoints posturales) (TODO)

- **Fuente**: capturas en tiempo real con webcam (autograbación o expresiones actuadas).
- **Contenido**: expresiones corporales simuladas de emociones básicas.
- **Uso en este proyecto**:
  - Generación de puntos clave con MediaPipe Pose para entrenar clasificador postural.
- **Ventajas**: se adapta al objetivo del proyecto.
- **Limitaciones**: no etiquetado masivo, no espontáneo.

---

## 4. Validación real – FabLab UPC

- **Fuente**: niños con TEA en interacción con el robot NAO durante sesión validada.
- **Uso**: validación externa de los modelos comparados, bajo consentimiento.
- **Consideraciones éticas**:
  - No se utilizarán sus imágenes para entrenamiento.
  - Participación bajo consentimiento informado y aprobación ética institucional.

---

## Actualizado: 2025-06-16
