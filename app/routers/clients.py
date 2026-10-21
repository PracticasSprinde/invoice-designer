from fastapi import FastAPI
from pydantic import BaseModel

# uvicorn uvicorn app.routers.clients:app --reload

# Instáncia de FastAPI
app = FastAPI()
# app = FastAPI(prefix = "/clients", tags= ["Clients"])


# Entidad
class Client(BaseModel):
    client_id: int
    name: str
    lastName: str
    enterprise: str
    cif_nif: str
    phone: int


client_list = [
    Client(client_id=1, name="Paco", lastName="Saez", enterprise="Google", cif_nif="B075673", phone=666666666),
    Client(client_id=2, name="Sara", lastName="Alonso",enterprise="Prisma", cif_nif="B0533567", phone=444444444),
    Client(client_id=3, name="Laura", lastName="Pascual",enterprise="Pallicer", cif_nif="B85373", phone=777777777),
    Client(client_id=4, name="Sergio", lastName="Perez",enterprise="Toyota", cif_nif="B88337", phone=699999999)
]

# Visualizar todos los clientes
@app.get("/clients")
async def get_clients():
    return client_list



# Visualizar cliente por ID - Path --> clientquery/5
# Parametros obligatorios
@app.get("/client/{id}")
async def get_client_id(id: int):
    return buscar_cliente(id)



# Visualizar cliente por ID - Query --> clientquery/?id=5
# Parametros no obligatorios para la query
@app.get("/clientquery/")
async def get_client_id(id: int):
    return buscar_cliente(id)



# Añadir client
@app.post("/client/")
async def new_client(client : Client):
    if type(buscar_cliente(client.client_id)) == Client:
        return{"error":"El usuario ya existe"}
    else:
        client_list.append(client)



# Editar cliente
@app.put("/client/")
async def update_client(client : Client):

    found = False

    for index, save_client in enumerate(client_list):

        if save_client.client_id == client.client_id:
            client_list[index] = client
            found = True
            return{"mensaje":"Usuario modificado"}

    if not found:
        return{"error":"Ususario no encontrado"}
            


# Eliminar cliente
@app.delete("/client/")
async def delete_client(client : Client):
    if type(buscar_cliente(client.client_id)) == Client:
        return{"error":"El usuario ya existe"}
    else:
        client_list.append(client)









# Metodo para obtener todos los clientes
def buscar_cliente(id : int):
    client = filter(lambda client: client.client_id == id, client_list)
    try:
         return list(client)[0]
    except:
        return {"error": "No se ha encontrado el id"}