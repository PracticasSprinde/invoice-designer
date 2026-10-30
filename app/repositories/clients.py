from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.clients import Client
from app.schemas.clients import ClientCreate

# Añadir cliente en la base de datos
def create_client( data: ClientCreate, db: Session) -> Client:
    client = Client(**data.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


# Retonra lista de clientes
def list_clients(db: Session) -> list[Client]:
    return list(db.scalars(select(Client)).all())


# Retorna cliente por ID
def get_client(client_id: int, db: Session) -> Client | None:
    return db.get(client_id, Client)


# Modifica cliente
def update_client(client_id: int, data: ClientCreate, db: Session) -> Client | None:
    client = get_client(client_id, db)
    if client is None:
        return None
    for field, value in data.model_dump().items():
        setattr(client, field, value)
    db.commit()
    db.refresh(client)
    return client

# Elimina cliente
def delete_client(client_id: int, db: Session) -> bool:
    client = get_client(client_id, db)
    if not client:
        return False
    db.delete(client)
    db.commit()
    return True