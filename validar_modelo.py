import numpy as np
from PIL import Image
import onnxruntime as ort
import os

# Nombre exacto de tu modelo exportado
RUTA_MODELO = "modelo_montanas_v1a.onnx"

def preprocesar_imagen(ruta_imagen):
    """Prepara una sola foto para que el modelo la entienda"""
    if not os.path.exists(ruta_imagen):
        print(f"❌ Error: No se encontró la imagen '{ruta_imagen}'")
        return None
        
    # 1. Abrir imagen y asegurar 3 canales (RGB)
    img = Image.open(ruta_imagen).convert('RGB')
    
    # 2. Forzar resolución exacta 224x224
    img = img.resize((224, 224))
    
    # 3. Convertir a números y aplicar la normalización (rescale=1./255)
    img_array = np.array(img, dtype=np.float32) / 255.0
    
    # 4. Agregar la dimensión del Batch: [1, 224, 224, 3]
    img_array = np.expand_dims(img_array, axis=0) 
    
    return img_array

def evaluar_foto(ruta_imagen):
    print(f"\nAnalizando: '{ruta_imagen}'...")
    
    # Preprocesamos la foto
    input_data = preprocesar_imagen(ruta_imagen)
    if input_data is None:
        return None, None
    
    # Iniciamos el motor de ONNX
    sesion = ort.InferenceSession(RUTA_MODELO)
    input_name = sesion.get_inputs()[0].name
    output_name = sesion.get_outputs()[0].name
    
    # Hacemos la predicción
    resultado = sesion.run([output_name], {input_name: input_data})
    score = resultado[0][0][0] # Extraemos el número final
    
    # ==========================================
    # LÓGICA DE DECISIÓN
    # ==========================================
    # Keras asignó 0 a Montañas y 1 a No_Montañas por orden alfabético.
    
    print("-" * 50)
    if score < 0.5: 
        # Si está más cerca de 0
        confianza = (1.0 - score) * 100
        es_montana = True
        print(f"✅ ¡ES UNA MONTAÑA!")
        print(f"📊 Nivel de certeza: {confianza:.2f}%")
    else:
        # Si está más cerca de 1
        confianza = score * 100
        es_montana = False
        print(f"❌ NO ES UNA MONTAÑA")
        print(f"📊 Nivel de certeza: {confianza:.2f}%")
    print("-" * 50)
    
    return es_montana, confianza

# ==========================================
# ZONA DE PRUEBAS
# ==========================================
if __name__ == "__main__":
    if not os.path.exists(RUTA_MODELO):
        print(f"⚠️ No se encontró '{RUTA_MODELO}'. Ejecuta el entrenamiento primero.")
    else:
        # Pon el nombre de las fotos que quieras probar aquí abajo:
        evaluar_foto("arbol_000.jpg") 
        evaluar_foto("plastic_1.jpg")
        evaluar_foto("coche rojo.avif")
        evaluar_foto("montana12.jpg")