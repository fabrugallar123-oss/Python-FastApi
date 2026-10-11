
from fastapi import FastAPI
from routers.path import videojuegos_router, desarrolladoras_router

app = FastAPI(
    title="API de Videojuegos y Desarrolladoras",
    description="TP de FastAPI + SQLModel + Alembic",
    version="1.0.0"
)


app.include_router(videojuegos_router)
app.include_router(desarrolladoras_router)

@app.get("/")
def home():
    return {"mensaje": "API funcionando correctamente con SQLModel y Alembic"}