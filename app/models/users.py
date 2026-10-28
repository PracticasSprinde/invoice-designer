from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    enterprise: Mapped[str | None] = mapped_column(String(50), nullable=True)
    cif_nif: Mapped[str] = mapped_column(String(25))
    email: 




    