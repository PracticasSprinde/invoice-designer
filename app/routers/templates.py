from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any

# Definir rutas
router = APIRouter(prefix="/templates", tags=["Templates"])

# Class de plantilla creada
class TemplateCreate(BaseModel):
    name: str
    layout: dict[str, Any] = {}

# Class de plantilla recuperada
class Template(TemplateCreate):
    template_id: int
    created_at: datetime = Field(default_factory = datetime.now)

template_list: list[Template] = []
next_id = 1

# Metodo para encontrar las plantillas por ID
def find_template(template_id: int) -> Template | None:
    return next((t for t in template_list if t.template_id == template_id), None)

# Obtener todas las plantillas
@router.get("/")
def all_templates():
    if not template_list:
        raise HTTPException(status_code=404, detail="No hay plantillas almacenadas")
    return template_list

# Obtener plantilla por ID
@router.get("/{template_id}")
def find_template(template_id:int):
    template = find_template(template_id)
    if template is None:
        raise HTTPException(status_code=404, detail="No hay ninguna plantilla con el ID proporcionado")
    return template

# Añadir plantilla
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_template(template: Template):
    if find_template(template.template_id):
        raise HTTPException(status_code=409, detail="No se ha podido crear la plantilla")
    template_list.append(template)
    return template

# Modificar plantilla
@router.put("/{template_id}")
def update_template(template_id:int, template:Template):
    for index, saved in enumerate(template_list):
        if saved.template_id == template.template_id:
            template_list[index] = template
            return template
    raise HTTPException(status_code=404, detail="No se ha podido modificar la plantilla")

# Eliminar plantilla
@router.delete("/{template_id}", status_code=status.HTT_204_NO_CONTENT)
def delete_template(template_id:int):
    template = find_template(template_id)
    if template is None:
        raise HTTPException(status_code=404, detail="No se ha podido eliminar la plantilla")
    template_list.remove(template)