from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import date
from app.services.calculations import calculate_invoice_totals

router = APIRouter(prefix="/invoices", tags=["Invoices"])

# Modelo para los datos de cada línea de la factura
class InvoiceLineCreate(BaseModel):
    description: str = Field(min_length=1)
    quantity: Decimal = Field(gt=0)
    unit_price: Decimal = Field(ge=0)
    tax_rate: Decimal = Field(default=Decimal("21"), ge=0, le=100) # 21% IVA


# Modelo con los datos necesarios para crear una factura
class InvoiceCreate(BaseModel):
    number: str = Field(min_length=1)
    issue_date: date = Field(default_factory=date.today) ##Fecha de hoy
    notes: str | None = None
    issuer_id: int
    client_id: int
    template_id: int | None = None
    discount_percent: Decimal = Field(default=Decimal("0"),ge=0, le=100)
    lines: list[InvoiceLineCreate] = Field(min_length=1) # Mínimo una línea


# Modelo de factura con su identificador y los importes calculados
class Invoice(InvoiceCreate):
    invoice_id: int
    subtotal: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    total: Decimal


# Modelo con los importes que devuelve la vista previa
class InvoiceTotals(BaseModel):
    subtotal: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    total: Decimal


# Calcula los importes sin guardar la factura
@router.post("/preview", response_model=InvoiceTotals)
def preview_invoice(data: InvoiceCreate):
    return calculate_invoice_totals(data.lines, data.discount_percent)