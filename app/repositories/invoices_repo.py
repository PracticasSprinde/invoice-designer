from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.invoices_mdl import InvoiceLine, Invoice
from app.models.products_mdl import Product
from app.schemas.invoices_sch import InvoiceCreate
from app.services.calculations import calculate_invoice_totals, calculate_line

#Convierte los desgloses a texto para poder guardarlos en JSON
def totals_for_db(lines, global_discount_percent) -> dict:
    totals = calculate_invoice_totals(lines, global_discount_percent)

    totals["base_breakdown"] = {
        str(rate): str(base) for rate, base in totals["base_breakdown"].items()
    }
    totals["tax_breakdown"] = {
        str(rate): str(tax) for rate, tax in totals["tax_breakdown"].items()
    }
    return totals


# Añadir factura en la base de datos
def create_invoice(data: InvoiceCreate, db: Session) -> Invoice:

    # Crear factura
    invoice = Invoice(**data.model_dump(exclude={"lines"}))

    # Preparar las líneas de la factura
    prepared_lines = []

    # Calcular y añadir linea
    for line in data.lines:

        # Buscar el producto en la base de datos
        product = db.get(Product, line.product_id)

        if product is None:
            raise ValueError(f"El producto {line.product_id} no existe")

        # Comprobar que el producto pertenece al usuario
        if product.user_id != data.user_id:
            raise ValueError("El producto no pertenece a este usuario")

        # Crear la línea con los datos actuales del producto
        invoice_line = InvoiceLine(
            product_id=product.product_id,
            description=product.description or product.name,
            unit_price=product.unit_price,
            tax_rate=product.tax_rate,
            quantity=line.quantity,
            discount_percent=line.discount_percent,
        )

        # Calcular el importe de la línea
        invoice_line.line_amount = calculate_line(invoice_line)

        prepared_lines.append(invoice_line)

    # Calcular los totales de la factura
    totals = totals_for_db(prepared_lines, data.global_discount_percent)

    # Guardar los totales en la factura
    for field, value in totals.items():
        setattr(invoice, field, value)

    # Añadir las líneas a la factura
    invoice.lines = prepared_lines

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
    for field, value in data.model_dump(exclude={"lines", "user_id"}).items():
        setattr(invoice, field, value)

    # Eliminar las líneas anteriores
    invoice.lines.clear()

    # Preparar las nuevas líneas
    prepared_lines = []

    for line in data.lines:

        # Buscar el producto en la base de datos
        product = db.get(Product, line.product_id)

        if product is None:
            raise ValueError(f"El producto {line.product_id} no existe")

        # Comprobar que el producto pertenece al usuario de la factura
        if product.user_id != invoice.user_id:
            raise ValueError("El producto no pertenece a este usuario")

        # Crear la nueva línea con los datos del producto
        invoice_line = InvoiceLine(
            product_id=product.product_id,
            description=product.description or product.name,
            unit_price=product.unit_price,
            tax_rate=product.tax_rate,
            quantity=line.quantity,
            discount_percent=line.discount_percent,
        )

        # Calcular el importe de la línea
        invoice_line.line_amount = calculate_line(invoice_line)

        prepared_lines.append(invoice_line)

    # Calcula totales
    totals = totals_for_db(prepared_lines, data.global_discount_percent)

    # Actualizar los totales
    for field, value in totals.items():
        setattr(invoice, field, value)

    # Eliminar lineas anteriores
    invoice.lines = prepared_lines

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
