from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Client(Base):
    __tablename__ = "clients"

    client_id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str | None] = mapped_column(String (100), nullable=True)
    enterprise: Mapped[str | None] = mapped_column(String(50), nullable=True)
    cif_nif: Mapped[str] = mapped_column(String(25))
    email: Mapped[str | None] = mapped_column(String(100), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(25), nullable=True)
    address: Mapped[str] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(50))
    postal_code: Mapped[str] = mapped_column(String(25))
    country: Mapped[str] = mapped_column(String(100), default="España")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))


