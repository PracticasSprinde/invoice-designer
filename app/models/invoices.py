from sqlalchemy import String, ForeignKey, Numeric, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from datetime import date
from decimal import Decimal

class Invoice(Base):
    __tablename__ = "invoices"

    invoice_id: Mapped[int] = mapped_column(primary_key=True)
    
    number: Mapped[str] = mapped_column(String(30))
    issue_date: Mapped[date] = mapped_column(default=date.today)
    notes: Mapped[str | None] = mapped_column(Text)
    global_discount_percent: Mapped[Decimal] = mapped_column(Numeric(5,2), default=Decimal("0"))

    client_id: Mapped[int] = mapped_column(ForeignKey("clients.client_id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    template_id: Mapped[int | None] = mapped_column(ForeignKey("templates.template_id"))

    subtotal: Mapped[Decimal] = mapped_column(Numeric(12,2))
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(12,2))
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12,2))
    total: Mapped[Decimal] = mapped_column(Numeric(12,2))

    lines: Mapped[list["InvoiceLine"]] = relationship(back_populates="invoice", cascade="all, delete-orphan")
    user: Mapped["User"] = relationship()
    client: Mapped["Client"] = relationship()
    template: Mapped["Template | None"] = relationship()


class InvoiceLine(Base):
    __tablename__ = "invoice_lines"

    line_id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.invoice_id"))

    category: Mapped[str | None] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(250))
    extra: Mapped[dict] = mapped_column(JSON,default=dict)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12,2))
    quantity: Mapped[Decimal] = mapped_column(Numeric(10,2))
    discount_percent: Mapped[Decimal] = mapped_column(Numeric(5,2), default=Decimal("0"))
    tax_rate: Mapped[Decimal] = mapped_column(Numeric(5,2), default=Decimal("21"))
    line_amount: Mapped[Decimal] = mapped_column(Numeric(12,2))
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12,2))

    invoice: Mapped["Invoice"] = relationship(back_populates="lines")