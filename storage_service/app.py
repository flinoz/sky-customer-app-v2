import os
import json
from flask import Flask, request, jsonify, abort

app = Flask(__name__)
# La carpeta para almacenar los datos de clientes.
# Usar una ruta absoluta para asegurar que Systemd la encuentre correctamente en EC2.
DATA_FOLDER = '/home/ec2-user/sky-customer-app-v2/storage_service/client_data' 

# Crear la carpeta para los datos si no existe
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

@app.route('/archivos/<nombre_cliente>', methods=['GET'])
def obtener_archivo(nombre_cliente):
    """Obtiene el archivo JSON de un cliente específico."""
    filepath = os.path.join(DATA_FOLDER, f"{nombre_cliente}.json")
    if not os.path.exists(filepath):
        abort(404, description="Cliente no encontrado")
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except json.JSONDecodeError:
        abort(500, description="Error al leer el archivo JSON del cliente.")
    except Exception as e:
        abort(500, description=f"Error inesperado al obtener archivo: {e}")

@app.route('/archivos', methods=['POST'])
def guardar_archivo():
    """Guarda o actualiza el archivo JSON de un cliente."""
    client_data = request.json
    nombre_cliente = client_data.get('nombre')
    
    if not nombre_cliente:
        abort(400, description="El nombre del cliente es requerido")

    filepath = os.path.join(DATA_FOLDER, f"{nombre_cliente}.json")
    try:
        with open(filepath, 'w') as f:
            json.dump(client_data, f, indent=4) # Guardar con indentación para legibilidad
            
        return jsonify({"status": "ok", "message": f"Cliente {nombre_cliente} guardado/actualizado."}), 201
    except Exception as e:
        abort(500, description=f"Error al guardar archivo: {e}")

@app.route('/archivos', methods=['GET'])
def listar_archivos():
    """Lista los nombres de todos los archivos de clientes guardados."""
    try:
        files = [f.replace('.json', '') for f in os.listdir(DATA_FOLDER) if f.endswith('.json')]
        return jsonify(files)
    except FileNotFoundError: # En caso de que DATA_FOLDER no exista (aunque lo creamos al inicio)
        return jsonify([]), 200 # Devolver lista vacía si no hay carpeta
    except Exception as e:
        abort(500, description=f"Error inesperado al listar archivos: {e}")

@app.route('/archivos/<nombre_cliente>', methods=['DELETE'])
def borrar_archivo(nombre_cliente):
    """Elimina el archivo JSON de un cliente específico."""
    filepath = os.path.join(DATA_FOLDER, f"{nombre_cliente}.json")
    if not os.path.exists(filepath):
        abort(404, description="Cliente no encontrado")
    
    try:
        os.remove(filepath)
        return jsonify({"status": "ok", "message": f"Cliente {nombre_cliente} eliminado."}), 200
    except Exception as e:
        abort(500, description=f"Error al eliminar archivo: {e}")


if __name__ == '__main__':
    # Para desarrollo local o si Nginx no está configurado para manejar el puerto
    app.run(host='0.0.0.0', port=5001, debug=True)