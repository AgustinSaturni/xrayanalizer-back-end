# xrayanalizer-back-end

## 🚀 Función

Servicio desarrollado con **FastAPI** para brindar soporte al frontend de la aplicación **XRayAnalizer**, encargado de procesar solicitudes y comunicarse con la base de datos.

---

## 🧪 ¿Cómo levantarlo localmente?

1. Clonar el repositorio:
   ```bash
   git clone <URL_DEL_REPO>
   cd xrayanalizer-back-end

2. Crear un entorno virtual:
   ```bash
    python3 -m venv venv

3. Activar el entorno virtual:
   ```bash
    source venv/bin/activate  # En Linux/Mac
    venv\Scripts\activate     # En Windows

4. Activar el entorno virtual:
   ```bash
   pip install -r requirements.txt

5. Ejecutar el servidor de desarrollo:
   ```bash
   uvicorn main:app --reload
