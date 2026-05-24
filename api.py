import os
import flask
from flask_cors import CORS

# Importamos tu función original que ya funciona con ONNX
from validar_modelo import evaluar_foto

app = flask.Flask(__name__)
# Permitimos que el Frontend (puerto 5173 o 3000) hable con el Backend (puerto 5000)
CORS(app) 

@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    # 1. Verificamos que React nos haya enviado una imagen
    if 'image' not in flask.request.files:
        return flask.jsonify({'error': 'No se envió ninguna imagen'}), 400
    
    file = flask.request.files['image']
    temp_path = "temp_upload.jpg"
    
    try:
        # 2. Guardamos la imagen temporalmente para que tu modelo pueda leerla
        file.save(temp_path)
        
        # 3. Llamamos a tu modelo ONNX exacto como lo hace la app de escritorio
        es_montana, confianza = evaluar_foto(temp_path)
        
        # 4. Eliminamos la imagen temporal para mantener todo limpio
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        if es_montana is None:
            return flask.jsonify({'error': 'Error al procesar la imagen con el modelo ONNX'}), 500
            
        # 5. Enviamos la respuesta de vuelta a React
        return flask.jsonify({
            'es_montana': bool(es_montana),
            'confianza': float(confianza)
        })
        
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return flask.jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Servidor IA Iniciado. Esperando a la interfaz web en el puerto 5000...")
    # Comentar la línea de desarrollo:
    # app.run(port=5000, debug=True)
    
    # Usar Waitress para producción (sin advertencias):
    from waitress import serve
    serve(app, host="127.0.0.1", port=5000)