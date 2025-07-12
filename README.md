# API de Predicción de Procesos con Machine Learning

## 📋 Propósito del Proyecto

Esta API REST desarrollada con FastAPI permite predecir si un proceso del sistema es problemático o no problemático basándose en métricas de rendimiento como uso de CPU, memoria, hilos, tiempo de ejecución y número de errores. Utiliza un modelo de Machine Learning pre-entrenado (LightGBM) para realizar las predicciones y almacena los resultados en una base de datos PostgreSQL.

## ✨ Características

- **Predicción en tiempo real** de procesos problemáticos
- **API REST completa** con operaciones CRUD
- **Modelo ML pre-entrenado** (LightGBM) para clasificación binaria
- **Base de datos PostgreSQL** para persistencia de datos
- **Arquitectura modular** con separación de responsabilidades
- **Containerización** con Docker

## 🚀 Instrucciones de Despliegue

1. **Crear la red de Docker:**
   ```bash
   docker network create pred-api-net
   ```

2. **Construir la imagen de la API:**
   ```bash
   docker build -t predmod-api .
   ```

3. **Ejecutar el contenedor de PostgreSQL:**
   ```bash
   docker run --name postgres-db --network pred-api-net \
     -e POSTGRES_PASSWORD=p4ssw0rd \
     -p 5432:5432 -d postgres:latest
   ```

4. **Crear la tabla en PostgreSQL:**
   Conectate a la base de datos con el cliente de tu preferencia y ejecuta:

   ```SQL
   CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    Uso_CPU FLOAT,
    Uso_Memoria FLOAT,
    Numero_Hilos FLOAT,
    Tiempo_Ejecucion FLOAT,
    Numero_Errores FLOAT,
    Aplicacion BOOLEAN,
    Servicio BOOLEAN,
    Sistema BOOLEAN,
    pred TEXT
   );
   ```

5. **Ejecutar el contenedor del API:**
   ```bash
   docker run --name pred-api --network pred-api-net \
     -p 8000:8000 -d predmod-api:latest
   ```

## 📡 Endpoints Principales

### Predicción
- **POST** `/predict` - Realizar nueva predicción
  ```json
  {
    "Uso_CPU": 0.75,
    "Uso_Memoria": 0.60,
    "Numero_Hilos": 4.0,
    "Tiempo_Ejecucion": 120.5,
    "Numero_Errores": 2.0,
    "Aplicación": true,
    "Servicio": false,
    "Sistema": false
  }
  ```

### Consultas
- **GET** `/predictions` - Obtener todas las predicciones
- **GET** `/predictions/{id}` - Obtener predicción por ID

### Actualización y Eliminación
- **PUT** `/predict/{id}` - Actualizar predicción existente
- **DELETE** `/delete/{id}` - Eliminar predicción

### Documentación
- **GET** `/docs` - Documentación interactiva Swagger
- **GET** `/redoc` - Documentación ReDoc

## 📁 Estructura del Proyecto

```
Modulo 6 - API modelo ML/
├── controllers/                 # Controladores y modelos Pydantic
│   ├── __init__.py
│   └── prediction_controles.py  # Modelo Pred para validación
├── models/                      # Carga y gestión del modelo ML
│   ├── __init__.py
│   └── models.py               # Carga del modelo LightGBM
├── .gitignore                  # Archivos ignorados por Git
├── Dockerfile                  # Imagen de la API
├── main.py                     # Aplicación principal FastAPI
├── model.pkl                   # Modelo ML pre-entrenado
├── requirements.txt            # Dependencias Python
└── README.md                   # Este archivo
```

## 🗄️ Esquema de Base de Datos

La tabla `predictions` contiene:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL PRIMARY KEY | Identificador único |
| Uso_CPU | FLOAT | Porcentaje de uso de CPU |
| Uso_Memoria | FLOAT | Porcentaje de uso de memoria |
| Numero_Hilos | FLOAT | Número de hilos del proceso |
| Tiempo_Ejecucion | FLOAT | Tiempo de ejecución en segundos |
| Numero_Errores | FLOAT | Cantidad de errores registrados |
| Aplicacion | BOOLEAN | Si es proceso de aplicación |
| Servicio | BOOLEAN | Si es proceso de servicio |
| Sistema | BOOLEAN | Si es proceso del sistema |
| pred | TEXT | Resultado: "Proceso problemático" o "Proceso no problemático" |

## 🔧 Tecnologías Utilizadas

- **FastAPI** - Framework web moderno para APIs
- **LightGBM** - Modelo de Machine Learning
- **PostgreSQL** - Base de datos relacional
- **Pydantic** - Validación de datos
- **Docker** - Containerización
- **Uvicorn** - Servidor ASGI

## 📊 Rangos de Datos del Modelo

El modelo espera valores en los siguientes rangos:
- **Uso_CPU**: (-1.7337, 1.7314)
- **Uso_Memoria**: (-1.7312, 1.7348)
- **Numero_Hilos**: (-1.6983, 1.6939)
- **Tiempo_Ejecucion**: (-1.7324, 1.7329)
- **Numero_Errores**: (-2.2367, 6.2568)
- **Aplicación, Servicio, Sistema**: Boolean (True/False)

## 🛠️ Configuración

### Credenciales por defecto de Base de Datos

- **Usuario**: postgres
- **Contraseña**: p4ssw0rd
- **Base de datos**: postgres
- **Puerto**: 5432

## 🚨 Notas Importantes

1. **Modelo ML**: El archivo `model.pkl` debe estar presente en el directorio raíz. Para consultar el código fuente de entrenamiento del algoritmo visita: 
2. **Compatibilidad**: Probado con Python 3.11.
3. **Seguridad**: Cambiar credenciales por defecto en producción.
4. **Logs**: Los logs se muestran en la consola del contenedor.
5. **Futuras actualizaciones**: La siguiente versión incluirá una opción de despliegue con Docker Compose.