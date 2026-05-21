import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np

BASE_DIR = 'dataset'

print("\n--- 1. PROBANDO EL DATASET ---")
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    zoom_range=0.2,
    width_shift_range=0.1,
    height_shift_range=0.1
)

# Cargamos el dataset desde las carpetas locales
train_generator = datagen.flow_from_directory(
    BASE_DIR,
    target_size=(224, 224), 
    batch_size=32, 
    class_mode='binary'
)

print("\nClases detectadas:", train_generator.class_indices)

# Extraemos un solo lote (batch) para verificar dimensiones
imagenes, etiquetas = next(train_generator)
print(f"Formato de las imágenes (Batch, Alto, Ancho, Canales): {imagenes.shape}")
print(f"Formato de las etiquetas: {etiquetas.shape}")

# Verificación estricta
assert imagenes.shape[1:] == (224, 224, 3), "❌ Error: La resolución o los canales no coinciden."
print("✅ El dataset funciona perfectamente y entrega el formato correcto.")

print("\n--- 2. CONSTRUYENDO LA CNN ---")
input_tensor = layers.Input(shape=(224, 224, 3), name="cam_input", dtype=tf.float32)

x = layers.Conv2D(32, (3, 3), activation='relu')(input_tensor)
x = layers.MaxPooling2D((2, 2))(x)
x = layers.Conv2D(64, (3, 3), activation='relu')(x)
x = layers.MaxPooling2D((2, 2))(x)
x = layers.Conv2D(128, (3, 3), activation='relu')(x)
x = layers.MaxPooling2D((2, 2))(x)
x = layers.Flatten()(x)
x = layers.Dense(128, activation='relu')(x)

# Salida Binaria [1, 1]
output_tensor = layers.Dense(1, activation='sigmoid', name="confidence_score")(x)

model = models.Model(inputs=input_tensor, outputs=output_tensor)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Mostrar la tabla de la arquitectura
model.summary()
print("\n✅ La arquitectura CNN compiló correctamente. ¡Listo para entrenar!")

