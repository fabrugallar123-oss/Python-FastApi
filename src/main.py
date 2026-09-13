
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from src.models.db import (Juego,)

from src.routers.path import videojuegos_router
from src.routers.saludar import saludar_routers



app = FastAPI(  )
app.title = "PRACTICO N° 4"


Base.metadata.create_all(bind=engine)



app.include_router(videojuegos_router)
app.include_router(saludar_routers)
#######falta hacer los path operation