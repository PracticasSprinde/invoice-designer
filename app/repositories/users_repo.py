from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.users_mdl import User
from app.schemas.users_sch import UserCreate


# Añadir usuario en la base de datos
def create_user(data: UserCreate, db: Session) -> User:
    # Crear usuario
    user = User(**data.model_dump())

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Retorna todos los usuarios
def list_users(db: Session) -> list[User]:
    return list(db.scalars(select(User)).all())


# Retorna usuario por ID
def get_user(user_id: int, db: Session) -> User | None:
    return db.get(User, user_id)


# Modificar usuario
def update_user(user_id: int, data: UserCreate, db: Session) -> User | None:
    user = get_user(user_id, db)
    
    if user is None:
        return None

    # Actualiza datos
    for field, value in data.model_dump().items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


# Eliminar usuario de la base de datos
def delete_user(user_id: int, db: Session) -> bool:
    user = get_user(user_id, db)

    if not user:
        return False

    db.delete(user)
    db.commit()
    return True
