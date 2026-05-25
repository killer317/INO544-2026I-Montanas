# Grupo - Montañas 
## IUJO — Feria de Haceres Período I-2026
### Unidad Curricular: INO-544 (Investigación de Operaciones)

---

## 👥 Integrantes y Roles

* Integrante 1: Jeanfreiber Medina - 30519862
  * Rol: encargado de recopilación y limpieza del dataset de montañas, estructuración de directorios y configuración de las transformaciones de *Data Augmentation* (rotación, zoom, brillo) para evitar el sobreajuste.

* **Integrante 2:** Jesus Moco - 29804224
  * **Rol: responsable en el diseño de la arquitectura de la Red Neuronal (CNN), selección de la función de activación, ajuste de hiperparámetros (Learning Rate, Optimizador, Épocas) y ejecución del entrenamiento.

* **Integrante 3:** Gilbert vera - 
  * **Rol: Responsabilidades Homologación del modelo, conversión estricta desde Keras al formato universal **ONNX v12**, y garantía de que los tensores de entrada/salida ([1, 224, 224, 3] y [1, 1]) cumplan con los estándares de la feria.

* **Integrante 4:** Leonardo Garcia - 30594076
  * **Rol: Responsabilidades Desarrollo de los scripts de inferencia y validación local, recolección de las métricas de rendimiento (Accuracy y Loss), generación de gráficas de entrenamiento y documentación del proyecto.

---

## 🎯 1. Clase/Tema Seleccionado
* Tema asignado: Montañas
* Descripción del Objeto: Estructuras geológicas caracterizadas por elevaciones naturales del terreno, picos pronunciados, laderas, texturas rocosas, posible presencia de nieve en las cimas y contrastes marcados con el cielo o la vegetación circundante. El modelo debe distinguir estas formas masivas de otros paisajes o entornos urbanos.

---

## 📊 2. Gestión del Dataset (Ingeniería de Datos)
* Cantidad de imágenes originales recopiladas: imágenes (Aproximadame entre 500-550).
* Estrategia de Data Augmentation aplicada:
    * *Rotación:* Entre -20° y +20°.
    * *Zoom:* Rango del 20% (0.2).
    * *Cambios de Brillo:* Rango de 0.8 a 1.2.
    * *Otras transformaciones:* Volteo horizontal (Horizontal Flip) y Desplazamiento (Width/Height Shift) del 10% de movimiento lateral y vertical para simular distintos encuadres de cámara.
* Total de imágenes generadas para el entrenamiento: 2500 de montañas 
* Resolución y formato estandarizado: 224x224 píxeles, JPG, canales RGB (Formato Tensor: [1, 224, 224, 3]).

---

## 🧠 3. Arquitectura del Modelo y Entrenamiento
* Framework utilizado: TensorFlow / Keras
* Descripción de la Red (CNN): Se diseñó una red neuronal convolucional (CNN) compuesta por 3 capas Conv2D (32, 64 y 128 filtros respectivamente) para la extracción de características visuales, cada una seguida de una capa MaxPooling2D para la reducción de dimensionalidad. Finalmente, una capa Flatten conecta con una capa densa oculta de 128 neuronas y una capa de salida de 1 neurona.
* **Hiperparámetros óptimos seleccionados:**
    * *Función de pérdida (Loss):* Binary Crossentropy (ideal para clasificación binaria Montaña vs No Montaña).
    * *Optimizador:* Adam.
    * *Tasa de Aprendizaje (Learning Rate):* 0.001 (Por defecto de Adam).
    * *Épocas (Epochs):* 10
    * *Tamaño de lote (Batch Size):* 32

### 💡 Justificación Crítica (Control de Autoría)
*Explique detalladamente por qué el equipo eligió esa Tasa de Aprendizaje (Learning Rate) específica y el impacto que tuvo en las gráficas de pérdida durante el laboratorio:*
> ### 💡 Justificación Crítica (Control de Autoría)
*Explique detalladamente por qué el equipo eligió esa Tasa de Aprendizaje (Learning Rate) específica y el impacto que tuvo en las gráficas de pérdida durante el laboratorio:*

 Durante las pruebas iniciales en el laboratorio, estuvimos ajustando varios valores para evaluar cómo reaccionaba el modelo. Primero intentamos forzar un aprendizaje rápido con una tasa de "0.01", pero al observar la gráfica de pérdida, vimos que la curva rebotaba de forma errática; el modelo era demasiado agresivo, "saltaba" por encima de los mínimos y no lograba estabilizarse.
 
 Por otro lado, cuando probamos bajarla demasiado (a "0.0001"), la curva era muy estable, pero el aprendizaje se volvía desesperantemente lento y la red apenas mejoraba tras cada época, lo que no era viable para nuestros tiempos de prueba.
 
 Finalmente, decidimos establecer la tasa en "0.001" trabajando en conjunto con el optimizador Adam. Esta resultó ser la decisión más sensata: al analizar la gráfica final, notamos que la curva de pérdida de entrenamiento y validación descendía de forma limpia y fluida. El modelo logró converger de manera segura hacia las últimas épocas sin que ambas líneas se separaran drásticamente, lo que nos confirmó que estábamos evitando el *overfitting* (sobreajuste). En resumen, fue el punto de equilibrio perfecto entre velocidad de cómputo y la capacidad real de la red para generalizar y reconocer las montañas.

---

## 📈 4. Métricas de Rendimiento (Testing - 20%)
* Precisión final (Accuracy) en la data de test: promedio 99.2%
* **Pérdida final (Loss) en la data de test:** promedio 0.8%

*(Inserte aquí abajo la captura de pantalla de la gráfica de entrenamiento Accuracy/Loss de su modelo)*
![Gráfica de Entrenamiento](src/grafica_rendimiento.png)

prueba de el modelo en la terminal 
---<img width="1043" height="329" alt="pruebas en terminal" src="https://github.com/user-attachments/assets/85a9fbc3-9b59-4bcc-a326-e87418aa4bed" />
primer modelo de la interfaz 1.0v ¨es una montaña¨
<img width="1099" height="725" alt="modelo primera fase montaña" src="https://github.com/user-attachments/assets/ef6268ed-f1f6-4676-85e5-30be887b6107" />
primer modelo de la interfaz 1.0v ¨no es una montaña¨
<img width="1094" height="727" alt="modelo primera fase no montaña" src="https://github.com/user-attachments/assets/10e854e3-cb54-4f03-a733-05a9bba1970e" />
modelo final de la interfaz 2.0v ¨es una montaña¨
<img width="1895" height="902" alt="montaña" src="https://github.com/user-attachments/assets/c1861117-a5b3-43d8-af6e-aea0ed588084" />
modelo final de la interfaz 2.0v ¨no es una montaña¨
<img width="1895" height="897" alt="no montaña" src="https://github.com/user-attachments/assets/c3a5d0f1-ec11-401e-aa68-31f14214e550" />


## ⚙️ 5. Especificación de Exportación ONNX
El modelo se ha homologado bajo los estándares requeridos por la interfaz centralizada:
* Nombre del archivo: modelo_montanas_v1a.onnx
* Tensor de Entrada (Input Shape): [1, 224, 224, 3] (Tipo: float32, Nombre: cam_input)
* Tensor de Salida (Output Shape): [1, 1] (Tipo: float32, Nombre: confidence_score)
* Función de activación final: Sigmoide (Rango de salida de 0.0 a 1.0 para conversión a porcentaje).

---

## 🚀 6. Instrucciones de Ejecución Local
Para replicar el preprocesamiento y el entrenamiento del modelo:

1. Clonar el repositorio:
   ```bash
   git clone [[https://github.com/](https://github.com/)[usuario]/[repositorio].git](https://github.com/killer317/INO544-2026I-Montanas.git)
   cd C:\Users\yeiber y gilbert\OneDrive\Desktop
