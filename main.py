from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum, auto
from typing import List
from datetime import date

# Implementación del enum propuesto en el modelo
class Material(Enum):
    BRONCE = auto()
    PLATA = auto()
    ORO = auto()

# Implementación del modelo propuesto
class Caballero(BaseModel):
    id: int
    name: str
    material: Material
    attack: int
    constelation: str

app = FastAPI(title="API Caballeros del Zodiaco")

# Base de datos simulada en memoria
db_caballeros: List[Caballero] = []

# ==========================================
# ENDPOINTS
# ==========================================

# 1. Función para mostrar todos los caballeros
@app.get("/caballeros", response_model=List[Caballero], tags=["Caballeros"])
def get_all_caballeros():
    return db_caballeros

# Endpoint extra para poder crear caballeros y probar la API
@app.post("/caballeros", response_model=Caballero, tags=["Caballeros"])
def create_caballero(caballero: Caballero):
    db_caballeros.append(caballero)
    return caballero

# 2. Función showCaballero implementada en un endpoint
@app.get("/caballeros/{caballero_id}", response_model=Caballero, tags=["Caballeros"])
def show_caballero(caballero_id: int):
    for c in db_caballeros:
        if c.id == caballero_id:
            return c
    raise HTTPException(status_code=404, detail="Caballero no encontrado")

# 3. Función showConstelacion implementada en un endpoint
@app.get("/caballeros/{caballero_id}/constelation", tags=["Caballeros"])
def show_constelation(caballero_id: int):
    for c in db_caballeros:
        if c.id == caballero_id:
            return {"caballero": c.name, "constelation": c.constelation}
    raise HTTPException(status_code=404, detail="Caballero no encontrado")

# 4. Función fightCaballero implementada en un endpoint
@app.post("/caballeros/{caballero_id}/fight", tags=["Batallas"])
def fight_caballero(caballero_id: int, enemy_id: int):
    caballero1 = next((c for c in db_caballeros if c.id == caballero_id), None)
    caballero2 = next((c for c in db_caballeros if c.id == enemy_id), None)
    
    if not caballero1 or not caballero2:
        raise HTTPException(status_code=404, detail="Ambos caballeros deben existir para pelear")
        
    if caballero1.attack > caballero2.attack:
        winner = caballero1.name
    elif caballero2.attack > caballero1.attack:
        winner = caballero2.name
    else:
        winner = "Empate (Milagro cósmico)"
        
    return {
        "fighter_1": caballero1.name, 
        "fighter_2": caballero2.name, 
        "winner": winner
    }

# 5. Función showYourCaballero implementada en un endpoint
@app.get("/caballeros/your/{birth_date}", tags=["Extras"])
def show_your_caballero(birth_date: date):
    # Lógica simulada: te asigna un caballero dependiendo de si hay datos
    if db_caballeros:
        # Aquí podrías poner lógica real de signos zodiacales según la fecha
        asignado = db_caballeros[0] 
        return {"birth_date": birth_date, "your_caballero_is": asignado.name}
    return {"message": "La orden de Atena aún no tiene caballeros registrados"}