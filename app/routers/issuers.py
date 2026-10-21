from fastapi import FastAPI

# Instáncia de FastAPI
app = FastAPI()

# Devuelve todos los emisores
@app.get("/issuers")
async def get_issuers():
    return{"Todos los emisores"}

# Devuelve el emisor por su ID
@app.get("/issuers/{issue_id}")
async def get_issuer_id(issue_id:int):
    return{
        "mensaje" : "Id de emisor", 
        "ID Emisor" : issue_id
    }


# Añade emisor
##@app.post(issuers)