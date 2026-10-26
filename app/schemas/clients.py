from pydantic import BaseModel

class Client(BaseModel):
    client_id: int
    name: str
    last_name: str
    email: str
    enterprise: str
    cif_nif: str
    phone: str