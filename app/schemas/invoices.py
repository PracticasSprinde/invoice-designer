from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import date
from typing import Any


# Modelo para los datos de cada línea de la factura
class InvoiceLineCreate(BaseModel):
    category: str | None = Field(default=None, max_length=50)
    description: str = Field(min_length=1, max_length=250)
    extra: dict[str, Any] = {}
    unit_price: Decimal = Field(ge=0)
    quantity: Decimal = Field(gt=0)
    discount_percent: Decimal = Field(default=Decimal("0"),ge=0, le=100)
    tax_rate: Decimal = Field(default=Decimal("21"), ge=0, le=100) # 21% IVA


# Línea de factura con los importes calculados de la linea y la cuota de IVA de la linea
class InvoiceLine(InvoiceLineCreate):
    line_amount: Decimal
    tax_amount: Decimal
    model_config = ConfigDict(from_attributes=True)

# Modelo con los datos necesarios para crear una factura
class InvoiceCreate(BaseModel):
    number: str = Field(min_length=1, max_length=30)
    issue_date: date = Field(default_factory=date.today) ##Fecha de hoy
    client_id: int
    user_id: int
    template_id: int | None = None
    global_discount_percent: Decimal = Field(default=Decimal("0"),ge=0, le=100)
    notes: str | None = None
    lines: list[InvoiceLineCreate] = Field(min_length=1) # Mínimo una línea


# Modelo de factura con su identificador y los importes calculados
class Invoice(InvoiceCreate):
    invoice_id: int
    subtotal: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    total: Decimal
    lines: list[InvoiceLine] = Field(min_length=1) # Mínimo una línea
    model_config = ConfigDict(from_attributes=True)


# Modelo con los importes que devuelve la vista previa
class InvoiceTotals(BaseModel):
    subtotal: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    total: Decimal