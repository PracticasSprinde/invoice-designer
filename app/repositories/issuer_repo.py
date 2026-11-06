from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.issuer_mdl import Issuer
from app.schemas.issuer_sch import IssuerCreate


# Añadir usuario en la base de datos
def create_user(data: IssuerCreate, db: Session) -> Issuer:
    # Crear usuario
    issuer = Issuer(**data.model_dump())

    db.add(issuer)
    db.commit()
    db.refresh(issuer)
    return issuer


# Retorna todos los usuarios
def list_users(db: Session) -> list[Issuer]:
    return list(db.scalars(select(Issuer)).all())


# Retorna usuario por ID
def get_user(issuer_id: int, db: Session) -> Issuer | None:
    return db.get(Issuer, issuer_id)


# Modificar usuario
def update_user(issuer_id: int, data: IssuerCreate, db: Session) -> Issuer | None:
    issuer = get_user(issuer_id, db)
    
    if issuer is None:
        return None

    # Actualiza datos
    for field, value in data.model_dump().items():
        setattr(issuer, field, value)

    db.commit()
    db.refresh(issuer)
    return issuer


# Eliminar usuario de la base de datos
def delete_user(issuer_id: int, db: Session) -> bool:
    issuer = get_user(issuer_id, db)

    if not issuer:
        return False

    db.delete(issuer)
    db.commit()
    return True
