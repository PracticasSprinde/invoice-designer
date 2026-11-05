from fastapi import FastAPI
from pydantic import BaseModel
from app.routers import clients_rt, invoices_rt, templates_rt, users_rt, products_rt

app = FastAPI()

# Registrar las rutas de clientes
app.include_router(clients_rt.router_memory)
app.include_router(users_rt.router_memory)
app.include_router(products_rt.router_memory)
app.include_router(templates_rt.router_memory)
app.include_router(invoices_rt.router_memory)


class Main(BaseModel):
    name: str
    lastName: str


@app.get("/memory/")
async def inicio():
    return {"mensaje": "API funcionando correctamente"}

# Arrancar FastAPI
# uvicorn app.main:app --reload

# http://127.0.0.1:8000/docs
# python run.py -> Abre navegador con FastAPI