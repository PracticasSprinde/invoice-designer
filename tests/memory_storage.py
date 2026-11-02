from app.models.users_mdl import User
from app.models.clients_mdl import Client
from app.models.templates_mdl import Template
from app.models.invoices_mdl import Invoice


# ================== PRUEBAS USUARIOS ==================

# Lista de usuarios
users_list = [
    User(user_id=1, name="Paco", last_name="Saez", email="aaa@gmail.com", enterprise="Google", cif_nif="B075673", phone="666666666", address="Calle Mayor 1", city="Madrid", postal_code="28001"),
    User(user_id=2, name="Sara", last_name="Alonso", email="aaa@gmail.com", enterprise="Prisma", cif_nif="B0533567", phone="444444444", address="Avenida Libertad 23", city="Barcelona", postal_code="08001"),
    User(user_id=3, name="Laura", last_name="Pascual", email="aaa@gmail.com", enterprise="Pallicer", cif_nif="B85373", phone="777777777", address="Calle Gran Vía 45", city="Valencia", postal_code="46001"),
    User(user_id=4, name="Sergio", last_name="Perez", email="aaa@gmail.com", enterprise="Toyota", cif_nif="B88337", phone="699999999", address="Calle Real 12", city="Sevilla", postal_code="41001")
]

# Devuelve el primer usuario que coincida con el ID
def find_user(user_id: int) -> User | None:
    return next((i for i in
    users_list if i.user_id == user_id), None)


# ================== PRUEBAS CLIENTES ==================

# Lista de clientes
client_list = [
    Client(client_id=1, name="Paco", last_name="Saez", email="aaa@gmail.com", enterprise="Google", cif_nif="B075673", phone="666666666", address="Calle Falsa 123", city="Madrid", postal_code="28001",  user_id=1),
    Client(client_id=2, name="Sara", last_name="Alonso", email="aaa@gmail.com", enterprise="Prisma", cif_nif="B0533567", phone="444444444", address="Avenida Principal 45", city="Barcelona", postal_code="08001",  user_id=1),
    Client(client_id=3, name="Laura", last_name="Pascual", email="aaa@gmail.com", enterprise="Pallicer", cif_nif="B85373", phone="777777777", address="Plaza Mayor 2", city="Valencia", postal_code="46001",  user_id=1),
    Client(client_id=4, name="Sergio", last_name="Perez", email="aaa@gmail.com", enterprise="Toyota", cif_nif="B88337", phone="699999999", address="Calle Alta 8", city="Sevilla", postal_code="41001",  user_id=1)
]


# Devuelve el primer cliente que coincida con el ID
def find_client(client_id: int) -> Client | None:
    return next((c for c in client_list if c.client_id == client_id), None)


# ================== PRUEBAS PLANTILLAS ==================

# Variables para la gestión de plantillas
template_list: list[Template] = [] # Base datos temporal

# Devuelve la primera plantilla que coincida con el ID
def find_template(template_id: int) -> Template | None:
    return next((t for t in template_list if t.template_id == template_id), None)


# ================== PRUEBAS FACTURAS ==================

invoice_list: list[Invoice] = []

# Devuelve la primera factura que coincida con el ID
def find_invoice(invoice_id: int) -> Invoice | None:
    return next((i for i in invoice_list if i.invoice_id == invoice_id), None)