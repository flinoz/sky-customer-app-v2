# Sky App v2.0 - Sistema de Gestión de Clientes

![Sky App v2.0 Logo](img/LOGO.PNG)

## Descripción General del Proyecto

`Sky App v2.0` es un sistema de gestión de clientes con arquitectura de microservicios en Python (Flask). Demuestra Diseño Basado en Domininios (DDD) y un pipeline DevOps completo (CI/CD con GitHub Actions, despliegue en AWS EC2). Permite operaciones CRUD sobre clientes y sus servicios.

## Características Clave

* **Arquitectura de Microservicios:** `customer_service` y `storage_service` desacoplados.
* **API RESTful:** Interfaz HTTP para la gestión de clientes.
* **Despliegue en AWS EC2:** Alojado en instancia Amazon Linux 2 EC2 (`t2.micro`).
* **CI/CD con GitHub Actions:** Automatización de pruebas, despliegues y gestión de issues/Pull Requests.
* **Control de Versiones Robusto:** Gestión con Git y GitHub, incluyendo recuperación por reversión.
* **Gestión de Acceso IAM:** Control granular de permisos en AWS.

## Estructura del Repositorio

sky-customer-app-v2/ ├── .github/ # Workflows de GitHub Actions ├── customer_service/ # Microservicio de clientes ├── storage_service/ # Microservicio de almacenamiento ├── .gitignore # Archivo para ignorar en Git ├── README.md # Este archivo ├── LICENSE # Licencia MIT └── img/ # Imágenes (logo y evidencias) ├── LOGO.PNG ├── EVI01.png ├── EVI02.png ├── EVI03.png └── EVI04.png


## Configuración y Ejecución Local

1.  **Requisitos:** Python 3.8+, Git, VS Code (opcional).
2.  **Clonar:** `git clone https://github.com/flinoz/sky-customer-app-v2.git`
3.  **Entorno Virtual:**
    ```bash
    python -m venv venv
    # Windows: & .\venv\Scripts\activate
    # Linux/macOS: source venv/bin/activate
    ```
4.  **Instalar Dependencias:**
    ```bash
    cd customer_service && pip install -r requirements.txt && cd ..
    cd storage_service && pip install -r requirements.txt && cd ..
    ```
5.  **Arrancar Servicios (en terminales separadas):**
    ```bash
    # Terminal 1:
    cd storage_service && python app.py
    # Terminal 2:
    cd customer_service && python app.py
    ```

## Evidencia Visual del Funcionamiento del Sistema

Aquí se muestran capturas de pantalla que verifican el correcto funcionamiento de los microservicios y sus interacciones.

### **Evidencia 1: Instalando Dependencias**
Descripción: Muestra la instalación de los paquetes de Python (Flask, requests, etc.) usando `pip install -r requirements.txt` dentro del entorno virtual.
![Evidencia 1 - Instalando Dependencias](img/EVI01.png)

### **Evidencia 2: Servicio Corriendo (Customer Service)**
Descripción: Muestra la terminal con el `customer_service` (app.py) ejecutándose y escuchando en el puerto 5002.
![Evidencia 2 - Customer Service Corriendo](img/EVI02.png)

### **Evidencia 3: Servicio Corriendo (Storage Service)**
Descripción: Muestra la segunda terminal con el `storage_service` (app.py) ejecutándose y escuchando en el puerto 5001.
![Evidencia 3 - Storage Service Corriendo](img/EVI03.png)

### **Evidencia 4: Probando el Funcionamiento del Sistema (Consultas)**
Descripción: Muestra la tercera terminal realizando consultas `curl` (como POST para crear un cliente y GET para consultarlo) con sus respuestas JSON exitosas.
![Evidencia 4 - Probando con cURL](img/EVI04.png)

## Despliegue en AWS EC2 (Entorno de Producción)

Configurado para desplegarse en una instancia **Amazon Linux 2 EC2** (`t2.micro`).
Incluye configuración de `systemd` (con Gunicorn), Nginx (opcional) y gestión de acceso con **IAM** (grupos y usuarios específicos, incluyendo un `Evaluator_SkyApp` con `AdministratorAccess`).

## GitHub Actions (CI/CD)

Workflows ubicados en `.github/workflows/`:
* **`ci.yml`**: Integración Continua (pruebas y verificación de inicio).
* **`deploy_production.yml`**: Despliegue Continuo manual a EC2 (requiere Secrets).
* **`handle_issues.yml`**: Automatización para gestión de `issues`.
* **`code_review_required.yml`**: Recordatorios para revisión de código.

## Demostración de Versionamiento y Recuperación

El proyecto demuestra el uso de Git (`git revert`) para la recuperación de desastres y la gestión de versiones.

## Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE).

## Enlaces del ProyectO

* **Repositorio GitHub:** `https://github.com/flinoz/sky-customer-app-v2`

## Contacto

FLINOZ91@GMAIL.COM o abre un `issue` en el repositorio.
