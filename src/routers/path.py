
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel import Session, select
from database import get_db

from models.db import (
    Juego,
    JuegoBase, 
    JuegoRead, 
    JuegoReadConDesarrolladora, 
    Desarrolladora, 
    DesarrolladoraBase, 
    DesarrolladoraReadConJuegos,
    DesarrolladoraRead
)


videojuegos_router = APIRouter(prefix="/juegos", tags=["juegos"]
)

desarrolladoras_router = APIRouter(prefix="/desarrolladoras", tags=["desarrolladoras"]
)


@videojuegos_router.get("/", response_model=list[JuegoReadConDesarrolladora])
async def get_videojuegos(db: Session = Depends(get_db)):
    # En SQLModel se usa select() en lugar de db.query()
    videojuegos = db.exec(select(Juego)).all()
    return videojuegos


# GET por ID
@videojuegos_router.get("/{id}", response_model=JuegoReadConDesarrolladora)
async def get_videojuego_id(
    id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db)
):
    videojuego_obtenido = db.get(Juego, id)
    if not videojuego_obtenido:
        raise HTTPException(
            status_code=404,
            detail="Videojuego no encontrado"
        )
    return videojuego_obtenido


# POST (Crear juego)
@videojuegos_router.post("/", response_model=JuegoRead)
async def post_videojuego(
    juego: JuegoBase, 
    db: Session = Depends(get_db)
):
    # Convertimos el schema base en un objeto de la DB
    juego_db = Juego.model_validate(juego)
    db.add(juego_db)
    db.commit()
    db.refresh(juego_db)
    return juego_db


# PUT (Editar juego)
@videojuegos_router.put("/{id}", response_model=JuegoRead)
async def put_videojuego(
    id: Annotated[int, Path(gt=0)],
    juego_update: JuegoBase,
    db: Session = Depends(get_db)
):
    juego_db = db.get(Juego, id)
    if not juego_db:
        raise HTTPException(
            status_code=404, 
            detail=f"Juego con id {id} no encontrado"
        )

    # Actualización simplificada con SQLModel
    datos_actualizado = juego_update.model_dump(exclude_unset=True)
    for clave, valor in datos_actualizado.items():
        setattr(juego_db, clave, valor)

    db.add(juego_db)
    db.commit()
    db.refresh(juego_db)
    return juego_db


# DELETE
@videojuegos_router.delete("/{id}")
async def delete_videojuego(
    id: Annotated[int, Path(gt=0)], 
    db: Session = Depends(get_db)
):
    juego_db = db.get(Juego, id)
    if not juego_db:
        raise HTTPException(
            status_code=404, 
            detail=f"No se puede borrar el juego con id:{id}, porque no fue encontrado"
        )

    db.delete(juego_db)
    db.commit()
    return {"mensaje": f"El videojuego con ID {id} fue eliminado correctamente"}



#crear DESARROLLADORA
@desarrolladoras_router.post("/", response_model=DesarrolladoraRead)
async def post_desarrolladora(
    desarrolladora: DesarrolladoraBase,
    db: Session = Depends(get_db)
):
    desarrolladora_db = Desarrolladora.model_validate(desarrolladora)

    db.add(desarrolladora_db)
    db.commit()
    db.refresh(desarrolladora_db)

    return desarrolladora_db


#GET: consultar una desarrolladora con sus videojuegos
@desarrolladoras_router.get(
    "/{id}",
    response_model=DesarrolladoraReadConJuegos
)
async def get_desarrolladora_id(
    id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db)
):
    desarrolladora_db = db.get(Desarrolladora, id)

    if not desarrolladora_db:
        raise HTTPException(
            status_code=404,
            detail="Desarrolladora no encontrada"
        )

    return desarrolladora_db