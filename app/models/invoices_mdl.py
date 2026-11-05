from sqlalchemy import String, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.users_mdl import User
from app.models.clients_mdl import Client
from app.models.products_mdl import Product
from app.models.templates_mdl import Template

from datetime import date
from decimal import Decimal


class Invoice(Base):
    __tablename__ = "invoices"

    invoice_id: Mapped[int] = mapped_column(primary_key=True)

    number: Mapped[str] = mapped_column(String(30))
    issue_date: Mapped[date] = mapped_column(default=date.today)
    notes: Mapped[str | None] = mapped_column(Text)

    global_discount_percent: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), default=Decimal("0")
    )

    client_id: Mapped[int] = mapped_column(ForeignKey("clients.client_id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    template_id: Mapped[int | None] = mapped_column(ForeignKey("templates.template_id"))

    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    lines: Mapped[list["InvoiceLine"]] = relationship(
        back_populates="invoice", cascade="all, delete-orphan"
    )
    user: Mapped["User"] = relationship()
    client: Mapped["Client"] = relationship()
    template: Mapped["Template | None"] = relationship()


class InvoiceLine(Base):
    __tablename__ = "invoice_lines"

    line_id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.invoice_id"))
    product_id: Mapped[int | None] = mapped_column(ForeignKey("product.product_id"))

    quantity: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    discount_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0"))
    line_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    invoice: Mapped["Invoice"] = relationship(back_populates="lines")
    product: Mapped["Product"] = relationship()
