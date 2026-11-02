
import requests
import time


# ================== URLS DE LA API ==================

BASE_URL = "http://127.0.0.1:8000"

USERS_URL = f"{BASE_URL}/memory/users"
CLIENTS_URL = f"{BASE_URL}/memory/clients"
TEMPLATES_URL = f"{BASE_URL}/memory/templates"
INVOICES_URL = f"{BASE_URL}/memory/invoices"


# Identificadores unicos para las pruebas
TEST_ID = int(time.time())


# ================== FUNCIONES AUXILIARES ==================

def check_response(response, expected_status, description):
    print(f"\n{description}")
    print("Codigo HTTP:", response.status_code)

    try:
        print("Respuesta:", response.json())
    except ValueError:
        print("Respuesta sin contenido")

    if response.status_code == expected_status:
        print("CORRECTO")
        return True

    print("ERROR: Codigo HTTP inesperado")
    return False


# ================== PRUEBA DE CONEXION ==================

def test_connection():
    print("\n========== CONEXION ==========")

    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)

        return check_response(
            response, 200, "Comprobar conexion con FastAPI"
        )

    except requests.exceptions.ConnectionError:
        print("ERROR: No se ha podido conectar con la API")
        return False


# ================== CRUD USUARIOS ==================

def test_users():

    print("\n========== CRUD USERS ==========")

    user_id = TEST_ID

    user_data = {
        "user_id": user_id,
        "name": "Usuario de prueba",
        "last_name": "Test",
        "enterprise": "Invoice Designer",
        "cif_nif": f"TEST-U-{TEST_ID}",
        "email": "test@example.com",
        "phone": "600123456",
        "address": "Calle de prueba 1",
        "city": "Palma",
        "postal_code": "07001",
        "country": "España"
    }

    # POST: Crear usuario
    response = requests.post(USERS_URL, json=user_data)

    if not check_response(response, 201, "POST - Crear usuario"):
        return False

    # GET: Obtener todos los usuarios
    response = requests.get(USERS_URL)

    if not check_response(response, 200, "GET - Obtener usuarios"):
        return False

    # GET: Obtener usuario por ID
    response = requests.get(f"{USERS_URL}/{user_id}")

    if not check_response(response, 200, "GET - Obtener usuario por ID"):
        return False

    # PUT: Modificar usuario
    user_data["name"] = "Usuario modificado"

    response = requests.put(
        f"{USERS_URL}/{user_id}",
        json=user_data
    )

    if not check_response(response, 200, "PUT - Modificar usuario"):
        return False

    return True


# ================== CRUD CLIENTES ==================

def test_clients(user_id):

    print("\n========== CRUD CLIENTS ==========")

    client_id = TEST_ID + 1

    client_data = {
        "client_id": client_id,
        "name": "Cliente de prueba",
        "last_name": "Test",
        "enterprise": "Empresa de prueba",
        "cif_nif": f"TEST-C-{TEST_ID}",
        "email": "cliente@example.com",
        "phone": "611123456",
        "address": "Calle de prueba 2",
        "city": "Palma",
        "postal_code": "07002",
        "country": "España",
        "user_id": user_id
    }

    # POST: Crear cliente
    response = requests.post(CLIENTS_URL, json=client_data)

    if not check_response(response, 201, "POST - Crear cliente"):
        return False

    # GET: Obtener todos los clientes
    response = requests.get(CLIENTS_URL)

    if not check_response(response, 200, "GET - Obtener clientes"):
        return False

    # GET: Obtener cliente por ID
    response = requests.get(f"{CLIENTS_URL}/{client_id}")

    if not check_response(response, 200, "GET - Obtener cliente por ID"):
        return False

    # PUT: Modificar cliente
    client_data["name"] = "Cliente modificado"

    response = requests.put(
        f"{CLIENTS_URL}/{client_id}",
        json=client_data
    )

    if not check_response(response, 200, "PUT - Modificar cliente"):
        return False

    return client_id


# ================== CRUD PLANTILLAS ==================

def test_templates(user_id):

    print("\n========== CRUD TEMPLATES ==========")

    template_data = {
        "name": f"Plantilla de prueba {TEST_ID}",
        "layout": {
            "color": "purple",
            "font": "Arial"
        },
        "user_id": user_id
    }

    # POST: Crear plantilla
    response = requests.post(TEMPLATES_URL, json=template_data)

    if not check_response(response, 201, "POST - Crear plantilla"):
        return None

    template_id = response.json()["template_id"]

    # GET: Obtener todas las plantillas
    response = requests.get(TEMPLATES_URL)

    if not check_response(response, 200, "GET - Obtener plantillas"):
        return None

    # GET: Obtener plantilla por ID
    response = requests.get(f"{TEMPLATES_URL}/{template_id}")

    if not check_response(response, 200, "GET - Obtener plantilla por ID"):
        return None

    # PUT: Modificar plantilla
    template_data["name"] = f"Plantilla modificada {TEST_ID}"

    response = requests.put(
        f"{TEMPLATES_URL}/{template_id}",
        json=template_data
    )

    if not check_response(response, 200, "PUT - Modificar plantilla"):
        return None

    return template_id


# ================== CRUD FACTURAS ==================

def test_invoices(user_id, client_id, template_id):

    print("\n========== CRUD INVOICES ==========")

    invoice_data = {
        "number": f"FAC-TEST-{TEST_ID}",
        "client_id": client_id,
        "user_id": user_id,
        "template_id": template_id,
        "global_discount_percent": 0,
        "notes": "Factura de prueba",
        "lines": [
            {
                "category": "Servicios",
                "description": "Servicio de prueba",
                "unit_price": 100,
                "quantity": 2,
                "discount_percent": 0,
                "tax_rate": 21
            }
        ]
    }

    # POST: Crear factura
    response = requests.post(INVOICES_URL, json=invoice_data)

    if not check_response(response, 201, "POST - Crear factura"):
        return None

    invoice_id = response.json()["invoice_id"]

    # GET: Obtener todas las facturas
    response = requests.get(INVOICES_URL)

    if not check_response(response, 200, "GET - Obtener facturas"):
        return None

    # GET: Obtener factura por ID
    response = requests.get(f"{INVOICES_URL}/{invoice_id}")

    if not check_response(response, 200, "GET - Obtener factura por ID"):
        return None

    # PUT: Modificar factura
    invoice_data["number"] = f"FAC-MOD-{TEST_ID}"
    invoice_data["lines"][0]["unit_price"] = 150

    response = requests.put(
        f"{INVOICES_URL}/{invoice_id}",
        json=invoice_data
    )

    if not check_response(response, 200, "PUT - Modificar factura"):
        return None

    return invoice_id


# ================== ELIMINAR REGISTROS ==================

def test_delete(user_id, client_id, template_id, invoice_id):

    print("\n========== DELETE ==========")

    # Eliminar factura
    response = requests.delete(f"{INVOICES_URL}/{invoice_id}")

    if not check_response(response, 204, "DELETE - Eliminar factura"):
        return False

    # Eliminar plantilla
    response = requests.delete(f"{TEMPLATES_URL}/{template_id}")

    if not check_response(response, 204, "DELETE - Eliminar plantilla"):
        return False

    # Eliminar cliente
    response = requests.delete(f"{CLIENTS_URL}/{client_id}")

    if not check_response(response, 204, "DELETE - Eliminar cliente"):
        return False

    # Eliminar usuario
    response = requests.delete(f"{USERS_URL}/{user_id}")

    if not check_response(response, 204, "DELETE - Eliminar usuario"):
        return False

    return True


# ================== EJECUTAR PRUEBAS ==================

if __name__ == "__main__":

    if test_connection():

        user_id = TEST_ID

        if test_users():

            client_id = test_clients(user_id)

            if client_id is not False:

                template_id = test_templates(user_id)

                if template_id is not None:

                    invoice_id = test_invoices(
                        user_id, client_id, template_id
                    )

                    if invoice_id is not None:

                        test_delete(
                            user_id,
                            client_id,
                            template_id,
                            invoice_id
                        )

    print("\n========== FIN DE LAS PRUEBAS ==========")
