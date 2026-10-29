from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    enterprise: str | None = Field(default=None, min_length=1, max_length=50)
    cif_nif: str = Field(min_length=1, max_length=25)
    email: EmailStr | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = Field(default=None, min_length=1, max_length=25)
    address: str = Field(min_length=1, max_length=150)
    city: str = Field(min_length=1, max_length=50)
    postal_code: str = Field(min_length=1, max_length=25)
    country: str = Field(default="España", min_length=1, max_length=100)

class User(UserCreate):
    user_id: int