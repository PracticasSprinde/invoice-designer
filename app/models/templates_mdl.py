from sqlalchemy import String, ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

from datetime import datetime


class Template(Base):
    __tablename__ = "templates"

    template_id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    name: Mapped[str] = mapped_column(String(100))
    layout: Mapped[dict] = mapped_column(JSON, default=dict)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
