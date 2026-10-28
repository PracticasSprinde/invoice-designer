from fastapi import APIRouter, HTTPException, status
from app.schemas.clients import Client

# Define ruta
router = APIRouter(prefix="/clients", tags=["Clients"])


# -----------------------------ATRIBUTOS Y METODOS-----------------------------

client_list = [
    Client(client_id=1, name="Paco", last_name="Saez", email="aaa@gmail.com", enterprise="Google", cif_nif="B075673", phone="666666666", adress="Calle Falsa 123", city="Madrid", postal_code="28001"),
    Client(client_id=2, name="Sara", last_name="Alonso", email="aaa@gmail.com", enterprise="Prisma", cif_nif="B0533567", phone="444444444", adress="Avenida Principal 45", city="Barcelona", postal_code="08001"),
    Client(client_id=3, name="Laura", last_name="Pascual", email="aaa@gmail.com", enterprise="Pallicer", cif_nif="B85373", phone="777777777", adress="Plaza Mayor 2", city="Valencia", postal_code="46001"),
    Client(client_id=4, name="Sergio", last_name="Perez", email="aaa@gmail.com", enterprise="Toyota", cif_nif="B88337", phone="699999999", adress="Calle Alta 8", city="Sevilla", postal_code="41001")
]


# Devuelve el primer cliente que coincida con el ID
def find_client(client_id: int) -> Client | None:
    return next((c for c in client_list if c.client_id == client_id), None)


# -----------------------------ENDPOINTS-----------------------------

# Obtener todos los clientes
@router.get("/", summary="Get list of clients")
def get_clients():
    if not client_list:
        raise HTTPException(status_code=404, detail="No registered clients found.")
    return client_list


# Obtener cliente por ID - Path --> client/5
@router.get("/{client_id}", summary="Get a client by ID")
def get_client(client_id: int):
    client = find_client(client_id)
    if client is None:
        raise HTTPException(status_code=404, detail=f"No client found with ID {client_id}.")
    return client


# Añadir client
@router.post("/", summary="Create a new client" ,status_code=status.HTTP_201_CREATED)
def create_client(client : Client):
    if find_client(client.client_id):
        raise HTTPException(status_code=409, detail=f"Creation failed: client with ID {client.client_id} already exists")
    client_list.append(client)
    return client


# Modificar cliente
@router.put("/{client_id}", summary="Update an existing client")
async def update_client(client_id : int, client:Client):
    for index, saved in enumerate(client_list):
        if saved.client_id == client_id:
            client.client_id = client_id
            client_list[index] = client
            return client
    raise HTTPException(status_code=404, detail=f"Update failed: client with ID {client_id} not found")


# Eliminar cliente
@router.delete("/{client_id}", summary="Delete a client" ,status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id : int):
    client = find_client(client_id)
    if client is None:
        raise HTTPException(status_code=404, detail=f"Deletion failed: client with ID {client_id} not found")
    client_list.remove(client)