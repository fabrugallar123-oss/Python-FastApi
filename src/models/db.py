

from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

from src.schema.modularizacion import nomb, precioVent, BoolActivo, Tipo, intPositivo


#Tabla Padre
class DesarrolladoraBase(SQLModel):
    nombre: str = Field(min_length=2, max_length=50)
    pais: str = Field(min_length=2, max_length=50)


class Desarrolladora(DesarrolladoraBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    #relacion 1 a N:
    juegos: list["Juego"] = Relationship(back_populates="desarrolladora")


#Tabla Hija con Foreign Key
class JuegoBase(SQLModel):
    nombre: nomb
    tipo_de_consola: Tipo
    precio: precioVent
    activo: BoolActivo = True
    
    # FOREIGN KEY hacienda referencia a la tabla Desarrolladora
    desarrolladora_id: Optional[int] = Field(default=None, foreign_key="desarrolladora.id")

class Juego(JuegoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relación inversa
    desarrolladora: Optional[Desarrolladora] = Relationship(back_populates="juegos")


#SCHEMAS PARA DATOS ANIDADOS
# Sirven para cuando FastAPI devuelve una Desarrolladora CON la lista de sus Juegos adentro,
# o un Juego CON los datos de su Desarrolladora adentro.

class JuegoRead(JuegoBase):
    id: int

class DesarrolladoraRead(DesarrolladoraBase):
    id: int

# --- Schemas Anidados ---

class JuegoReadConDesarrolladora(JuegoRead):
    desarrolladora: Optional[DesarrolladoraRead] = None

class DesarrolladoraReadConJuegos(DesarrolladoraRead):
    juegos: list[JuegoRead] = []