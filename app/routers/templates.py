from fastapi import APIRouter, HTTPException, status
from app.schemas.templates import TemplateCreate, Template


# Define ruta
router = APIRouter(prefix="/templates", tags=["Templates"])



# -----------------------------ATRIBUTOS Y METODOS-----------------------------

template_list: list[Template] = [] # Base datos temporal
next_id = 1 # Contador de ID


# Devuelve la primera plantilla que coincida con el ID
def find_template(template_id: int) -> Template | None:
    return next((t for t in template_list if t.template_id == template_id), None)

# -----------------------------ENDPOINTS-----------------------------

# Obtener todas las plantillas
@router.get("/", summary="Get list of templates")
def get_templates():
    if not template_list:
        raise HTTPException(status_code=404, detail="No registered templates found.")
    return template_list


# Obtener plantilla por ID
@router.get("/{template_id}", summary="Get a template by ID", response_model=Template)
def get_template(template_id:int):
    template = find_template(template_id)
    if template is None:
        raise HTTPException(status_code=404, detail=f"No template found with ID {template_id}.")
    return template


# Añadir plantilla
@router.post("/", summary="Create a new template", response_model=Template, status_code=status.HTTP_201_CREATED)
def create_template(data: TemplateCreate):
    global next_id # Variable a modificar fuera de la función

    for template in template_list:
        if template.name == data.name:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Creation failed: a template with name {data.name} already exists")

    template = Template(template_id = next_id, **data.model_dump()) # Convierte modelo en diccionario y desempaqueta
    next_id += 1
    template_list.append(template)
    return template


# Modificar plantilla
# Si existe, cambia nombre y layout
@router.put("/{template_id}",summary="Update an existing template", response_model=Template)
def update_template(template_id:int, data:TemplateCreate):
    template = find_template(template_id)
    if template is  None:
        raise HTTPException(status_code=404, detail=f"Update failed: template with ID {template_id} not found.")
    template.name = data.name
    template.layout = data.layout
    return template


# Eliminar plantilla
@router.delete("/{template_id}", summary="Delete a template", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(template_id:int):
    template = find_template(template_id)
    if template is None:
        raise HTTPException(status_code=404, detail=f"Deletion failed: template with ID {template_id} not found.")
    template_list.remove(template)