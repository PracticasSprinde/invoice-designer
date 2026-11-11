from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.templates_mdl import Template
from app.schemas.templates_sch import TemplateCreate


# Añadir plantilla en la base de datos
def create_template(data: TemplateCreate, db: Session) -> Template:
    # Crear plantilla
    template = Template(**data.model_dump())

    db.add(template)
    db.commit()
    db.refresh(template)
    return template


# Retorna todas las plantillas
def list_templates(issuer_id: int, db: Session) -> list[Template]:
    query = select(Template).where(Template.issuer_id == issuer_id)
    return list(db.scalars(query).all())


# Retorna plantilla por ID
def get_template(template_id: int, issuer_id: int, db: Session) -> Template | None:
    query = select(Template).where(Template.template_id == template_id, Template.issuer_id == issuer_id)
    return db.scalars(query).first()


# Modificar plantilla
def update_template(
    template_id: int, issuer_id: int, data: TemplateCreate, db: Session
) -> Template | None:
    template = get_template(template_id, issuer_id, db)

    if template is None:
        return None

    # Actualiza datos
    template.name = data.name
    template.layout = data.layout

    db.commit()
    db.refresh(template)
    return template


# Eliminar plantilla de la base de datos
def delete_template(template_id: int, issuer_id: int, db: Session) -> bool:
    template = get_template(template_id, issuer_id, db)

    if not template:
        return False

    db.delete(template)
    db.commit()
    return True
