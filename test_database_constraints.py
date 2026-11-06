
from sqlalchemy.exc import IntegrityError

from app.core.database import SessionLocal
from app.schemas.invoices_sch import InvoiceCreate, InvoiceLineCreate
from app.repositories import invoices_repo as invoices


# Abrir sesion
db = SessionLocal()

try:
    # PRUEBA 1: CLAVE FORANEA DE USUARIO
    print("\n--- PRUEBA USER_ID INEXISTENTE ---")

    invoice_data = InvoiceCreate(
        number="FAC-INVALID-001",
        client_id=999999,
        user_id=999999,
        template_id=None,
        lines=[
            InvoiceLineCreate(
                description="Linea de prueba",
                unit_price=100,
                quantity=1
            )
        ]
    )

    try:
        invoices.create_invoice(invoice_data, db)
        print("ERROR: Se ha permitido una referencia inexistente")

    except IntegrityError:
        db.rollback()
        print("CORRECTO: PostgreSQL ha rechazado la referencia inexistente")

finally:
    db.close()


# PRUEBA 2: PERSISTENCIA
print("\n--- PRUEBA DE PERSISTENCIA ---")

db = SessionLocal()

try:
    invoice_list = invoices.list_invoices(db)
    print("Facturas encontradas:", len(invoice_list))

finally:
    db.close()



# PRUEBA 3: PERSISTENCIA DE DATOS
print("\n--- PRUEBA DE PERSISTENCIA ---")

from app.repositories import issuer_repo as users
from app.schemas.issuer_sch import UserCreate

db = SessionLocal()

try:
    # Crear usuario de prueba
    user_data = UserCreate(
        name="Usuario Persistencia",
        cif_nif="TEST-PERSIST-001",
        address="Calle de prueba",
        city="Palma",
        postal_code="07001"
    )

    new_user = users.create_user(user_data, db)
    user_id = new_user.user_id

    print("Usuario creado:", user_id)

finally:
    db.close()


# Abrir una nueva sesion
db = SessionLocal()

try:
    saved_user = users.get_user(user_id, db)

    if saved_user:
        print("CORRECTO: El usuario sigue guardado en PostgreSQL")
        print("Nombre:", saved_user.name)
    else:
        print("ERROR: No se ha encontrado el usuario")

    # Eliminar el usuario de prueba
    users.delete_user(user_id, db)

finally:
    db.close()

