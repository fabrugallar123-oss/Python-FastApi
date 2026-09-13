from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from database import get_db
from models.db import Juego

from schemas.baseModel import juegoSchema, VideojuegoSchema

videojuegos_router = APIRouter()


#get generico (get.all())
@videojuegos_router.get("/", response_model=list[VideojuegoSchema])
async def get_videojuegos(db: Session = Depends(get_db)):
    videojuegos =db.query(Juego).all()
    return videojuegos


#get especifico (get{id})
@videojuegos_router.get("/{id}",
                        response_model=juegoSchema)

async def get_videojuego_id(
    id: Annotated[int, Path(gt=0)],db: Session = Depends(get_db)):
    videojuego_obtenido = db.get(Juego, id)

    if videojuego_obtenido is not None:
        return videojuego_obtenido
    raise HTTPException(
        status_code= 404,
        detail= "Videojuego no encontrado"
    ) 

#post (crear videojuego)
@videojuegos_router.post("/",
                          response_model=juegoSchema)

async def post_videojuego(
    juego : VideojuegoSchema,
      db: Session = Depends(get_db)):

    juego_db =  Juego(**juego.model_dump())
    db.add(juego_db)
    db.commit()
    db.refresh(juego_db)
    return juego_db


#editar juego (put)
@videojuegos_router.put("/{id}",
                         response_model=juegoSchema)

async def put_videojuego(
    id: Annotated[int,Path(gt=0)],
    juego_update : VideojuegoSchema,
    db: Session = Depends(get_db)
):
#continuar los path(falta terminar put y hacer delete)

    juego_db = db.query(Juego).filter(Juego.id == id).first()#buca en la tabla el primer registro q coincida con el id

    if not juego_db:
        raise HTTPException (
            status_code= 404,
            detail= f"Juego con id {id} no fue encontrado"
                      )

    datos_actualizado = juego_update.model_dump(exclude_unset=True)

    for clave, valor in datos_actualizado.items():
        setattr(juego_db, clave, valor) #Modifica dinámicamente cada atributo del objeto ORM con los nuevos valores del cuerpo enviad en el request

    db.commit()
    db.refresh(juego_db)
    return juego_db 

#borrar juego(delete)

@videojuegos_router.delete("/{id}")
async def delete_videojuego( 
    id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db)
):
    juego_db = db.query(Juego).filter(Juego.id == id).first()

    if not juego_db:
        raise HTTPException(
            status_code= 404,
            detail=f"No se puede borrar el juego con id:{id}, pq no fue encontrado"
        )

    db.delete(juego_db)
    db.commit()

    return {"mensaje": f"El videojuego con ID {id} fue eliminado correctamente"}