from sqlalchemy import String, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from datetime import date
from decimal import Decimal


class Product(Base):
    __tablename__ = "product"

    product_id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str | None] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(250))
    category: Mapped[str | None] = mapped_column(String(50))
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12,2))
    tax_rate: Mapped[Decimal] = mapped_column(Numeric(5,2), default=Decimal("21"))

    issuer_id: Mapped[int] = mapped_column(ForeignKey("issuer.issuer_id"))
    