from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.users import User
from app.schemas.users import User as UserSchema, UserCreate
from app.repositories import users as users_repo
from app.routers.prueba_routers import users_list, find_user

# Define ruta
router = APIRouter(prefix="/users", tags=["Users"])

# ================== CONSULTAS API ==================

# Añadir usuario
@router.post("/", summary="Create a new user", status_code=status.HTTP_201_CREATED)
def create_user(user : User):
    if find_user(user.user_id):
        raise HTTPException(status_code=409, detail=f"Creation failed: user with ID {user.user_id} already exists.")
    users_list.append(user)
    return user


# Obtener todos los usuarios
@router.get("/", summary="Get list of users")
def get_users():
    if not users_list:
        raise HTTPException(status_code=404, detail="No registered users found.")
    return users_list


# Obtener usuario por ID
@router.get("/{user_id}", summary="Get a user by ID")
def get_user(user_id:int):
    user = find_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"No user found with ID {user_id}.")
    return user


# Modificar usuario
@router.put("/{user_id}", summary="Update an existing user")
def update_user(user_id: int, user:User):
    for index, saved in enumerate (users_list):
        if saved.user_id == user_id:
            user.user_id = user_id
            users_list[index] = user
            return user
    raise HTTPException(status_code=404, detail=f"Update failed: user with ID {user_id} not found.")


# Eliminar usuario
@router.delete("/{user_id}", summary="Delete a user", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    user = find_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"Deletion failed: user with ID {user_id} not found.")
    users_list.remove(user)


# ================== CONSULTAS BASE DATOS ==================

# Añadir usuario
@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return users_repo.create_user(data, db)


# Obtener todos los usuarios
@router.get("/", response_model=list[UserSchema], summary="Get list of users")
def list_users(db: Session = Depends(get_db)):
    return users_repo.list_users(db)


# Obtener usuario por ID
@router.get("/{user_id}", response_model= UserSchema, summary="Get a user by ID")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = users_repo.get_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f"No user found with ID {user_id}.")
    return user


# Modificar usuario
@router.put("/{user_id}", response_model= UserSchema, summary="Update an existing user")
def update_user(user_id: int, data: UserCreate, db: Session = Depends(get_db)):
    user = users_repo.update_user(user_id, data, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f"Update failed: user with ID {user_id} not found.")
    return user

# Eliminar usuario
@router.delete("/{user_id}", summary="Delete a user", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = users_repo.delete_user(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail=f"Deletion failed: user with ID {user_id} not found.")