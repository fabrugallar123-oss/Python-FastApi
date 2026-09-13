#aca se van a crear las tablas-columnas-filas q va tener la base de dato

from database import Base

from sqlalchemy import Column, Integer, String, Float, Boolean

class Juego(Base):
    __tablename__ = "Juego"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key= True, )
    nombre = Column(String)
    tipo_de_consola = Column(String)
    precio = Column(Float)
    activo = Column(Boolean, default=True)
    