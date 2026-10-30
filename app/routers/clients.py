from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.clients import Client
from app.schemas.clients import Client as ClientSchema, ClientCreate
from app.repositories  import clients as clients_repo
from app.routers.prueba_routers import client_list, find_client


# Define ruta
router = APIRouter(prefix="/clients", tags=["Clients"])

# ================== CONSULTAS API ==================

# Añadir cliente
@router.post("/", summary="Create a new client" ,status_code=status.HTTP_201_CREATED)
def create_client(client : Client):
    if find_client(client.client_id):
        raise HTTPException(status_code=409, detail=f"Creation failed: client with ID {client.client_id} already exists")
    client_list.append(client)
    return client


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


# Modificar cliente
@router.put("/{client_id}", summary="Update an existing client")
def update_client(client_id : int, client:Client):
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


# ================== CONSULTAS BASE DATOS ==================

# Añadir cliente
@router.post("/", response_model=ClientSchema, summary="Create a new client" ,status_code=status.HTTP_201_CREATED)
def create_client(data : ClientCreate, db:Session = Depends(get_db)):
    return clients_repo.create_client(data, db)


# Obtener todos los clientes
@router.get("/", response_model=list[ClientSchema], summary="Get list of clients")
def list_clients(db: Session = Depends(get_db)):
    return clients_repo.list_clients(db)


# Obtener cliente por ID
@router.get("/{client_id}", response_model=ClientSchema, summary="Get a client by ID")
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = clients_repo.get_client(client_id, db)
    if client is None:
        raise HTTPException(status_code=404, detail=f"No client found with ID {client_id}.")
    return client



# Modificar cliente
@router.put("/{client_id}", response_model=ClientSchema, summary="Update an existing client")
async def update_client(client_id : int, data:ClientCreate, db:Session = Depends(get_db)):
    client = clients_repo.get_client(client_id, data, db)
    if client is None:
        raise HTTPException(status_code=404, detail=f"Update failed: client with ID {client_id} not found")
    return client


# Eliminar cliente
@router.delete("/{client_id}", response_model=ClientSchema, summary="Delete a client" ,status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id : int, db:Session = Depends(get_db), ):
    client = clients_repo.delete_client(client_id, db)
    if not client:
        raise HTTPException(status_code=404, detail=f"Deletion failed: client with ID {client_id} not found")