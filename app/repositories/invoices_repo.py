from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.invoices_mdl import InvoiceLine, Invoice
from app.schemas.invoices_sch import InvoiceCreate
from app.services.calculations import calculate_invoice_totals, calculate_line


# Añadir factura en la base de datos
def create_invoice(data: InvoiceCreate, db: Session) -> Invoice:
    # Calcular importes totales
    totals = calculate_invoice_totals(data.lines, data.global_discount_percent)

    # Crear factura
    invoice = Invoice(**data.model_dump(exclude={"lines"}), **totals)

    # Calcular y añadir linea
    for line in data.lines:
        line_amount, lines_tax = calculate_line(line, data.global_discount_percent)

        invoice.lines.append(
            InvoiceLine(
                **line.model_dump(), line_amount=line_amount, tax_amount=lines_tax
            )
        )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


# Retorna todas las facturas
def list_invoices(db: Session) -> list[Invoice]:
    return list(db.scalars(select(Invoice)).all())


# Retorna factura por ID
def get_invoice(invoice_id: int, db: Session) -> Invoice | None:
    return db.get(Invoice, invoice_id)


# Modificar factura
def update_invoice(invoice_id: int, data: InvoiceCreate, db: Session) -> Invoice | None:
    invoice = get_invoice(invoice_id, db)
    
    if invoice is None:
        return None

    # Actualiza datos
    for field, value in data.model_dump(exclude={"lines"}).items():
        setattr(invoice, field, value)

    # Calcula totales
    totals = calculate_invoice_totals(data.lines, data.global_discount_percent)

    for field, value in totals.items():
        setattr(invoice, field, value)

    # Eliminar lineas anteriores
    invoice.lines.clear()

    # Añadir nueva linea
    for line in data.lines:
        line_amount, lines_tax = calculate_line(line, data.global_discount_percent)

        invoice.lines.append(
            InvoiceLine(
                **line.model_dump(), line_amount=line_amount, tax_amount=lines_tax
            )
        )

    db.commit()
    db.refresh(invoice)
    return invoice


# Eliminar factura
def delete_invoice(invoice_id: int, db: Session) -> bool:
    invoice = get_invoice(invoice_id, db)

    if not invoice:
        return False

    db.delete(invoice)
    db.commit()
    return True
