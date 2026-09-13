#aca se creara el base model, q validara los datos de entrada 

from typing import Annotated
from pydantic import BaseModel, ConfigDict

from .modularizacion import nomb, precioVent, BoolActivo, Tipo, intPositivo

class VideojuegoSchema(BaseModel):#estos datos son los q nos va pedir Fastapi a la hora de crear/guardar
    nombre : nomb
    tipo_de_consola : Tipo
    precio : precioVent
    activo : BoolActivo = True

class juegoSchema(VideojuegoSchema):    
    id : intPositivo

    model_config = ConfigDict(from_attributes=True)
#from_atributes = True --> Permite que Pydantic lea directamente los objetos de SQLAlchemy
#ya q SQLAlchemy devuelve objetos, no diccionarios esto permite extraer atributos