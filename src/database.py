#se define toda la configueracion necesaria para q la Api de comunique con la db 

"""SQLALchemy:
Engine= El motor, 
Sesion= ida y vuelta, lo usa la Api para buscar y traer datos
models= Definimos las tablas de la db
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

url = "sqlite:///./base_db.db"

engine = create_engine(url, connect_args = {"check_same_thread":False})
#check_same_thread":False --> indica q no se fije si las peticiones viene de un solo hilo

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#es la encargada de usar el engine para obtener o hacer cambion en la db(ida y vuelta)
#autocommit persistir por cada min interaccion

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db  #return que NO termina la función /*== a return, pero permite seguir ejecutando*/
    finally:
        db.close()