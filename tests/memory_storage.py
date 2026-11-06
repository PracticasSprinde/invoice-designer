from decimal import Decimal

from app.models.issuer_mdl import Issuer
from app.models.clients_mdl import Client
from app.models.templates_mdl import Template
from app.models.invoices_mdl import Invoice
from app.models.products_mdl import Product


# ================== PRUEBAS USUARIOS ==================

# Lista de usuarios
issuers_list = [
    Issuer(issuer_id=1, name="Paco", last_name="Saez", email="aaa@gmail.com", enterprise="Google", cif_nif="B075673", phone="666666666", address="Calle Mayor 1", city="Madrid", postal_code="28001"),
    Issuer(issuer_id=2, name="Sara", last_name="Alonso", email="aaa@gmail.com", enterprise="Prisma", cif_nif="B0533567", phone="444444444", address="Avenida Libertad 23", city="Barcelona", postal_code="08001"),
    Issuer(issuer_id=3, name="Laura", last_name="Pascual", email="aaa@gmail.com", enterprise="Pallicer", cif_nif="B85373", phone="777777777", address="Calle Gran Vía 45", city="Valencia", postal_code="46001"),
    Issuer(issuer_id=4, name="Sergio", last_name="Perez", email="aaa@gmail.com", enterprise="Toyota", cif_nif="B88337", phone="699999999", address="Calle Real 12", city="Sevilla", postal_code="41001")
]

# Devuelve el primer usuario que coincida con el ID
def find_issuer(issuer_id: int) -> Issuer | None:
    return next((i for i in
    issuers_list if i.issuer_id == issuer_id), None)



# ================== PRUEBAS CLIENTES ==================

# Lista de clientes
client_list = [
    Client(client_id=1, name="Paco", last_name="Saez", email="aaa@gmail.com", enterprise="Google", cif_nif="B075673", phone="666666666", address="Calle Falsa 123", city="Madrid", postal_code="28001",  issuer_id=1),
    Client(client_id=2, name="Sara", last_name="Alonso", email="aaa@gmail.com", enterprise="Prisma", cif_nif="B0533567", phone="444444444", address="Avenida Principal 45", city="Barcelona", postal_code="08001",  issuer_id=1),
    Client(client_id=3, name="Laura", last_name="Pascual", email="aaa@gmail.com", enterprise="Pallicer", cif_nif="B85373", phone="777777777", address="Plaza Mayor 2", city="Valencia", postal_code="46001",  issuer_id=1),
    Client(client_id=4, name="Sergio", last_name="Perez", email="aaa@gmail.com", enterprise="Toyota", cif_nif="B88337", phone="699999999", address="Calle Alta 8", city="Sevilla", postal_code="41001",  issuer_id=1)
]


# Devuelve el primer cliente que coincida con el ID
def find_client(client_id: int) -> Client | None:
    return next((c for c in client_list if c.client_id == client_id), None)



# ================== PRUEBAS PRODUCTOS ==================

# Lista de productos
product_list = [
    Product(product_id=1, code="PROD-001", name="Portátil HP", description="Portátil de 15.6 pulgadas con 16GB RAM", category="Informática", unit_price=Decimal("750.00"), tax_rate=Decimal("21.00"), issuer_id=1),
    Product(product_id=2, code="PROD-002", name="Ratón inalámbrico", description="Ratón óptico ergonómico USB", category="Periféricos", unit_price=Decimal("25.50"), tax_rate=Decimal("21.00"), issuer_id=1),
    Product(product_id=3, code="PROD-003", name="Monitor 27\"", description="Monitor LED Full HD 75Hz", category="Informática", unit_price=Decimal("180.00"), tax_rate=Decimal("21.00"), issuer_id=1),
    Product(product_id=4, code="PROD-004", name="Teclado mecánico", description="Teclado RGB con switches red", category="Periféricos", unit_price=Decimal("60.25"), tax_rate=Decimal("21.00"), issuer_id=1)
]

# Devuelve el primer usuario que coincida con el ID
def find_product(product_id: int) -> Product | None:
    return next((i for i in
    product_list if i.product_id == product_id), None)


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