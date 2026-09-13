

from typing import Annotated
from pydantic import Field

nomb = Annotated[str, Field(min_length=2, max_length=35, description= "Nombre del Juego")]
precioVent = Annotated[float, Field(gt=500, lt=999999, description="Precio del Juego")]
BoolActivo = Annotated[bool, Field(description="Sigue disponible?")]
Tipo = Annotated[str, Field(min_length=2, max_length=35, description="Para q consola/plataforma es")]
intPositivo = Annotated[int, Field(gt=0)] 