from fastapi import FastAPI
from pydantic import BaseModel
from app.routers import clients_rt, invoices_rt, templates_rt, issuer_rt, products_rt
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permite que el front y el back se comuniquen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar las rutas de API en memoria
app.include_router(clients_rt.router_memory)
app.include_router(issuer_rt.router_memory)
app.include_router(products_rt.router_memory)
app.include_router(templates_rt.router_memory)
app.include_router(invoices_rt.router_memory)


# Registrar las rutas de PostgreSQL
app.include_router(clients_rt.router)
app.include_router(issuer_rt.router)
app.include_router(products_rt.router)
app.include_router(templates_rt.router)
app.include_router(invoices_rt.router)


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