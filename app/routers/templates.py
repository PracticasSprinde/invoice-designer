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
@router.get("/")
def all_templates():
    if not template_list:
        raise HTTPException(status_code=404, detail="No hay plantillas almacenadas")
    return template_list


# Obtener plantilla por ID
@router.get("/{template_id}", response_model=Template)
def get_template(template_id:int):
    template = find_template(template_id)
    if template is None:
        raise HTTPException(status_code=404, detail="No hay ninguna plantilla con el ID proporcionado")
    return template


# Añadir plantilla
@router.post("/",response_model=Template, status_code=status.HTTP_201_CREATED)
def create_template(data: TemplateCreate):
    global next_id # Variable a modificar fuera de la función
    template = Template(template_id = next_id, **data.model_dump()) # Convierte modelo en diccionario y desempaqueta
    next_id += 1
    template_list.append(template)
    return template


# Modificar plantilla
# Si existe, cambia nombre y layout
@router.put("/{template_id}", response_model=Template)
def update_template(template_id:int, data:TemplateCreate):
    template = find_template(template_id)
    if template is  None:
        raise HTTPException(status_code=404, detail="No se ha podido encontrar la plantilla")
    template.name = data.name
    template.layout = data.layout
    return template


# Eliminar plantilla
@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(template_id:int):
    template = find_template(template_id)
    if template is None:
        raise HTTPException(status_code=404, detail="No se ha podido eliminar la plantilla")
    template_list.remove(template)