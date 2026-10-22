from fastapi import FastAPI
from pydantic import BaseModel
from app.routers import clients, issuers, templates, invoices

app = FastAPI()

# Registrar las rutas de clientes
app.include_router(clients.router)
app.include_router(issuers.router)
app.include_router(templates.router)
app.include_router(invoices.router)


class Main(BaseModel):
    name: str
    lastName: str


@app.get("/")
async def inicio():
    return {"mensaje": "API funcionando correctamente"}

# Arrancar FastAPI
# uvicorn app.main:app --reload

# http://127.0.0.1:8000/docs
# python run.py -> Abre navegador con FastAPI