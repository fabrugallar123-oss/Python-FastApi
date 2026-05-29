from fastapi import FastAPI, Body, Path, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()
app.title= "Mi primera API"
app.version = "1.0"


videojuegos = [
    {"id": 1, "nombre": "God of War Ragnarok", "precio":50000},
    {"id": 2, "nombre": "Ghost of Tsushima", "precio": 45000},
    {"id": 3, "nombre": "EA Sport FC 25", "precio": 30000}]


class Videojuego(BaseModel):
    id: Annotated[int, Field(gt=0)]
    nombre: Annotated[
        str,
        Field(min_length=3, max_length=30)
    ]
    precio: Annotated[int, Field(gt=0)]


#GET para todos
@app.get("/videojuegos",response_model=list[Videojuego])
async def get_videojuegos():
    return videojuegos

#GET por ID
@app.get(
        "/videojuegos/{id}",
          response_model=Videojuego,
          responses={
        404: {
            "description": "Videojuego no encontrado"
        }
    }
)
def get_videojuego(
    id: Annotated[int, Path(gt=0)]
):
    for v in videojuegos:
        if v["id"] == id:
            return v
    raise HTTPException(
        status_code= 404,
        detail="No existe")


#crear un videojuego
@app.post("/videojuegos", response_model=list[Videojuego])
def crear_videojuego(
    juego:Videojuego
):
    videojuegos.append(juego.model_dump())

    return videojuegos


#editar videojuego:
@app.put("/videojuegos/{id}",
          response_model=Videojuego,
          responses={
        404: {
            "description": "Videojuego no encontrado"
        }
    }
)

def editar_videojuego(
    id: Annotated[int, Path(gt=0)],
    nombre: str = Body(),
    precio: int = Body()
):
    for jueg in videojuegos:
        if jueg["id"] == id:
            jueg["nombre"] = nombre
            jueg["precio"] = precio
            return jueg
    raise HTTPException(
        status_code= 404,
        detail="No existe")


#eliminar videojuego
@app.delete("/videojuego/{id}",
            responses={
                404:{
                    "description": "Videojuego no encontrado"
                }
            }
)
def eliminar_videojuego(id: Annotated[int, Path(gt=0)]):
    
    for v in videojuegos:
        if v["id"] == id:
            videojuegos.remove(v)
            return {
                "videojuego eliminado": videojuegos
                }
        
    raise HTTPException(
        status_code= 404,
        detail= "El videjuego no existe"
    )

#model_dump() se usa para convertir el objeto de Pydantic
#en un diccionario normal de Python, así todos los datos
#quedan con el mismo formato dentro de la lista.

#Usamos model_dump() porque la lista videojuegos
#guarda diccionarios, no objetos Pydantic.