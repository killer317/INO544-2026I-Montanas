import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
import tf2onnx

# ==========================================
# 1. CONFIGURACIÓN DEL DATASET (80% Train / 20% Test)
# ==========================================
BASE_DIR = 'dataset'

print("\n--- PREPARANDO DATOS Y TRANSFORMACIONES ---")
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    zoom_range=0.2,
    width_shift_range=0.1,
    height_shift_range=0.1,
    validation_split=0.2  # Define el 20% para pruebas
)

train_generator = datagen.flow_from_directory(
    BASE_DIR,
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    BASE_DIR,
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    subset='validation'
)

print("\nDiccionario de clases:", train_generator.class_indices)

# ==========================================
# 2. ARQUITECTURA CNN
# ==========================================
print("\n--- CONSTRUYENDO LA RED NEURONAL ---")
input_tensor = layers.Input(shape=(224, 224, 3), name="cam_input", dtype=tf.float32)

# Ajuste de escala: El script de validación entrega [0, 1], pero MobileNetV2 espera [-1, 1].
x = layers.Rescaling(scale=2.0, offset=-1.0)(input_tensor)

# Usamos Transfer Learning con MobileNetV2 (modelo avanzado y ligero)
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False  # Congelamos el modelo base para que no pierda lo aprendido

x = base_model(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(128, activation='relu')(x)
x = layers.Dropout(0.5)(x)

# Salida Binaria
output_tensor = layers.Dense(1, activation='sigmoid', name="confidence_score")(x)

model = models.Model(inputs=input_tensor, outputs=output_tensor)
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# ==========================================
# 3. ENTRENAMIENTO
# ==========================================
print("\n--- INICIANDO ENTRENAMIENTO ---")

# Detiene el entrenamiento si el modelo alcanza su límite y restaura los mejores pesos
early_stopping = EarlyStopping(
    monitor='val_accuracy', 
    patience=5, 
    restore_best_weights=True
)

history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=25,
    callbacks=[early_stopping]
)

# ==========================================
# 4. EXPORTACIÓN ESTRICTA A ONNX v12
# ==========================================
print("\n--- EXPORTANDO MODELO A ONNX ---")
# Definimos la firma exacta [1, 224, 224, 3] en formato NHWC
input_signature = [tf.TensorSpec([1, 224, 224, 3], tf.float32, name="cam_input")]
onnx_model_path = "modelo_montanas_v1a.onnx"

model_proto, _ = tf2onnx.convert.from_keras(
    model, 
    input_signature=input_signature, 
    opset=12, 
    output_path=onnx_model_path
)

print("=" * 50)
print(f"✅ ¡PROCESO COMPLETADO!")
print(f"Tu modelo está listo y guardado como: {onnx_model_path}")
print("=" * 50)