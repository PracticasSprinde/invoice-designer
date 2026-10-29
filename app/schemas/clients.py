from pydantic import BaseModel, Field, EmailStr

class ClientCreate(BaseModel):
    name: str = Field(min_length=1)
    last_name: str | None = None
    enterprise: str | None = None
    cif_nif: str = Field(min_length=1)
    email: EmailStr | None = None
    phone: str | None = None
    address: str = Field(min_length=1)
    city: str = Field(min_length=1)
    postal_code: str = Field(min_length=1)
    country: str = Field(default="España", min_length=1)

class Client(ClientCreate):
    client_id: int