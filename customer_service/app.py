from flask import Flask, request, jsonify, abort
import requests
import datetime

app = Flask(__name__)
# Esta URL se actualizará en AWS para apuntar al storage_service.
# Para ejecución local, usa 127.0.0.1. En EC2, si están en la misma instancia, también 127.0.0.1.
STORAGE_SERVICE_URL = "http://127.0.0.1:5001" 

@app.route('/clientes', methods=['POST'])
def crear_cliente():
    """Crea un nuevo cliente o devuelve un error si ya existe."""
    data = request.json
    nombre = data.get('nombre')
    contacto = data.get('contacto')
    servicio_inicial = data.get('servicio')

    if not all([nombre, contacto, servicio_inicial]):
        abort(400, description="Faltan datos: nombre, contacto y servicio son requeridos.")

    try:
        # Intentar obtener el cliente para verificar si ya existe
        response = requests.get(f"{STORAGE_SERVICE_URL}/archivos/{nombre}")
        response.raise_for_status() # Lanza HTTPError si el estado no es 2xx
        return jsonify({"error": f"El cliente '{nombre}' ya existe."}), 409
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            # Cliente no existe, podemos proceder a crearlo
            pass 
        else:
            # Otro tipo de error HTTP del storage_service
            abort(500, description=f"Error en servicio de almacenamiento: {e.response.text}")
    except requests.exceptions.ConnectionError:
        abort(500, description="No se pudo conectar con el servicio de almacenamiento.")
    except Exception as e:
        abort(500, description=f"Error inesperado al verificar cliente: {e}")

    nuevo_cliente = {
        "nombre": nombre,
        "contacto": contacto,
        "servicios": [
            {
                "descripcion": servicio_inicial,
                "fecha_contratacion": datetime.date.today().isoformat()
            }
        ]
    }

    try:
        response = requests.post(f"{STORAGE_SERVICE_URL}/archivos", json=nuevo_cliente)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        abort(500, description=f"Error al guardar cliente en storage: {e}")


@app.route('/clientes/<nombre>/servicios', methods=['POST'])
def agregar_servicio_cliente(nombre):
    """Agrega un nuevo servicio a un cliente existente."""
    data = request.json
    nuevo_servicio_desc = data.get('servicio')

    if not nuevo_servicio_desc:
        abort(400, description="El campo 'servicio' es requerido.")

    try:
        response = requests.get(f"{STORAGE_SERVICE_URL}/archivos/{nombre}")
        response.raise_for_status()
        cliente_data = response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return jsonify({"error": f"El cliente '{nombre}' no fue encontrado."}), 404
        abort(500, description=f"Error en servicio de almacenamiento al buscar cliente: {e.response.text}")
    except requests.exceptions.ConnectionError:
        abort(500, description="No se pudo conectar con el servicio de almacenamiento.")
    except Exception as e:
        abort(500, description=f"Error inesperado al obtener cliente para agregar servicio: {e}")
        
    nuevo_servicio = {
        "descripcion": nuevo_servicio_desc,
        "fecha_contratacion": datetime.date.today().isoformat()
    }
    cliente_data['servicios'].append(nuevo_servicio)

    try:
        response = requests.post(f"{STORAGE_SERVICE_URL}/archivos", json=cliente_data)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        abort(500, description=f"Error al actualizar cliente en storage: {e}")


@app.route('/clientes/<nombre>', methods=['PUT'])
def modificar_cliente(nombre):
    """Modifica los datos de contacto u otros campos de un cliente existente."""
    data = request.json
    try:
        response = requests.get(f"{STORAGE_SERVICE_URL}/archivos/{nombre}")
        response.raise_for_status()
        cliente_data = response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return jsonify({"error": f"El cliente '{nombre}' no fue encontrado."}), 404
        abort(500, description=f"Error en servicio de almacenamiento al buscar cliente para modificar: {e.response.text}")
    except requests.exceptions.ConnectionError:
        abort(500, description="No se pudo conectar con el servicio de almacenamiento.")
    except Exception as e:
        abort(500, description=f"Error inesperado al obtener cliente para modificar: {e}")

    # Actualizar campos permitidos
    if 'contacto' in data:
        cliente_data['contacto'] = data['contacto']
    # Aquí se podrían añadir más campos a modificar

    try:
        response = requests.post(f"{STORAGE_SERVICE_URL}/archivos", json=cliente_data)
        response.raise_for_status()
        return jsonify({"status": "ok", "message": f"Cliente {nombre} actualizado."}), 200
    except requests.exceptions.RequestException as e:
        abort(500, description=f"Error al actualizar cliente en storage: {e}")


@app.route('/clientes/<nombre>', methods=['GET'])
def obtener_cliente(nombre):
    """Obtiene la información detallada de un cliente."""
    try:
        response = requests.get(f"{STORAGE_SERVICE_URL}/archivos/{nombre}")
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return jsonify({"error": f"El cliente '{nombre}' no fue encontrado."}), 404
        abort(500, description=f"Error en servicio de almacenamiento al obtener cliente: {e.response.text}")
    except requests.exceptions.ConnectionError:
        abort(500, description="No se pudo conectar con el servicio de almacenamiento.")
    except Exception as e:
        abort(500, description=f"Error inesperado al obtener cliente: {e}")


@app.route('/clientes', methods=['GET'])
def listar_clientes():
    """Lista todos los nombres de los clientes existentes."""
    try:
        response = requests.get(f"{STORAGE_SERVICE_URL}/archivos")
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        abort(500, description="No se pudo contactar el servicio de almacenamiento.")
    except Exception as e:
        abort(500, description=f"Error inesperado al listar clientes: {e}")

# Nuevo endpoint de ejemplo para simular un cambio/mejora
@app.route('/saludo', methods=['GET'])
def saludo():
    """Endpoint de ejemplo para probar una nueva funcionalidad o mejora."""
    return jsonify({"message": "Hola desde Sky App v2.0 mejorada!"})


if __name__ == '__main__':
    # Para desarrollo local o si Nginx no está configurado para manejar el puerto
    app.run(host='0.0.0.0', port=5002, debug=True)