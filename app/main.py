from fastapi import FastAPI
from pydantic import BaseModel
from app.routers import clients, issuers, templates, invoices

app = FastAPI()

# Registrar las rutas de clientes
app.include_router(clients.router, issuers.router, templates.router, invoices.router)


class Main(BaseModel):
    name: str
    lastName: str


@app.get("/")
async def inicio():
    return {"mensaje": "API funcionando correctamente"}

# Arrancar FastAPI
# uvicorn app.main:app --reload

# Async: Llamada la servidor, segundo plano