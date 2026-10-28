from fastapi import APIRouter, HTTPException, status
from app.schemas.users import User

# Define ruta
router = APIRouter(prefix="/users", tags=["Users"])

# -----------------------------ATRIBUTOS Y METODOS-----------------------------

users_list = [
    User(user_id=1, name="Paco", last_name="Saez", email="aaa@gmail.com", enterprise="Google", cif_nif="B075673", phone="666666666", adress="Calle Mayor 1", city="Madrid", postal_code="28001"),
    User(user_id=2, name="Sara", last_name="Alonso", email="aaa@gmail.com", enterprise="Prisma", cif_nif="B0533567", phone="444444444", adress="Avenida Libertad 23", city="Barcelona", postal_code="08001"),
    User(user_id=3, name="Laura", last_name="Pascual", email="aaa@gmail.com", enterprise="Pallicer", cif_nif="B85373", phone="777777777", adress="Calle Gran Vía 45", city="Valencia", postal_code="46001"),
    User(user_id=4, name="Sergio", last_name="Perez", email="aaa@gmail.com", enterprise="Toyota", cif_nif="B88337", phone="699999999", adress="Calle Real 12", city="Sevilla", postal_code="41001")
]

# Devuelve el primer usuario que coincida con el ID
def find_user(user_id: int) -> User | None:
    return next((i for i in
    users_list if i.user_id == user_id), None)


# -----------------------------ENDPOINTS-----------------------------

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

# Añadir usuario
@router.post("/", summary="Create a new user", status_code=status.HTTP_201_CREATED)
def create_user(user : User):
    if find_user(user.user_id):
        raise HTTPException(status_code=409, detail=f"Creation failed: user with ID {user.user_id} already exists.")
    users_list.append(user)
    return user

# Modificar usuario
@router.put("/{user_id}", summary="Update an existing user")
def update_user(user_id: int, user:User):
    for index, saved in enumerate (users_list):
        if saved.user_id == user_id:
            user.issuer_id = user_id
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