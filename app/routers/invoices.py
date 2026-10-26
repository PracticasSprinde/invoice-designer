from fastapi import APIRouter, HTTPException, status
from app.schemas.invoices import InvoiceLine, InvoiceCreate, Invoice, InvoiceTotals
from app.services.calculations import calculate_line,calculate_invoice_totals

# Define ruta
router = APIRouter(prefix="/invoices", tags=["Invoices"])


# -----------------------------ATRIBUTOS Y METODOS-----------------------------

invoice_list: list[Invoice] = []
next_id = 1


# Devuelve la primera factura que coincida con el ID
def find_invoice(invoice_id: int) -> Invoice | None:
    return next((i for i in invoice_list if i.invoice_id == invoice_id), None)


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


# Modificar factura
@router.put("/{invoice_id}", response_model=Invoice)
def update_invoice(invoice_id: int, data: InvoiceCreate):
    invoice = find_invoice(invoice_id)
    if invoice is None:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    # No permite numero de factura repetido
    for saved in invoice_list:
        if saved.number == data.number and saved.invoice_id != invoice_id:
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
    updated = Invoice(
        **data.model_dump(exclude={"lines"}),
        invoice_id=invoice_id,
        lines=invoice_lines,
        **totals
    )

    # Sustituye factura antigua por nueva
    index = invoice_list.index(invoice)
    invoice_list[index] = updated
    return updated


# Eliminar factura
@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(invoice_id:int):
    invoice = find_invoice(invoice_id)
    if invoice is None:
        raise HTTPException(status_code=404, detail="No se ha podido eliminar la factura")
    invoice_list.remove(invoice)
