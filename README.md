# Sky App v2.0 - Sistema de Gestión de Clientes

![Sky App v2.0 Logo](https://raw.githubusercontent.com/flinoz/sky-customer-app-v2/main/img/sky_app_logo.png)

## Descripción General del Proyecto

`Sky App v2.0` es un sistema de gestión de clientes desarrollado como un proyecto de microservicios en Python con el framework Flask. Su objetivo es demostrar una una arquitectura moderna, siguiendo principios de Diseño Basado en Dominios (DDD) y un flujo de trabajo DevOps completo. La aplicación permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) básicas sobre información de clientes y sus servicios asociados.

Este repositorio documenta la Fase 2 del proyecto, enfocándose en la implementación, el despliegue en la nube de AWS (EC2), y la automatización del pipeline CI/CD utilizando GitHub Actions, junto con la demostración de la gestión de versiones y la capacidad de recuperación ante fallas.

## Características Clave

* **Arquitectura de Microservicios:** Dos servicios desacoplados (`customer_service` y `storage_service`) que se comunican para gestionar los datos de clientes.
* **API RESTful:** Interfaz HTTP para la interacción programática con la aplicación.
* **Despliegue en AWS EC2:** La aplicación está alojada en una instancia de Amazon EC2 para accesibilidad global.
* **CI/CD con GitHub Actions:**
    * **Integración Continua:** Pruebas automatizadas en cada `push` o `Pull Request`.
    * **Despliegue Continuo:** Workflow manual para desplegar la aplicación en producción (EC2).
    * **Automatización de Issues:** Gestión automática de etiquetas y comentarios en `issues`.
    * **Revisión de Código:** Recordatorios para Pull Requests que requieren revisión.
* **Control de Versiones Robusto:** Gestión completa del historial de código con Git y GitHub, incluyendo demostración de reversión a versiones anteriores para recuperación de desastres.
* **Gestión de Acceso IAM:** Control granular de permisos para equipos de desarrollo, operaciones y evaluadores en AWS.

## Estructura del Repositorio

sky-customer-app-v2/ ├── .github/ # Definiciones de workflows de GitHub Actions │ └── workflows/ │ ├── ci.yml # Workflow de Integración Continua y Pruebas │ ├── deploy_production.yml # Workflow de Despliegue a Producción en AWS EC2 │ ├── handle_issues.yml # Workflow para Automatización de la gestión de Issues │ └── code_review_required.yml # Workflow de recordatorio de revisión de código ├── customer_service/ # Microservicio de Lógica de Negocio de Clientes │ ├── app.py # Aplicación Flask principal (API REST para clientes) │ └── requirements.txt # Dependencias Python específicas para customer_service ├── storage_service/ # Microservicio de Almacenamiento de Datos (simulado con JSON local) │ ├── app.py # Aplicación Flask de almacenamiento (API REST para datos) │ └── requirements.txt # Dependencias Python específicas para storage_service ├── .gitignore # Archivo para Git que especifica archivos y directorios a ignorar ├── README.md # Este archivo de documentación ├── LICENSE # Archivo de licencia MIT └── img/ # Carpeta para imágenes (logo y evidencias de funcionamiento) ├── sky_app_logo.png # Archivo del logo del proyecto ├── EVI01.png # Evidencia visual 1: Instalación de dependencias ├── EVI02.png # Evidencia visual 2: Customer Service corriendo ├── EVI03.png # Evidencia visual 3: Storage Service corriendo └── EVI04.png # Evidencia visual 4: Pruebas con cURL


## Microservicios Detallados

### 1. `customer_service` (Puerto por defecto: 5002)

Este servicio es la interfaz principal para la gestión de clientes.

* **Endpoints Principales:**
    * `POST /clientes`: Crea un nuevo cliente.
    * `GET /clientes/<nombre>`: Recupera detalles de un cliente.
    * `PUT /clientes/<nombre>`: Modifica la información de contacto de un cliente.
    * `POST /clientes/<nombre>/servicios`: Agrega un nuevo servicio a un cliente.
    * `GET /clientes`: Lista los nombres de todos los clientes.
    * `GET /saludo`: Un endpoint de prueba/demostración.

### 2. `storage_service` (Puerto por defecto: 5001)

Este servicio se encarga de la persistencia de los datos de los clientes. En esta implementación, simula un almacenamiento con archivos JSON locales.

* **Endpoints Principales:**
    * `POST /archivos`: Guarda o actualiza el archivo JSON de un cliente.
    * `GET /archivos/<nombre_cliente>`: Obtiene el archivo JSON de un cliente.
    * `GET /archivos`: Lista los nombres de todos los archivos de clientes.
    * `DELETE /archivos/<nombre_cliente>`: Elimina el archivo JSON de un cliente.

## Configuración y Ejecución del Sistema Localmente

Para poner en marcha y probar la aplicación en tu máquina local:

1.  **Requisitos Previos:**
    * **Python 3.8+** (con `pip` instalado).
    * **Git**.
    * **Visual Studio Code** (recomendado, con las extensiones `Python` y `Pylance` para una mejor experiencia de desarrollo).

2.  **Clonar el Repositorio:**
    ```bash
    git clone [https://github.com/flinoz/sky-customer-app-v2.git](https://github.com/flinoz/sky-customer-app-v2.git)
    cd sky-customer-app-v2
    ```

3.  **Crear y Activar un Entorno Virtual:**
    Es **crucial** trabajar dentro de un entorno virtual para aislar las dependencias del proyecto.

    ```bash
    python -m venv venv
    ```

    *Luego, **activa el entorno virtual en cada terminal nueva** que abras para ejecutar los servicios o las pruebas.*
    * **En Windows (PowerShell/CMD):**
        ```powershell
        & .\venv\Scripts\activate
        ```
    * **En macOS/Linux (Bash/Zsh) o Git Bash en Windows:**
        ```bash
        source venv/bin/activate
        ```
    * **Recomendación en VS Code:** Una vez creado el `venv`, presiona `Ctrl+Shift+P`, busca `Python: Select Interpreter` y selecciona el intérprete `venv`. VS Code activará automáticamente el entorno en las nuevas terminales.

4.  **Instalar Dependencias de Python:**
    Asegúrate de que tu entorno virtual esté activo para instalar las dependencias correctamente.

    ```bash
    # Para customer_service
    cd customer_service
    pip install -r requirements.txt
    
    # Vuelve a la raíz del proyecto
    cd ..
    
    # Para storage_service
    cd storage_service
    pip install -r requirements.txt
    
    # Vuelve a la raíz del proyecto
    cd ..
    ```

5.  **Arrancar los Microservicios (en Terminales Separadas):**
    Cada microservicio debe ejecutarse en su propia terminal. Asegúrate de activar el entorno virtual en cada una.

    * **Terminal 1 (para `storage_service` - Puerto 5001):**
        ```bash
        # Asegúrate de que (venv) esté activo
        cd storage_service
        python app.py
        ```
        *Verás `* Running on http://127.0.0.1:5001`.*

    * **Terminal 2 (para `customer_service` - Puerto 5002):**
        ```bash
        # Asegúrate de que (venv) esté activo
        cd customer_service
        python app.py
        ```
        *Verás `* Running on http://127.0.0.1:5002`.*

    Deja ambas terminales ejecutándose.

### **6. Realizar Pruebas del Sistema (en una Tercera Terminal)**

Con ambos servicios corriendo, abre una **tercera terminal** en VS Code. Activa el entorno virtual en ella.

**¡Importante para PowerShell\!** Los comandos `curl` con múltiples opciones (`-H`, `-d`) deben escribirse en **una sola línea** en PowerShell. Los saltos de línea con `\` no funcionan como en Bash.

#### **6.1. Crear un Nuevo Cliente (`POST /clientes`)**

```powershell
curl -X POST [http://127.0.0.1:5002/clientes](http://127.0.0.1:5002/clientes) -H "Content-Type: application/json" -d '{"nombre": "Maria Lopez", "contacto": "maria.lopez@sky.com", "servicio": "Paquete Premium TV"}'
Salida esperada: {"message": "Cliente Maria Lopez guardado/actualizado.", "status": "ok"}

6.2. Intentar Crear el Mismo Cliente (Verificar Duplicados)
PowerShell

curl -X POST [http://127.0.0.1:5002/clientes](http://127.0.0.1:5002/clientes) -H "Content-Type: application/json" -d '{"nombre": "Maria Lopez", "contacto": "maria.lopez@sky.com", "servicio": "Otro Servicio"}'
Salida esperada: {"error": "El cliente 'Maria Lopez' ya existe."}

6.3. Obtener Información de un Cliente Específico (GET /clientes/<nombre>)
PowerShell

curl [http://127.0.0.1:5002/clientes/Maria%20Lopez](http://127.0.0.1:5002/clientes/Maria%20Lopez)
Salida esperada (ejemplo JSON):

JSON

{
    "contacto": "maria.lopez@sky.com",
    "nombre": "Maria Lopez",
    "servicios": [
        {
            "descripcion": "Paquete Premium TV",
            "fecha_contratacion": "YYYY-MM-DD"
        }
    ]
}
6.4. Agregar un Nuevo Servicio a un Cliente Existente (POST /clientes/<nombre>/servicios)
PowerShell

curl -X POST [http://127.0.0.1:5002/clientes/Maria%20Lopez/servicios](http://127.0.0.1:5002/clientes/Maria%20Lopez/servicios) -H "Content-Type: application/json" -d '{"servicio": "Internet Fibra 1Gbps"}'
Salida esperada: {"message": "Cliente Maria Lopez guardado/actualizado.", "status": "ok"} (Puedes repetir la prueba 6.3 para verificar el nuevo servicio).

6.5. Modificar el Contacto de un Cliente Existente (PUT /clientes/<nombre>)
PowerShell

curl -X PUT [http://127.0.0.1:5002/clientes/Maria%20Lopez](http://127.0.0.1:5002/clientes/Maria%20Lopez) -H "Content-Type: application/json" -d '{"contacto": "nuevo.contacto@sky.com"}'
Salida esperada: {"message": "Cliente Maria Lopez actualizado.", "status": "ok"} (Puedes repetir la prueba 6.3 para verificar el contacto actualizado).

6.6. Listar Todos los Clientes (GET /clientes)
PowerShell

curl [http://127.0.0.1:5002/clientes](http://127.0.0.1:5002/clientes)
Salida esperada (ejemplo): ["Maria Lopez"]

6.7. Probar el Endpoint de Saludo/Mejora (GET /saludo)
PowerShell

curl [http://127.0.0.1:5002/saludo](http://127.0.0.1:5002/saludo)
Salida esperada: {"message": "Hola desde Sky App v2.0 mejorada!"}

6.8. (Opcional) Eliminar un Cliente (Directo al storage_service)
PowerShell

curl -X DELETE [http://127.0.0.1:5001/archivos/Maria%20Lopez](http://127.0.0.1:5001/archivos/Maria%20Lopez)
Salida esperada: {"message": "Cliente Maria Lopez eliminado.", "status": "ok"} (Tras esto, las búsquedas de "Maria Lopez" deberían resultar en "Cliente no encontrado").

Evidencia Visual del Funcionamiento del Sistema
Aquí se muestran capturas de pantalla que verifican el correcto funcionamiento de los microservicios y sus interacciones.

Evidencia 1: Instalando Dependencias
Descripción: Muestra la instalación de los paquetes de Python (Flask, requests, etc.) usando pip install -r requirements.txt dentro del entorno virtual.

Evidencia 2: Servicio Corriendo (Customer Service)
Descripción: Muestra la terminal con el customer_service (app.py) ejecutándose y escuchando en el puerto 5002.

Evidencia 3: Servicio Corriendo (Storage Service)
Descripción: Muestra la segunda terminal con el storage_service (app.py) ejecutándose y escuchando en el puerto 5001.

Evidencia 4: Probando el Funcionamiento del Sistema (Consultas)
Descripción: Muestra la tercera terminal realizando consultas curl (como POST para crear un cliente y GET para consultarlo) con sus respuestas JSON exitosas.

Despliegue en AWS EC2 (Entorno de Producción)
La aplicación está diseñada para desplegarse en una instancia Amazon Linux 2 EC2 (t2.micro).

Configuración en EC2:

Instalación de Python 3, pip, git, gunicorn, nginx.

Clonación del repositorio en /home/ec2-user/sky-customer-app-v2.

Configuración de customer_service.service y storage_service.service con systemd para ejecución persistente con Gunicorn en los puertos 5002 y 5001 respectivamente.

Configuración opcional de Nginx como proxy inverso para redirigir el tráfico del puerto 80 al customer_service (puerto 5002).

URL de Acceso: http://<IP_PUBLICA_DE_TU_INSTANCIA_EC2> (si Nginx está configurado).

Gestión de Acceso con IAM:

Se creó un grupo IAM SkyApp_DevTeam con políticas de acceso adecuadas para EC2, S3 (potencialmente) y CloudWatch.

Se crearon usuarios específicos para roles de desarrollo, TI y soporte, asignados a este grupo.

Acceso para el Evaluador: Un usuario IAM dedicado (Evaluator_SkyApp) con AdministratorAccess se proporciona para una revisión completa de la infraestructura.

GitHub Actions (CI/CD)
Los workflows se encuentran en la carpeta .github/workflows/.

ci.yml: Se ejecuta en cada push o Pull Request, instalando dependencias, realizando pruebas de sintaxis básicas y verificando que los microservicios pueden iniciar.

deploy_production.yml: Workflow manual que se activa desde la interfaz de GitHub para desplegar la última versión de la rama main en la instancia EC2. Requiere que se configuren AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, EC2_PUBLIC_IP y SSH_PRIVATE_KEY como Secrets del repositorio.

handle_issues.yml: Asigna etiquetas automáticamente (ej. bug, feature) y añade un comentario de bienvenida a los nuevos issues.

code_review_required.yml: Emite un recordatorio en los Pull Requests para asegurar que se realicen revisiones de código.

Demostración de Versionamiento y Recuperación
El proyecto incluye una demostración de cómo el control de versiones con Git/GitHub permite:

Introducir un cambio (una nueva funcionalidad o incluso un error).

Desplegar ese cambio.

Si surge un problema, utilizar git revert para deshacer un commit problemático.

Volver a desplegar una versión funcional anterior en producción, minimizando el tiempo de inactividad.

Licencia
Este proyecto está bajo la Licencia MIT. Para más detalles, consulta el archivo LICENSE en la raíz de este repositorio.

Enlaces del Proyecto
URL de este Repositorio GitHub: https://github.com/flinoz/sky-customer-app-v2


Contacto
Para preguntas o comentarios, por favor abre un issue en este repositorio o contacta a: FLINOZ91@GMAIL.COM