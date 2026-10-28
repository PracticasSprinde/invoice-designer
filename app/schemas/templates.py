from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any # Cualquier tipo

# Modelo de la plantilla que envia el usuario
class TemplateCreate(BaseModel):
    name: str = Field(min_length=1)
    layout: dict[str, Any] = {} # Opcional


# Hereda de TemplateCreate
# Servidor añade id y fecha de creación a la plantilla
class Template(TemplateCreate):
    template_id: int
    created_at: datetime = Field(default_factory = datetime.now) # Añade fecha en momento de creación
