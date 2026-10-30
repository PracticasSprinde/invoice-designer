from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.users import User
from app.schemas.users import UserCreate

# Añadir usuario en la base de datos
def create_user(db: Session, data: UserCreate) -> User:
    user = User(**data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Retorna usuario por ID
def get_user(db:Session, user_id: int) -> User | None:
    return db.get(User, user_id)

# Retorna todos los usuarios
def get_users(db: Session) -> list[User]:
    return list(db.scalars(select(User)).all())

# Modificar usuario
def update_user(db: Session, user_id: int, data: UserCreate) -> User | None:
    user = get_user(db,user_id)
    if user is None:
        return None
    for field, value in data.model_dump().items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

# Eliminar usuario de la base de datos
def delete_user(db: Session, user_id: int) -> bool:
    user = get_user(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
    
