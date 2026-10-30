from pydantic import BaseModel, Field, EmailStr, ConfigDict

class ClientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    enterprise: str | None = Field(default=None, max_length=50)
    cif_nif: str = Field(min_length=1, max_length=25)
    email: EmailStr | None = Field(default=None)
    phone: str | None = Field(default=None, max_length=25)
    address: str = Field(min_length=1, max_length=150)
    city: str = Field(min_length=1, max_length=50)
    postal_code: str = Field(min_length=1, max_length=25)
    country: str = Field(default="España", min_length=1, max_length=100)
    user_id: int

class Client(ClientCreate):
    client_id: int
    model_config = ConfigDict(from_attributes=True)