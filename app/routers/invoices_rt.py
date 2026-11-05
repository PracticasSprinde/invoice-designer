from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.invoices_sch import Invoice as InvoiceSchema,InvoiceLine,InvoiceCreate,InvoiceTotals
from app.repositories import invoices_repo as invoices_repo
from app.services.calculations import calculate_line, calculate_invoice_totals
from tests.memory_storage import invoice_list, find_invoice

# Define ruta
router = APIRouter(prefix="/invoices", tags=["Invoices"])
router_memory = APIRouter(prefix="/memory/invoices", tags=["Invoices (memory)"])
next_id = 1


# ================== CONSULTAS API ==================


# Calcula los importes sin guardar la factura (vista previa)
@router_memory.post("/preview", summary="Create a preview invoice", response_model=InvoiceTotals)
def preview_invoice(data: InvoiceCreate):
    return calculate_invoice_totals(data.lines, data.global_discount_percent)


# Crea una factura: calcula sus líneas y totales y la guarda
@router_memory.post("/",summary="Create a new invoice",response_model=InvoiceSchema,status_code=status.HTTP_201_CREATED,)
def create_invoice(data: InvoiceCreate):
    global next_id

    # No permite numero de factura repetido
    for invoice in invoice_list:
        if invoice.number == data.number:
            raise HTTPException(
                status_code=409,
                detail=f"Creation failed: invoice with ID {invoice.invoice_id} already exists.",
            )

    # Calculo de la línea
    invoice_lines = []
    for line in data.lines:
        line_amount, lines_tax = calculate_line(line, data.global_discount_percent)
        invoice_lines.append(
            InvoiceLine(
                **line.model_dump(), line_amount=line_amount, tax_amount=lines_tax
            )
        )

    # Calculo de los totales de la factura
    totals = calculate_invoice_totals(data.lines, data.global_discount_percent)

    # Construye factura y la guarda
    invoice = InvoiceSchema(
        **data.model_dump(exclude={"lines"}),
        invoice_id=next_id,
        lines=invoice_lines,
        **totals,  # Añade las claves y valores al diccionario invoice
    )

    next_id += 1
    invoice_list.append(invoice)
    return invoice


# Obtener todas las facturas
@router_memory.get("/", summary="Get list of invoices")
def get_invoices():
    if not invoice_list:
        raise HTTPException(status_code=404, detail="No registered invoices found.")

    return invoice_list


# Obtener factura por ID
@router_memory.get("/{invoice_id}", summary="Get an invoice by ID", response_model=InvoiceSchema)
def get_invoice(invoice_id: int):
    invoice = find_invoice(invoice_id)

    if invoice is None:
        raise HTTPException(
            status_code=404, detail=f"No invoice found with ID {invoice_id}."
        )

    return invoice


# Modificar factura
@router_memory.put("/{invoice_id}", summary="Update an existing invoice", response_model=InvoiceSchema)
def update_invoice(invoice_id: int, data: InvoiceCreate):
    invoice = find_invoice(invoice_id)

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail=f"Update failed: invoice with ID {invoice_id} not found.",
        )

    # No permite numero de factura repetido
    for saved in invoice_list:
        if saved.number == data.number and saved.invoice_id != invoice_id:
            raise HTTPException(
                status_code=409,
                detail=f"Update failed: an invoice with number '{data.number}' already exists.",
            )

    # Calculo de la línea
    invoice_lines = []
    for line in data.lines:
        line_amount, lines_tax = calculate_line(line, data.global_discount_percent)
        invoice_lines.append(
            InvoiceLine(
                **line.model_dump(), line_amount=line_amount, tax_amount=lines_tax
            )
        )

    # Calculo de los totales de la factura
    totals = calculate_invoice_totals(data.lines, data.global_discount_percent)

    # Construye factura y la guarda
    updated = InvoiceSchema(
        **data.model_dump(exclude={"lines"}),
        invoice_id=invoice_id,
        lines=invoice_lines,
        **totals,
    )

    # Sustituye factura antigua por nueva
    index = invoice_list.index(invoice)
    invoice_list[index] = updated
    return updated


# Eliminar factura
@router_memory.delete("/{invoice_id}", summary="Delete an invoice", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(invoice_id: int):
    invoice = find_invoice(invoice_id)

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail=f"Deletion failed: invoice with ID {invoice_id} not found.",
        )

    invoice_list.remove(invoice)


# ================== CONSULTAS BASE DATOS ==================


# Añadir factura
@router.post("/",response_model=InvoiceSchema,summary="Create a new invoice",status_code=status.HTTP_201_CREATED,)
def create_invoice(data: InvoiceCreate, db: Session = Depends(get_db)):
    try:
        return invoices_repo.create_invoice(data, db)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(error))


# Obtener todas las facturas
@router.get("/", response_model=list[InvoiceSchema], summary="Get list of invoices")
def list_invoices(db: Session = Depends(get_db)):
    return invoices_repo.list_invoices(db)


# Obtener factura por ID
@router.get("/{invoice_id}", response_model=InvoiceSchema, summary="Get an invoice for ID")
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = invoices_repo.get_invoice(invoice_id, db)

    if invoice is None:
        raise HTTPException(
            status_code=404, 
            detail=f"No invoice found with ID {invoice_id}."
        )

    return invoice


# Modificar factura
@router.put("/{invoice_id}", response_model=InvoiceSchema, summary="Update an existing invoice")
def update_invoice(invoice_id: int, data: InvoiceCreate, db: Session = Depends(get_db)):
    try:
        invoice = invoices_repo.update_invoice(invoice_id, data, db)

        if invoice is None:
            raise HTTPException(
                status_code=404,
                detail=f"Update failed: invoice with ID {invoice_id} not found",
            )

        return invoice
    
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )



# Eliminar factura
@router.delete("/{invoice_id}", summary="Delete an invoice", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = invoices_repo.delete_invoice(invoice_id, db)
    if not invoice:
        raise HTTPException(
            status_code=404,
            detail=f"Deletion failed: invoice with ID {invoice_id} not found",
        )
