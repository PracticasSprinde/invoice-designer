from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.templates_sch import Template as TemplateSchema, TemplateCreate
from app.repositories import templates_repo as templates_repo
from tests.memory_storage import template_list, find_template


# Define ruta
router = APIRouter(prefix="/templates", tags=["Templates"])
router_memory = APIRouter(prefix="/memory/templates", tags=["Templates (memory)"])
next_id = 1

# ================== CONSULTAS API ==================

# Añadir plantilla
@router_memory.post("/", summary="Create a new template", response_model=TemplateSchema, status_code=status.HTTP_201_CREATED)
def create_template(data: TemplateCreate):
    global next_id # Variable a modificar fuera de la función

    for template in template_list:
        if template.name == data.name:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail=f"Creation failed: a template with name {data.name} already exists"
            )

    template = TemplateSchema(template_id = next_id, **data.model_dump()) # Convierte modelo en diccionario y desempaqueta
    next_id += 1
    template_list.append(template)
    return template


# Obtener todas las plantillas
@router_memory.get("/", summary="Get list of templates")
def get_templates():
    if not template_list:
        raise HTTPException(
            status_code=404, 
            detail="No registered templates found."
        )
    
    return template_list


# Obtener plantilla por ID
@router_memory.get("/{template_id}", summary="Get a template by ID", response_model=TemplateSchema)
def get_template(template_id:int):
    template = find_template(template_id)
    
    if template is None:
        raise HTTPException(
            status_code=404, 
            detail=f"No template found with ID {template_id}."
        )
    
    return template


# Modificar plantilla
# Si existe, cambia nombre y layout
@router_memory.put("/{template_id}",summary="Update an existing template", response_model=TemplateSchema)
def update_template(template_id:int, data:TemplateCreate):
    template = find_template(template_id)
    
    if template is  None:
        raise HTTPException(
            status_code=404, 
            detail=f"Update failed: template with ID {template_id} not found."
        )
    
    template.name = data.name
    template.layout = data.layout
    return template


# Eliminar plantilla
@router_memory.delete("/{template_id}", summary="Delete a template", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(template_id:int):
    template = find_template(template_id)
    
    if template is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Deletion failed: template with ID {template_id} not found."
        )
    
    template_list.remove(template)


# ================== CONSULTAS BASE DATOS ==================


# Añadir plantilla
@router.post("/", response_model=TemplateSchema, summary="Create a new template", status_code=status.HTTP_201_CREATED)
def create_template(data: TemplateCreate, db: Session = Depends(get_db)):
    return templates_repo.create_template(data, db)

# Obtener todas las plantillas
@router.get("/", response_model=list[TemplateSchema], summary="Get list of templates")
def list_clients(db: Session = Depends(get_db)):
    return templates_repo.list_templates(db)

# Obtener plantilla por ID
@router.get("/{templet_id}", response_model=TemplateSchema, summary="Get a template by ID")
def get_template(template_id: int, db: Session = Depends(get_db)):
    template = templates_repo.get_template(template_id, db)
    
    if template is None:
        raise HTTPException(
            status_code=404, 
            detail=f"No template found with ID {template_id}."
        )
    
    return template

# Modificar plantilla
@router.put("/{template_id}", response_model=TemplateSchema, summary="Update an existing template")
def update_template(template_id: int,data: TemplateCreate, db: Session = Depends(get_db)):
    template = templates_repo.update_template(template_id, data, db)
    
    if template is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Update failed: template with Id {template_id} not found"
        )
    
    return template

# Eliminar plantilla
@router.delete("/{template_id}", summary="Delete a template", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(template_id: int, db: Session = Depends(get_db)):
    template = templates_repo.delete_template(template_id, db)
    
    if not template:
        raise HTTPException(
            status_code=404, 
            detail=f"Deletion failed: template with ID {template_id} not found"
        )