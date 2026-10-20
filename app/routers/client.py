from fastapi import FastAPI

# Instáncia de FastAPI
app = FastAPI()
#app = FastAPI(prefix = "/clients", tags= ["Clients"])

#Endpoint GET
@app.get("/clients")
def get_clients():
    return {"mensaje": "Mi Client funciona correctamente"}

#Endpoint GET
@app.get("/clients/{client_id}")
def get_client_id(client_id:int):
    return{
        "mensaje": "Mi id de Client funciona correctamente",
        "Client_id": client_id
    }