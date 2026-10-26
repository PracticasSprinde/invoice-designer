from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

# Define ruta
router = APIRouter(prefix="/clients", tags=["Clients"])

# -----------------------------CLASES-----------------------------

# Entidad
class Client(BaseModel):
    client_id: int
    name: str
    last_name: str
    email: str
    enterprise: str
    cif_nif: str
    phone: str


# -----------------------------ATRIBUTOS Y METODOS-----------------------------

client_list = [
    Client(client_id=1, name="Paco", last_name="Saez", email= "aaa@gmail.com",enterprise="Google", cif_nif="B075673", phone="666666666"),
    Client(client_id=2, name="Sara", last_name="Alonso",email= "aaa@gmail.com", enterprise="Prisma", cif_nif="B0533567", phone="444444444"),
    Client(client_id=3, name="Laura", last_name="Pascual",email= "aaa@gmail.com", enterprise="Pallicer", cif_nif="B85373", phone="777777777"),
    Client(client_id=4, name="Sergio", last_name="Perez",email= "aaa@gmail.com", enterprise="Toyota", cif_nif="B88337", phone="699999999")
]


# Devuelve el primer cliente que coincida con el ID
def find_client(client_id: int) -> Client | None:
    return next((c for c in client_list if c.client_id == client_id), None)


# -----------------------------ENDPOINTS-----------------------------

# Obtener todos los clientes
@router.get("/")
def all_clients():
    if not client_list:
        raise HTTPException(status_code=404, detail="No hay clientes")
    return client_list


# Obtener cliente por ID - Path --> clientquery/5
# Parametros obligatorios
@router.get("/{client_id}")
def get_client(client_id: int):
    client = find_client(client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client


# Añadir client
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_client(client : Client):
    if find_client(client.client_id):
        raise HTTPException(status_code=409, detail="El cliente ya existe")
    client_list.append(client)
    return client


# Modificar cliente
@router.put("/{client_id}")
async def update_client(client_id : int, client:Client):

    for index, saved in enumerate(client_list):

        if saved.client_id == client.client_id:
            client_list[index] = client
            return client
    raise HTTPException(status_code=404, detail="Cliente no encontrado")


# Eliminar cliente
@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id : int):
    client = find_client(client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    client_list.remove(client)