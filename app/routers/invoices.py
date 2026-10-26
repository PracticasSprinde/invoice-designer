from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import date
from typing import Any
from app.services.calculations import calculate_line,calculate_invoice_totals


# Define ruta
router = APIRouter(prefix="/invoices", tags=["Invoices"])

# -----------------------------CLASES-----------------------------

# Modelo para los datos de cada línea de la factura
class InvoiceLineCreate(BaseModel):
    category: str | None = None
    description: str = Field(min_length=1)
    extra: dict[str, Any] = {}
    unit_price: Decimal = Field(ge=0)
    quantity: Decimal = Field(gt=0)
    discount_percent: Decimal = Field(default=Decimal("0"),ge=0, le=100)
    tax_rate: Decimal = Field(default=Decimal("21"), ge=0, le=100) # 21% IVA


# Línea de factura con los importes calculados de la linea y la cuota de IVA de la linea
class InvoiceLine(InvoiceLineCreate):
    line_amount: Decimal
    tax_amount: Decimal


# Modelo con los datos necesarios para crear una factura
class InvoiceCreate(BaseModel):
    number: str = Field(min_length=1)
    issue_date: date = Field(default_factory=date.today) ##Fecha de hoy
    client_id: int
    issuer_id: int
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


# Modelo con los importes que devuelve la vista previa
class InvoiceTotals(BaseModel):
    subtotal: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    total: Decimal


# -----------------------------ATRIBUTOS Y METODOS-----------------------------

invoice_list: list[Invoice] = []
next_id = 1


# Recorre lista en busca de plantilla que coincida con ID
def find_invoice(invoice_id: int) -> Invoice | None:
    for invoice in invoice_list:
        if invoice.invoice_id == invoice_id:
            return invoice
    return None 
    #return next((i for i in invoice_list if i.invoice_id == invoice_id), None)


# -----------------------------ENDPOINTS-----------------------------

# Obtener todas las facturas
@router.get("/")
def all_invoices():
    return invoice_list


# Obtener factura por ID
@router.get("/{invoice_id}", response_model=Invoice)
def get_invoice(invoice_id: int):
    invoice = find_invoice(invoice_id)
    if invoice is None:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return invoice


# Calcula los importes sin guardar la factura (vista previa)
@router.post("/preview", response_model=InvoiceTotals)
def preview_invoice(data: InvoiceCreate):
    return calculate_invoice_totals(data.lines, data.global_discount_percent)


# Crea una factura: calcula sus líneas y totales y la guarda
@router.post("/", response_model=Invoice, status_code=status.HTTP_201_CREATED)
def create_invoice(data: InvoiceCreate):
    global next_id

    # No permite numero de factura repetido
    for invoice in invoice_list:
        if invoice.number == data.number:
            raise HTTPException(status_code=409, detail="Ya existe una factura con ese número")

    # Calculo de la línea
    invoice_lines = []
    for line in data.lines:
        line_amount, lines_tax = calculate_line(line, data.global_discount_percent)
        invoice_lines.append(
            InvoiceLine(**line.model_dump(), line_amount=line_amount, tax_amount=lines_tax)
        )

    # Calculo de los totales de la factura
    totals = calculate_invoice_totals(data.lines, data.global_discount_percent)

    # Construye factura y la guarda
    invoice = Invoice(
        **data.model_dump(exclude={"lines"}),
        invoice_id=next_id,
        lines=invoice_lines,
        **totals, # Añade las claves y valores al diccionario invoice
    )
    next_id +=1
    invoice_list.append(invoice)
    return invoice