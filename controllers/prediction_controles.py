from pydantic import BaseModel

class Pred(BaseModel):
    Uso_CPU: float
    Uso_Memoria: float
    Numero_Hilos: float
    Tiempo_Ejecucion: float
    Numero_Errores: float
    Aplicación: bool
    Servicio: bool
    Sistema: bool