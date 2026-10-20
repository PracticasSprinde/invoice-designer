from fastapi import FastAPI

# Instáncia de FastAPI
app = FastAPI()
#app = FastAPI(prefix = "/clients", tags= ["Clients"])

#Endpoint para visualizar todos los clientes
@app.get("/clients")
def get_clients():
    return {"mensaje": "Mi Client funciona correctamente"}

#Endpoint para visualizar el cliente por ID
@app.get("/clients/{client_id}")
def get_client_id(client_id:int):
    return{
        "mensaje": "Mi id de Client funciona correctamente",
        "Client_id": client_id
    }

#Endpoint para visualizar el cliente por empresa