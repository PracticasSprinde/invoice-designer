from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Main(BaseModel):
    name: str
    lastName: str

users = [Main(name="Paco", lastName="Saez"),
         Main(name="Sara", lastName="Alonso"),
         Main(name="Laura", lastName="Pascual"),
         Main(name="Sergio", lastName="Perez")
         ]

@app.get("/")
async def inicio():
    return users

# Arrancar FastAPI
# uvicorn app.main:app --reload

# Async: Llamada la servidor, segundo plano