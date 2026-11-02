from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.templates import Template
from app.schemas.templates import TemplateCreate

# Añadir plantilla en la base de datos
def create_template(data: TemplateCreate, db: Session) -> Template:
    template = Template(**data.model_dump())
    db.add(template)
    db.commit()
    db.refresh(template)
    return template

# Retorna todas las plantillas
def list_templates(db: Session) -> list[Template]:
    return list(db.scalars(select(Template)).all())

# Retorna plantilla por ID
def get_template(template_id: int, db: Session) -> Template | None:
    return db.get(template_id, Template)

# Modificar plantilla
def update_template(template_id: int, data: TemplateCreate, db: Session) -> Template | None:
    template = get_template(template_id, db)
    if template is None:
        return None
    for field, value in data.model_dump().items():
        setattr(template, field, value)
    db.commit()
    db.refresh(template)
    return template

# Eliminar plantilla de la base de datos
def delete_template(template_id: int, db: Session) -> bool:
    template = get_template(template_id, db)
    if not template:
        return False
    db.delete(template)
    db.commit()
    return True