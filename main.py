from fastapi import FastAPI
import psycopg2
import os
from controllers.prediction_controles import Pred
from models.models import ml_model

p_meaning = {0: "Proceso no problemático", 1: "Proceso problemático"}
db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'p4ssw0rd',
    'host': 'postgres-db',
    'port': '5432',
}

app = FastAPI()

conn = psycopg2.connect(**db_params)

app = FastAPI()

# Uso_CPU (-1.7337, 1.7314), Uso_Memoria (-1.7312, 1.7348), Numero_Hilos (-1.6983, 1.6939), Tiempo_Ejecucion (-1.7324, 1.7329), Numero_Errores (-2.2367, 6.2568), Aplicación (False, True), Servicio (False, True), Sistema (False, True)
@app.post("/predict")
def predict(data: Pred):
    prediction = ml_model.predict([[data.Uso_CPU, data.Uso_Memoria, data.Numero_Hilos, data.Tiempo_Ejecucion, data.Numero_Errores, data.Aplicación, data.Servicio, data.Sistema]])
    meaning = p_meaning[prediction[0]]
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO predictions (Uso_CPU, Uso_Memoria, Numero_Hilos, Tiempo_Ejecucion, Numero_Errores, Aplicacion, Servicio, Sistema, pred) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (data.Uso_CPU, data.Uso_Memoria, data.Numero_Hilos, data.Tiempo_Ejecucion, data.Numero_Errores, data.Aplicación, data.Servicio, data.Sistema, meaning)
    )
    conn.commit()
    cur.close()
    return {"prediction": meaning}

@app.get("/predictions")
def read_items():
    cur = conn.cursor()
    cur.execute("SELECT * FROM predictions")
    rows = cur.fetchall()
    cur.close()
    return {"predictios": rows}

@app.get("/predictions/{id}")
def read_items(id: int):
    cur = conn.cursor()
    cur.execute("SELECT * FROM predictions WHERE id = %s", (id,))
    row = cur.fetchone()
    cur.close()
    if row is None:
        return {"error": f"No se encontró el registro con id {id}"}
    return {"prediction": {
        "id": row[0], "Uso_CPU": row[1], "Uso_Memoria": row[2], "Numero_Hilos": row[3], "Tiempo_Ejecucion": row[4], "Numero_Errores": row[5], "Aplicación": row[6], "Servicio": row[7],  "Sistema": row[8], "pred": row[9]
    }}

@app.put("/predict/{id}")
def put_item(id: int, prediction: int, data: Pred):
    cur = conn.cursor()
    cur.execute("SELECT id FROM predictions WHERE id = %s", (id,))
    if cur.fetchone() is None:
        cur.close()
        return {"error": f"No se encontró el registro con id {id}"}
    
    meaning = p_meaning[prediction]
    cur.execute(
        "UPDATE predictions SET Uso_CPU = %s, Uso_Memoria = %s, Numero_Hilos = %s, Tiempo_Ejecucion = %s, Numero_Errores = %s, Aplicacion = %s, Servicio = %s, Sistema = %s, pred = %s WHERE id = %s",
        (data.Uso_CPU, data.Uso_Memoria, data.Numero_Hilos, data.Tiempo_Ejecucion, data.Numero_Errores, data.Aplicación, data.Servicio, data.Sistema, meaning, id)
    )
    conn.commit()
    cur.close()
    return {"updated_id": id}

@app.delete("/delete/{id}")
def delete_item(id: int):
    cur = conn.cursor()
    cur.execute("SELECT id FROM predictions WHERE id = %s", (id,))
    if cur.fetchone() is None:
        cur.close()
        return {"error": f"No se encontró el registro con id {id}"}
        
    cur.execute("DELETE FROM predictions WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    return {"deleted_item_id": id}