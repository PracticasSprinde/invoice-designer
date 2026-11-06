
from app.core.database import SessionLocal
from app.schemas.issuer_sch import UserCreate
from app.repositories import issuer_repo as users
from app.schemas.clients_sch import ClientCreate
from app.repositories import clients_repo as clients
from app.schemas.templates_sch import TemplateCreate
from app.repositories import templates_repo as templates
from app.schemas.invoices_sch import InvoiceCreate, InvoiceLineCreate
from app.repositories import invoices_repo as invoices


# Crear sesion con la base de datos
db = SessionLocal()

try:
    # CREAR USUARIO
    user_data = UserCreate(
        name="Usuario",
        last_name="Prueba",
        enterprise="Empresa Test",
        cif_nif="12345678Z",
        email="usuario.prueba@test.com",
        phone="600000000",
        address="Calle de prueba 1",
        city="Palma",
        postal_code="07001",
        country="España"
    )

    user = users.create_user(user_data, db)
    print("Usuario creado:", user.user_id)

    # CONSULTAR TODOS LOS USUARIOS
    user_list = users.list_users(db)
    print("Usuarios registrados:", len(user_list))

    # CONSULTAR USUARIO POR ID
    user_found = users.get_user(user.user_id, db)
    print("Usuario encontrado:", user_found.name)

    # MODIFICAR USUARIO
    updated_data = UserCreate(
        name="Usuario Modificado",
        last_name="Prueba",
        enterprise="Empresa Test",
        cif_nif="12345678Z",
        email="usuario.prueba@test.com",
        phone="600000000",
        address="Calle de prueba 1",
        city="Palma",
        postal_code="07001",
        country="España"
    )

    updated_user = users.update_user(user.user_id, updated_data, db)
    print("Usuario actualizado:", updated_user.name)

    # ELIMINAR USUARIO
    deleted = users.delete_user(user.user_id, db)
    print("Usuario eliminado:", deleted)

        # CREAR USUARIO PARA EL CLIENTE
    user_data = UserCreate(
        name="Usuario",
        last_name="Prueba",
        enterprise="Empresa Test",
        cif_nif="12345678Z",
        email="usuario.cliente@test.com",
        phone="600000000",
        address="Calle de prueba 1",
        city="Palma",
        postal_code="07001",
        country="España"
    )

    user = users.create_user(user_data, db)

    # CREAR CLIENTE
    client_data = ClientCreate(
        name="Cliente",
        last_name="Prueba",
        enterprise="Empresa Cliente",
        cif_nif="B12345678",
        email="cliente.prueba@test.com",
        phone="611111111",
        address="Calle Cliente 1",
        city="Palma",
        postal_code="07002",
        country="España",
        user_id=user.user_id
    )

    client = clients.create_client(client_data, db)
    print("Cliente creado:", client.client_id)

    # CONSULTAR CLIENTES
    client_list = clients.list_clients(db)
    print("Clientes registrados:", len(client_list))

    # CONSULTAR CLIENTE POR ID
    client_found = clients.get_client(client.client_id, db)
    print("Cliente encontrado:", client_found.name)

    # MODIFICAR CLIENTE
    updated_data = ClientCreate(
        name="Cliente Modificado",
        last_name="Prueba",
        enterprise="Empresa Cliente",
        cif_nif="B12345678",
        email="cliente.prueba@test.com",
        phone="611111111",
        address="Calle Cliente 1",
        city="Palma",
        postal_code="07002",
        country="España",
        user_id=user.user_id
    )

    updated_client = clients.update_client(
        client.client_id, updated_data, db
    )
    print("Cliente actualizado:", updated_client.name)

    # ELIMINAR CLIENTE
    deleted_client = clients.delete_client(client.client_id, db)
    print("Cliente eliminado:", deleted_client)

    # ELIMINAR USUARIO TEMPORAL
    users.delete_user(user.user_id, db)

    
    # CREAR USUARIO PARA LA PLANTILLA
    user_data = UserCreate(
        name="Usuario",
        last_name="Plantillas",
        enterprise="Empresa Test",
        cif_nif="12345678Z",
        email="usuario.plantilla@test.com",
        phone="600000000",
        address="Calle de prueba 1",
        city="Palma",
        postal_code="07001",
        country="España"
    )

    user = users.create_user(user_data, db)

    # CREAR PLANTILLA
    template_data = TemplateCreate(
        name="Plantilla de prueba",
        layout={"color": "blue", "font": "Arial"},
        user_id=user.user_id
    )

    template = templates.create_template(template_data, db)
    print("Plantilla creada:", template.template_id)

    # CONSULTAR PLANTILLAS
    template_list = templates.list_templates(db)
    print("Plantillas registradas:", len(template_list))

    # CONSULTAR PLANTILLA POR ID
    template_found = templates.get_template(template.template_id, db)
    print("Plantilla encontrada:", template_found.name)

    # MODIFICAR PLANTILLA
    updated_data = TemplateCreate(
        name="Plantilla modificada",
        layout={"color": "purple", "font": "Arial"},
        user_id=user.user_id
    )

    updated_template = templates.update_template(
        template.template_id, updated_data, db
    )
    print("Plantilla actualizada:", updated_template.name)

    # ELIMINAR PLANTILLA
    deleted_template = templates.delete_template(template.template_id, db)
    print("Plantilla eliminada:", deleted_template)

    # ELIMINAR USUARIO TEMPORAL
    users.delete_user(user.user_id, db)

    
    # CREAR USUARIO PARA LA FACTURA
    user_data = UserCreate(
        name="Usuario",
        last_name="Factura",
        enterprise="Empresa Test",
        cif_nif="12345678Z",
        email="usuario.factura@test.com",
        address="Calle de prueba 1",
        city="Palma",
        postal_code="07001",
        country="España"
    )

    user = users.create_user(user_data, db)

    # CREAR CLIENTE PARA LA FACTURA
    client_data = ClientCreate(
        name="Cliente",
        last_name="Factura",
        enterprise="Empresa Test",
        cif_nif="B12345678",
        email="cliente.factura@test.com",
        address="Calle de prueba 2",
        city="Palma",
        postal_code="07002",
        country="España",
        user_id=user.user_id
    )

    client = clients.create_client(client_data, db)

    # CREAR FACTURA
    invoice_data = InvoiceCreate(
        number="FAC-TEST-001",
        client_id=client.client_id,
        user_id=user.user_id,
        global_discount_percent=0,
        notes="Factura de prueba",
        lines=[
            InvoiceLineCreate(
                category="Servicios",
                description="Diseño web",
                unit_price=100,
                quantity=2,
                discount_percent=0,
                tax_rate=21
            )
        ]
    )

    invoice = invoices.create_invoice(invoice_data, db)
    print("Factura creada:", invoice.invoice_id)
    print("Subtotal:", invoice.subtotal)
    print("Descuento:", invoice.discount_amount)
    print("IVA:", invoice.tax_amount)
    print("Total:", invoice.total)

    # CONSULTAR TODAS LAS FACTURAS
    invoice_list = invoices.list_invoices(db)
    print("Facturas registradas:", len(invoice_list))

    # CONSULTAR FACTURA POR ID
    invoice_found = invoices.get_invoice(invoice.invoice_id, db)
    print("Factura encontrada:", invoice_found.number)

    # MODIFICAR FACTURA
    updated_data = InvoiceCreate(
        number="FAC-TEST-002",
        client_id=client.client_id,
        user_id=user.user_id,
        global_discount_percent=10,
        notes="Factura modificada",
        lines=[
            InvoiceLineCreate(
                category="Servicios",
                description="Diseño web actualizado",
                unit_price=150,
                quantity=2,
                discount_percent=0,
                tax_rate=21
            )
        ]
    )

    updated_invoice = invoices.update_invoice(
        invoice.invoice_id, updated_data, db
    )

    print("Factura actualizada:", updated_invoice.number)
    print("Nuevo total:", updated_invoice.total)

    # ELIMINAR FACTURA
    deleted_invoice = invoices.delete_invoice(invoice.invoice_id, db)
    print("Factura eliminada:", deleted_invoice)

    # ELIMINAR CLIENTE Y USUARIO TEMPORALES
    clients.delete_client(client.client_id, db)
    users.delete_user(user.user_id, db)



finally:
    db.close()
